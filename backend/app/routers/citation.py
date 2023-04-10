import re

import win32com.client


path = ''
# 打开Word程序并打开文档
"""
   https://learn.microsoft.com/en-us/office/vba/api/word.find.execute 
"""
word = win32com.client.DispatchEx("Word.Application")
word.Visible = True
word.DisplayAlerts = False
docx = word.Documents.Open('C:\\Users\GM\Desktop\\1027文稿修改3_基于实物期权法的H光伏发电项目投资决策研）.docx')
word.Selection.Find.IgnoreSpace = True
word.Selection.Find.IgnorePunct = True
word.Selection.Find.MatchByte = False
word.Selection.Find.Forward = True
word.Selection.Find.MatchWildcards = True

# 使用Selection对象查找包含“参考文献”的段落

find_result = word.Selection.Find.Execute("<参考文献>")
"""
https://learn.microsoft.com/en-us/office/vba/api/word.wdunits
"""
paragraph_text_items = []
if find_result:
    word.Selection.MoveUntil(4)

    while 1 > 0:
        word.Selection.MoveRight()
        # 获取当前光标位置
        selection = word.Selection
        current_range = word.Selection.Range

        # 获取当前光标所在段落的范围
        current_range.Paragraphs(1).Range.Select()
        paragraph_range = selection.Range

        # 获取段落内容
        paragraph_text = paragraph_range.Text
        word.Selection.Delete()
        if len(paragraph_text) > 12:
            paragraph_text_items.append(paragraph_text)
        else:
            break

else:
    print("并没有找到起点")

word.Selection.Find.MatchWildcards = False
name_items = list(map(lambda x: re.sub(r'(?=\.).*', '', x), paragraph_text_items))
name_items = list(map(lambda x: re.sub(r',.*', '', x), name_items))
nofind =[]
for index, item in enumerate(name_items):
    word.Selection.WholeStory()
    result = word.Selection.Find.Execute(item)
    if result:
        word.Selection.MoveRight()
        word.Selection.TypeText("[clone]")
        docx.Footnotes.Add(word.Selection.Range)
        word.Selection.TypeText(paragraph_text_items[index].replace("\r", ""))
        word.Selection.WholeStory()
        if index == len(name_items) -1 :
            break
        word.Selection.MoveUp(5)
    else:
        nofind.append(item)

find_itmes = []

footnotes_range = word.Selection.Range
for paragraph in footnotes_range.Paragraphs:
    find_itmes.append(paragraph.Range.Text.replace(" ",""))

word.Selection.MoveUp(5)
word.Selection.WholeStory()
word.Selection.Find.MatchWildcards = True
find_result = word.Selection.Find.Execute("<参考文献>")
word.Selection.MoveRight()
word.Selection.TypeParagraph()
for _ in find_itmes:
    word.Selection.TypeText(_)
    word.Selection.MoveRight()
word.Selection.TypeText("____未进行标记____")
word.Selection.TypeParagraph()
for _ in nofind:
    word.Selection.TypeText(_.replace("\r", ""))
    word.Selection.MoveRight()