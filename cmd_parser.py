# -*- coding:utf-8 -*-

import sys
import getopt

class CmdParser(object):
	def __init__(self) -> None:
		# éçšćæ°
		self.func = None
		self.start = None
		self.end = None
		self.xmind = None
		self.markdown = None
		self.output = None

	def get_date(self, dateStr):
		dateStrArr = dateStr.strip().split(".")
		return (int(dateStrArr[0]), int(dateStrArr[1]))

	def parser(self, func, args):
		self.func = func

		try:
			opts, args = getopt.getopt(args, "s:e:x:m:o:", ["start=","end=", "xmind=", "markdown=", "output="])
		except getopt.GetoptError as err:
			print(str(err))
			sys.exit(2)

		for o, a in opts:
			if o in ("-s", "--start"):
				self.start = self.get_date(a)
			elif o in ("-e", "--end"):
				self.end = self.get_date(a)
			elif o in ("--xmind", "-x"):
				self.xmind = a
			elif o in ("--markdown", "-m"):
				self.markdown = a
			elif o in ("--output", "-o"):
				self.output = a

			



