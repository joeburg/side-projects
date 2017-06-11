#Purpose: find the total word frequency for the wikipedia data
#Joe Burg


from collections import Counter
import re

######################################################################################

all_words = [[],[]]
all_words_and_freq = []
for i in range(100):
    if i<10:
        filename = 'wiki_0'+str(i)
    else:
        filename = 'wiki_'+str(i)

    words = re.findall(r'\w+', open(filename).read().lower())

    most_common_words_and_freq = Counter(words)

##    for i in range(len(most_common_words_and_freq)):
##        if most_common_words_and_freq[i][0] in all_words:


    for i in range(len(most_common_words_and_freq)):
        if most_common_words_and_freq[i][0] in all_words[0]:
            word = most_common_words_and_freq[i][0]
            for j in range(len(all_words[0])):
                if all_words[0][j]==word:
                    all_words[1][j] = all_words[1][j]+most_common_words_and_freq[i][1]
        else:
            all_words[0].append(most_common_words_and_freq[i][0])
            all_words[1].append(most_common_words_and_freq[i][1])
                    
                
                
all_words = [list(x) for x in zip(*all_words)]

print all_words[0]
print ''
print all_words[100]
print ''
print 'Length = ',len(all_words)
print ''
print all_words[len(all_words)-1]


    
