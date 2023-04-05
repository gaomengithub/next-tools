# import json
import json
import os
import re
import uuid
# import pythoncom
import win32com
import win32com.client
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from ..internal.auth import check_token_exp_time
from ..tools.typeset_config import typeset_config
from fastapi import UploadFile, Form
from .websocket import manager

router = APIRouter(dependencies=[Depends(check_token_exp_time)])


@router.websocket('/ws/typeset/{timestamp}')
async def typeset(websocket: WebSocket, timestamp: int):
    await manager.connect(websocket)
    try:
        while True:
            params = await websocket.receive_text()
            params = json.loads(params)  # receive params
            file_bytes = await websocket.receive_bytes()
            prefix_name = str(timestamp) + params['filename']
            f = open(os.path.abspath('.') + '\\temp\\word\\' + prefix_name, 'wb')
            f.write(file_bytes)
            f.close()
            await manager.send_personal_json({'status': '上传已完成，初始化中'}, websocket)
            _typeset = TypeSet(os.path.abspath('.') + '\\temp\\word\\' + prefix_name, params['school'], websocket)
            # _typeset.set_page()
            await _typeset.set_style()
            _typeset.docx.Save()
            _typeset.docx.Close()
            _typeset.word.Quit()
            f = open(os.path.abspath('.') + '\\temp\\word\\' + prefix_name, 'rb')
            file_bytes = f.read()
            f.close()
            await manager.send_personal_bytes(file_bytes, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


name_num_map = {'标题': 0, '标题 1': 1, '标题 2': 2, '标题 3': 3, '正文': 4, '题注': 5, 'TOC 1': 6, 'TOC 2': 7,
                'TOC 3': 8}

num_name_map = {0: '标题', 1: '标题 1', 2: '标题 2', 3: '标题 3', 4: '正文', 5: '题注', 6: 'TOC 1', 7: 'TOC 2',
                8: 'TOC 3', 10.0: '请等待'}


# @router.get('/get_process_status')
# def get_process_status():
#     return str(num_name_map[num.value])


@router.get('/get_school_config/{school_name}')
async def get_school_config(school_name):
    return typeset_config[school_name]


@router.get('/get_schools_list')
async def get_schools_list():
    return list(typeset_config.keys())


@router.post('/typeset/')
async def typeset(file: UploadFile, school: str = Form(...), client_id: str = Form(...)):
    prefix_name = str(uuid.uuid4())
    # pythoncom.CoInitialize()
    # global num
    # num = multiprocessing.Value("d", 10.0)
    # _child_typeset = multiprocessing.Process(target=child_typeset, args=(prefix_name, file, school, num))
    # _child_typeset.start()
    # _child_typeset.join()
    await child_typeset(prefix_name, file, school, int(client_id))
    return FileResponse(os.path.abspath('.') + '\\temp\\word\\' + prefix_name + file.filename,
                        headers={'file_name': prefix_name, 'file_type': re.sub(r".*\.", "", file.filename)})
    # _child_typeset.join()

    # pythoncom.CoInitialize()


# def child_typeset(prefix_name, file, school, num):
async def child_typeset(prefix_name, file, school, client_id):
    file_bytes = file.file.read()
    f = open(os.path.abspath('.') + '\\temp\\word\\' + prefix_name + file.filename, 'wb')
    f.write(file_bytes)
    f.close()
    # _typeset = TypeSet(os.path.abspath('.') + '\\temp\\word\\' + prefix_name + file.filename, school, num)
    _typeset = TypeSet(os.path.abspath('.') + '\\temp\\word\\' + prefix_name + file.filename, school, client_id)

    # _typeset.set_page()
    await _typeset.set_style()
    _typeset.docx.Save()
    _typeset.docx.Close()
    _typeset.word.Quit()


class TypeSet:
    # def __init__(self, word_path, school, num):
    def __init__(self, word_path, school, websocket):
        self.websocket = websocket
        self.word_path = word_path
        # print(school)
        self.typeset_config = typeset_config[school]
        # pythoncom.CoInitialize()
        self.word = win32com.client.DispatchEx('Word.Application')
        self.word.Visible = False
        self.word.DisplayAlerts = False
        self.docx = self.word.Documents.Open(self.word_path)

    def set_page(self):
        # self.word.Selection.WholeStory()
        # for sp in self.word.Selection.Sections:

        ps = self.word.ActiveDocument.PageSetup
        ps.LineNumbering.Active = False
        ps.Orientation = 0  # 指定页面布局方向 0 纵向 1 横向
        ps.TopMargin = self.typeset_config["页面设置"]['上边距'] * 28.35  # 1 厘米 = 28.35 磅
        ps.BottomMargin = self.typeset_config["页面设置"]['下边距'] * 28.35
        ps.LeftMargin = self.typeset_config["页面设置"]['左边距'] * 28.35
        ps.RightMargin = self.typeset_config["页面设置"]['右边距'] * 28.35
        ps.Gutter = self.typeset_config["页面设置"]['装订线'] * 28.35
        ps.HeaderDistance = self.typeset_config["页面设置"]['距边界-页眉'] * 28.35
        ps.FooterDistance = self.typeset_config["页面设置"]['距边界-页脚'] * 28.35
        ps.PageWidth = 21 * 28.35
        ps.PageHeight = 29.7 * 28.35
        ps.FirstPageTray = 0
        ps.OtherPagesTray = 0
        ps.SectionStart = 2
        ps.OddAndEvenPagesHeaderFooter = False
        ps.DifferentFirstPageHeaderFooter = self.typeset_config["页面设置"]['奇偶页不同']
        ps.VerticalAlignment = 0
        ps.SuppressEndnotes = False
        ps.MirrorMargins = False
        ps.TwoPagesOnOne = False
        ps.BookFoldPrinting = False
        ps.BookFoldRevPrinting = False
        ps.BookFoldPrintingSheets = 1
        ps.GutterPos = self.typeset_config["页面设置"]['装订线位置']
        ps.LayoutMode = 0  # 0 No grid is used to lay out text.

    async def set_style(self):
        for style_name in list(list(self.typeset_config.keys())[0:9]):
            s = self.word.ActiveDocument.Styles(style_name)
            s.BaseStyle = ""
            s.NextParagraphStyle = "正文"
            s.AutomaticallyUpdate = False
            # 设置样式 - 段落
            s.ParagraphFormat.LeftIndent = self.typeset_config[style_name]['缩进-左侧'][0] * 28.35
            s.ParagraphFormat.RightIndent = self.typeset_config[style_name]['缩进-右侧'][0] * 28.35
            s.ParagraphFormat.SpaceBefore = self.typeset_config[style_name]['间距-段前'][0]
            s.ParagraphFormat.SpaceBeforeAuto = self.typeset_config[style_name]['间距-段前'][1]
            s.ParagraphFormat.SpaceAfter = self.typeset_config[style_name]['间距-段后'][0]
            s.ParagraphFormat.SpaceAfterAuto = self.typeset_config[style_name]['间距-段后'][1]
            s.ParagraphFormat.LineSpacingRule = self.typeset_config[style_name]['间距-行距']
            s.ParagraphFormat.LineSpacing = self.typeset_config[style_name]['间距-设置值']
            s.ParagraphFormat.Alignment = self.typeset_config[style_name]['对齐方式']
            s.ParagraphFormat.WidowControl = False
            s.ParagraphFormat.KeepWithNext = False
            s.ParagraphFormat.KeepTogether = False
            s.ParagraphFormat.PageBreakBefore = False
            s.ParagraphFormat.NoLineNumber = False
            s.ParagraphFormat.Hyphenation = True
            s.ParagraphFormat.FirstLineIndent = self.typeset_config[style_name]['缩进-特殊-首行'][0] * 28.35
            s.ParagraphFormat.OutlineLevel = self.typeset_config[style_name]['大纲级别']
            s.ParagraphFormat.CharacterUnitLeftIndent = self.typeset_config[style_name]['缩进-左侧'][1]
            s.ParagraphFormat.CharacterUnitRightIndent = self.typeset_config[style_name]['缩进-左侧'][1]
            s.ParagraphFormat.CharacterUnitFirstLineIndent = self.typeset_config[style_name]['缩进-特殊-首行'][1]
            s.ParagraphFormat.LineUnitBefore = self.typeset_config[style_name]['间距-段前'][2]
            s.ParagraphFormat.LineUnitAfter = self.typeset_config[style_name]['间距-段后'][2]
            s.ParagraphFormat.MirrorIndents = False
            s.ParagraphFormat.TextboxTightWrap = 0  # 文字不紧密环绕文本框的内容
            s.ParagraphFormat.CollapsedByDefault = False
            s.ParagraphFormat.AutoAdjustRightIndent = True
            s.ParagraphFormat.DisableLineHeightGrid = False
            s.ParagraphFormat.FarEastLineBreakControl = True
            s.ParagraphFormat.WordWrap = True
            s.ParagraphFormat.HangingPunctuation = True
            s.ParagraphFormat.HalfWidthPunctuationOnTopOfLine = False
            s.ParagraphFormat.AddSpaceBetweenFarEastAndAlpha = True
            s.ParagraphFormat.AddSpaceBetweenFarEastAndDigit = True
            s.ParagraphFormat.BaseLineAlignment = 4  # 自动调整字体的基线对齐方式

            # 设置样式的字体
            s.Font.NameFarEast = self.typeset_config[style_name]['中文字体']
            s.Font.NameAscii = self.typeset_config[style_name]['西文字体']
            s.Font.NameOther = self.typeset_config[style_name]['西文字体']
            s.Font.Name = self.typeset_config[style_name]['西文字体']
            s.Font.Size = self.typeset_config[style_name]['字号']
            s.Font.Bold = self.typeset_config[style_name]['加粗']
            s.Font.Italic = False
            s.Font.Underline = 0
            s.Font.UnderlineColor = -16777216
            s.Font.StrikeThrough = False
            s.Font.DoubleStrikeThrough = False
            s.Font.Outline = False
            s.Font.Emboss = False
            s.Font.Shadow = False
            s.Font.Hidden = False
            s.Font.SmallCaps = False
            s.Font.AllCaps = False
            s.Font.Color = -16777216
            s.Font.Engrave = False
            s.Font.Superscript = False
            s.Font.Subscript = False
            s.Font.Scaling = 100
            s.Font.Kerning = 1
            s.Font.Animation = 0
            s.Font.DisableCharacterSpaceGrid = False
            s.Font.EmphasisMark = 0  # 0 没有着重号
            s.Font.Ligatures = 0  # 0 不对字体应用任何连字
            s.Font.NumberSpacing = 0  # 0 应用字体的默认数字间距。
            s.Font.NumberForm = 0  # 0 应用字体的默认数字形式
            s.Font.StylisticSet = 0  # 0 指定字体的默认样式集
            s.Font.ContextualAlternates = 0
            # print(style_name)
            await manager.send_personal_json({'status': style_name}, self.websocket)
        await manager.send_personal_json({'status': '已经结束，请注意下载'}, self.websocket)
        # self.num.value = name_num_map[style_name]

    # def set_header_bottom_of_page(self):
