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

# create regular expression for matching pinyin word
def create_regex(pinyin):

	# extract parts (example "rban")
	tone = pinyin[0] 	# "r"
	initial = pinyin[1] 	# "b"
	final = pinyin[2:] 	# "an"

	# reserved characters
	no_tone = "[^lntdr]*"
	no_pinyin = "[^bpmfdtnlgkhjqxzcshrwyaeioungr]*"
	no_final = "[^aeioungr]*"

	# construct regex
	regexp = "^"
	regexp += no_tone + tone
	regexp += no_pinyin + initial + no_final
	for char in final:
		regexp += char + no_final
	regexp += "$"

	return re.compile(regexp)


# ban4 -> rban
def create_mnemo(pinyin):
	parts = pinyin.split(" ")
	for part in parts:
		text = "" # store the text without the tone number (e.g. "ban") 

		# check if tone specified by number after text (e.g. 4 in "ban4")
		tone = part[len(part) - 1]
		if(tone in '1234'):
			text = part[:-1] # the text part does not contain the tone
		# no tone specified -> tone 0
		else:
			tone = "0"
			text = part

		# get tone character
		tonechar = "lntdr"[int(tone)]

		result = tonechar + text
		return result


# look in all words
def search_matches(pinyin,words):
	result = set([])
	regex = create_regex(pinyin)
	for word in words:
		if(regex.match(word) and word != pinyin):
			result.add(word)
	result = list(result)
	result.sort(key=len)
	return result

def process(inputname):
	inputfile = open(inputname,"r")
	for line in inputfile:
		line = line.strip() # remove trailing newline
		elements = line.split(',')
		if(len(elements) == 2):
			pinyin = elements[0]
			translation = elements[1]
			mnemo = create_mnemo(pinyin)
			print(pinyin + " => " + mnemo)


# process file
def process_file(inputfilename,dictfilename,outputfilename):
	maxwords = 10
	dictwords = read_words(dictfilename)

	inputfile = open(inputfilename)
	texfile = open(outputfilename,"w")

	texfile.write("\\documentclass{article}")
	texfile.write("\\begin{document}")
	texfile.write("\\title{Pinyin Mnemonics}")
	texfile.write("\\author{Thomas Raes}")
	texfile.write("\\maketitle")

	for line in inputfile:
		line = line.strip() # remove trailing newline
		print(line)
		elements = line.split(',')
		if(len(elements) == 2):
			pinyin = elements[0]
			translation = elements[1]
			mnemo = create_mnemo(pinyin)
			matches = search_matches(mnemo,dictwords)
			texfile.write("\\paragraph{" + pinyin + "}")
			texfile.write("(" + translation + ") ")
			for match in matches[0:maxwords]:
				texfile.write(match + "\n")

	texfile.write("\\end{document}")
	inputfile.close()
	texfile.close()

outname = "pinyin.tex"
process_file("pinyin.txt","words.txt",outname)
os.system("pdflatex " + outname)
