#Purpose: find the total word frequency for the wikipedia data
#Joe Burg

from operator import itemgetter, attrgetter
from collections import Counter
import re

######################################################################################

all_words = [[],[]]
for i in range(100):
    print 'Scanning page '+str(i)
    if i<10:
        filename = 'wiki_0'+str(i)
    else:
        filename = 'wiki_'+str(i)

    words = re.findall(r'\w+', open(filename).read().lower())

    most_common_words_and_freq = Counter(words).most_common(10000)


    for i in range(len(most_common_words_and_freq)):
        if most_common_words_and_freq[i][0] in all_words[0]:
            word = most_common_words_and_freq[i][0]
            for j in range(len(all_words[0])):
                if all_words[0][j]==word:
                    all_words[1][j] = all_words[1][j]+most_common_words_and_freq[i][1]
        else:
            all_words[0].append(most_common_words_and_freq[i][0])
            all_words[1].append(most_common_words_and_freq[i][1])
                    

                    
#change column data back into rows (each row is a word with it's frequency)
all_words = [list(x) for x in zip(*all_words)]

#sort words according to their frequency
all_words = sorted(all_words, key=lambda x: x[1], reverse=True)

#change frequency numbers to strings to it can be written to a .txt file
for i in range(len(all_words)):
    all_words[i][1] = str(all_words[i][1])


print ''
print all_words[0]
print ''
print all_words[50]
print ''
print all_words[100]
print ''
print 'Length = ',len(all_words)
print ''
print all_words[len(all_words)-1]

all_words_100 = all_words[:100]

print all_words_100

#write to a text file
#the .join() method takes an array, i, and concantenates all the elements together
# with a space " " between each element.  Then a newline "\n" is added to make sure
# your output is broken up into separate lines

dataFile = open('word_frequency.txt', 'w')
for eachitem in all_words:
    dataFile.write(" ".join(eachitem)+'\n')

dataFile.close()


###access the list of words only to write the data list
##most_common_words = []
##for pair in all_words:
##    most_common_words.append(pair[0])
##    
##dataFile = open('most_common_words.txt', 'w')
##for eachitem in all_words:
##    dataFile.write(" ".join(eachitem)+'\n')
##
##dataFile.close()

print "All done!"

    
