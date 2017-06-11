#Purpose: function to make question into tags
#Joe Burg
import string

def parse_question(question):
    get_tags = question.strip().split()

    #remove punctuation
    parsed_question = []
    for tag in get_tags:
        clean_tag = tag.translate(string.maketrans("",""),string.punctuation)
        parsed_question.append(clean_tag)

        
    #if there is a number in the question make a string with the previous
    # word since it may be a class title
    numbers = []  
    for i in range(len(parsed_question)):
        if parsed_question[i][0] in '0123456789':
            numbers.append(i)

    for i in numbers:
        new_tag = parsed_question[i-1]+' '+parsed_question[i]
        parsed_question.append(new_tag)

    #if there is a capital word in a sentance, make a string with the
    # previous word
    capital_words = []
    for i in range(len(parsed_question)):
        if parsed_question[i][0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            capital_words.append(i)

    for i in capital_words: #may need to add code for more than 2 words
        if i>0:
            if parsed_question[i-1][0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                new_tag = parsed_question[i-1]+' '+parsed_question[i]
                parsed_question.append(new_tag)

    #all tags are capitalized in user lists so captialize the rest
    # of the words
    for i in range(len(parsed_question)):
        if parsed_question[i][0] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            parsed_question[i] = parsed_question[i].capitalize()
        
            
    return parsed_question
