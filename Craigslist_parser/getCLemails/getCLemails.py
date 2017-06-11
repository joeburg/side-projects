import json
import time

from bs4 import BeautifulSoup
from urllib2 import urlopen

#------------------------------------------------------------------------#
def get_Nlistings(url_CLsearch):
	''' finds the number of listings from a given CL search '''

	html = urlopen(url_CLsearch)
	soup = BeautifulSoup(html, 'html.parser')

	Nlistings = soup.find('span', class_="totalcount")
	if Nlistings:
		Nlistings = Nlistings.text	

	return int(Nlistings)

def get_listing_urls(baseUrl,url_CLsearch,Nlisting):
	''' gets all the url listings from the search; each page only lists 200 
	listings, so it contiues until the total number of listings is reached '''

	listingsURLS = set([])
	Nlisting_prev = 0
	while True:
		url = url_CLsearch.format(Nlisting-1)
		html = urlopen(url)
		soup = BeautifulSoup(html, 'html.parser')

		for href in soup.find_all('a'):
			link = href.get('href')
			if link:
				if 'html' in link:
					link = baseUrl+link
					if link not in listingsURLS:
						listingsURLS.add(link)
						Nlisting += 1

		if Nlisting - Nlisting_prev == 0:
			break
		else:
			Nlisting_prev = Nlisting

	return listingsURLS

def get_email_phone(soup,url):
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

def process_CL_html(listingsURLS,baseUrl):
	i = 0
	emails = set([])
	phones = set([])

	fPM = open('PM_emails.txt', 'a')
	fCL = open('CL_emails.txt', 'a')
	fph = open('phones.txt','a')
	for url in listingsURLS:
		print 'Processing listing number %d ...' %i
		i += 1

		html = urlopen(url)
		soup = BeautifulSoup(html, 'html.parser')

		email,phone = get_email_phone(soup,baseUrl)

		if email and phone:
			if email not in emails:
				emails.add(email)
				phones.add(phone)
				print 'Found email and phone!'		

				if 'craigslist' in email:
					fCL.write('%s    %s\n' %(email,phone))
				else:
					fPM.write('%s    %s\n' %(email,phone))

		elif email:
			if email not in emails:
				emails.add(email)
				print 'Found email!'
				if 'craigslist' in email:
					fCL.write('%s\n' %email)
				else:
					fPM.write('%s\n' %email)

		elif phone:
			if phone not in phones:
				phones.add(phone)
				fph.write('%s\n' %phone)
				print 'Found phone!'

	fPM.close()
	fCL.close()
	fph.close()

#------------------------------------------------------------------------#
# main program

# url = 'http://sfbay.craigslist.org/reply/sfo/apa/5165944239'
# html = urlopen(url)
# soup = BeautifulSoup(html,'html.parser')

# print soup.prettify()
# email = soup.find('div',class_='anonemail')


baseUrl = 'http://sfbay.craigslist.org'
url_CLsearch = 'http://sfbay.craigslist.org/search/sfc/apa?s={}&min_price=4000'

t0 = time.time()
print 'Finding the listing urls...'
listingsURLS = get_listing_urls(baseUrl,url_CLsearch,1000)
print 'Found %d urls!\n\n' %len(listingsURLS)

process_CL_html(listingsURLS,baseUrl)

print '\nProcessing time: %.2f seconds' %(time.time() - t0)


