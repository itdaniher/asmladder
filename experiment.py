import re

# read object dump with inline line numbers
fileobj = open("main.objdump").read()
fileobj = fileobj.split('\n')[6:-1]

# read source file
filec = open("main.c").read()
filec = filec.split('\n')

# filter function definitions and includes
matchFunctions = re.compile(".*\([^;]*\).*{$")
matchInclude = re.compile("#.*")

def safeMatch(match = None):
	if match:
		return match.group()
	else:
		return None

def removeItems(regex, lst):
	results = []
	for item in lst:
		results.append(safeMatch(re.search(regex, item)))
	return [item if item not in results else '' for item in lst]

filec = removeItems(matchInclude, filec)
filec = removeItems(matchFunctions, filec)

last = 0
for item in fileobj:
	if len(item) > 0: 
		if item[0] != '/':
			item = item.split()
			try:
				item = item[0:item.index(';')]
			except:
				pass
			if item[0].find(':') in [2,1]:
				item = item[3::]
			print "asm", item
		else:
			lineNumber = int(item.split(':')[-1])
			print "\n", "c", filter(bool, filec[last:lineNumber])
			last = int(lineNumber)

