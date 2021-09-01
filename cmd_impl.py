# -*- coding: utf-8 -*-
from LibSrc.xmindparser.xreader import image_of
import pprint
import re
from sys import prefix
from LibSrc import xmindparser
import sys
from md_parser import MDTree
from cmd_decorator import usercmd
from outline import Outline
import time
import os
pp = pprint.PrettyPrinter(indent=2)


@usercmd("gen", usage="generate monthly report")
def generate001(cmdObj):
	xmindPath = cmdObj.xmind
	mdPath = cmdObj.markdown

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
	report_str = o.buildOutlineTree(thingList, cmdObj.start, cmdObj.end)
	
	if report_str is not None:
		timeSuffix = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
		fileName = os.path.join("report_{}.txt".format(timeSuffix))
		if cmdObj.output is not None:
			if os.path.exists(cmdObj.output):
				fileName = os.path.join(cmdObj.output, fileName)
			else:
				raise RuntimeError("Output path not exists! {}".format(cmdObj.output))
		

		with open(fileName, "w", encoding="utf-8") as f:
			f.write(report_str)


@usercmd("gen2", usage="generate monthly report")
def generate002(cmdObj):

	# py main.py gen2 -x=D:\CloudDisk\Qsync\工作内容\工作记录\2021-08.xmind
	xmindPath = cmdObj.xmind
	mdPath = cmdObj.markdown


	# 加载xmind文件
	xmindparser.config["showTopicId"] = True
	xmindDict = xmindparser.xmind_to_dict(xmindPath)
	# pp.pprint(xmindDict)

	# 基于xmind文件，生成话题树
	o = Outline()
	o.load(xmindDict)

	# 将话题列表，排入xmind构架的Outline当中
	report_str = o.BuildTopicThingList()
	
	if report_str is not None:
		timeSuffix = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
		fileName = os.path.join("report_{}.txt".format(timeSuffix))
		if cmdObj.output is not None:
			if os.path.exists(cmdObj.output):
				fileName = os.path.join(cmdObj.output, fileName)
			else:
				raise RuntimeError("Output path not exists! {}".format(cmdObj.output))
		

		with open(fileName, "w", encoding="utf-8") as f:
			f.write(report_str)
