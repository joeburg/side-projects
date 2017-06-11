import os
import yaml

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------#
class users:

	def __init__(self,user_data_file):

		# data attribues of the directories object
		self.user_data = None
		self.user_data_file = user_data_file

		# load the user data
		self.load_user_data(user_data_file)

	#------------------------------------------------------------------------#

	def load_user_data(self,user_data_file):
		''' load the user database '''
		with open(user_data_file) as f:
			self.user_data = yaml.load(f)

	def update_database(self):
		''' updates the database '''
		with open(self.user_data_file, 'w') as f:
			yaml.dump(self.user_data,f)

	def validate_user_id(self,user_id):
		''' check if a user is in the database, if not add him/her '''

		# check if the user is in the data base; if not set a password
		if user_id not in self.user_data:
			self.user_data[user_id] = {'password' : '', 'Nlisting' : 0}
			self.set_password(user_id)

		# update the database
		self.update_database()

	def set_password(self,user_id):
		''' set a password for the new user '''

		password = raw_input('Set a password: ')
		password_confirm = raw_input('Confirm your password: ')

		if password != password_confirm:
			print 'Your passwords do not match. Try again.'
			self.set_password(user_id)

		else:
			self.user_data[user_id]['password'] = password

#----------------------------------------------------------------------------------------#			
#----------------------------------------------------------------------------------------#
class userDirPath:

	def __init__(self,user_id):

		# data attributes of the userDirPath object
		self.user_dir_path = None
		self.user_listings_html = None
		self.user_listings_yaml = None

		# update the path name 
		self.generate_user_dir(user_id)

	#------------------------------------------------------------------------#
	def generate_user_dir(self,user_id):
		''' method that checks if a user directory exists; if not it makes a new directory '''

		dir_name = '../users/{}/'.format(user_id)
		html_listings_dir = '{}listings_html/'.format(dir_name)
		yaml_listing_dir = '{}listings_yaml/'.format(dir_name)

		if not os.path.exists(dir_name):
			# make the user directory
			self.user_dir_path = dir_name
			os.makedirs(dir_name)

			# make the html listing directory
			self.user_listings_html = html_listings_dir
			os.makedirs(html_listings_dir)

			# make the yaml data listing directory
			self.user_listings_yaml = yaml_listing_dir
			os.makedirs(yaml_listing_dir)

		else:
			self.user_dir_path = dir_name
			self.user_listings_html = html_listings_dir
			self.user_listings_yaml = yaml_listing_dir

	def get_user_dir(self):
		return self.user_dir_path

	def get_user_listings_html(self):
		return self.user_listings_html

	def get_user_listings_yaml(self):
		return self.user_listings_yaml

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------#



