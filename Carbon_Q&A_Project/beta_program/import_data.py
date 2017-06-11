#Purpose: function to call users, upload tag lists, and store in dictionary
#Joe Burg

def import_data(user_IDs):
    user_classes_and_tags_dictionary = {}
    for user in user_IDs:
        user_file = user+'.txt'
        
        user_data = []
        with open(user_file) as inputfile:
            for line in inputfile:
                user_data.append(line.strip())

        for i in range(len(user_data)):
            if user_data[i] == 'Classes:':
                class_index = i
            if user_data[i] == 'Tags:':
                tag_index = i

        user_classes = []
        for i in range(class_index+1,tag_index-1):
            user_classes.append(user_data[i])

        user_tags = []
        for i in range(tag_index+1,len(user_data)):
            user_tags.append(user_data[i])

        user_classes_and_tags_dictionary[user]=[user_classes,user_tags]

    return user_classes_and_tags_dictionary

        
            
        

