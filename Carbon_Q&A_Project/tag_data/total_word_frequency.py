#Purpose: make total word frequency list
#Joe Burg


##################################################################################

list1 = []
with open('word_frequency_AA.txt') as inputfile:
    for line in inputfile:
        list1.append(line.strip().split())


list2 = []
with open('word_frequency_EA.txt') as inputfile:
    for line in inputfile:
        list2.append(line.strip().split())


list3 = []
with open('word_frequency_CH.txt') as inputfile:
    for line in inputfile:
        list3.append(line.strip().split())


##list4 = []
##with open('word_frequency_GO.txt') as inputfile:
##    for line in inputfile:
##        list4.append(line.strip().split())


##################################################################################
#check lists and add to frequencies

all_lists = list1+list2+list3

unique_words = [[],[]]
for i in range(len(all_lists)):
    if all_lists[i][0] in unique_words[0]:
        word = all_lists[i][0]
        for j in range(len(unique_words[0])):
            if unique_words[0][j]==word:
                unique_words[1][j] = unique_words[1][j]+all_lists[i][1]
    else:
        unique_words[0].append(all_lists[i][0])
        unique_words[1].append(all_lists[i][1])

                    
#change column data back into rows (each row is a word with it's frequency)
unique_words = [list(x) for x in zip(*unique_words)]

#sort words according to their frequency
unique_words = sorted(unique_words, key=lambda x: x[1], reverse=True)

#change frequency numbers to strings to it can be written to a .txt file
for i in range(len(unique_words)):
    unique_words[i][1] = str(unique_words[i][1])
            
dataFile = open('total_word_frequency.txt', 'w')
for eachitem in unique_words:
    dataFile.write(" ".join(eachitem)+'\n')

dataFile.close()




