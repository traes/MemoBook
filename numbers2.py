#!/usr/bin/python
import os

# character to number mapping
lookup = {}
lookup['l'] = 0
lookup['n'] = 1
lookup['t'] = 2
lookup['d'] = 3
lookup['r'] = 4
lookup['f'] = 5
lookup['s'] = 6
lookup['p'] = 7
lookup['k'] = 8
lookup['g'] = 9

# return the word for a given number
def decode_word(word):
	result = ""
	for c in word:
		if c  in lookup:
			result += str(lookup[c])
	return result

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


# process all words
def process(dictionary,outputfilename):
	# config
	maxwords = 30 # the max number of words to show for each number
	minwords = 5 # split word if fewer than minwords found
	
	# local vars
	elements = {} 
	words = read_words(dictionary)

	# search words
	print("searching words...")
	for word in words:
		decoded = decode_word(word)
		if(decoded not in elements):
			elements[decoded] = []
		elements[decoded].append(word)

	# output
	print("writing results...")
	texfile = open(outputfilename,"w")
	texfile.write("\\documentclass{article}")
	texfile.write("\\begin{document}")
	texfile.write("\\title{Number Mnemonics}")
	texfile.write("\\maketitle")

	# write table
	texfile.write("\\begin{tabular}{| c | c | l |}\r")
	texfile.write("\\hline 0 & L & nuL \\\\ 1 & N & eeN \\\\ 2 & T & Twee \\\\ 3 & D & Drie \\\\ 4 & R & vieR \\\\ 5 & F & vijF \\\\ 6 & S & zeS \\\\ 7 & P & sePt \\\\ 8 & K & oKtopus \\\\ 9 & G & neGen \\\\  \\hline") 
	texfile.write("\\end{tabular}")

	# write numbers
	for number in range(0,9999):
		strnumber = str(number)
		texfile.write("\\paragraph{" + strnumber + "}")

		# get the matching words for this number
		words = elements.get(strnumber,[])
		words.sort(key=len)

		# show the first n words	
		for word in words[0:maxwords]:
			texfile.write(word + "\n")

		# if not enough words found, split up
		if(len(words) < minwords):
			# split number in two
			first = strnumber[0:len(strnumber)/2]
			last = strnumber[len(strnumber)/2:]

			# get matches for parts
			firstmatches = elements.get(first,[]) 
			lastmatches = elements.get(last,[])

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

# run the program
outname = "numbers2.tex"
process("words.txt",outname)
os.system("pdflatex " + outname)
