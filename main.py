# -*- coding: utf-8 -*-
import pprint
import re
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
		self.parent = None
		self.path = []
		
	def loadRecursively(self, topicDict, parent=None):
		self.id = topicDict['id']
		self.title = topicDict['title']
		self.parent = parent
		if parent:
			self.path.extend(parent.path)
		self.path.append(self.title)		

		titleSet = set()		
		if 'topics' in topicDict:
			for subTopicDict in topicDict['topics']:
				subTitle = subTopicDict['title']
				
				assert subTitle not in titleSet, "A duplicate name exists within same depth!!!"
				titleSet.add(subTitle)

				topicNode = TopicTreeNode()
				topicNode.loadRecursively(subTopicDict, self)
				self.children.append(topicNode)

	def GenerateReversePath(self):
		indexList = [1, 0]
		d = 1
		p = self
		resultList = []
		def visit(node):
			if len(node.children) == 0:
				# 访问到叶子节点
				resultList.append((node.path, node.id))

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
		self.rootList = []
		self.revPathDict = {}

	def load(self, xmindDict):
		self.rootList = []
		for sheetDict in xmindDict:
			topicNode = TopicTreeNode()
			topicNode.loadRecursively(sheetDict['topic'], None)
			
			self.rootList.append(topicNode)

		for rootNode in self.rootList:
			pathList = rootNode.GenerateReversePath()
			for nodeInfo in pathList:
				path, nodeId = nodeInfo
				path = list(reversed(path))
				if len(path) > 1:
					self.revPathDict.setdefault(path[0], []).append((path[1:], nodeId))
				else:
					self.revPathDict.setdefault(path[0], [])

		pp.pprint(self.revPathDict)

	def GetOutlinePath(self, topicSimplePath):
		reverseSimplePath = list(reversed(topicSimplePath))
		outlineList = self.revPathDict.get(reverseSimplePath[0], None)
		if outlineList is None:
			return False, "No path match-01!"

		def checkPathMatch(fullPath):
			i, j = 1, 0
			while i < len(reverseSimplePath) and j < len(fullPath):
				if reverseSimplePath[i] == fullPath[j]:
					i += 1
					j += 1
				else:
					j += 1
			if i == len(reverseSimplePath):
				return True
			else:
				return False

		if len(outlineList) == 1:
			# 这里也要做一次检查
			isMatch = checkPathMatch(outlineList[0][0])
			if isMatch:
				return True, outlineList[0]
			else:
				return False, "No path match-02!"
		else:
			validList = []
			for item in outlineList:
				fullPath, nodeID = item
				isMatch = checkPathMatch(fullPath)
				if isMatch:
					# 说明找到了
					validList.append(item)
			if len(validList) > 1:
				# raise RuntimeError()
				return False, "Duplication Path Error!"
			elif len(validList) == 1:
				return True, validList[0]
			else:
				return False, "No path match-03!"




	def buildOutlineTree(self, topicList):
		for item in topicList:
			topicTitle = item['topicTitle']
			topicSimplePath = [val.strip() for val in topicTitle.split('-')]
			isMatched, exData = self.GetOutlinePath(topicSimplePath)
			if not isMatched:
				print(isMatched, exData)
				print("\t", topicTitle)


# class MDTreeNode(object):

from mdParser import MDTree


atHome = True

if atHome == True:
	xmindPath = r"E:\CloudDisk\Nas001\工作内容\工作记录\structure.xmind"
	mdPath = r"E:\CloudDisk\Nas001\工作内容\工作记录\2021.md"
else:
	xmindPath = r"E:\Qsync\工作内容\工作记录\structure.xmind"
	mdPath = r"E:\Qsync\工作内容\工作记录\2021.md"


# 加载MD文件，匹配和解析header和list
md = MDTree()
md.load(mdPath)

# 基于header和list结构，构建日志树
jounral = md.GetJournal()
# 基于日志树，平铺展开为话题列表
topicList = jounral.GetTopicList()
#pp.pprint(topicList)



# 加载xmind文件
xmindparser.config["showTopicId"] = True
xmindDict = xmindparser.xmind_to_dict(xmindPath)
pp.pprint(xmindDict)

# 基于xmind文件，生成话题树
o = Outline()
o.load(xmindDict)

# 将话题列表，排入xmind构架的Outline当中
o.buildOutlineTree(topicList)


