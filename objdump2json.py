import re
import pprint
import json

# read object dump with inline line numbers
fileobj = open("main.objdump").read()
fileobj = fileobj.split('\n')[6:-1]

functions = [item.split('\n') for item in '\n'.join(fileobj).split('\n\n')]

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

# remove includes and function definitions from the C code
filec = removeItems(matchInclude, filec)
#filec = removeItems(matchFunctions, filec)


last = 0
functionList = []

for function in functions:

	functionList.append([])
	lineList = []

	if len(function) != 0:

		for item in function:

			if item[0] == '/': # if not a /path:number reference, then assume it to be assembly

				lineNumber = int(item.split(':')[-1]) # determine the line number mentioned
				relevantLines = filter(bool, filec[last:lineNumber]) # all the non-empty lines between last and current line numbers
				comments = [item.replace('//', '').strip() for item in relevantLines if item.find('//') != -1]
				code = [item.strip() for item in relevantLines if item.find('//') == -1]
				lineList.append({'comment': comments})
				lineList[-1].update({'code': code})
				lineList[-1].update({'asm': []})
				last = lineNumber

			else:

				item = item.split() # split the line
				if item.count(';') > 0: 
					item = item[0:item.index(';')]
				try:
					int(item[0])
					functionList[-1].append(re.sub('[<>:]', '', item[1]))
				except:

					if item[0].find('()') == -1:
						item = item[3::] # discard line number and bytecode
						item = [item[0], list([item.strip(',') for item in item[1::]])]
						lineList[-1]['asm'].append(item)

		functionList[-1].append(lineList)

pprint.pprint(functionList)
json.dumps(functionList, indent=1)
