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
	no_pinyin = "[^bpmfdtnlgkhjqxzcshrwyaeioungr]*"
	no_final = "[^aeioungr]*"
	regexp = "^"
	regexp += no_pinyin + pinyin[0] + no_final
	for index in range(1,len(pinyin)):
		regexp += pinyin[index] + no_final
	regexp += "$"
	return re.compile(regexp)

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
process_file("input.txt","words.txt",outname)
os.system("pdflatex " + outname)
