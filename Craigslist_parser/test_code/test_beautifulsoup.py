import json
import re

from bs4 import BeautifulSoup
from urllib2 import urlopen

#------------------------------------------------------------------------#
def get_title(soup):
	''' gets the title of the CL add '''
	title = soup.title
	if title:
		title = title.contents[0]
	return title


def is_number(str_data):
	if str_data in '0123456789':
		return True
	else:
		return False

def find_numberZ(str_data):
	''' finds a number (integers) in a string; format is 123</b>BD so search
	up to key index (BD, Ba, ft, etc.)'''
	idx = 0
	Num = None 
	for i in range(len(str_data)):
		if is_number(str_data[i]):
			idx = i
			Num = str_data[idx]
			break

	for item in str_data[idx+1:]:
		if is_number(item):
			Num += item

	return Num

def find_numberR(str_data):
	''' finds a real number in a string '''
	idx = 0
	Num = None 
	for i in range(len(str_data)):
		if is_number(str_data[i]):
			idx = i
			Num = str_data[idx]
			break

	for item in str_data[idx+1:]:
		if is_number(item) or item == '.':
			Num += item

	return Num

def get_beds_baths(str_data):
	''' finds the number of bedrooms and baths from the string data
	the number of bedrooms comes before bathrooms in the CL format '''

	Nbeds = None
	idx = str_data.find('BR')
	if idx != -1:
		Nbeds = find_numberZ(str_data[:idx])

	Nbaths = None
	idx = str_data.find('Ba')
	if idx != -1:
		Nbaths = find_numberR(str_data[idx-7:idx])

	return (Nbeds,Nbaths)

def get_Sq_footage(str_data):
	''' finds the square footage of the unit '''

	sqft = None 
	idx = str_data.find('ft')
	if idx != -1:
		sqft = find_numberZ(str_data[:idx])

	return sqft

def extract_str_from_span(str_data):
	''' return a substring between > & < '''
	idx1 = str_data.find('>')
	idx2 = str_data.find('<',idx1+1)
	return str_data[idx1+1:idx2]

def get_laundry(str_data):
	''' finds if there is laundry in the unit; CL format 
	is <span>laundry in bldg</span> so search between >...< '''
	return extract_str_from_span(str_data)

def get_parking(str_data):
	''' find the data on parking; CL format is 
	<span>no parking</span> so search between >...< '''
	return extract_str_from_span(str_data)

def get_moveIn_date(str_data):
	''' finds the move-in date from the CL data; the indicator is date="2015-08-20" '''
	idx = str_data.find('date=') + len('date=') + 1
	date = ''
	for item in str_data[idx:]:
		if is_number(item) or item == '-':
			date += item
		else:
			break
	return date

def get_showing_date(str_data):
	''' finds a showing date from the CL data, indicator is sale_date=2015-08-20 '''
	idx = str_data.find('sale_date=') + len('sale_date=')
	date = ''
	for item in str_data[idx:]:
		if is_number(item) or item == '-':
			date += item
		else:
			break
	return date


def get_cats_allowed(str_data):
	return extract_str_from_span(str_data)

def get_dogs_allowed(str_data):
	return extract_str_from_span(str_data)

def get_smoking_not_allowed(str_data):
	return extract_str_from_span(str_data)

def get_handicap_accessible(str_data):
	return extract_str_from_span(str_data)

def get_if_furnished(str_data):
	return extract_str_from_span(str_data)

def get_unit_type(str_data):
	return extract_str_from_span(str_data)

def get_price(soup):
	price = soup.find(class_="price")
	if price:
		price = price.text
	return price
	# return soup.find(class_="price").string

def get_post_description(soup,baseUrl):
	''' find the description of the posting '''

	# first check if there is a embedded link with contact info
	show_contact_info = soup.find('a', class_="showcontact")
	if show_contact_info:
		url = baseUrl + show_contact_info.get('href')
		html = urlopen(url)
		soup = BeautifulSoup(html,'html.parser')
		description = soup.find('div', class_="posting_body").text.strip()
		return description
	
	# if there is no link you can acess text using id="postingbody"
	else:
		description = soup.find(id="postingbody")
		if description:
			description = description.text.strip()
		return description
		# return soup.find(id="postingbody").text.strip()

