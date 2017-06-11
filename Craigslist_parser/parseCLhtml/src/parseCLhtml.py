import json
import yaml

from bs4 import BeautifulSoup
from urllib2 import urlopen
from userDir import userDirPath

#------------------------------------------------------------------------#
class CLlisting:

	def __init__(self,user_id,user_data_file,url):

		# data attributes of the CL listing object
		self.outfile = None

		self.title = None
		self.price = None
		self.email = None
		self.phone = None
		self.address = None
		self.images = set([])
		self.description = None
		self.mapUrl = None
		self.unitspecs = None

		self.beds = None
		self.baths = None
		self.showings = []
		self.sqft = None 
		self.laundry = None
		self.parking = None
		self.unitType = None
		self.date = None
		self.cats = None 
		self.dogs = None 
		self.smoking = None 
		self.handicap = None
		self.furnished = None

		# load the url
		soup, baseUrl = self.load_url(url)

		# process the listing 
		self.process_CL_html(soup,baseUrl)

		# generate the output file
		self.outfile = self.generate_outfile(user_id,user_data_file)

		# write out the data to file
		self.write_data_yaml()

	#------------------------------------------------------------------------#
	''' CLlisting processing methods '''

	def load_url(self,url):
		html = urlopen(url)
		soup = BeautifulSoup(html, 'html.parser')

		# find the base url
		idx = url.find('.org') + len('.org')
		baseUrl = url[:idx]

		return (soup, baseUrl)

	def generate_outfile(self,user_id,user_data_file):
		''' write method to get the number listings for that user '''
		numlisting = self.get_num_listing(user_data_file,user_id)

		self.update_num_listing(user_data_file,user_id, numlisting+1)

		outfile_dir = userDirPath(user_id).get_user_listings_yaml()
		outfile = '%s%s_%s.yml' %(outfile_dir,user_id,numlisting+1)
		return outfile

	def get_num_listing(self,user_data_file,user_id):
		''' get the listing number for a user '''
		with open(user_data_file) as f:
			user_data = yaml.load(f)

		return user_data[user_id]['Nlisting']

	def update_num_listing(self,user_data_file,user_id,numlisting):
		''' update the listing number for that user '''
		with open(user_data_file) as f:
			user_data = yaml.load(f)

		user_data[user_id]['Nlisting'] = numlisting
		
		with open(user_data_file, 'w') as f:
			yaml.dump(user_data,f)

	def process_CL_html(self,soup,baseUrl):
		''' method to call the get_() methods for listing data '''

		# get title 
		self.get_title(soup)

		# get the price
		self.get_price(soup)

		# get the email/phone from reply
		# self.get_email_phone(soup,baseUrl)

		# get the images 
		self.get_images(soup)

		# get the post description
		self.get_post_description(soup,baseUrl)

		# get the map url
		self.get_map(soup)

		# get the address 
		self.get_address(soup)

		# get the move-in date, beds, baths, laundry, type, pets, furnished, showings, handicap, size, parking
		self.get_unit_specs(soup)

	def write_data_yaml(self):
		f = open(self.outfile,'w')
		f.write('${title} : %s\n' %self.title)
		f.write('${price} : %s\n' %self.price)
		f.write('${email} : %s\n' %self.email)
		f.write('${phone} : %s\n' %self.phone)
		f.write('${address} : %s\n' %self.address)
		f.write('${images} : %s\n' %self.images)
		f.write('${postinfo} : %s\n' %self.description)
		f.write('${map} : %s\n' %self.mapUrl)
		f.write('${bedrooms} : %s\n' %self.beds)
		f.write('${bathrooms} : %s\n' %self.baths)
		f.write('${showings} :  %s\n' %self.showings)
		f.write('${sqft} :  %s\n' %self.sqft)
		f.write('${laundry} :  %s\n' %self.laundry)
		f.write('${parking} :  %s\n' %self.parking)
		f.write('${unitType} :  %s\n' %self.unitType)
		f.write('${date} :  %s\n' %self.date)
		f.write('${cats} :  %s\n' %self.cats)
		f.write('${dogs} :  %s\n' %self.dogs)
		f.write('${smoking} :  %s\n' %self.smoking)
		f.write('${handicap} :  %s\n' %self.handicap)
		f.write('${furnished} :  %s\n' %self.furnished)
		f.close()

	#------------------------------------------------------------------------#
	''' methods to get CLlisting object's data attributes '''

	def get_CLlisting_yaml_file(self):
		return self.outfile

	def get_title(self,soup):
		''' gets the title of the CL add '''
		# title = soup.title
		# if title:
		# 	self.title = title.contents[0].encode('utf-8')

		title = soup.find(class_="postingtitletext")
		if title:
			self.title = title.text.encode('utf-8')
	

	def get_city(self,soup):
		''' gets the city of the listing (currently in title) '''



	def get_beds_baths(self,str_data):
		''' finds the number of bedrooms and baths from the string data
		the number of bedrooms comes before bathrooms in the CL format '''

		idx = str_data.find('BR')
		if idx != -1:
			self.beds = self.find_numberZ(str_data[:idx])

		idx = str_data.find('Ba')
		if idx != -1:
			self.baths = self.find_numberR(str_data[idx-7:idx])

	def get_Sq_footage(self,str_data):
		''' finds the square footage of the unit '''

		idx = str_data.find('ft')
		if idx != -1:
			self.sqft = self.find_numberZ(str_data[:idx])

	def get_laundry(self,str_data):
		''' finds if there is laundry in the unit; CL format 
		is <span>laundry in bldg</span> so search between >...< '''
		self.laundry = self.extract_str_from_span(str_data)

	def get_parking(self,str_data):
		''' find the data on parking; CL format is 
		<span>no parking</span> so search between >...< '''
		self.parking = self.extract_str_from_span(str_data)

	def get_moveIn_date(self,str_data):
		''' finds the move-in date from the CL data; the indicator is date="2015-08-20" '''
		idx = str_data.find('date=') + len('date=') + 1
		self.date = ''
		for item in str_data[idx:]:
			if self.is_number(item) or item == '-':
				self.date += item
			else:
				break

	def get_showing_date(self,str_data):
		''' finds a showing date from the CL data, indicator is sale_date=2015-08-20 '''
		idx = str_data.find('sale_date=') + len('sale_date=')
		date = ''
		for item in str_data[idx:]:
			if self.is_number(item) or item == '-':
				date += item
			else:
				break
		return date


	def get_cats_allowed(self,str_data):
		self.cats = self.extract_str_from_span(str_data)

	def get_dogs_allowed(self,str_data):
		self.dogs = self.extract_str_from_span(str_data)

	def get_smoking_not_allowed(self,str_data):
		self.smoking = self.extract_str_from_span(str_data)

	def get_handicap_accessible(self,str_data):
		self.handicap = self.extract_str_from_span(str_data)

	def get_if_furnished(self,str_data):
		self.furnished = self.extract_str_from_span(str_data)

	def get_unit_type(self,str_data):
		self.unitType = self.extract_str_from_span(str_data)

	def get_price(self,soup):
		price = soup.find(class_="price")
		if price:
			self.price = price.text.encode('utf-8')

	def get_post_description(self,soup,baseUrl):
		''' find the description of the posting '''

		# first check if there is a embedded link with contact info
		show_contact_info = soup.find('a', class_="showcontact")
		if show_contact_info:
			url = baseUrl + show_contact_info.get('href')
			html = urlopen(url)
			soup = BeautifulSoup(html,'html.parser')
			self.description = soup.find('div', class_="posting_body").text.strip().encode('utf-8')
		
		# if there is no link you can acess text using id="postingbody"
		else:
			description = soup.find(id="postingbody")
			if description:
				self.description = description.text.strip().encode('utf-8')

	def get_images(self,soup):
		''' extracts the js code from the html and gets urls from the data structure '''
		jsdata = soup.find_all('script',type="text/javascript")
		for jscode in jsdata:
			jscode = jscode.string
			if jscode:
				if jscode.find('var imgList') != -1:

					jscode = jscode.replace('<!--','')
					jscode = jscode.replace('-->','')
					jscode = jscode.replace('var imgList = ','')
					jscode = jscode.replace('var imageText = "image";','')
					jscode = jscode.replace(';','')
					jscode = jscode.strip()

					imgList = json.loads(jscode)

					for img in imgList:
						if img['url'] not in self.images:
							self.images.add(img['url'])
					break	

	def get_map(self,soup):
		mapUrl = None
		links = soup.find_all('a')
		for link in links:
			url = link.get('href')
			if url:
				if 'maps.google.com' in url:
					self.mapUrl = url
					break

	def get_address(self,soup):
		''' find the address if one is given '''
		address = soup.find('div', class_="mapaddress")
		if address:
			self.address = address.text

	def get_email_phone(self,soup,baseUrl):
		''' follow the link on the reply button to get the phone and/or email '''

		reply = soup.find('a', id="replylink")
		if reply:
			replyUrl = baseUrl + reply.get('href')
			html = urlopen(replyUrl)
			soup = BeautifulSoup(html,'html.parser')

			# get phone number if available 
			phone = soup.find('a', class_="mobile-only replytellink")
			if phone:
				phone = phone.get('href')
				if 'tel:' in phone:
					self.phone = phone.replace('tel:','').strip()
				if 'sms:' in phone:
					self.phone = phone.replace('sms:','').strip()

			# get the email if available 
			email = soup.find('div', class_="anonemail")
			if email:
				self.email = email.text

	def get_unit_specs(self,soup):
		laundry_fields = set(['w/d in unit','laundry in bldg','laundry on site',
			'w/d hookups','no laundry on site'])

		parking_fields = set(['carport','attached garage','detached garage',
			'off-street parking','street parking','valet parking','no parking'])

		unitType_fields = set(['apartment','condo','cottage/cabin','duplex',
			'flat','house','in-law','loft','townhouse','manufactured',
			'assisted living','land'])

		notFoundBedBath = True
		notFoundSize = True
		notFoundLaundry = True
		notFoundParking = True
		notFoundMoveIn = True
		notFoundCats = True
		notFoundDogs = True
		notFoundFurnished = True
		notFoundType = True
		notFoundSmoking = True
		notFoundHandicap = True

		Nshowing = 0

		unitSpecs = soup.find_all('p', class_="attrgroup")
		for category in unitSpecs:
			spandata = category.find_all('span')
			for data in spandata:
				data = str(data)
				# data = data.string # does not work because it skips beds/baths/etc.

				if notFoundBedBath:
					if ('BR' in data) or ('Ba' in data):
						self.get_beds_baths(data)
						notFoundBedBath = False

				if notFoundSize:
					if 'ft' in data:
						self.get_Sq_footage(data)
						notFoundSize = False

				if notFoundLaundry:
					for field in laundry_fields:
						if field in data:
							self.get_laundry(data)
							notFoundLaundry = False
							break

				if notFoundParking:
					for field in parking_fields:
						if field in data:
							self.get_parking(data)
							notFoundParking = False
							break

				if notFoundType:
					for field in unitType_fields:
						if field in data:
							self.get_unit_type(data)
							notFoundType = False
							break

				if notFoundMoveIn:
					if 'date=' in data and 'sale_data=' not in data:
						self.get_moveIn_date(data)
						notFoundMoveIn = False

				# CL limits to 3 showings in the post
				if Nshowing < 3:
					if 'sale_date=' in data:
						showing = self.get_showing_date(data)
						self.showings.append(showing)
						Nshowing += 1

				if notFoundCats:
					if 'cats' in data:
						self.get_cats_allowed(data)
						notFoundCats = False

				if notFoundDogs:
					if 'dogs' in data:
						self.get_dogs_allowed(data)
						notFoundDogs = False

				if notFoundSmoking:
					if 'smoking' in data:
						self.smoking = self.get_smoking_not_allowed(data)
						notFoundSmoking = False

				if notFoundHandicap:
					if 'wheelchair' in data:
						self.get_handicap_accessible(data)
						notFoundHandicap = False

				if notFoundFurnished:
					if 'furnished' in data:
						self.get_if_furnished(data)
						notFoundFurnished = False

		if len(self.showings) == 0:
			self.showings = None

	#------------------------------------------------------------------------#
	''' methods for get_() utilities '''

	def is_number(self,str_data):
		if str_data in '0123456789':
			return True
		else:
			return False

	def find_numberZ(self,str_data):
		''' finds a number (integers) in a string; format is 123</b>BD so search
		up to key index (BD, Ba, ft, etc.)'''
		idx = 0
		Num = None 
		for i in range(len(str_data)):
			if self.is_number(str_data[i]):
				idx = i
				Num = str_data[idx]
				break

		for item in str_data[idx+1:]:
			if self.is_number(item):
				Num += item

		return Num

	def find_numberR(self,str_data):
		''' finds a real number in a string '''
		idx = 0
		Num = None 
		for i in range(len(str_data)):
			if self.is_number(str_data[i]):
				idx = i

				Num = str_data[idx]
				break

		for item in str_data[idx+1:]:
			if self.is_number(item) or item == '.':
				Num += item

		return Num

	def extract_str_from_span(self,str_data):
		''' return a substring between > & < '''
		idx1 = str_data.find('>')
		idx2 = str_data.find('<',idx1+1)
		return str_data[idx1+1:idx2]
