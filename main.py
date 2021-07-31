# -*- coding: utf-8 -*-
import pprint
import re
from sys import prefix
from LibSrc import xmindparser


pp = pprint.PrettyPrinter(indent=2)
# pp.pprint(xmindDict)


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
	

	def BuildTree(self, topicDict, parent=None):
		self.InitNode(topicDict['id'], topicDict['title'], parent)		
		if 'topics' in topicDict:
			self.BuildSubTree(topicDict['topics'])

	def BuildSubTree(self, subList):
		for subTopic in subList:
			newNode = self.AddChild(subTopic["id"], subTopic['title'])
			if 'topics' in subTopic:
				newNode.BuildSubTree(subTopic['topics'])

	def AddChild(self, childId, title):
		if self.HasChild(childId):
			raise RuntimeError("Duplicated Node Error: add child.")
		newNode = TopicTreeNode()
		newNode.InitNode(childId, title, self)
		
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

	def InitNode(self, nodeId, title, parent=None):
		self.id = nodeId
		self.title = title
		self.parent = parent
		if parent:
			self.path.extend(parent.path)
		self.path.append((self.id, self.title))

	def InsertPath(self, fullPathList, oneThing):
		if len(fullPathList) == 0:
			self.thingList.append(oneThing)
		else:
			childId, childTitle = fullPathList[0]
			restPath = fullPathList[1:]

			childNode = self.GetChildByID(childId)
			if childNode is None:
				childNode = self.AddChild(childId, childTitle)
			
			childNode.InsertPath(restPath, oneThing)
	
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

		


class Outline(object):

	def __init__(self):
		self.rootNode = TopicTreeNode() 
		self.revPathDict = {}

	def load(self, xmindDict):
		self.rootList = []
		for sheetDict in xmindDict:
			if sheetDict['topic']['title'] == "工作内容框架":
				self.rootNode.BuildTree(sheetDict['topic'], None)
				break

		
		pathList = self.rootNode.GenerateReversePath()
		for root2leafPath in pathList:
			leaf2rootPath = list(reversed(root2leafPath))
			leafid, leafTitle = leaf2rootPath[0]
			self.revPathDict.setdefault(leafTitle, []).append(leaf2rootPath)				

		print("\n -----------------------revPathDict------------------------")
		pp.pprint(self.revPathDict)

	def GetOutlinePath(self, topicSimplePath):
		"""[summary]

		Args:
			topicSimplePath ([type]): 这个列表的每个元素只有一个Title， 不包含id信息，注意这一点和revPathDict是不同的

		Returns:
			[type]: [description]
		"""
		reverseSimplePath = list(reversed(topicSimplePath))
		outlineList = self.revPathDict.get(reverseSimplePath[0], None)
		if outlineList is None:
			return False, "No path match-01!"

		def checkPathMatch(fullPath):
			i, j = 0, 0
			while i < len(reverseSimplePath) and j < len(fullPath):
				titleId, title = fullPath[j]
				if reverseSimplePath[i] == title:
					i += 1
					j += 1
				else:
					j += 1
			if i == len(reverseSimplePath):
				return True
			else:
				return False

		validList = []
		for fullPath in outlineList:
			isMatch = checkPathMatch(fullPath)
			if isMatch:
				# 说明找到了
				validList.append(list(reversed(fullPath)))
		if len(validList) > 1:
			# raise RuntimeError()
			return False, "Duplication Path Error!"
		elif len(validList) == 1:
			return True, validList[0]
		else:
			return False, "No path match-03!"




	def buildOutlineTree(self, thingList):
		notMatchedList = []
		matchedList = []
		for oneThing in thingList:
			topicTitle = oneThing.topicTitle
			topicSimplePath = [val.strip() for val in topicTitle.split('-')]
			isMatched, exData = self.GetOutlinePath(topicSimplePath)
			if not isMatched:
				notMatchedList.append((
					oneThing, exData
				))
			else:
				fullPath = exData
				matchedList.append((
					oneThing, fullPath
				))
		if len(notMatchedList) > 0:
			for item in notMatchedList:
				oneThing, exData = item
				print(oneThing.date, oneThing.topicTitle, exData)
		else:
			# 全都match上了，我们打印一下结果
			newTreeRoot = TopicTreeNode()
			for item in matchedList:
				oneThing, fullPath = item
				print(fullPath, oneThing)
				newTreeRoot.InsertPath(fullPath, oneThing)

			print(newTreeRoot.GetStr())
			

# class MDTreeNode(object):

from mdParser import MDTree


atHome = True

if atHome == True:
	xmindPath = r"E:\CloudDisk\Nas001\工作内容\工作记录\structure.xmind"
	mdPath = r"E:\CloudDisk\Nas001\工作内容\工作记录\2021.md"
else:
	xmindPath = r"E:\Qsync\工作内容\工作记录\structure.xmind"
	mdPath = r"E:\Qsync\工作内容\工作记录\2021.md"

def printSplitter(txt):
	print("# "* 40)
	print("# ", txt)
	print("# "* 40)

# 加载MD文件，匹配和解析header和list
md = MDTree()
md.load(mdPath)

# 基于header和list结构，构建日志树
jounral = md.GetJournal()
# 基于日志树，平铺展开为话题列表
thingList = jounral.GetThingList()
printSplitter("topicList")
pp.pprint(thingList)



# 加载xmind文件
xmindparser.config["showTopicId"] = True
xmindDict = xmindparser.xmind_to_dict(xmindPath)
pp.pprint(xmindDict)

# 基于xmind文件，生成话题树
o = Outline()
o.load(xmindDict)

# 将话题列表，排入xmind构架的Outline当中
o.buildOutlineTree(thingList)


