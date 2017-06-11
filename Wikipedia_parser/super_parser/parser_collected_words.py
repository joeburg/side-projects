#Purpose: parse the file of wiki pagss for tags; filter common words
#Joe Burg

import re

############################################################################
cutoff = raw_input('What filter do you want to use? ')

common_words = re.findall(r'\w+', open('common_word_filter_'+cutoff+'.txt').read().lower())


tags = []
for i in range(200):
    pring 'Scanning file '+str(i)

    filename = 'all_words_'+str(i)

    scraped_words = re.findall(r'\w+', open(filename).read().lower())

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
