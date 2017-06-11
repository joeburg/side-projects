#Purpose: function to make question into tags
#Joe Burg
import string
import re

def parse_question2(Qfile):
    common_words = re.findall(r'\w+', open('common_word_filter_1000.txt').read().lower())
        
    contractions = re.findall(r'\w+', open('misspelled_contractions.txt').read().lower())
    
    get_tags = re.findall(r'\w+', open(Qfile).read().lower())
    
##    get_tags_with_punc = question.lower().split()
##
##    #remove punctuation
##    get_tags = []
##    for tag in get_tags_with_punc:
##        clean_tag = tag.translate(string.maketrans("",""),string.punctuation)
##        get_tags.append(clean_tag)


    all_tags = []
    for tag in get_tags:
        if tag not in common_words:
            if tag not in contractions:
                if tag.isdigit()==False: #remove numbers 
                    if tag[-2:] != 'ly': #remove adverbs
                        if tag not in all_tags: #remove repeats
                            all_tags.append(tag)
                    
    return all_tags
