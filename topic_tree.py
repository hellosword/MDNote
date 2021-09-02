# -*- coding: utf-8 -*-
def int_to_Roman(num, needSub=True):
	val = [
		1000, 900, 500, 400,
		100, 90, 50, 40,
		10, 9, 5, 4,
		1
		]
	syb = [
		"M", "CM", "D", "CD",
		"C", "XC", "L", "XL",
		"X", "IX", "V", "IV",
		"I"
		]
	roman_num = ''
	i = 0
	while  num > 0:
		for _ in range(num // val[i]):
			roman_num += syb[i]
			num -= val[i]
		i += 1
	return roman_num.lower() if needSub else roman_num

def int_to_alphabat(index):
	return chr(ord('`')+index)
# LETTERS = {letter: str(index) for index, letter in enumerate(ascii_lowercase, start=1)} 

class TopicTreeNode(object):
	# NODE_TYPE_ROOT = 0
	# NODE_TYPE_BRACH = 1
	# NODE_TYPE_LEAF = 2
	def __init__(self) -> None:
		# super(TopicTreeNode, self).__init__()
		self.id = None
		self.title = None
		self.children = []
		self.childrenIdToIndex = {}
		self.parent = None
		self.path = []

		self.thingList = []
		self.thingRecurCnt = None

		self.labels = ""
	

	def BuildTree(self, topicDict, parent=None):
		self.InitNode(topicDict, parent)		
		if 'topics' in topicDict:
			self.BuildSubTree(topicDict['topics'])

	def BuildSubTree(self, subList):
		for subTopic in subList:
			newNode = self.AddChild(subTopic)
			if 'topics' in subTopic:
				newNode.BuildSubTree(subTopic['topics'])

	def AddChild(self, subTopic):
		childId = subTopic["id"]
		if self.HasChild(childId):
			raise RuntimeError("Duplicated Node Error: add child.")
		newNode = TopicTreeNode()
		newNode.InitNode(subTopic, self)
		
		self.children.append(newNode)
		self.childrenIdToIndex[childId] = len(self.children) - 1
		return newNode

	def GetChildByID(self, childId):
		childIndex = self.childrenIdToIndex.get(childId, None)
		if childIndex is None:
			return None
		else:
			return self.children[childIndex]

	def HasChild(self, childId):
		return self.GetChildByID(childId) is not None

	def InitNode(self, infoDict, parent=None):
		# self.id = infoDict["id"]
		# self.title = infoDict["title"]
		for key in infoDict.keys():
			if hasattr(self, key):
				setattr(self, key, infoDict[key])

		self.parent = parent
		if parent:
			self.path.extend(parent.path)
		self.path.append((self.id, self.title))

	def InsertPath(self, fullPathList, oneThing, autoNewPath=False):
		if len(fullPathList) == 0:
			self.thingList.append(oneThing)
		else:
			childId, childTitle = fullPathList[0]
			restPath = fullPathList[1:]

			childNode = self.GetChildByID(childId)
			if childNode is None:
				if autoNewPath:
					childNode = self.AddChild(childId, childTitle)
				else:
					raise RuntimeError("Path Error: ", fullPathList)
			
			childNode.InsertPath(restPath, oneThing)
	
	def ClearAllThings(self):
		self.thingList = []
		self.thingRecurCnt = None
		for child in self.children:
			child.ClearAllThings()

	def CountThings(self, isRecursive=True):
		if isRecursive and self.thingRecurCnt is not None:
			return self.thingRecurCnt

		n = len(self.thingList) 
		if isRecursive:
			# from functools import reduce
			# n += reduce(lambda a, b: a + b, [len(child.thingList) for child in self.children])
			n += sum([child.CountThings() for child in self.children])

		# 好像并不会重复计算，这个缓存应该没什么卵用
		self.thingRecurCnt = n

		return n

	def GetStr(self, prefix=""):
		
		prefix =  prefix + "    "
		sstr = ""
		sstr += prefix + "<{}>\n".format(self.title)
		n = len(self.thingList)
		if n > 0:
			for oneThing in self.thingList:
				sstr += prefix + "    Thing: {}\n".format(oneThing)
		
		for item in self.children:
			sstr += item.GetStr(prefix)
		return sstr

	def BuildStr(self):
		if self.CountThings(isRecursive=True) == 0:
			# 没有做事情的分支，啥也不显示
			return ""

		level = len(self.path)
		
		prefix =  "    " * level
		sstr = ""
		n = self.CountThings()
		sstr += prefix + "{}({})\n".format(self.title, n)
		# if self.labels:
		# 	print(self.labels)
		if level == 2 or "flatten" in self.labels:
			itemList = self.BuildThingList([])
			# itemList = sorted(itemList, key=lambda item: item[1])
			lienList = ["{:>2}.".format(index+1) + ("" if len(item[0]) == 0 else "【{}】".format("/".join(item[0]))) + "{}".format(item[1]) for index, item in enumerate(itemList)]
			for line in lienList:
				if not line.endswith("。"):
					line += "。"
				sstr += prefix + "    " + line + "\n"
		else:
			for item in self.children:
				sstr += item.BuildStr()
		return sstr

	def BuildThingList(self, prefix):
		result = []
		newprefix = []
		newprefix.extend(prefix)
		# newprefix.append(self.title)

		# thingList = sorted(, reverse=True, key=lambda item: item.date)
		if self.title == "预警节点":
			print(11)
		for oneThing in self.thingList:
			result.append((
				newprefix, oneThing
			))
		for child in self.children:
			t = [] + prefix
			t.append(child.title)
			result.extend(child.BuildThingList(t))

		return result


	def GenerateReversePath(self):
		"""[summary]
		返回全部的路径列表，结构为
		[
			[
				(rootId, rootTitle),
				...,
				(leafId, leafTitle),
			]
		]
		Returns:
			[type]: [description]
		"""
		indexList = [1, 0]
		d = 1
		p = self
		resultList = []
		def visit(node):
			if len(node.children) == 0:
				# 访问到叶子节点
				resultList.append(node.path)
			else:
				# 枝节点也可以添加子项 - 和叶节点的处理没有区别
				resultList.append(node.path)

		while p is not None:
			nextChildIndex = indexList[d]
			if nextChildIndex < len(p.children):
				# 访问子节点
				p = p.children[nextChildIndex]
				# 当前层指针后移
				indexList[d] += 1
				# 层数+1
				d += 1
				# 下一层指针重置为0
				indexList.append(0)
			else:
				# 子节点都访问完了，那么访问节点自身
				visit(p)
				# 清空当前层指针，且层数减一
				indexList = indexList[:-1]				
				d -= 1				
				p = p.parent
		
		return resultList

	##########################################
	# 新版的一些处理

	def BuildTopicThingList(self):
		if self.CountThings2(isRecursive=True) == 0:
			# 没有做事情的分支，啥也不显示
			return ""

		level = len(self.path)
		
		prefix =  "    " * level
		sstr = ""
		# n = self.CountThings2()
		sstr += prefix + "{}\n".format(self.title)
		# if self.labels:
		# 	print(self.labels)
		if level == 2 or "flatten" in self.labels:
			itemList = self.BuildThingList2([], hasSelfTitle=False)

			lastPack = []
			lastPath = None
			lienList = []
			def buildPack(index):
				if lastPath is not None:	
					if len(lastPack) <= 2:
						# 只有一条则只占领一行
						for line in lastPack:
							newStr = "{:>2}.".format(index) + lastPath + "{}".format(line)
							index += 1
							lienList.append(newStr)
					else:
						newStr = "{:>2}.".format(index) + lastPath + "："
						index += 1
						lienList.append(newStr)
						subIndex = 1
						for subline in lastPack:
							newStr = "        {}.{}".format(int_to_alphabat(subIndex), subline)
							lienList.append(newStr)
							subIndex += 1
				return index
			index = 1
			for item in itemList:
				curPath = "" if len(item[0]) == 0 else "【{}】".format("/".join(item[0]))
				curline = "{}".format(item[1])
				if not curline.endswith("。"):
					curline += "。"
				if curPath == lastPath:
					lastPack.append(curline)
				else:
					index = buildPack(index)
					lastPath = curPath
					lastPack = [curline]
			buildPack(index)

			# lienList = ["{:>2}.".format(index+1) + ("" if len(item[0]) == 0 else "【{}】".format("/".join(item[0]))) + "{}".format(item[1]) for index, item in enumerate(itemList)]
			for line in lienList:
				sstr += prefix + "    " + line + "\n"
		else:
			for item in self.children:
				sstr += item.BuildTopicThingList()
		return sstr

	def BuildThingList2(self, prefix, hasSelfTitle=True):
		result = []
		# newprefix = []
		# newprefix.extend(prefix)
		# newprefix.append(self.title)

		# thingList = sorted(, reverse=True, key=lambda item: item.date)
		isThingNode = self.IsThingNode()
		if isThingNode:
			startIndex = self.title.find("-")
			title = self.title[startIndex+1:]
			result.append((
				prefix, title
			))
		else:
			t = [] + prefix
			if hasSelfTitle:
				t.append(self.title)
			for child in self.children:
				result.extend(child.BuildThingList2(t))

		return result

	def IsThingNode(self):
		return self.title.strip().startswith("-")

	def CountThings2(self, isRecursive=True):
		if isRecursive and self.thingRecurCnt is not None:
			return self.thingRecurCnt

		n = 0

		isThingNode = self.IsThingNode()
		if isThingNode:
			n = 1
		elif isRecursive:
			# from functools import reduce
			# n += reduce(lambda a, b: a + b, [len(child.thingList) for child in self.children])
			n += sum([child.CountThings2() for child in self.children])

		# 好像并不会重复计算，这个缓存应该没什么卵用
		self.thingRecurCnt = n

		return n
		

