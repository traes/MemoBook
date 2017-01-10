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

# ban4 -> rban
def create_mnemo(part):
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
def search_subs(pinyin,words):
	result = set([])
	for word in words:
		if pinyin in word:
			result.add(word)
	result = list(result)
	result.sort(key=len)
	return result

# relaxed search (letters can appear between tone and rest of pinyin)
def search_subs_easy(pinyin,words):
	result = set([])

	regex = ".*"
	regex += pinyin[0]
	regex += "[^nltd]*"
	regex += pinyin[1:]
	regex += ".*"
	test = re.compile(regex)

	for word in words:
		if(test.match(word)):
			result.add(word)

	result = list(result)
	result.sort(key=len)
	return result

# relaxed search (letters can appear between tone and rest of pinyin)
def search_subs_real_easy(pinyin,words):
	result = set([])

	regex = ""
	for char in pinyin:
		regex += char
		regex += "[^aeoiunr]*"
	test = re.compile(regex)

	for word in words:
		if(test.match(word)):
			result.add(word)

	result = list(result)
	result.sort(key=len)
	return result


# process file
def process_file(inputfilename,dictfilename,outputfilename):
	maxwords = 20
	minwords = 5
	dictwords = read_words(dictfilename)

	inputfile = open(inputfilename)
	texfile = open(outputfilename,"w")

	texfile.write("\\documentclass{article}\r")
	texfile.write("\\begin{document}\r")
	texfile.write("\\title{Pinyin Mnemonics}\r")
	texfile.write("\\maketitle\r")

	texfile.write("\\begin{tabular}{| c | c | l |}\r")
	texfile.write("\\hline tone & letter & reason \\\\ \\hline 0 & L & nuLL \\\\ 1 & N & eeN, oNe \\\\ 2 & T & Twee, Two \\\\ 3 & D & Drie \\\\ 4 & R & vieR, fouR \\\\ \\hline") 
	texfile.write("\\end{tabular}")

	texfile.write("\\begin{itemize}")
	texfile.write("\\item{mai3} (to buy): mai with 3rd tone $\\rightarrow$ d + mai $\\Rightarrow$ handmaid")
	texfile.write("\\item{mai4} (to sell): mai with 4th tone $\\rightarrow$ r + mai $\\Rightarrow$ airmail")
	texfile.write("\\end{itemize}")

	for line in inputfile:
		line = line.strip() # remove trailing newline
		print(line)
		elements = line.split(',')
		if(len(elements) == 2):
			pinyin = elements[0]
			translation = elements[1]
			pinyinparts = pinyin.split(" ")

			texfile.write("\\paragraph{" + pinyin + "}")
			texfile.write("(" + translation + ") ")

			for part in pinyinparts:

				# only write part subparts if there are multiple
				if(len(pinyinparts) > 1):
					texfile.write("\\subparagraph{" + part + "}")

				# create the mnemo (e.g "ban4 -> rban")
				mnemo = create_mnemo(part)

				# search memory aids
				subs = search_subs(mnemo,dictwords)
				subs += search_subs_easy(mnemo,dictwords)
				subs += search_subs_real_easy(mnemo,dictwords)

				# write the subs
				for sub in subs[0:maxwords]:
					texfile.write(sub + "\n")
		
	texfile.write("\\end{document}")
	inputfile.close()
	texfile.close()

def run():
	outname = "pinyin.tex"
	process_file("pinyin.txt","words.txt",outname)
	os.system("pdflatex " + outname)

run()
