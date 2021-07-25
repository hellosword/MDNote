# -*- coding: utf-8 -*-
from common.singleton import Singleton
import re
from journal import Journal

allPatternMap = {}
allMDClsMap = {}

def reg_md_pattern_cls():
	def _reg_md_pattern_cls(klass):
		allPatternMap.update(klass.patternMap)
		for k, v in klass.patternMap.items():
			allMDClsMap[k] = klass()
		return klass
	return _reg_md_pattern_cls

class PatternBase(Singleton):
	patternMap = {}
	
	def GetPatterns(self):
		patternList = list(self.patternMap.values())
		return patternList

@reg_md_pattern_cls()
class MDHeader(PatternBase):
	patternMap = {
		# 下面这种方式不是太好
		# "h%s" % (i, ): r'(?P<h%s>(\t)*(#){%s}[^#]{1}.*)' %(i, i) for i in range(1, 7)
		"header" :r'(?P<header>([^#\s])*(#+)(.*))',
	}
		
	def GetContent(self, val):
		# 这是一种替换的方法，但是不够接近本质
		# return re.sub(r'#{1,6}', "", val.strip(), count=1).strip()

		val = val.strip()
		matchObj = re.match(r'(#+){1}(.*)', val)
		if matchObj:
			# 解析出符号等级和内容
			level = len(matchObj.group(1).strip())
			content = matchObj.group(2).strip()
			return level, content
		return None, None

@reg_md_pattern_cls()
class MDList(PatternBase):
	patternMap =  {
		# "l%s" % (i, ): r'(?P<l%s>(  ){%s}(-){1}.*)' %(i, i-1) for i in range(1, 7)
		"list" : r'(?P<list>(  )*[\+\-\*]{1}(.*))'
	}

	def GetContent(self, val):
		# 这里和上面不同之处在于，我们需要精确的知道双空格的总数量
		matchObj = re.match( r'((  )*){1}[\+\-\*]{1}(.*)', val)
		if matchObj:
			level = int(len(matchObj.group(1)) / 2)
			content = matchObj.group(3).strip()
			# 级别默认从1开始
			return level+1, content
		return None, None


class MDTree(object):
	# 知识点：
	# re.M 匹配多行，如果结合S，就会造成一个.*匹配了后续所有内容。
	# re.S .额外匹配换行符，如果想要匹配类似python的docstring三单引号包围的字符串，则需要用词。
	# re.I 不缺分大小写用。

	def __init__(self) -> None:
		self.infoList = []
		self.raw = []
		self.raw2 = []
		self.patterns = re.compile('|'.join(list(allPatternMap.values())))

	def GetTypeParser(self, mdType):
		return allMDClsMap.get(mdType)


	def load(self, path):
		with open(path, "r", encoding='utf-8') as f:
			data =f.read()
			# for item in f.readlines():
			# 	self.raw.append(item)
				# print(repr(item))
		for match in re.finditer(self.patterns, data):
			# match.groupdict(),
			mdType, lineInfo = match.lastgroup, match.group()
			# print(mdType, lineInfo)
			tp = self.GetTypeParser(mdType)	
			level, content = tp.GetContent(lineInfo)
			self.raw2.append((mdType, level, content))

	def GetJournal(self):
		journal = Journal()

		curState = 0		
		for item in self.raw2:
			mdType, level, content = item
			
			if mdType == "header" and level == 2:
				if content == "工作日志":
					curState = 1
				else:
					curState = 0
				continue
			
			if curState == 1:
				journal.append(mdType, level, content)
		
		return journal		


