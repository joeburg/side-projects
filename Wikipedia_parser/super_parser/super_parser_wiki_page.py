#Purpose: parse a wiki page for tag; filter common words
#Joe Burg

import re

############################################################################
filename = raw_input('Provide the filename: ')
cutoff = raw_input('What filter do you want to use? ')

common_words = re.findall(r'\w+', open('common_word_filter_'+cutoff+'.txt').read().lower())

scraped_words = re.findall(r'\w+', open(filename).read().lower())

tags = []
for word in scraped_words:
    if word not in common_words:
        if word.isdigit()==False: #remove numbers 
            if word[-2:] != 'ly': #remove adverbs
                if word not in tags: #remove repeats
                    tags.append(word)

print len(tags)

#############################################################################
dataFile = open('tags_with_'+str(cutoff)+'_filter.txt', 'w')
for eachitem in tags:
    dataFile.write("".join(eachitem)+'\n')

dataFile.close()        

print "All done!"
