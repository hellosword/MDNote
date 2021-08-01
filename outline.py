# -*- coding: utf-8 -*-
from topic_tree import TopicTreeNode

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

		# print("\n -----------------------revPathDict------------------------")
		# pp.pprint(self.revPathDict)

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




	def buildOutlineTree(self, thingList, start, end):
		notMatchedList = []
		matchedList = []
		for oneThing in thingList:
			if not oneThing.checkTime(start, end):
				continue				
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
			newTreeRoot = self.rootNode
			newTreeRoot.ClearAllThings()
			for item in matchedList:
				oneThing, fullPath = item
				print(fullPath, oneThing)
				newTreeRoot.InsertPath(fullPath[1:], oneThing)

			report_str = newTreeRoot.BuildStr()
			print(report_str)
			return report_str
			
