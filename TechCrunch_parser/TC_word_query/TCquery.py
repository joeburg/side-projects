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
		# get the value of the most frequent word 
		max_val = max(data[year].iteritems(), key=operator.itemgetter(1))[1]

		# get the frequency of the word and normalize by max value
		try:
			frequency = data[year][word]/float(max_val)
		except:
			frequency = 0

		years.append(year)
		frequencies.append(frequency)

	plt.figure()
	plt.plot(years,frequencies, '-bo')
	plt.ticklabel_format(useOffset=0, style='plain', scilimits=(2010,2017))
	plt.title('TC trend for "{}"'.format(word),size=24,**arialfont)
	plt.xlabel('Year',size=20,**arialfont)
	plt.ylabel('Frequency',size=20,**arialfont)
	plt.xlim(2010,2016)
	plt.savefig(filename,bbox_inches='tight')
	plt.close()

#------------------------------------------------------------------------#
# set font type and axes thickness
arialfont = {'fontname':'Arial'}
plt.rcParams['axes.linewidth'] = 2
plt.rcParams.update({'fontname':'Arial','font.size': 16})

#------------------------------------------------------------------------#
''' load the word and frequency data for each year '''

# run through each of the years 
files = ['TC_2015_most_common_words.txt','TC_2014_most_common_words.txt',
		'TC_2013_most_common_words.txt', 'TC_2012_most_common_words.txt',
		'TC_2011_most_common_words.txt']

years = [2015,2014,2013,2012,2011]
data = {}

for i in range(len(files)):
	data[years[i]] = load_words_frequency(files[i])

#------------------------------------------------------------------------#
''' given a query, plot the trend over the years '''

word = raw_input('Give a word to query:  ')
word = word.lower()

directory = 'queries/'
ofile = '%s%s.pdf' %(directory,word)
plot_data(data,word,ofile)






