#Purpose: export new tags to user file
#Joe Burg

def export_user_tags(user_classes,user_tags,user_ID):
    user_data = [['Classes:'],\
                 user_classes,\
                 [''],\
                 ['Tags:'],\
                 user_tags]

    dataFile = open(user_ID+'.txt', 'w')
    for line in user_data:
        for tag in line:
            dataFile.write(''.join(tag)+'\n')
    dataFile.close()

    return user_data
                 
                 
