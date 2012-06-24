import json
from bs4 import BeautifulSoup

import xml.etree.ElementTree as etree

ladder = json.loads(open("main.json").read())

def append(item):

	if isinstance(item, (unicode, str)):
		tree.data(item)

	elif isinstance(item, dict):
		for key, value in item.iteritems():
			tree.start("div",{"class":key})
			append(value)
			tree.end("div")

	elif isinstance(item, list):
		for thing in item:
			append(thing)

tree = etree.TreeBuilder()
tree.start("div", {"class":"body"})
append(ladder)
tree.end("div")


print BeautifulSoup(etree.tostring(tree.close())).prettify()
