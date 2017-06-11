#Purpose: check question's tags against users list to see who it's relevant to
#Joe Burg

from parse_question import parse_question
from parse_question2 import parse_question2
from Q_to_file import Q_to_file
from get_Qnumber import get_Qnumber
from import_data import import_data
from export_user_tags import export_user_tags

###################################################################
user_ID_for_Q = raw_input('What is the user ID? ')
question = raw_input('What is your question: ')

#import the user IDs
user_IDs = []
with open('user_IDs.txt') as inputfile:
    for line in inputfile:
        user_IDs.append(line.strip())


#using the user IDs, use the import_data function to access each
# user's tag file and organize all the user's data into a dictionary
# with the user's ID as the key and their data as [[classes],[tags]]

user_classes_and_tags_dictionary = import_data(user_IDs)

###################################################################
#create Qfile to store question and it's associated tags; parse
# the question for tag; each question's filename is the data+time+
# a random number bewteen (1,100000)
flag=True
Qnumber = get_Qnumber(flag)

print Qnumber 

Qfile = Q_to_file(question,Qnumber)

parsed_question = parse_question2(Qfile)

#add tags to Qfile
tags_to_Qfile = [[''],[''],['Tags:'],parsed_question]
with open(Qfile, "a") as dataFile:
    for line in tags_to_Qfile:
        for tag in line:
            dataFile.write(''.join(tag)+'\n')
dataFile.close()

print parsed_question
print ''


###################################################################
#check if the question's tags are in the user's data
class_tag_guage_dictionary = {}
for user in user_IDs:
    if user != user_ID_for_Q: #exclude the user who is asking the question
        class_guage=0
        tag_guage=0
        user_classes = user_classes_and_tags_dictionary[user][0]
        user_tags = user_classes_and_tags_dictionary[user][1]

    ##    print user+' classes'
    ##    print user_classes
    ##    print user+' tags'
    ##    print user_tags

        for tag in parsed_question:
            if tag in user_classes:
                class_guage = class_guage + 1

            if tag in user_tags:
                tag_guage = tag_guage + 1

        if class_guage > 0:
            print 'This question is relevant to '+user+"\'s classes."
            in_class = True
        else:
            in_class = False 

        if tag_guage > 0:
            print 'This question is relevant to '+user+"\'s tags."
            in_tags = True
        else:
            in_tags = False

        total_guage = class_guage+tag_guage
         
        class_tag_guage_dictionary[user] = [class_guage,tag_guage,total_guage]

###################################################################
#Check the class/tag dictionary to see who the question is most
# relevant to
class_tag_guage_dictionary.keys()

relevant_users_scores = []
for user in user_IDs:
    if user == user_ID_for_Q:
        relevant_users_scores.append(0) #not relevant to user asking question
    else:
        relevant_users_scores.append(class_tag_guage_dictionary[user][2])
        

max_score = max(relevant_users_scores)


most_relevant_users = []
l=0
for i in range(len(user_IDs)):
    if max_score>0:
        if relevant_users_scores[i]==max_score:
            l=l+1
            most_relevant_users.append(user_IDs[i])
            max_score_user = user_IDs[i]

if l==0:
    print 'This question is not relevant to any of the users.'
else:
    print ''
    print 'This question is most relevant to...'
    for user in most_relevant_users:
        print user
        


###################################################################
#now check tags from question to see if they are in the existing
# tag library; if not, then add it; do the same for user asking question

user_classes_for_Q = user_classes_and_tags_dictionary[user_ID_for_Q][0]
user_tags_for_Q = user_classes_and_tags_dictionary[user_ID_for_Q][1]
for tag in parsed_question:
    if tag not in user_tags_for_Q:
        user_tags_for_Q.append(tag)

        #export_user_tags writes out new user data file
        user_data = export_user_tags(user_classes_for_Q,user_tags_for_Q,user_ID_for_Q)
    


print ''
print 'All done!'

