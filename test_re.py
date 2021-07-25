# -*- coding: utf-8 -*-
import re

Keyword = r'(?P<Keyword>(auto){1}|(double){1}|(int){1}|(if){1}|' \
			r'(#include){1}|(return){1}|(char){1}|(stdio\.h){1}|(const){1})'

Operator = r'(?P<Operator>\+\+|\+=|\+|--|-=|-|\*=|/=|/|%=|%|#)'


Separator = r'(?P<Separator>[,;:\{}:)(<>\[\]])'


Number = r'(?P<Number>\d*[.]?\d+)'

ID = r'(?P<ID>[a-zA-Z_][a-zA-Z_0-9]*)'

Cmd = r'(?P<Cmd>(cast){1}|(tooltips){1})'

Error = r'\"(?P<Error>.*)\"'

Annotation = r'(?P<Annotation>/\*(.|[\r\n])*/|//[^\n]*)'

# patterns = re.compile('|'.join([Annotation, Keyword, Cmd, ID, Number, Separator, Operator, Error]))

headerPatternMap = {
	# "h%s" % (i, ): r'(?P<h%s>(\t)*(#){%s}[^#]{1}(.*))' %(i, i) for i in range(1, 7)
	"header": r'(?P<header>([^#\s])*(#+)(.*))',
	
}
headerPatterns = list(headerPatternMap.values())

listPatternMap =  {
	# "l%s" % (i, ): r'(?P<l%s>(  ){%s}(-){1}(.*))' %(i, i-1) for i in range(1, 7)
	"list": r'(?P<list>(  )*[\+\-\*]{1}(.*))',
}
listPatterns = list(listPatternMap.values())

# 知识点：
# re.M 匹配多行，如果结合S，就会造成一个.*匹配了后续所有内容。
# re.S .额外匹配换行符，如果想要匹配类似python的docstring三单引号包围的字符串，则需要用词。
# re.I 不缺分大小写用。
patterns = re.compile('|'.join(headerPatterns + listPatterns))
line = '''
# 工作日志

### 7月19日

- 多语言翻译平台 - 文档和沟通 - G108沟通
  - 0716回复TechCall相关问题
  - 补充技术文档，关于DevDB和StringDB的关系
'''
# print(line)


print("* - "* 20)
for match in re.finditer(patterns, line):
	# print(match.groupdict()),
	print(match.lastgroup, match.group())

# 测试完毕，sub可以用来移除不想要的前缀
# print(re.sub(r'#{1,6}', "", "### 7月19#日", count=1))


print("* - "* 20)
matchObj = re.match(r'(#+){1}(.*)', "### 7月19日")
print("group: ", matchObj.group())	# group和group0是一样的
print("group0: ", matchObj.group(0))
print("group1: ", matchObj.group(1))
print("group2: ", matchObj.group(2))
print("groups: ", matchObj.groups())


print("* - "* 20)
matchObj = re.match(r'((  )*){1}[\+\-\*]{1}(.*)', "      - 7月19日")
print("group: ", matchObj.group())	# group和group0是一样的
print("group1: ", matchObj.group(1))
print("group2: ", matchObj.group(2))
print("groups: ", matchObj.groups())