def get_images(soup):
	images = set([])

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
					if img['url'] not in images:
						images.add(img['url'])
				break	
	return images

def get_map(soup):
	mapUrl = None
	links = soup.find_all('a')
	for link in links:
		url = link.get('href')
		if url:
			if 'maps.google.com' in url:
				mapUrl = url
				break
	return mapUrl	

def get_address(soup):
	''' find the address if one is given '''
	address = soup.find('div', class_="mapaddress")
	if address:
		address = address.text
	return address

def get_email_phone(soup,baseUrl):
	''' follow the link on the reply button to get the phone and/or email '''

	email = None 
	phone = None

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
				phone = phone.replace('tel:','').strip()
			if 'sms:' in phone:
				phone = phone.replace('sms:','').strip()

		# get the email if available 
		email = soup.find('div', class_="anonemail")
		if email:
			email = email.text

	return (email,phone)

def get_unit_specs(soup):
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

	NBedsBaths = ()
	showings = []
	sqft = None 
	laundry = None
	parking = None
	unitType = None
	date = None
	cats = None 
	dogs = None 
	smoking = None 
	handicap = None
	furnished = None

	unitSpecs = soup.find_all('p', class_="attrgroup")
	for category in unitSpecs:
		spandata = category.find_all('span')
		for data in spandata:
			data = str(data)
			# data = data.string # does not work because it skips beds/baths/etc.

			if notFoundBedBath:
				if ('BR' in data) or ('Ba' in data):
					NBedsBaths = get_beds_baths(data)
					notFoundBedBath = False
					# print 'Found bedrooms and baths: %s, %s\n' %(NBedsBaths[0],NBedsBaths[1])

			if notFoundSize:
				if 'ft' in data:
					sqft = get_Sq_footage(data)
					notFoundSize = False
					# print 'Found square footage: %s\n' %sqft

			if notFoundLaundry:
				for field in laundry_fields:
					if field in data:
						laundry = get_laundry(data)
						notFoundLaundry = False
						# print 'Found laundry: %s\n' %laundry
						break

			if notFoundParking:
				for field in parking_fields:
					if field in data:
						parking = get_parking(data)
						notFoundParking = False
						# print 'Found parking: %s\n' %parking
						break

			if notFoundType:
				for field in unitType_fields:
					if field in data:
						unitType = get_unit_type(data)
						notFoundType = False
						# print 'Found unit type: %s\n' %unitType
						break

			if notFoundMoveIn:
				if 'date=' in data and 'sale_data=' not in data:
					date = get_moveIn_date(data)
					notFoundMoveIn = False
					# print 'Found date available: %s\n' %date


			# CL limits to 3 showings in the post
			if Nshowing < 3:
				if 'sale_date=' in data:
					showing = get_showing_date(data)
					showings.append(showing)
					Nshowing += 1
					# print 'Found showing date: %s\n' %showing

			if notFoundCats:
				if 'cats' in data:
					cats = get_cats_allowed(data)
					notFoundCats = False
					# print 'Found if cats are allowed: %s\n' %cats

			if notFoundDogs:
				if 'dogs' in data:
					dogs = get_dogs_allowed(data)
					notFoundDogs = False
					# print 'Found if dogs are allowed: %s\n' %dogs

			if notFoundSmoking:
				if 'smoking' in data:
					smoking = get_smoking_not_allowed(data)
					notFoundSmoking = False
					# print 'Found smoking: %s\n' %smoking

			if notFoundHandicap:
				if 'wheelchair' in data:
					handicap = get_handicap_accessible(data)
					notFoundHandicap = False
					# print 'Found handicap: %s\n' %handicap

			if notFoundFurnished:
				if 'furnished' in data:
					furnished = get_if_furnished(data)
					notFoundFurnished = False
					# print 'Found if furnished: %s\n' %furnished	

	if len(NBedsBaths) == 0:
		NBedsBaths = (None,None)

	if len(showings) == 0:
		showings = None

	return [NBedsBaths,showings,sqft,laundry,parking,unitType,date,cats,dogs,smoking,handicap,furnished]


