import pprint
import re
from LibSrc import xmindparser

xmindparser.config["showTopicId"] = True
xmindDict = xmindparser.xmind_to_dict(r"structure.xmind")

pp = pprint.PrettyPrinter(indent=2)
# pp.pprint(xmindDict)


class TopicTreeNode(object):
	# NODE_TYPE_ROOT = 0
	# NODE_TYPE_BRACH = 1
	# NODE_TYPE_LEAF = 2
	def __init__(self) -> None:
		# super(TopicTreeNode, self).__init__()
		# self.id = None
		self.title = None
		self.children = []
		self.parent = None
		self.path = []
		
	def loadRecursively(self, topicDict, parent=None):
		# self.id = topicDict['id']
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
			for path in pathList:
				path = list(reversed(path))
				if len(path) > 1:
					self.revPathDict.setdefault(path[0], []).append(path[1:])
				else:
					self.revPathDict.setdefault(path[0], [])

		pp.pprint(self.revPathDict)

	def searchTitle()

o = Outline()
o.load(xmindDict)



