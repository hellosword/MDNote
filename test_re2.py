# -*- coding: utf-8 -*-
import re


ExactString = r'(?P<ExactString>\"([^\"])*\")'
Operator = r'(?P<Operator>(OR){1}|(AND){1})'
Bracket = r'(?P<Bracket>\(|\)'
NormalString = r'(?P<NormalString>([^\"\s\(\)])+)'
NormalStringKey = "NormalString"
OperatorKey = "Operator"
BracketKey = "Bracket"

patterns = re.compile('|'.join([ExactString, Operator, NormalString]))


line = "我AND(你OR他和我)\"LaLaLa\""

print("* - "* 20)
itemList = []
for match in re.finditer(patterns, line):
    
    item = match.lastgroup, match.group()
    if item[0] == "ExactString":
        item = NormalStringKey, item[1][1:-1]
    print(item)
    itemList.append(item)

normalList = []
for item in itemList:
    if len(normalList) > 0:
        lastItem = normalList[-1]
        if lastItem[0] in (NormalStringKey, BracketKey) and item[0] == NormalStringKey:
            normalList.append(("Operator", "OR"))
    normalList.append(item)

#map(print, normalList)
print(normalList)

# 1.初始化两个栈：运算符栈s1和储存中间结果的栈s2；
# 2.从左至右扫描中缀表达式；
# 3.遇到操作数时，将其压s2；
# 4.遇到运算符时，比较其与s1栈顶运算符的优先级：
# 　（1）如果s1为空，或栈顶运算符为左括号“(”，则直接将此运算符入栈；
# 　（2）否则，若优先级比栈顶运算符的高，也将运算符压入s1；
# 　（3）否则，将s1栈顶的运算符弹出并压入到s2中，再次转到(4.1)与s1中新的栈顶运算符相比较； 
# 5.遇到括号时：　（1）如果是左括号"("，则直接压入s1　（2）如果是右括号")"，则依次弹出s1栈顶的运算符，并压入s2，直到遇到左括号为止，此时将这一对括号丢弃6.重复步骤2至5，直到表达式的最右边
# 7.将s1中剩余的运算符依次弹出并压入s2
# 8.依次弹出s2中的元素并输出，结果的逆序即为中缀表达式对应的后缀表达式
def compare(a, b):
    if a == "AND" and b == "OR":
        return 1
    elif b == "AND" and a == "OR":
        return -1
    else:
        return 0



s1,  s2 = [], []
i = 0
while i < len(normalList):
    item = normalList[i]
    if item[0] == NormalStringKey:
        s2.append(item)
    elif item[0] == OperatorKey:
        if len(s1) == 0:
            s1.append(item)
        elif s1[-1][0] == OperatorKey and compare(item[1], s1[-1][1]) > 0:
            s1.append(item)
        else:
            a = s1[-1]
            s1 = s1[:-1]
            s2.append(a)
            i -= 1
    elif item[0] == BracketKey:
        if item[1] == "(":
            s1.append(item)
        else:
            while True:
                if len(s1) == 0:
                    break
                topItem = s1[-1]
                if topItem[0] == BracketKey and topItem[1] == "(":
                    s1 = s1[:-1]
                    break
                if topItem[0] != BracketKey and topItem[1] != "(":
                    a = s1[-1]
                    s1 = s1[:-1]
                    s2.append(a)
    i += 1

while len(s1) > 0:
    a = s1[-1]
    s1 = s1[:-1]
    s2.append(a)
print(s2)
# print(list(reversed(s2)))