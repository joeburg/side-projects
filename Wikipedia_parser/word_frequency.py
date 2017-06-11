#Purpose: find the frequency of words given an input file
#Joe Burg

from collections import Counter
import re

######################################################################################

filename = raw_input("Provide the filename: ")

data = []
with open(filename) as inputfile:
    for line in inputfile:
        data.append(line.strip().split())

######################################################################################
#find urls, put them in list, and remove those lines from data
urls = []
k=0
titles = []
for line in data:
    
    if len(line)==1 or len(line)==2:
        k=k+1
        titles.append(line)
    if len(line)==0:
        data.remove(line)
        
    for word in line:
        if 'url=' in word:
            urls.append(word)
            data.remove(line)
        if word=='</doc>':
            data.remove(line)

###find frequency of words in list
##for line in data:
##    for word in line:
        
words = re.findall(r'\w+', open(filename).read().lower())

most_common_words_and_freq = Counter(words).most_common(300)

test = Counter(words)

most_common_words = []
for pair in most_common_words_and_freq:
    most_common_words.append(pair[0])

print ''
print most_common_words_and_freq

print len(urls)
