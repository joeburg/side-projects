#Purpose: check question's tags against users list to see who it's relevant to
#Joe Burg

from parse_question import parse_question
from import_data import import_data

###################################################################
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
#check if the question's tags are in the user's data

parsed_question = parse_question(question)


for user in user_IDs:
    class_guage=0
    tag_guage=0
    user_classes = user_classes_and_tags_dictionary[user][0]
    user_tags = user_classes_and_tags_dictionary[user][1]

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


print ''
print 'All done!'

