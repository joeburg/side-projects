#Purpose: find the unique words between lists
#Joe Burg

import re

#############################################################################
unique_words = []
N_words = 0
for i in range(5):
    words = re.findall(r'\w+', open('tags_with_50000_filter_'+str(i)+'.txt').read().lower())

    N_words = N_words+len(words)
    
    print len(words)
    for word in words:
        if word not in unique_words:
            unique_words.append(word)

print ''
print 'Number of words: ',N_words
print 'Number of unique words: ',len(unique_words)
print 'Percent change: ',float(N_words-len(unique_words))/float(N_words)


#############################################################################
dataFile = open('unique_words.txt', 'w')
for eachitem in unique_words:
    dataFile.write("".join(eachitem)+'\n')

dataFile.close()        

print "All done!"
