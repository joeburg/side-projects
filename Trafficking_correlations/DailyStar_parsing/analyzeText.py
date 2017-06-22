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

def load_TC_text(inputfile):
	all_words = {}
	f = open(inputfile)
	while True:
		text_data = f.readline().strip().split()
		if text_data:
			for i in range(len(text_data)):
				word1 = text_data[i].lower()
				word1 = remove_punctuation(word1)
				word1 = clean_word(word1)

				if word1:
					if word1 not in all_words:
						all_words[word1] = 1
					else:
						all_words[word1] += 1

				# consider 2 words for search 		
				if i+1 < len(text_data):
					word2 = text_data[i+1].lower()
					word2 = remove_punctuation(word2)
					word2 = clean_word(word2)
					word2 = '{} {}'.format(word1, word2) 

					if word2:
						if word2 not in all_words:
							all_words[word2] = 1
						else:
							all_words[word2] += 1
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

fall = open('DailyStar_all_text.txt', 'w')
f03 = open('DailyStar_2003_text.txt', 'w')
f04 = open('DailyStar_2004_text.txt', 'w')
f05 = open('DailyStar_2005_text.txt', 'w')
f06 = open('DailyStar_2006_text.txt', 'w')
f07 = open('DailyStar_2007_text.txt', 'w')
f08 = open('DailyStar_2008_text.txt', 'w')
f09 = open('DailyStar_2009_text.txt', 'w')
f10 = open('DailyStar_2010_text.txt', 'w')
f11 = open('DailyStar_2011_text.txt', 'w')
f12 = open('DailyStar_2012_text.txt', 'w')
f13 = open('DailyStar_2013_text.txt', 'w')
f14 = open('DailyStar_2014_text.txt', 'w')
f15 = open('DailyStar_2015_text.txt', 'w')

f = open('DailyStar_all_data.txt')
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
			elif '2010' == date[:4]:
				f10.write('%s ' %text)
			elif '2009' == date[:4]:
				f09.write('%s ' %text)
			elif '2008' == date[:4]:
				f08.write('%s ' %text)
			elif '2007' == date[:4]:
				f07.write('%s ' %text)
			elif '2006' == date[:4]:
				f06.write('%s ' %text)
			elif '2005' == date[:4]:
				f05.write('%s ' %text)
			elif '2004' == date[:4]:
				f04.write('%s ' %text)
			elif '2003' == date[:4]:
				f03.write('%s ' %text)

			fall.write('%s ' %text)
		else:
			continue
	else:
		break
f.close()

fall.close()
f03.close()
f04.close()
f05.close()
f06.close()
f07.close()
f08.close()
f09.close()
f10.close()
f11.close()
f12.close()
f13.close()
f14.close()
f15.close()

#------------------------------------------------------------------------#
''' find the word frequencies for each year '''

# filtered_words = load_filtered_words('common_word_filter_1000.txt')

# run through each of the years 
files = []
for i in range(2003,2016):
	files.append('DailyStar_{}_text.txt'.format(i))


for ifile in files: 
	ofile = '%s_word_frequencies.txt' %ifile[:len('DailyStar_2015')]
	print ofile

	words = load_TC_text(ifile)
	write_word_frequencies(ofile, words)


print '\nProcessed TechCrunch in %.2f minutes.' % ((time.time()-t0)/60.0)



