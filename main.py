# -*- coding: utf-8 -*-
import sys
import cmd_impl

def work():	
	cmdArgs = []
	if len(sys.argv) == 1:
		func = None
	else:
		func = sys.argv[1]
		cmdArgs  = sys.argv[2:]

	if func == None:
		print("Need function name!")
		return

	from cmd_parser import CmdParser
	from cmd_manager import get_cmd_func
	cmd_obj = CmdParser()
	cmd_obj.parser(func, cmdArgs)
	
	work_func = get_cmd_func(func)
	if work_func:
		work_func(cmd_obj)
	else:
		print("Cannot find cmd: ", func)


if __name__ == "__main__":
	work()