#Purpose: check tag against single user data
#Joe Burg

from question_to_tags import parse_question


###################################################################
#inputs
personal_file = raw_input('Provide the personal tags file name: ')
print ''
question = raw_input('What is your question: ')

data = []
with open(personal_file) as inputfile:
    for line in inputfile:
        data.append(line.strip())

#name_id = data[0]

###################################################################
#get classes and tags
for i in range(len(data)):
    if data[i][0:3] == 'id_':
        name_id = data[i]
    if data[i] == 'Classes:':
        class_index = i
    if data[i] == 'Tags:':
        tag_index = i 

classes = []
for i in range(class_index+1,tag_index-2):
    classes.append(data[i])

tags = []
for i in range(tag_index+1,len(data)-1):
    tags.append(data[i])


##print name_id+"\'s classes: ",classes
##print ''
##print name_id+"\'s tags: ",tags
##print ''

###################################################################
#check if input tag or class is in user's data file

parsed_question = parse_question(question)

class_guage=0
tag_guage=0
for tag in parsed_question:
    if tag in classes:
        class_guage = class_guage + 1

    if tag in tags:
        tag_guage = tag_guage + 1


if class_guage > 0:
    print 'This question is relevant to '+name_id+"\'s classes."
    in_class = True
else:
    in_class = False

if tag_guage > 0:
    print 'This question is relevant to '+name_id+"\'s tags."
    in_tags = True
else:
    in_tags = False

if class_guage==0 and tag_guage==0:
    print 'This question is not relevenat to '+name_id+'.'


print ''
print "All done!"
