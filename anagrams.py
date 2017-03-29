#!/usr/bin/python

# sort("xzycab") => "abcxyz"
def sort(text):
	x = list(text)
	x.sort()
	return ''.join(x)

# read filename and return dict with words by sorted name
def read(filename):
	words = {}
	f = open(filename,"r")
	for word in f:
		word = word.rstrip()
		alpha = sort(word)
		words.setdefault(alpha,[]).append(word)
	f.close()
	return words

# subset("abc","axbycz") -> True
def subset(a,b):
	return (len(set(a) - set(b)) == 0)

# remainder("abc","axbycz") -> "xyz"
def remainder(a,b):
	result = b
	for c in a:
		# remove the character from the b string (once)
		result = result.replace(c,'',1)
	return sort(result)
	
# return pairs of sorted words that together form the given name
def findpairs(name):
	result = []
	for word in words:
		if(subset(word,name)):
			other = remainder(word,name)
			if(other < word and other in words):
				if(sort(other + word) == sort(name)):
						result.append([word,other])
	return result

# read the words
print("reading dictionary...")
words = read("words.txt")

# find matching words for a given name
def findmatches(name):
	# check complete words
	if(sort(name) in words):
		for word in words[sort(name)]:
			print(word)

	# check word pairs
	pairs = findpairs(name)
	for pair in pairs:
		a = words[pair[0]]
		b = words[pair[1]]
		print('/'.join(a) + " " + '/'.join(b))
		
# read input
while(True):
	word = raw_input("enter word:")
	findmatches(word)
	print("")
