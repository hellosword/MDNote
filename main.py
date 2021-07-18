import pprint
import xmindparser

xmindparser.config["showTopicId"] = True
xmindDict = xmindparser.xmind_to_dict(r"xmind_zen.xmind")

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(xmindDict)