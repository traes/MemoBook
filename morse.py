# Script to find mnemonics for remembering the morse code alphabet

# morse code
morse = {}
morse['a'] = ".-"
morse['b'] = "-..."
morse['c'] = "-.-."
morse['d'] = "-.."
morse['e'] = "."
morse['f'] = "..-."
morse['g'] = "--."
morse['h'] = "...."
morse['i'] = ".."
morse['j'] = ".---"
morse['k'] = "-.-"
morse['l'] = ".-.."
morse['m'] = "--"
morse['n'] = "-."
morse['o'] = "---"
morse['p'] = ".--."
morse['q'] = "--.-"
morse['r'] = ".-."
morse['s'] = "..."
morse['t'] = "-"
morse['u'] = "..-"
morse['v'] = "...-"
morse['w'] = ".--"
morse['x'] = "-..-"
morse['y'] = "-.--"
morse['z'] = "--.."

# decore a word, given a character for . and -
def decode(word,dotchar,linechar):
	result = ""
	for char in word:
		if(char == dotchar):
			result += "."
		if(char == linechar):
			result += "-"
	return result

# return all words in a given file
def readwords(filename):
	result = []
	wordsfile = open(filename)
	for line in wordsfile:
		line = line.strip()
		line = line.lower()
		result.append(line)	
	wordsfile.close()
	return result

# find mnemonics for all characters using the give dot and line characters
def process(dictionary,dotchar,linechar):

	print "[dot] = " + dotchar + " " + "[line] = " + linechar

	results = {}
	words = readwords(dictionary)

	# find 
	for word in words:
		decoded = decode(word,dotchar,linechar)
		firstchar = word[0]
		if(morse[firstchar] == decoded):
			# initiate if necessary
			if(firstchar not in results):
				results[firstchar] = []
			# add element
			results[firstchar].append(word)

	# show words
	for c in "abcdefghijklmnopqrstuvwxyz":
		elements = results.get(c,[])
		elements.sort(key=len)
		print  c + ": " + " ".join(elements[0:10])

	# the score is based on the number of characters for which we found a word
	score = 0
	for c in "abcdefghijklmnopqrstuvwxyz":
		if(c in results):
			score += 1

	return score


# try all possible dot and line characters combinzations for the best scores
def find_best_score():
	scores = {}
	for dot in "abcdefghijklmnopqrstuvwxyz":
		for line in "abcdefghijklmnopqrstuvwxyz":
			score = process("words.txt",dot,line)
			scores[dot + "," + line] = score
			print dot + "," + line + " " + str(score)

	print "--- best matches ---"
	combokeys = scores.keys()
	combokeys = sorted(combokeys,key=lambda n:scores[n],reverse = True)

	for combokey in combokeys[0:30]:
		print combokey + ": " + str(scores[combokey])

process("words.txt","r","e")
