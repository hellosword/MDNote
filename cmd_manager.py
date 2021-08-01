# -*- coding:utf-8 -*-

from cmd_decorator import cmd_map

# 获取指令函数
def get_cmd_func(funcName):
	return cmd_map.get(funcName, None)