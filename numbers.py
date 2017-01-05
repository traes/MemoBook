#!/usr/bin/python
import re
import os

# read words from file
def read_words(filename):
	result = []
	wordsfile = open(filename)
	for word in wordsfile:
		word = word.strip()
		word = word.lower()
		result.append(word)
	wordsfile.close()
	return result

# create regular expression for matching number word
def create_regex(number):
	lookup = "lntdrfspkg" # 0:l,1:n,2:t,...,g:9
	filler = "[^" + lookup + "v" + "]*" # v is reserved (avoids confusion with 'p' for 7)
	regexp = "^" + filler
	numberstring = str(number)
	for index in range(0,len(numberstring)):
		digit = numberstring[index]
		character = lookup[int(digit)]
		regexp += character + filler
	regexp += "$"
	return re.compile(regexp)

def search_matches(number,words):
	result = set([])
	regex = create_regex(number)
	for word in words:
		if(regex.match(word) and word != number):
			result.add(word)
	result = list(result)
	result.sort(key=len)
	return result

# process file
def process_sequence(dictfilename,outputfilename):
	maxwords = 20 # the max number of words to show for each number
	minwords = 5 # split word if fewer than minwords found
	dictwords = read_words(dictfilename)
	texfile = open(outputfilename,"w")
	texfile.write("\\documentclass{article}")
	texfile.write("\\begin{document}")
	texfile.write("\\title{Number Mnemonics}")
	texfile.write("\\author{Thomas Raes}")
	texfile.write("\\maketitle")
	for number in range(0,2100):
		print(number)
		texfile.write("\\paragraph{" + str(number) + "}")

		# try single word (e.g 1985)
		matches = search_matches(number,dictwords)
		for match in matches[0:maxwords]:
			texfile.write(match + "\n")

		# if only a few single words found, split number in two (eg. 19 and 85)
		if(len(matches) < minwords):
			strnumber = str(number)

			# split number in two
			first = strnumber[0:len(strnumber)/2]
			last = strnumber[len(strnumber)/2:]

			# get matches for parts
			firstmatches = search_matches(int(first),dictwords)
			lastmatches = search_matches(int(last),dictwords) 

			# write first matches
			texfile.write("\\subparagraph{" + first + "}")
			for match in firstmatches[0:maxwords]:
				texfile.write(match + "\n")

			# write last matches
			texfile.write("\\subparagraph{" + last + "}")
			for match in lastmatches[0:maxwords]:
				texfile.write(match + "\n")

			
	texfile.write("\\end{document}")
	texfile.close()

outname = "numbers.tex"
process_sequence("words.txt",outname)
os.system("pdflatex " + outname)
