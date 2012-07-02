import re
import pprint
import json

# read object dump with inline line numbers
fileobj = open("main.objdump").read()
fileobj = fileobj.split('\n')[6:-1]

functions = [item.split('\n') for item in '\n'.join(fileobj).split('\n\n')]
functions = filter(bool, functions)

# read source file
filec = open("main.c").read()
filec = filec.split('\n')

# filter function definitions and includes
matchFunctions = re.compile(".*\([^;]*\).*{$")
matchInclude = re.compile("#.*")

def safeMatch(match = None):
	""" sugar function for regex matches """
	if match:
		return match.group()
	else:
		return None

def removeItems(regex, lst):
	""" takes a regular expression and a list and replaces all instances of the regex with an empty string """
	results = []
	for item in lst:
		results.append(safeMatch(re.search(regex, item)))
	return [item if item not in results else '' for item in lst]

# remove function definitions from the C code
filec = removeItems(matchInclude, filec)

last = 0
functionList = []

for function in functions:

	functionList.append({'name':'', 'lines':''})
	lineList = []

	for item in function: # iterate through the lists of lines

		if re.match("(.*/.*)+:\d+", item):

			lineNumber = int(item.split(':')[-1]) # determine the line number mentioned
			relevantLines = filter(bool, filec[last:lineNumber]) # all the non-empty lines between last and current line numbers
			comments = [item.replace('//', '').strip() for item in relevantLines if re.search("//.*", item)] # parse source code lines for comments
			code = [item.strip() for item in relevantLines if not re.search("//.*", item)] # clean lines
			lineList.append({'comment': comments}) # make new dictionary in lineList, add comments
			lineList[-1].update({'code': code}) # append the raw C code
			lineList[-1].update({'asm': []}) # make an empty dictionary for the parsed ASM
			last = lineNumber 

		elif re.match("\w{8} <(.*)>:", item):
			functionList[-1]['name'] = re.match("\w{8} <(.*)>:", item).groups()[0]
		elif re.match("\w+\(\):", item):
			pass
		else:
			cmd = re.search("\s+\t(?P<opcode>\w+)\t?(?P<addr0>[\w.+]+)?(, (?P<addr1>\w+))?.*", item).groupdict()
			cmd = dict([ (k, v) for k, v in cmd.iteritems() if v ])
			lineList[-1]['asm'].append(cmd) # append it to the asm object in the last line

	functionList[-1]['lines'] = lineList # append the line to the list of lines of the last function

functionList = {"functions":functionList}

import pystache

open('main.html', 'w').write(pystache.render(open("main.stache").read(), functionList))
