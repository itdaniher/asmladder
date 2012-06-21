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

# remove function definitions from the C code
filec = removeItems(matchInclude, filec)

last = 0
functionList = []

for function in functions:

	functionList.append([])
	lineList = []

	if len(function) != 0: # robustify the function parser by ignoring empty ones

		for item in function: # iterate through the lists of lines

			if item[0] == '/': # if not a /path:number reference, then assume it to be assembly

				lineNumber = int(item.split(':')[-1]) # determine the line number mentioned
				relevantLines = filter(bool, filec[last:lineNumber]) # all the non-empty lines between last and current line numbers
				comments = [item.replace('//', '').strip() for item in relevantLines if item.find('//') != -1] # parse source code lines for comments
				code = [item.strip() for item in relevantLines if item.find('//') == -1] # clean lines
				lineList.append({'comment': comments}) # make new dictionary in lineList, add comments
				lineList[-1].update({'code': code}) # append the raw C code
				lineList[-1].update({'asm': []}) # make an empty dictionary for the parsed ASM
				last = lineNumber 

			else:

				item = item.split() # split the line
				if item.count(';') > 0: # if the line contains a semicolon
					item = item[0:item.index(';')] # remove it, and everything after it
				try: # check to see if the line starts with an offset
					int(item[0]) # asm lines specifying function/offset start with an integer
					functionList[-1].append(re.sub('[<>:]', '', item[1])) # use the string at index = 1 as the name of the function
				except:

					if item[0].find('()') == -1: # check to make sure that this isn't a function definition
						item = item[3::] # discard line number and bytecode 
						cmd = {'opcode':item[0]} # build 'cmd' dictionary with opcode
						addrs = list([txt.strip(',') for txt in item[1::]]) # build list of opcode arguments
						for i in range(len(addrs)): # iterate over list
							cmd.update({'addr'+str(i):addrs[i]}) # for item in list, add a regx:value pair to 'cmd'
						lineList[-1]['asm'].append(cmd) # append it to the asm object in the last line

		functionList[-1].append(lineList) # append the line to the list of lines of the last function

pprint.pprint(functionList)
open("main.json", "w").write(json.dumps(functionList, indent=1))
