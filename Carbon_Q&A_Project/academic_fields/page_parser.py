#Purpose: parse a wiki page for tags
#Joe Burg

import re

############################################################################

def digit_check(word):
    for i in range(len(word)):
        if word[i] in '0123456789':
            return False
        else:
            return True 

############################################################################
filename = raw_input('Provide the filename: ')

filtered_words = re.findall(r'\w+', open('common_word_filter_1000.txt').read().lower())

scraped_words = re.findall(r'\w+', open(filename).read().lower())

print scraped_words[:100]

tags = []
for word in scraped_words:
    if word not in filtered_words:
        if word.isdigit()==False: #remove numbers
            if digit_check(word)==True:
                if word[-2:] != 'ly': #remove adverbs
                    if word not in tags: #remove repeats
                        tags.append(word)

print ''
print len(tags)
print ''
print tags[:100]

###############################################################################
##dataFile = open('tags_with_'+str(cutoff)+'_filter.txt', 'w'x)
##for eachitem in tags:
##    dataFile.write("".join(eachitem)+'\n')
##
##dataFile.close()        
##
##print "All done!"
