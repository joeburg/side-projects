#Purpose: look for new tags in a question, conversation, etc.
# the existing tag list can be the complete library (for a question)
# or a user tag library (for their answers, conversations,
# question, etc.)
#Joe Burg

def new_tags(tag_library,tags_list)
    for tag in tags_list:
        if tag not in tag_library:
            tag_library.append(tag)

    return tag_library