def write_data_yaml(title,price,emailphone,address,images,postinfo,mapUrl,unitspecs):
	f = open('test.yml','w')
	f.write('${title} : %s\n' %title)
	f.write('${price} : %s\n' %price)
	f.write('${email} : %s\n' %emailphone[0])
	f.write('${phone} : %s\n' %emailphone[1])
	f.write('${address} : %s\n' %address)
	f.write('${images} : %s\n' %images)
	f.write('${postinfo} : %s\n' %postinfo)
	f.write('${map} : %s\n' %mapUrl)
	f.write('${bedrooms} : %s\n' %unitspecs[0][0])
	f.write('${bathrooms} : %s\n' %unitspecs[0][1])

	unitspecs.remove(unitspecs[0])
	unitspecs_keys = ['showings','sqft','laundry','parking','unitType','date',
	'cats','dogs','smoking','handicap','furnished']

	for i in range(len(unitspecs)):
		f.write('${%s} : %s\n' %(unitspecs_keys[i], unitspecs[i]))

	f.close()

# str_data = '<span class="housing_movein_now property_date" date="2015-09-01" today_msg="available now">available sep 01</span>'
# date = get_moveIn_date(str_data)
# print date  

#------------------------------------------------------------------------#

# url = 'http://sfbay.craigslist.org/sfc/apa/5171178913.html'
# url = 'http://sfbay.craigslist.org/sfc/apa/5174416452.html'
# url = 'http://sfbay.craigslist.org/sfc/apa/5170840706.html'
# url = 'http://sfbay.craigslist.org/sby/apa/5182750122.html'
# url = 'http://sfbay.craigslist.org/eby/apa/5183880201.html'
# url = 'http://sfbay.craigslist.org/pen/apa/5180553598.html'
# url = 'http://sfbay.craigslist.org/eby/apa/5184246714.html'
# url = 'http://sfbay.craigslist.org/eby/apa/5184246033.html'
# url = 'http://sfbay.craigslist.org/pen/apa/5180580374.html'
# url = 'http://sfbay.craigslist.org/sfc/apa/5161057371.html'
# url = 'http://sfbay.craigslist.org/sfc/apa/5137513638.html'
# url = 'http://sfbay.craigslist.org/sby/apa/5184196367.html'
# url = 'http://sfbay.craigslist.org/sby/apa/5184225902.html'
# url = 'http://sfbay.craigslist.org/sfc/apa/5184238166.html'
# url = 'http://sfbay.craigslist.org/sby/apa/5184214759.html'
# url = 'http://sfbay.craigslist.org/sfc/apa/5184236552.html'
# url = 'http://sfbay.craigslist.org/sfc/apa/5156544964.html'
# url = 'http://sfbay.craigslist.org/sby/apa/5184199589.html'
# url = 'http://sfbay.craigslist.org/sby/apa/5184160454.html'
# url = 'http://sfbay.craigslist.org/sby/apa/5184407077.html'
# url = 'http://sfbay.craigslist.org/sby/apa/5178580519.html'
# url = 'http://sfbay.craigslist.org/sby/apa/5160219079.html'
url = 'http://sfbay.craigslist.org/sfc/apa/5184408849.html'


# url = 'http://www.yourhtmlsource.com/myfirstsite/'

html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

# data = soup.prettify()
# print data

# address = soup.find('div', class_="mapaddress").text
# print address

# data = soup.find(id="postingbody")
# data = soup.find('div', class_="posting_body")
# print data

# baseUrl = 'http://sfbay.craigslist.org'
# show_contact_info = soup.find('a', class_="showcontact")
# # print show_contact_info
# if show_contact_info:
# 	url = baseUrl + show_contact_info.get('href')
# 	html = urlopen(url)
# 	soup = BeautifulSoup(html,'html.parser')
# 	description = soup.find('div', class_="posting_body").text.strip()
# 	print description

# # hack to get email response 
# baseUrl = 'http://sfbay.craigslist.org'
# reply = soup.find('a', id="replylink")
# if reply:
# 	replyUrl = baseUrl + reply.get('href')
# 	html = urlopen(replyUrl)
# 	soup = BeautifulSoup(html,'html.parser')

