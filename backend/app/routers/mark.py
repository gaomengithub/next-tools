import json
import os.path
import re
import uuid
from lxml import etree
import subprocess
import win32com
import win32com.client
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, UploadFile, Form
from ..internal.auth import check_token_exp_time
from fastapi.responses import FileResponse
from .websocket import manager

router = APIRouter(dependencies=[Depends(check_token_exp_time)])


@router.websocket("/ws/mark_color/upload_report_extract_colors/{timestamp}")
async def upload_report_extract_colors(websocket: WebSocket, timestamp: int):
    await manager.connect(websocket)
    try:
        while True:
            file_bytes = await websocket.receive_bytes()
            f = open(os.path.abspath('.') + '\\temp\\pdf\\' + str(timestamp) + '.pdf', 'wb')
            f.write(file_bytes)
            f.close()
            await manager.send_personal_json({'status': '上传已完成，正在解析PDF'}, websocket)
            _extract_colors = ExtractColors(str(timestamp))  # convert to html , html_name = str(timestamp)
            colors = _extract_colors.run()
            toggle = list(map(lambda x: re.findall(r'rgb\(\d+,\d+,\d+\)', x)[0], colors))
            await manager.send_personal_json(
                {'status': '已返回数据，请等待', 'toggle': '|'.join(toggle), 'colors': colors}, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.websocket("/ws/mark_color/upload_word_mark_color/{timestamp}")
async def upload_word_mark_color(websocket: WebSocket, timestamp: int):
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
            _mark_colors = MarkColors(html_name=str(timestamp), word_name=prefix_name, params=params,
                                      websocket=websocket)
            _mark_colors.get_curr_content()
            await _mark_colors.run()
            f = open(os.path.abspath('.') + '\\temp\\word\\' + prefix_name, 'rb')
            file_bytes = f.read()
            f.close()
            await manager.send_personal_bytes(file_bytes, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.post("/mark_color/check_report/")
async def check_report(file: UploadFile):
    file_bytes = file.file.read()
    temp_name = str(uuid.uuid4())
    f = open(os.path.abspath('.') + '\\temp\\pdf\\' + temp_name + '.pdf', 'wb')
    f.write(file_bytes)
    f.close()
    _extract_colors = ExtractColors(temp_name)
    colors = _extract_colors.run()
    toggle = list(map(lambda x: re.findall(r'rgb\(\d+,\d+,\d+\)', x)[0], colors))
    return {'id': temp_name, 'toggle': toggle, 'is': [], 'colors': colors}


@router.post("/mark_color/mark_word/")
async def mark_word(file: UploadFile, params: str = Form(...), client_id: str = Form(...)):
    params = json.loads(params)
    file_bytes = file.file.read()
    f = open(os.path.abspath('.') + '\\temp\\word\\' + params['id'] + file.filename, 'wb')
    f.write(file_bytes)
    f.close()
    _mark_colors = MarkColors(params['id'], params['id'] + file.filename, params, int(client_id))
    _mark_colors.get_curr_content()
    await _mark_colors.run()
    return FileResponse(os.path.abspath('.') + '\\temp\\word\\' + params['id'] + file.filename,
                        headers={'file_name': params['id'], 'file_type': re.sub(r".*\.", "", file.filename)})


class ExtractColors:
    def __init__(self, filename):
        self.filename = filename
        self.exe_path = os.path.abspath('.') + '\\tools\\' + '\\pdf2htmlEX\\pdf2htmlEX.exe'
        self.pdf_path = os.path.abspath('.') + '\\temp\\pdf\\' + self.filename + '.pdf'
        self.html_path = 'temp\\html\\' + self.filename + '.html'

    def run(self):
        subprocess.call([self.exe_path, self.pdf_path, self.html_path], shell=True)

        html = open(os.path.abspath('.') + '\\temp\\html\\' + self.filename + '.html', 'r', encoding='utf-8').read()
        pattern = re.compile(r'fc.{color:rgb\(\d+,\d+,\d+\);}')

        colors = re.findall(pattern, str(html))

        colors.sort(key=lambda x: int(re.findall(r'(?<=\()\d+', x)[0]), reverse=True)
        return colors


class MarkColors:
    def __init__(self, html_name, word_name, params, websocket):
        self.websocket = websocket
        self.curr_content = None
        self.word_path = os.path.abspath('.') + '\\temp\\word\\' + word_name
        self.html_path = os.path.abspath('.') + '\\temp\\html\\' + html_name + '.html'

        self.params = list(map(lambda x: params['colors'][x], params['is']))

    def get_curr_content(self):
        xpath = []
        for fsc in self.params:
            _xpath = '//div[contains(@class,"{0}")]/*[not(contains(@class,"fc0"))]//text() |' \
                     ' //span[contains(@class,"{0}")]/text()'.format(re.findall(r'.*(?={)', fsc)[0])
            xpath.append(_xpath)
        xpath_str = ' | '.join(xpath)
        html = open(self.html_path, 'r', encoding='utf-8').read()
        parse = etree.HTML(html)
        curr_content = parse.xpath(xpath_str)
        # 去除^ 和[]
        self.curr_content = sum(list(map(lambda x: re.split(r'\^|\[\d*]', x), curr_content)), [])
        # 去除查重报告前面的比例数字
        self.curr_content = list(
            filter(lambda x: bool(re.sub(r'\d+\.\d+%（\d+）|\d+\.\d+%(\d+)|\d+\.\d+%|\d+%|\d+ ', '', x)),
                   self.curr_content))

    async def run(self):
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = False
        docx = word.Documents.Open(self.word_path)
        word.Selection.Find.IgnoreSpace = True
        word.Selection.Find.IgnorePunct = True
        word.Selection.Find.MatchByte = False
        word.Selection.Find.Forward = True
        word.Selection.Find.Replacement.Font.Color = 255

        for _ in self.curr_content:
            word.Selection.Find.Execute(_, False, False, False, False, False, True, 1, True, '', 1)
            await manager.send_personal_json({'status': str(_)}, self.websocket)
        docx.Save()
        docx.Close()
        word.Quit()
        await manager.send_personal_json({'status': '后台已完成，请注意下载'}, self.websocket)
