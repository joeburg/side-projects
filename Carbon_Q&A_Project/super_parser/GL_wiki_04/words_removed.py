#Purpose: show which tags are filtered out
#Joe Burg

import re

filename1 = raw_input('Provide file name 1: ')
filename2 = raw_input('Proivde file name 2 (shorter list): ')

words1 = re.findall(r'\w+', open(filename1).read().lower())
words2 = re.findall(r'\w+', open(filename2).read().lower())

removed_words = []
for word in words1:
    if word not in words2:
        removed_words.append(word)

print len(removed_words)
#############################################################################
dataFile = open('removed_words.txt', 'w')
for eachitem in removed_words:
    dataFile.write("".join(eachitem)+'\n')

dataFile.close()        

print "All done!"