# 	# get phone number if available 
# 	phone = soup.find('a', class_="mobile-only replytellink")
# 	if phone:
# 		phone = phone.get('href')
# 		if 'tel:' in phone:
# 			phone = phone.replace('tel:','').strip()
# 		if 'sms:' in phone:
# 			phone = phone.replace('sms:','').strip()
# 		print phone

# 	email = soup.find('div', class_="anonemail")
# 	if email:
# 		email = email.text
# 		print email






# get title 
title = get_title(soup).encode('utf-8')
print 'Found title: %s\n' %title

# get the price
price = get_price(soup).encode('utf-8')
print 'Found the price: %s\n' %price

# get the email/phone from reply
baseUrl = 'http://sfbay.craigslist.org'
emailphone = get_email_phone(soup,baseUrl)
print 'Found the email: %s\n' %emailphone[0]
print 'Found the phone: %s\n' %emailphone[1]

# get the images 
images = get_images(soup)
print 'Found images: '
print images
print ''

# get the post description
baseUrl = 'http://sfbay.craigslist.org'
postinfo = get_post_description(soup,baseUrl).encode('utf-8')
print 'Found the post info: %s\n' %postinfo

# get the map url
mapUrl = get_map(soup)
print 'Found the map: %s\n' %mapUrl

# get the address 
address = get_address(soup)
print 'Found the address: %s\n' %address

# get the move-in date, beds, baths, laundry, type, pets, furnished, showings, handicap, size, parking
unitspecs = get_unit_specs(soup)
print 'Found the unit specs: '
print unitspecs

write_data_yaml(title,price,emailphone,address,images,postinfo,mapUrl,unitspecs)

# #------------------------------------------------------------------------#
# ''' finds the number of listings in the CL search ''' 

# url = 'http://sfbay.craigslist.org/search/sfc/apa?max_price=3000'
# html = urlopen(url)
# soup = BeautifulSoup(html, 'html.parser')

# text = soup.get_text()
# idx = len('displaying ... of ')+text.find('displaying ... of ')
# Nlistings = text[idx : idx+6]

# idx2 = 0
# for i in range(len(Nlistings)):
# 	idx2 = i
# 	if Nlistings[i] not in '0123456789':
# 		break

# Nlistings = int(Nlistings[:idx2])
# # print Nlistings

# #------------------------------------------------------------------------#
# ''' gets all the url listings from the search; each page only lists 200 
# listings, so it contiues until the total number of listings is reached '''

# baseUrl = 'http://sfbay.craigslist.org'

# listingsURLS = set([])
# Nlisting = 1
# while Nlisting < Nlistings:
# 	# print Nlisting
# 	url = 'http://sfbay.craigslist.org/search/sfc/apa?s={}&max_price=3000'.format(Nlisting-1)
# 	html = urlopen(url)
# 	soup = BeautifulSoup(html, 'html.parser')

# 	for href in soup.find_all('a'):
# 		link = href.get('href')
# 		if link:
# 			if 'html' in link:
# 				# print listing
# 				link = baseUrl+link
# 				if link not in listingsURLS:
# 					listingsURLS.add(link)
# 					# print link
# 					Nlisting += 1

# # print listings
# print listingsURLS
# #------------------------------------------------------------------------#
# ''' for each url in listings; load the url and then parse the information;
# get email and add to database; get listing description; get price; get location; 
# get title; get number of bedrooms; get number of bathrooms; get move-in date '''

# listingData = {}
# for url in listingsURLS:
# 	html = urlopen(url)
# 	soup = BeautifulSoup(html, 'html.parser')




# Nlistings = 0
# for href in soup.find_all('a'):
# 	link = href.get('href')
# 	if link:
# 		if 'html' in link:
# 			# print listing
# 			Nlistings += 1



# url2 = 'http://sfbay.craigslist.org/search/sfc/apa?s={}&max_price=3000'.format(Nlistings)
# html2 = urlopen(url2)
# soup2 = BeautifulSoup(html2, 'html.parser')

# for href in soup2.find_all('a'):
# 	link = href.get('href')
# 	if link:
# 		if 'html' in link:
# 			# print listing
# 			Nlistings += 1

# print '\n Found %d listings' %Nlistings
