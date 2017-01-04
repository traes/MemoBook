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

result = search_matches(9100,read_words("words.txt"))
for res in result:
	print(res)

# process file
def process_file(inputfilename,dictfilename,outputfilename):
	maxwords = 10
	dictwords = read_words(dictfilename)
	inputfile = open(inputfilename)
	texfile = open(outputfilename,"w")
	texfile.write("\\documentclass{article}")
	texfile.write("\\begin{document}")
	for inputword in inputfile:
		inputword = inputword.strip()
		matches = search_matches(inputword,dictwords)
		texfile.write("\\paragraph{" + inputword + "}")
		for match in matches[0:maxwords]:
			texfile.write(match + "\n")
	texfile.write("\\end{document}")
	inputfile.close()
	texfile.close()

outname = "output.tex"
#process_file("input.txt","words.txt",outname)
#os.system("pdflatex " + outname)
