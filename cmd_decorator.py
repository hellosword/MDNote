# -*- coding:utf-8 -*-

cmd_map = {}
# 装饰器
def usercmd(cmdName, **mkwarges):
	def _gmcmd(func):
		global cmd_map

		cmd_map[cmdName] = func
		func.usage = mkwarges.get("usage", "no usage")

		def wrapper(*args, **kwargs):
			print("RunCmd: {}\n args:{}\n kwargs:{}".format(cmdName, args, kwargs))
			func(*args, **kwargs)

		return wrapper
	return _gmcmd