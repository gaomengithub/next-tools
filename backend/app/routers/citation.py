import re
import win32com.client
import json
import os.path
import uuid
from lxml import etree
import subprocess
import win32com
import win32com.client
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, UploadFile, status, HTTPException
from ..internal.auth import check_token_exp_time
from fastapi.responses import FileResponse
from .websocket import manager

router = APIRouter(dependencies=[Depends(check_token_exp_time)])

positon_exception = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="并没有找到起点",
)

@router.websocket("/ws/citation-mark/upload_word/{timestamp}")
async def upload_word_run(websocket: WebSocket, timestamp: int):
    await manager.connect(websocket)
    try:
        while True:
            params = await websocket.receive_text()
            params = json.loads(params)  # receive params
            # print(params)
            file_bytes = await websocket.receive_bytes()  # receive word
            prefix_name = str(timestamp) + params['filename']
            f = open(os.path.abspath('.') + '\\temp\\word\\' + prefix_name, 'wb')
            f.write(file_bytes)
            f.close()
            await manager.send_personal_json({'status': '上传已完成，准备标记'}, websocket)
            citation_mark = CitationMark(os.path.abspath('.') + '\\temp\\word\\' + prefix_name)
            citation_mark.get_citation_list()
            await manager.send_personal_json({'status': '已获取到参考文献'},websocket)
            citation_mark.make_footnotes()
            await manager.send_personal_json({'status': '已完成脚注'}, websocket)
            citation_mark.sort_to_positon()
            await manager.send_personal_json({'status': '已完成整理工作，等待数据回传'}, websocket)
            citation_mark.save_docx()
            f = open(os.path.abspath('.') + '\\temp\\word\\' + prefix_name, 'rb')
            file_bytes = f.read()
            f.close()
            await manager.send_personal_bytes(file_bytes, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)



class CitationMark:

    def __init__(self,path):
        self.path = path
        self.citation_items = []
        self.name_items = []
        self.nofind = []
        self.find_list = []
        """
           https://learn.microsoft.com/en-us/office/vba/api/word.find.execute 
        """
        self.word = win32com.client.DispatchEx("Word.Application")
        self.word.Visible = True
        self.word.DisplayAlerts = False
        self.docx = self.word.Documents.Open(self.path)
        self.word.Selection.Find.IgnoreSpace = True
        self.word.Selection.Find.IgnorePunct = True
        self.word.Selection.Find.MatchByte = False
        self.word.Selection.Find.Forward = True

    def get_citation_list(self):
        self.word.Selection.Find.MatchWildcards = True
        find_result = self.word.Selection.Find.Execute("<参考文献>")
        """
        https://learn.microsoft.com/en-us/office/vba/api/word.wdunits
        """

        if find_result:
            self.word.Selection.MoveUntil(4)
            while 1 > 0:
                self.word.Selection.MoveRight()
                # 获取当前光标位置
                selection = self.word.Selection
                current_range = self.word.Selection.Range

                # 获取当前光标所在段落的范围
                current_range.Paragraphs(1).Range.Select()
                paragraph_range = selection.Range

                # 获取段落内容
                paragraph_text = paragraph_range.Text
                self.word.Selection.Delete()
                if len(paragraph_text) > 12:
                    self.citation_items.append(paragraph_text)
                else:
                    break

        else:
            raise positon_exception

    def make_footnotes(self):
        self.name_items = list(map(lambda x: re.sub(r'(?=\.).*', '', x), self.citation_items))
        self.name_items = list(map(lambda x: re.sub(r',.*', '', x), self.name_items))

        self.word.Selection.Find.MatchWildcards = False
        for index, item in enumerate(self.name_items):
            self.word.Selection.WholeStory()
            result = self.word.Selection.Find.Execute(item)
            if result:
                self.word.Selection.MoveRight()
                self.word.Selection.Find.Execute("。")
                self.word.Selection.MoveLeft()
                self.word.Selection.TypeText("[clone]")
                self.docx.Footnotes.Add(self.word.Selection.Range)
                self.word.Selection.TypeText(self.citation_items[index].replace("\r", ""))
                self.find_list.append(self.citation_items[index])
                self.word.Selection.WholeStory()
                if index == len(self.name_items) - 1:
                    break
                self.word.Selection.MoveUp(5)
            else:
                self.nofind.append(item)
    def sort_to_positon(self):
        self.word.Selection.MoveUp(5)
        self.word.Selection.WholeStory()
        self.word.Selection.Find.MatchWildcards = True
        result = self.word.Selection.Find.Execute("<参考文献>")
        if result:
            self.word.Selection.MoveRight()
            self.word.Selection.TypeParagraph()
            for _ in self.find_list:
                self.word.Selection.TypeText(_)
                self.word.Selection.MoveRight()
            self.word.Selection.TypeParagraph()
            self.word.Selection.TypeParagraph()

            for _ in self.nofind:
                self.word.Selection.Font.ColorIndex = 7
                self.word.Selection.TypeText(_)
                self.word.Selection.MoveRight()

        self.word.Selection.Find.MatchWildcards = False
        self.word.Selection.WholeStory()
        self.word.Selection.Find.Forward = True
        self.word.Selection.Find.Wrap = 0
        self.word.Selection.Find.Replacement.Font.Superscript = True
        count = 0
        while True:
            count += 1
            # self.word.Selection.Find.Text = "[clone]^f"
            # self.word.Selection.Find.Replacement.Text = "[" + str(count) + "]"
            if not self.word.Selection.Find.Execute("[clone]^f", False, False, False, False, False, True, 1, True, "[" + str(count) + "]", 1):
                break  # 没有符合条件的查找结果，结束循环
            # self.word.Selection.Range.Text = "[" + str(count) + "]"
            self.word.Selection.Start = self.word.Selection.End
    def save_docx(self):
        self.docx.Save()
        self.docx.Close()
        self.word.Quit()

