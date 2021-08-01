# -*- coding: utf-8 -*-
from LibSrc.xmindparser import xreader
from common.singleton import Singleton
import re
import uuid

class JTreeNode(object):

	def __init__(self, title, level, date=None) -> None:
		self.title = title
		self.level = level
		self.date = date
		self.children = []
		self.parent = None

	def AppendChild(self, title, date=None):
		if self.date is not None and self.date != date:
			# 父子Date应该保持一致？先不这样
			pass
		newNode = JTreeNode(title, self.level+1, date)
		self.children.append(newNode)
		newNode.parent = self
		return newNode

	def SerializeTopic(self):
		topics = []
		for item in self.children:
			subDict = item.SerializeTopic()
			topics.append(subDict)
		
		infoDict = {
			'id': str(uuid.uuid1()),
			'title': self.title,	
			'topics': topics,
		}
		return infoDict



	def GetStr(self, depth=0):
		sstr = "  " * depth 
		if self.date:
			sstr += "Date:{}, ".format(self.date)
		sstr += "Title:{} \n".format(self.title)
		for item in self.children:
			sstr += item.GetStr(depth+1)
		return sstr

class OneThing(object):
	def __init__(self, date, topicTitle, JTNode) -> None:
		self.JTNode = JTNode
		self.topicTitle = topicTitle
		self.date = date

	def __str__(self) -> str:
		sstr = ""
		sstr = self.JTNode.title
		return sstr
	
	def _compare_tuple(self, a, b):
		n = min(len(a), len(b))
		for i in range(n):
			if a[i] > b[i]:
				return 1
			elif a[i] < b[i]:
				return -1
		return len(a) - len(b)
		
	def checkTime(self, start, end):
		"""Determine whether the time is within the interval [a, b)

		Args:
			start ([type]): [description]
			end ([type]): [description]

		Returns:
			[type]: [description]
		"""
		if start is not None:
			if self._compare_tuple(self.date, start) < 0:
				return False
		if end is not None:
			if self._compare_tuple(self.date, end) >= 0:
				return False
		return True

class Journal(object):
	def __init__(self) -> None:
		self.root = JTreeNode("root", -1)
		self.cur = self.root
		self.curDate = None
		
	def __str__(self) -> str:
		return self.root.GetStr(0)

	@classmethod
	def GetDate(cls, val):
		val = val.strip()
		matchObj = re.match(r'(\d+)[月\./]{1}(\d+)', val)
		if matchObj:
			mon = int(matchObj.group(1))
			day = int(matchObj.group(2))
			return mon, day
		return None

	def appendLevelData(self, level, content):
		if self.curDate is None:
			raise RuntimeError("Need date info!")
		if level == self.cur.level + 1:
			# 添加子项，指针下移
			self.cur = self.cur.AppendChild(content)
		elif level == self.cur.level:
			# 添加同级别的,指针后移
			if self.cur.parent is not None:
				self.cur = self.cur.parent.AppendChild(content)
			else:
				raise RuntimeError("Level Error")
		elif level < self.cur.level:
			n = self.cur.level - level
			while n > 0:
				self.cur = self.cur.parent
				if self.cur == None:
					raise RuntimeError("Level Error")
				n -= 1
			self.cur = self.cur.parent.AppendChild(content)
		else:
			raise RuntimeError("Level Jump Error")

	def append(self, mdType, level, content):
		# 开始之后
		if mdType == "header" and level == 3:
			# h3表示日期
			self.curDate = self.GetDate(content)
			if self.curDate:
				print("date: ", self.curDate)
			self.cur = self.root.AppendChild("day_root", self.curDate)
		elif mdType == "list":
			self.appendLevelData(level, content)
		else:
			raise RuntimeError("Unsupported md type in journal: {}, {}, {}".format(mdType, level, content))

	def GetThingList(self):
		'''
		获取话题列表
		'''
		things = []
		curDate = None
		for dayRootNode in self.root.children:
			curDate = dayRootNode.date
			for topicNode in dayRootNode.children:
				for subTopicNode in topicNode.children:
					oneThing = OneThing(curDate, topicNode.title, subTopicNode)
					things.append(oneThing)
		return things