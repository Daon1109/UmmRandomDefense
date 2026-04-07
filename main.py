
import random

f = open('C:/Coding/doodles/UmmRandomDefence/raw.txt', 'r', encoding='utf-8')
lines = f.readlines()
lines_raw = tuple(lines)

# preprocessing
realcharList = []   # 빈칸 함수에 넣을 실제 한자 리스트
realcharidxList = []
fixedblankidxList = []  # 고정빈칸 인덱스

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
        elif lines[col][row] == '*':        # * 표지자 사이 한자는 건너뜀
            if passToggle:
                passToggle=False
            else:
                passToggle=True
        elif passToggle:
            pass
        elif lines[col][row] == '(':        # () 사이 고정빈칸용 한자 인덱스 저장
            includeToggle = True
        elif lines[col][row] == ')':
            includeToggle = False
        else:                               # 써먹을 한자만 뽑기
            if includeToggle:
                fixed_blank_temp.append(row)
            realchar_temp.append(lines[col][row])
            realchar_idx_temp.append(row)

    realcharList.append(realchar_temp)
    realcharidxList.append(realchar_idx_temp)
    fixedblankidxList.append(fixed_blank_temp)


# settings
allblank = input('모든 한자를 빈칸 처리할까요? *로 표지된 글자들에는 적용되지 않습니다(y/n): ')
if allblank == 'n':
    randomblank = input('랜덤으로 빈칸을 지정할까요?(y/n): ')
    if randomblank == 'y':
        print('빈칸 개수: 문장당 최소 min개, 최대 max개')
        rand_min = int(input('min: '))
        rand_max = int(input('max: '))
        rand_blank_num = random.randint(rand_min, rand_max)


# eraser
answeridx = []                          # 답지용 인덱스 저장(얘는 [[col,row],] 형식임)
realcharlen = len(realcharidxList)
rand_blank_element = []
if allblank == 'y':
    for i in range(realcharlen):
        for j in realcharidxList[i]:
            lines[i] = list(lines[i])
            lines[i][j] = '  '          #'O'
            answeridx.append([i,j])
else:
    for i in range(realcharlen):
        if randomblank == 'y':          # 랜덤빈칸
            irowLength = len(realcharidxList[i])
            if rand_blank_num > irowLength:
                rand_blank_num = irowLength
            rand_blank_element = random.sample(realcharidxList[i], rand_blank_num)
        for j in realcharidxList[i]:
            if j in fixedblankidxList[i] or j in rand_blank_element:   # 고정빈칸 처리
                lines[i] = list(lines[i])
                lines[i][j] = '  '      #'O'
                answeridx.append([i,j])


# prettier output
print(f'\n{'-'*100}\nRESULT:\n')
for i in range(len(lines)):
    # 나중에 표지자들 싹 replace시키기
    pass
for j in range(len(lines)):
    print(f"{j+1}. ", end='')
    for k in range(len(lines[j])):
        print(lines[j][k], end='')

# answersheet
q_num = 0
print(f'\n\n\n{'-'*100}\nANSWER:')
for a in answeridx:
    if q_num == a[0]+1:
        if a[1] == a_idx_temp+1:
            print(lines_raw[a[0]][a[1]], end='')
        else:
            print(f"\n- {lines_raw[a[0]][a[1]]}", end='')
    else:
        q_num = a[0]+1
        print(f"\n{q_num}.")
        print(f"- {lines_raw[a[0]][a[1]]}", end='')
    a_idx_temp = a[1]


# Write PDF File

