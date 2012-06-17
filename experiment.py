import re

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


# iterate through the dumped assembly and process it. 
# when a reference is made to a line in the C code, print all the lines between the last and most recent reference.
# parse lines from the dumped assembly and discard irrelevant information.

last = 0
for function in functions:
	for item in function:
		if len(item) > 0:
			if item[0] == '/': # if not a /path:number reference, then assume it to be assembly
				lineNumber = int(item.split(':')[-1]) # determine the line number mentioned
				relevantLines = filter(bool, filec[last:lineNumber]) # all the non-empty lines between last and current line numbers
				comments = [item.replace('//', '').strip() for item in relevantLines if item.find('//') != -1]
				code = [item.strip() for item in relevantLines if item.find('//') == -1]
				print '\n'
				print {'comment': comments}
				print {'code': code}
				last = lineNumber
			else:
				item = item.split() # split the line
				if item.count(';') > 0: 
					item = item[0:item.index(';')]
				try:
					int(item[0]) 
					print {"startFunction": item[1]}
				except:
					if item[0].find('()') == -1:
						item = item[3::] # discard line number and bytecode
						item = (item[0], tuple([item.strip(',') for item in item[1::]]))
						print {"asm": item}
	print ''
