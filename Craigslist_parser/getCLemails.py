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

def get_listing_urls(baseUrl,url_CLsearch):
	''' gets all the url listings from the search; each page only lists 200 
	listings, so it contiues until the total number of listings is reached '''

	listingsURLS = set([])
	Nlisting = 1
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

def get_email(soup,url):
	''' follow the link on the reply button to get the phone and/or email '''

	email = None 

	reply = soup.find('a', id="replylink")
	if reply:
		replyUrl = baseUrl + reply.get('href')
		html = urlopen(replyUrl)
		soup = BeautifulSoup(html,'html.parser')

		# get the email if available 
		email = soup.find('div', class_="anonemail")
		if email:
			email = email.text
			# print email

	return email

def process_CL_html(listingsURLS,baseUrl):
	i = 0
	emails = set([])

	fPM = open('PM_emails.txt', 'a')
	fCL = open('CL_emails.txt', 'a')
	for url in listingsURLS:
		print 'Processing listing number %d ...' %i
		i += 1

		html = urlopen(url)
		soup = BeautifulSoup(html, 'html.parser')

		email = get_email(soup,baseUrl)

		if email:
			if email not in emails:
				emails.add(email)
				print 'Found email!'
				if 'craigslist' in email:
					fCL.write('%s\n' %email)
				else:
					fPM.write('%s\n' %email)
	fPM.close()
	fCL.close()

#------------------------------------------------------------------------#
# main program

# url = 'http://sfbay.craigslist.org/reply/sfo/apa/5165944239'
# html = urlopen(url)
# soup = BeautifulSoup(html,'html.parser')

# print soup.prettify()
# email = soup.find('div',class_='anonemail')


baseUrl = 'http://sfbay.craigslist.org'
url_CLsearch = 'http://sfbay.craigslist.org/search/sfc/apa?s={}&min_price=2500'

t0 = time.time()
print 'Finding the listing urls...'
listingsURLS = get_listing_urls(baseUrl,url_CLsearch)
print 'Found %d urls!\n\n' %len(listingsURLS)

process_CL_html(listingsURLS,baseUrl)

print '\nProcessing time: %.2f seconds' %(time.time() - t0)


