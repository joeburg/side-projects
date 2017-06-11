#Purpose: parse a wiki page for tag; filter common words
#Joe Burg

import re

############################################################################
number = input('What number file is this? ')

all_words = []
for i in range(100):
    print 'Scanning page '+str(i)
    if i<10:
        filename = 'wiki_0'+str(i)
    else:
        filename = 'wiki_'+str(i)

    words = re.findall(r'\w+', open(filename).read().lower())

    all_words.append(words)
    
#############################################################################
dataFile = open('all_words_'+str(number)+'.txt', 'w')
for eachitem in all_words:
    dataFile.write(" ".join(eachitem)+'\n')

dataFile.close()        

print "All done!"
