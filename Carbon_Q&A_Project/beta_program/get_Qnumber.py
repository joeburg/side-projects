#Purpose: index each question with a Qnumber; indexing is by data, time, and
# a random number attachment just in case questions were posted at the same time
#Joe Burg

import time
from random import randint

def get_Qnumber(flag):
    if flag==True:
        post_date_time = time.strftime("%d:%m:%Y_%H:%M:%S")
        random_number = str(randint(1,1000000))

        Qnumber = post_date_time+'_'+random_number

        return Qnumber
    else:
        return 'Error'
    
