import sys  
import time
import yaml

from bs4 import BeautifulSoup
from urllib2 import urlopen

#------------------------------------------------------------------------#
# utility functions 
def getIntFromString(string):
	numbers = '0123456789'

	clean_string = ''
	for item in string:
		if item in numbers:
			clean_string += item

	return int(clean_string)


#------------------------------------------------------------------------#
# functions to get the resume links and text 

def getResumeText(url):
	html = urlopen(url)
	soup = BeautifulSoup(html, 'html.parser')

	resume_text = soup.find(id="resume_body").get_text()
	return resume_text


def getResumeLinks(url):
	base_url = 'https://www.indeed.com'

	html = urlopen(url)
	soup = BeautifulSoup(html, 'html.parser')

	Nresumes = soup.find(id="result_count").get_text()
	Nresumes = getIntFromString(Nresumes)

	html_links = soup.find(id="results").find_all('a', class_='app_link')

	links = []
	for link in html_links:
		link = '%s%s' %(base_url, link.get('href'))
		links.append(link) 

	return links

def processResumeLinks(links):
	text = []
	for link in links:
		resume_text = getResumeText(link)
		text.append(resume_text) 
	return text

#------------------------------------------------------------------------#
# functions to get the job listing links and text 

def getJobLinks(url):
	base_url = 'https://www.indeed.com'

	html = urlopen(url)
	soup = BeautifulSoup(html, 'html.parser')

	# print soup

	Njobs = soup.find(id="searchCount").get_text()
	idx = Njobs.find('of')
	Njobs = Njobs[idx:]
	Njobs = getIntFromString(Njobs)
	# print Njobs


	job_link_area = soup.find(id = 'resultsCol')
	# Get the URLS for the jobs
	job_urls = []
	job_urls_ads = []
	job_links = job_link_area.find_all('a')
	for link in job_links:
		link = link.get('href')
		if link:
			# links either contain 'clk' or 'company'
			if ('clk' in link) or ('company' in link):
				# links with length > 350 are sponsored links (ads)
				# the ad might not be an exact match for the query so separate them 
				if len(link) < 350:
					job_urls.append(link)
				else:
					job_urls_ads.append(link)
			
			# elif 'company' in link:
			# 	print ''
			# 	print link


	# job_URLS = [base_url + link.get('href') for link in job_link_area.find_all('a')] # Get the URLS for the jobs
	# print job_URLS

	# job_links = soup.find_all('a')
	# for link in job_links:
	# 	print link

	# job_listings1 = soup.find_all('div', class_="row result")
	# print len(job_listings1)

	# job_listings2 = soup.find_all('div', class_="row sjlast result")
	# print len(job_listings2)

	# want to avoid sponsord postings since they might not exactly match the search 

	# for listing in job_listings:
	# 	print '\n'
	# 	print listing
	# print len(job_listings)

	return job_urls, job_urls_ads


#------------------------------------------------------------------------#
reload(sys)  
sys.setdefaultencoding('utf8')

t0 = time.time()

Nlinks = 0

# resume query based on skill 
# https://www.indeed.com/resumes?q=python&co=US&start=50
# url = 'https://www.indeed.com/resumes?q=python&l='
# links = getResumeLinks(url)
# processResumeLinks(links)

# url = 'https://www.indeed.com/r/55b266890d5b6e4b'
# getResumeText(url)

# https://www.indeed.com/jobs?q=woodworker&l=
# url structure 
# q={Search Term}
# co={country}
# start={start number of query}
# l={location}
# Note: query attributes separated by '&'

# job listing query 
# url = 'https://www.indeed.com/q=woodworker-jobs'
# url = 'https://www.indeed.com/jobs?q=woodworker&start=0'
url = 'https://www.indeed.com/jobs?q=software+engineer&l='

links, links_ads = getJobLinks(url)
print len(links)
print len(links_ads)

print len(links_ads[0])


print '\nScraped %d links in %.2f seconds.' %(Nlinks, time.time()-t0)