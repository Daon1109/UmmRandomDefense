
import random
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import html

f = open('C:/Coding/doodles/UmmRandomDefense/raw.txt', 'r', encoding='utf-8')
lines = f.readlines()
lines_raw = tuple(lines)

# preprocessing
realcharList = []
realcharidxList = []
fixedblankidxList = []

passToggle = False
includeToggle = False
ignore = ['.', '\n', ',', ' ', ';', '?']
ignore_custom = input("무시할 한자를 입력하세요(없으면 엔터): ")
ignore_custom = ignore_custom.split(', ')
for i in range(len(ignore_custom)):
    ignore.append(ignore_custom[i])

for col in range(len(lines)):
    realchar_temp = []
    realchar_idx_temp = []
    fixed_blank_temp = []

    for row in range(len(lines[col])):
        if lines[col][row] in ignore:
            pass
        elif lines[col][row] == '*':
            passToggle = not passToggle
        elif passToggle:
            pass
        elif lines[col][row] == '(':
            includeToggle = True
        elif lines[col][row] == ')':
            includeToggle = False
        else:
            if includeToggle:
                fixed_blank_temp.append(row)
            realchar_temp.append(lines[col][row])
            realchar_idx_temp.append(row)

    realcharList.append(realchar_temp)
    realcharidxList.append(realchar_idx_temp)
    fixedblankidxList.append(fixed_blank_temp)

# settings
allblank = input('모든 한자를 빈칸 처리할까요? (y/n): ')
if allblank == 'n':
    randomblank = input('랜덤으로 빈칸을 지정할까요? (y/n): ')
    if randomblank == 'y':
        rand_min = int(input('min: '))
        rand_max = int(input('max: '))
        rand_blank_num = random.randint(rand_min, rand_max)

# eraser
answeridx = []
realcharlen = len(realcharidxList)
rand_blank_element = []

if allblank == 'y':
    for i in range(realcharlen):
        for j in realcharidxList[i]:
            lines[i] = list(lines[i])
            lines[i][j] = '  '
            answeridx.append([i, j])
else:
    for i in range(realcharlen):
        if randomblank == 'y':
            irowLength = len(realcharidxList[i])
            if rand_blank_num > irowLength:
                rand_blank_num = irowLength
            rand_blank_element = random.sample(realcharidxList[i], rand_blank_num)

        for j in realcharidxList[i]:
            if j in fixedblankidxList[i] or j in rand_blank_element:
                lines[i] = list(lines[i])
                lines[i][j] = '  '
                answeridx.append([i, j])

# prettier output
print(f'\n{"-"*100}\nRESULT:\n')
for i in range(len(lines)):
    lines[i] = ''.join(lines[i])
    lines[i] = lines[i].replace('*', '')
    print(f"{i+1}. {lines[i]}")
    lines[i] = f'{i+1}. ' + lines[i]

# answersheet
q_num = 0
a_idx_temp = -1
answer_lines = []

print(f'\n\n{"-"*100}\nANSWER:')

for a in answeridx:
    if q_num == a[0] + 1:
        if a[1] == a_idx_temp + 1:
            print(lines_raw[a[0]][a[1]], end='')
            answer_lines[-1] += lines_raw[a[0]][a[1]]
        else:
            print(f"\n- {lines_raw[a[0]][a[1]]}", end='')
            answer_lines.append(f"- {lines_raw[a[0]][a[1]]}")
    else:
        q_num = a[0] + 1
        print(f"\n{q_num}.")
        print(f"- {lines_raw[a[0]][a[1]]}", end='')
        answer_lines.append(f"{q_num}.")
        answer_lines.append(f"- {lines_raw[a[0]][a[1]]}")

    a_idx_temp = a[1]

# ---------------- PDF(by GPT) ----------------
pdfmetrics.registerFont(TTFont("msyh", "msyh.ttc"))
pdfmetrics.registerFont(TTFont("Noto", "C:/Coding/doodles/Fonts/Noto_Sans_TC/static/NotoSansTC-Medium.ttf"))
pdfmetrics.registerFont(TTFont("uni", "C:/Coding/doodles/Fonts/unifont-16.0.04.ttf"))

pdf = SimpleDocTemplate(
    'C:/Coding/doodles/UmmRandomDefense/result/URD.pdf',
    pagesize=A4
)

style = ParagraphStyle(
    name="Custom",
    fontName="Noto",
    fontSize=15,
    leading=18
)

def can_render(char, font_name):
    try:
        font = pdfmetrics.getFont(font_name)
        return ord(char) in font.face.charToGlyph
    except:
        return False

FONT_PRIORITY = ["msyh", "Noto", "uni"]

def split_by_font(text):
    result = []
    current_font = None
    buffer = ""

    for ch in text:
        for font in FONT_PRIORITY:
            if can_render(ch, font):
                selected_font = font
                break
        else:
            selected_font = FONT_PRIORITY[0]

        if selected_font != current_font:
            if buffer:
                result.append((current_font, buffer))
            buffer = ch
            current_font = selected_font
        else:
            buffer += ch

    if buffer:
        result.append((current_font, buffer))

    return result

elements = []

# 문제 영역
for row in lines:
    line = html.escape(row)
    line = line.replace(" ", "&nbsp;&nbsp;")

    chunks = split_by_font(line)

    formatted_line = ""
    for font_name, text_chunk in chunks:
        formatted_line += f'<font name="{font_name}">{text_chunk}</font>'

    elements.append(Paragraph(formatted_line, style))
    elements.append(Spacer(1, 10))

elements.append(PageBreak())

# 정답 영역
elements.append(Paragraph("<b>ANSWER</b>", style))
elements.append(Spacer(1, 20))

for row in answer_lines:
    line = html.escape(row)
    line = line.replace(" ", "&nbsp;&nbsp;")

    chunks = split_by_font(line)

    formatted_line = ""
    for font_name, text_chunk in chunks:
        formatted_line += f'<font name="{font_name}">{text_chunk}</font>'

    elements.append(Paragraph(formatted_line, style))
    elements.append(Spacer(1, 10))

pdf.build(elements)
