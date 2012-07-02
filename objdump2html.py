import re
import pprint
import json

# read object dump with inline line numbers
fileobj = open("main.objdump").read()

functions = [[item for item in item.split('\n') if bool(item)] for item in fileobj.split('\n\n') if item[0] != '\n']

# read source file
filec = open("main.c").read().splitlines()

# remove function definitions from the C code
filec = [item if not re.match("#.*", item) else '' for item in filec ]

last = 0
functionList = []

for function in functions:

	functionList.append({'name':'', 'lines':[]})

	for item in function: # iterate through the lists of lines

		if re.match("(.*/.*)+:\d+", item):
			functionList[-1]['lines'].append({'comment': [], 'code':[], 'asm':[]}) 
			lineNumber = int(item.split(':')[-1]) # determine the line number mentioned
			for line in filter(bool, filec[last:lineNumber]):
				match = re.search("((?<=// ).*)", line)
				if match:
					functionList[-1]['lines'][-1]['comment'].append(match.group())
				else:
					functionList[-1]['lines'][-1]['code'].append(line.strip())
			last = lineNumber 
		elif re.match("\w{8} <(.*)>:", item):
			functionList[-1]['name'] = re.match("\w{8} <(.*)>:", item).groups()[0]
		elif re.match("\w+\(\):", item):
			pass
		else:
			cmd = re.search("\s+\t(?P<opcode>\w+)\t?(?P<addr0>[\w.+]+)?(, (?P<addr1>\w+))?.*", item).groupdict()
			cmd = dict([ (k, v) for k, v in cmd.iteritems() if v ])
			functionList[-1]['lines'][-1]['asm'].append(cmd) # append it to the asm object in the last line

functionList = {"functions":functionList}

import pystache

open('main.html', 'w').write(pystache.render(open("main.stache").read(), functionList))
