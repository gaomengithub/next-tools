import os
import random
import re
import uuid
import win32com.client
import requests
from lxml.etree import HTML
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, status
from ..internal.auth import check_token_exp_time
from pydantic import BaseModel
from fastapi.responses import FileResponse
router = APIRouter(dependencies=[Depends(check_token_exp_time)])


class LiteratureReviewData(BaseModel):
    type: str
    content: str


alignment_exception = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="不能对齐文献，请检查是否复制完整,文献信息是否完整",
)


@router.post("/literature-review/")
async def literature_review(data: LiteratureReviewData):
    cnki = CNKI(data.type, data.content)
    cnki.seg_get()
    cnki.write_docx()
    return FileResponse(os.path.abspath('.') + '\\temp\\word\\' + cnki.docx_name + '.docx',
                        headers={'filename': cnki.docx_name})


class CNKI:
    def __init__(self, type: str, content: str):
        self.type = type
        self.content = content
        self.abstracts = None
        self.refs = None
        self.years = None
        self.names = None
        self.docx_name = str(uuid.uuid4())

    def seg_get(self):
        self.content = self.content.replace("[1]", "")
        segments = re.split(r"\n\[\d+]|\n摘要:", self.content)
        if len(segments) % 2 != 0:
            raise alignment_exception
        self.refs = list(map(lambda x: re.sub(r'^\[\d+]|DOI.*', '', x), segments[::2]))
        self.abstracts = list(map(lambda x: self.format_abstract(x), segments[1::2]))
        self.names = list(map(lambda x: re.sub(r'(?=\.).*', '', x), self.refs))
        self.names = list(map(lambda x: re.sub(r',.*', '等', x), self.names))
        self.years = list(map(lambda x: '或'.join(set(re.findall(r'19[5-9][0-9]|20[0-1][0-9]|202[0-3]', x))), self.refs))
        # if len({len(self.years), len(self.names), len(self.abstracts), len(self.refs)}) != 1:
        #     raise alignment_exception

    def format_abstract(self , abstract):
        abstract = re.sub(r'(?<=[\u4e00-\u9fa5])\.', '。',abstract)
        abstract = abstract.replace(',', '，').replace(';', '；').replace(':', '：')
        return abstract

    def write_docx(self):
        word = win32com.client.DispatchEx('Word.Application')
        word.Visible = True
        word.DisplayAlerts = 0
        doc = word.Documents.Add()
        s = word.ActiveDocument.Styles('正文')
        s.BaseStyle = ""
        s.AutomaticallyUpdate = False
        s.Font.NameFarEast = '宋体'
        s.Font.NameAscii = 'Times New Roman'
        s.Font.NameOther = 'Times New Roman'
        s.Font.Name = 'Times New Roman'
        s.Font.Size = 12
        if '人名+年份+摘要+外标注' == self.type:
            for name, year, abstract, refer in zip(self.names, self.years, self.abstracts, self.refs):
                word.Selection.TypeText(name)
                word.Selection.TypeText('（' + year + '）')
                word.Selection.TypeText(abstract)
                word.Selection.Footnotes.Add(Range=word.Selection.Range, Reference="")
                word.Selection.TypeText(refer)
                word.ActiveDocument.Paragraphs.Last.Range.Select()
                word.Selection.EndKey()
                word.Selection.TypeParagraph()
                word.Selection.TypeParagraph()
        elif '人名+年份+摘要+内标注' == self.type:
            for name, year, abstract, refer in zip(self.names, self.years, self.abstracts, self.refs):
                word.Selection.TypeText(name)
                word.Selection.TypeText('（' + year + '）')
                word.Selection.TypeText(abstract)
                word.Selection.MoveLeft(1, 1)
                word.Selection.Footnotes.Add(Range=word.Selection.Range, Reference="")
                word.Selection.TypeText(refer)
                word.ActiveDocument.Paragraphs.Last.Range.Select()
                word.Selection.EndKey()
                word.Selection.TypeParagraph()
                word.Selection.TypeParagraph()
        elif '人名+摘要+外标注' == self.type:
            for name, year, abstract, refer in zip(self.names, self.years, self.abstracts, self.refs):
                word.Selection.TypeText(name)
                word.Selection.TypeText(abstract)
                word.Selection.Footnotes.Add(Range=word.Selection.Range, Reference="")
                word.Selection.TypeText(refer)
                word.ActiveDocument.Paragraphs.Last.Range.Select()
                word.Selection.EndKey()
                word.Selection.TypeParagraph()
                word.Selection.TypeParagraph()
        elif '人名+摘要+内标注' == self.type:
            for name, year, abstract, refer in zip(self.names, self.years, self.abstracts, self.refs):
                word.Selection.TypeText(name)
                word.Selection.TypeText(abstract)
                word.Selection.MoveLeft(1, 1)
                word.Selection.Footnotes.Add(Range=word.Selection.Range, Reference="")
                word.Selection.TypeText(refer)
                word.ActiveDocument.Paragraphs.Last.Range.Select()
                word.Selection.EndKey()
                word.Selection.TypeParagraph()
                word.Selection.TypeParagraph()
        elif '摘要+（人名+标注，年份）' == self.type:
            for name, year, abstract, refer in zip(self.names, self.years, self.abstracts, self.refs):
                word.Selection.TypeText(abstract)
                word.Selection.TypeText('（' + name)
                word.Selection.Footnotes.Add(Range=word.Selection.Range, Reference="")
                word.Selection.TypeText(refer)
                word.ActiveDocument.Paragraphs.Last.Range.Select()
                word.Selection.EndKey()
                word.Selection.TypeText('，' + year + '）')
                # word.Selection.EndKey()
                word.Selection.TypeParagraph()
                word.Selection.TypeParagraph()
        elif '人名+年份+标注+摘要' == self.type:
            for name, year, abstract, refer in zip(self.names, self.years, self.abstracts, self.refs):
                word.Selection.TypeText(name)
                word.Selection.TypeText('（' + year + '）')
                word.Selection.Footnotes.Add(Range=word.Selection.Range, Reference="")
                word.Selection.TypeText(refer)
                word.ActiveDocument.Paragraphs.Last.Range.Select()
                word.Selection.EndKey()
                word.Selection.TypeText(abstract)
                word.Selection.TypeParagraph()
                word.Selection.TypeParagraph()
        elif '人名+标注+年份+摘要' == self.type:
            for name, year, abstract, refer in zip(self.names, self.years, self.abstracts, self.refs):
                word.Selection.TypeText(name)
                word.Selection.Footnotes.Add(Range=word.Selection.Range, Reference="")
                word.Selection.TypeText(refer)
                word.ActiveDocument.Paragraphs.Last.Range.Select()
                word.Selection.EndKey()
                word.Selection.TypeText('（' + year + '）')
                word.Selection.TypeText(abstract)
                word.Selection.TypeParagraph()
                word.Selection.TypeParagraph()
        elif '人名+标注+摘要' == self.type:
            for name, year, abstract, refer in zip(self.names, self.years, self.abstracts, self.refs):
                word.Selection.TypeText(name)
                word.Selection.Footnotes.Add(Range=word.Selection.Range, Reference="")
                word.Selection.TypeText(refer)
                word.ActiveDocument.Paragraphs.Last.Range.Select()
                word.Selection.EndKey()
                word.Selection.TypeText(abstract)
                word.Selection.TypeParagraph()
                word.Selection.TypeParagraph()
        doc.SaveAs(os.path.abspath('.') + '\\temp\\word\\' + self.docx_name + '.docx')
        doc.Close(-1)
        word.Quit()
