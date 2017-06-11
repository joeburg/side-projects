import operator
import re
import string
import time

#------------------------------------------------------------------------#
def read_in_data(f):
	link = f.readline().strip()
	title = f.readline().strip()
	date = f.readline().strip()

	# read the text until --!> is reached
	text = ''
	while True:
		fields = f.readline().strip()
		if fields == '--!>':
			break
		else:
			text += fields

	return link, title, date, text

def load_filtered_words(inputfile):
	filtered_words = set([])
	f = open(inputfile)
	while True:
		word = f.readline().strip()
		if word:
			filtered_words.add(word)
		else:
			break
	f.close()
	return filtered_words

def clean_word(word):
	alphabet = 'abcdefghijiklmnopqrstuvwxyz'
	for item in word:
		if item not in alphabet:
			word = word.replace(item,'')
	return word

def load_TC_text(inputfile, filtered_words):
	all_words = {}
	f = open(inputfile)
	while True:
		text_data = f.readline().strip().split()
		if text_data:
			for word in text_data:
				word = word.lower()
				word = remove_punctuation(word)
				word = clean_word(word)
				if word:
					if word not in filtered_words:
						if word[-2:] != 'ly':
							if word not in all_words:
								all_words[word] = 1
							else:
								all_words[word] += 1
		else:
			break
	f.close()

	# sort the words by frequency (value)
	sorted_words = sorted(all_words.items(), key=operator.itemgetter(1), reverse=True)

	return sorted_words	

def remove_punctuation(word):
	return word.translate(string.maketrans("",""),string.punctuation)

def write_word_frequencies(outputfile, all_words):
	f = open(outputfile, 'w')
	for word in all_words:
		f.write('%s  %d\n' %(word[0], word[1]))
	f.close()

def get_top_words(filename, Nwords):
	ifile = '%s_most_common_words.txt' %filename[:len('TC_2015')]
	ofile = '%s_top_%d_words.txt' %(filename[:len('TC_2015')], Nwords)

	fin = open(ifile)
	fout = open(ofile,'w')

	N = 0
	for line in fin:
		if N > Nwords:
			break
		else:
			fout.write(line)
			N += 1
	fin.close()
	fout.close()

#------------------------------------------------------------------------#
''' read in the all the data and organize into years '''

t0 = time.time()

fall = open('TC_allf_text.txt', 'w')
f15 = open('TC_2015_text.txt', 'w')
f14 = open('TC_2014_text.txt', 'w')
f13 = open('TC_2013_text.txt', 'w')
f12 = open('TC_2012_text.txt', 'w')
f11 = open('TC_2011_text.txt', 'w')

f = open('TC_startup_articles_data3.txt')
while True:
	fields = f.readline().strip()
	if fields:
		# link, title, date, text
		if fields == '<!--':
			link, title, date, text = read_in_data(f)

			if '2015' == date[:4]:
				f15.write('%s ' %text)
			elif '2014' == date[:4]:
				f14.write('%s ' %text)
			elif '2013' == date[:4]:
				f13.write('%s ' %text)
			elif '2012' == date[:4]:
				f12.write('%s ' %text)
			elif '2011' == date[:4]:
				f11.write('%s ' %text)

			fall.write('%s ' %text)
		else:
			continue
	else:
		break
f.close()

#------------------------------------------------------------------------#
''' find the most frequent words in a given year '''

filtered_words = load_filtered_words('common_word_filter_1000.txt')

# run through each of the years 
files = ['TC_allf_text.txt','TC_2015_text.txt','TC_2014_text.txt','TC_2013_text.txt',
		'TC_2012_text.txt','TC_2011_text.txt']

for ifile in files: 
	ofile = '%s_most_common_words.txt' %ifile[:len('TC_2015')]
	print ofile

	sorted_words = load_TC_text(ifile, filtered_words)
	write_word_frequencies(ofile, sorted_words)

#------------------------------------------------------------------------#
''' take the top 500 words from each list '''

Nwords = 500 
for ifile in files:
	get_top_words(ifile,Nwords)

print '\nProcessed TechCrunch in %.2f minutes.' % ((time.time()-t0)/60.0)



