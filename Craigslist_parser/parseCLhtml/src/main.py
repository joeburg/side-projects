#!/usr/bin/env

import sys
import userDir

from parseCLhtml import CLlisting
#------------------------------------------------------------------------#

if len(sys.argv) < 3:
	print 'Usage:'
	print '  python %s <user_id> <url>' %sys.argv[0]
	exit()

user_id = sys.argv[1]
url = sys.argv[2]

user_data_file = '../database/user_database.yml'

try:
	# see if user is in database; if not add 
	userDir.users(user_data_file).validate_user_id(user_id)

	# generate the CL listing object with its attributes
	listing = CLlisting(user_id,user_data_file,url)

	# # grab the file with the listing data
	# outfile = listing.get_CLlisting_yaml_file()
	# print outfile

	print 'Your page has been made!'
except Exception, e:
	print 'ERROR: %s' % e 
	exit()


# if __name__ == '__main__':

# 	user_id = 'joeburg09@gmail.com'
# 	url = 'http://sfbay.craigslist.org/sfc/apa/5189006279.html'

# 	user_data_file = 'user_database.yml'

# 	try:
# 		CLlisting(user_id,user_data_file,url)
# 		print 'Your page has been made!'
# 	except Exception, e:
# 		print 'ERROR: %s' % e 
# 		exit()