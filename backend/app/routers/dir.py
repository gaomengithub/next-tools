# -*- coding: utf-8 -*-
import os
from fastapi.responses import FileResponse
import uuid
from fastapi import APIRouter, Depends
from typing import Dict
import requests
import random
import win32com
import win32com.client
from hashlib import md5
import re
import shutil
import pythoncom
from ..internal.auth import check_token_exp_time

# 术语表
glossary = {
    '摘要': 'Abstract(chinese)',
    'Abstract': 'Abstract(english)',
    '目录': 'Contents(chinese)',
    'Contents': 'Contents(english)',
    'contents': 'Contents(english)',
    '第一章': 'Chapter 1',
    '第二章': 'Chapter 2',
    '第三章': 'Chapter 3',
    '第四章': 'Chapter 4',
    '第五章': 'Chapter 5',
    '第六章': 'Chapter 6',
    '第七章': 'Chapter 7',
    '第八章': 'Chapter 8',
    '第九章': 'Chapter 9',
    '第1章': 'Chapter 1',
    '第2章': 'Chapter 2',
    '第3章': 'Chapter 3',
    '第4章': 'Chapter 4',
    '第5章': 'Chapter 5',
    '第6章': 'Chapter 6',
    '第7章': 'Chapter 7',
    '第8章': 'Chapter 8',
    '第9章': 'Chapter 9',
}
# 序号序列对照表
type_dict = {
    '1/1.1/1.1.1': [r"\d", r"\d\.\d", r"\d\.\d\.\d"],
    '第1章/1.1/1.1.1': [r"第\d章", r"\d\.\d", r"\d\.\d\.\d"],
    '第一章/1.1/1.1.1': [r"第[\u4e00-\u9fa5\u767e\u5343\u96f6]*章", r"\d\.\d", r"\d\.\d\.\d"],
    '第一章/第一节/一、': [r"第[\u4e00-\u9fa5\u767e\u5343\u96f6]*章", r"第[\u4e00-\u9fa5\u767e\u5343\u96f6]*节",
                          r"[\u4e00-\u9fa5\u767e\u5343\u96f6]{1,2}、"],
}

router = APIRouter(dependencies=[Depends(check_token_exp_time)])


@router.post("/dir_to_en/")
async def dir_to_en(form_data: Dict):
    content = list(filter(lambda x: len(x) > 0, form_data["content"].split("\n")))
    content = list(map(lambda x: {'text': re.sub(' ', '', x)}, content))
    _type = form_data['type']
    _school = form_data['school']
    pattern = type_dict[_type]
    _classify = Classify(content, pattern)
    _classify.page()
    _classify.outline_header()
    _classify.text_zh()
    trans = BaiduTrans('\n'.join(map(lambda x: x['text_zh'], _classify.content)))
    _classify.text_en(trans.run())
    _classify.trans_map()
    _word = Word(_classify.content, _school)
    _word.write_docx()
    return FileResponse(os.path.abspath('.') + '\\temp\\word\\' + _word.temp_name + '.docx',
                        headers={'filename': _word.temp_name})
    # print(_classify.content)


class Classify:
    def __init__(self, content, pattern):
        self.content = content
        self.pattern = pattern

    def page(self):
        for item in self.content:
            try:
                item['page'] = re.findall(r"(?<=\t).*", item['text'])[0]
            except IndexError:
                item['page'] = 'undefined'

    def outline_header(self):
        for item in self.content:
            try:
                item['header'] = re.findall(self.pattern[2], item['text'])[0]
                item['outline'] = 3
            except IndexError:
                try:
                    item['header'] = re.findall(self.pattern[1], item['text'])[0]
                    item['outline'] = 2
                except IndexError:
                    try:
                        item['header'] = re.findall(self.pattern[0], item['text'])[0]
                        item['outline'] = 1
                    except IndexError:
                        item['header'] = ''
                        item['outline'] = 1

    def text_zh(self):
        for item in self.content:
            item['text_zh'] = re.sub('^' + item['header'] + '|\t|' + item['page'] + '$', '', item['text'])
        # print(self.content)

    def text_en(self, trans_result):
        try:
            for item, _item in zip(self.content, trans_result):
                item['text_en'] = _item['dst'].capitalize().rstrip()
        except TypeError:
            pass

    def trans_map(self):
        for item in self.content:
            try:
                item['text_en'] = glossary[item['text_zh']]
            except KeyError:
                pass
            try:
                item['header'] = glossary[item['header']]
            except KeyError:
                pass


class BaiduTrans:
    def __init__(self, query):
        self.appid = '20200713000518532'
        self.appkey = 'YBsuet3z84MHIJyipZH2'
        self.from_lang = 'zh'
        self.to_lang = 'en'
        self.url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        self.salt = random.randint(32768, 65536)
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.query = query
        self.sign = self.make_md5(self.appid + self.query + str(self.salt) + self.appkey)
        self.payload = {'appid': self.appid, 'q': self.query, 'from': self.from_lang, 'to': self.to_lang,
                        'salt': self.salt, 'sign': self.sign}

    @staticmethod
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    def run(self):
        r = requests.post(self.url, params=self.payload, headers=self.headers)
        result = r.json()
        return result['trans_result']
        # print(json.dumps(result, indent=4, ensure_ascii=False))


class Word:
    def __init__(self, content, school):
        self.content = content
        self.temp_name = str(uuid.uuid4())
        self.school = school

    def write_docx(self):
        word = win32com.client.DispatchEx('Word.Application')
        word.Visible = False
        word.DisplayAlerts = False
        # pythoncom.CoInitialize()
        template_path = os.path.abspath('.') + '\\temp\\template\\' + self.school + '.docx'
        dst_path = os.path.abspath('.') + '\\temp\\word\\' + self.temp_name + '.docx'
        shutil.copy(template_path, dst_path)
        docx = word.Documents.Open(dst_path)
        word.Selection.MoveDown(Unit=5, Count=4)
        for item in self.content:
            if len(item['header']) > 0:
                header = item['header'] + ' '
            else:
                header = item['header']
            word.Selection.TypeText(header + item['text_en'] + '\t' + item['page'])
            word.Selection.Style = word.ActiveDocument.Styles("TOC " + str(item['outline']))
            word.Selection.TypeParagraph()
        docx.SaveAs2(os.path.abspath('.') + '\\temp\\word\\' + self.temp_name + '.docx')
        docx.Close()
        word.Quit()
        # pythoncom.CoInitialize()
