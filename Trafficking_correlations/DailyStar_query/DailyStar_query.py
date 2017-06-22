import matplotlib.pyplot as plt
import numpy
import operator

#------------------------------------------------------------------------#

def load_words_frequency(inputfile):
	word_data = {}
	f = open(inputfile)
	while True:
		fields = f.readline().strip().split()
		if fields:
			if len(fields) == 3:
				word1 = fields[0]
				word2 = fields[1]
				word = '{} {}'.format(word1,word2)
				freq = int(fields[2])
				word_data[word] = freq

			elif len(fields) == 2:
				word = fields[0]
				freq = int(fields[1])
				word_data[word] = freq
		else:
			break
	f.close()
	return word_data	

def plot_data(data,word,filename):
	
	# get the frequency of the word for each year and normalize 
	# by the most frequent word of that year 
	years = []
	frequencies = []
	for year in data:
		# # get the value of the most frequent word 
		# max_val = max(data[year].iteritems(), key=operator.itemgetter(1))[1]

		# get the frequency of the word 
		try:
			frequency = data[year][word]
		except:
			frequency = 0

		years.append(year)
		frequencies.append(frequency)



	plt.figure()
	plt.plot(years,frequencies, '-bo')
	plt.ticklabel_format(useOffset=0, style='plain', scilimits=(2002,2017))
	plt.title('TC trend for "{}"'.format(word),size=24,**arialfont)
	plt.xlabel('Year',size=20,**arialfont)
	plt.ylabel('Frequency',size=20,**arialfont)
	plt.xlim(2002,2016)
	plt.savefig(filename,bbox_inches='tight')
	plt.close()

def write_result(f,data,word):
	f.write('%s: \n' %word)
	for year in data:
		# get the frequency of the word 
		try:
			frequency = data[year][word]
		except:
			frequency = 0

		f.write('%d,%d\n' %(year,frequency))

#------------------------------------------------------------------------#
# set font type and axes thickness
arialfont = {'fontname':'Arial'}
plt.rcParams['axes.linewidth'] = 2
plt.rcParams.update({'fontname':'Arial','font.size': 16})

#------------------------------------------------------------------------#
''' load the word and frequency data for each year '''

# run through each of the years 
files = []
years = []
for i in range(2003,2016):
	files.append('DailyStar_{}_word_frequencies.txt'.format(i))
	years.append(i)

data = {}
for i in range(len(files)):
	data[years[i]] = load_words_frequency(files[i])

#------------------------------------------------------------------------#
''' given a query, plot the trend over the years '''

Nqueries = input("How many words do you want to serch? ")
f = open('queries/search_results.txt', 'a')
for i in range(Nqueries):	
	word = raw_input('Give a word to query:  ')
	word = word.lower()

	directory = 'queries/'
	ofile = '%s%s.pdf' %(directory,word)
	plot_data(data,word,ofile)

	write_result(f,data,word)
f.close()


