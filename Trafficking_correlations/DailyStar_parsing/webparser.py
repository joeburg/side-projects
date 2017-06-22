import sys  
import time
import yaml

from bs4 import BeautifulSoup
from urllib2 import urlopen

#------------------------------------------------------------------------#
def get_title_archive(soup):
	return None

def get_text_archive(soup):
	text = soup.text
	if text:
		return text
	else:
		return None

def get_links_archive(f,soup,date,N_articles):
	baseurl = 'http://archive.thedailystar.net/{}/'.format(date)

	articles = soup.find_all('a',class_="mainheadlink2",href=True)
	if articles:
		for article in articles:
			link = article.get('href')

			if link[0] == 'd':
				link = '{}{}'.format(baseurl,link)
				# print link
			else:
				continue

			# process the article
			# try to open the link and grab the text
			try:
				# some stories are removed
				html_l = urlopen(link)
			except:
				continue
			
			soup_l = BeautifulSoup(html_l, 'html.parser')
			title = get_title_archive(soup_l)
			article_text = get_text_archive(soup_l)

			# write data to file
			N_articles = write_data(f,link,title,date,article_text,N_articles)	

	return N_articles	

def get_title_archive_php(soupdata):
	title = soupdata.text
	if title:
		return title
	else:
		return None

def get_text_archive_php(soup):
	article_entry = soup.find_all('p')
	if article_entry:
		article_text = ''
		for data in article_entry:
			article_text += data.text+' '
		return article_text
	else:
		return None

def get_links_archive_php(f,soup,date,N_articles):
	articles = soup.find_all('div',class_="newes")
	for article in articles:
		data = article.find('a')
		link = data.get('href')
		title = get_title_archive_php(data)

		# try to open the link and grab the text
		try:
			# some stories are removed
			html_l = urlopen(link)
		except:
			continue

		soup_l = BeautifulSoup(html_l, 'html.parser')
		article_text = get_text_archive_php(soup_l)

		# write data to file
		N_articles = write_data(f,link,title,date,article_text,N_articles)

	return N_articles

def get_links_beta2(f,soup,date,N_articles):
	articles = soup.find_all('div',class_="read-more")
	for article in articles:
		link = article.find('a').get('href')

		# try to open the link and grab the text
		try:
			# some stories are removed
			html_l = urlopen(link)
		except:
			continue

		soup_l = BeautifulSoup(html_l, 'html.parser')
		title = get_title_current(soup_l)
		article_text = get_text_current(soup_l)

		# write data to file
		N_articles = write_data(f,link,title,date,article_text,N_articles)

	return N_articles

def get_title_current(soup):
	title = soup.title.text.strip()
	if title:
		return title
	else:
		return None

def get_text_current(soup):
	article_entry = soup.find_all('p')
	if article_entry:
		article_text = ''
		for data in article_entry:
			article_text += data.text+' '
		return article_text
	else:
		return None

def get_links_current(f,soup,date,N_articles):
	baseurl = 'http://www.thedailystar.net'

	articles = soup.find_all('div', class_='list-content')
	if articles:
		for article in articles:
			# get the link
			link = article.find('a',href=True).get('href')

			if link:
				link = '{}{}'.format(baseurl,link)
				# print link
			else:
				continue

			# process the article
			# try to open the link and grab the text
			try:
				# some stories are removed
				html_l = urlopen(link)
			except:
				continue
			
			soup_l = BeautifulSoup(html_l, 'html.parser')
			title = get_title_current(soup_l)
			article_text = get_text_current(soup_l)

			# write data to file
			N_articles = write_data(f,link,title,date,article_text,N_articles)

	return N_articles


def write_data(f,link,title,date,article_text,N_articles):
	# write the data to a file
	N_articles += 1
	print 'Article Number = %d' %N_articles
	f.write('<!--\n%s\n%s\n%s\n%s\n--!>\n' %(link, title, date, article_text))
	return N_articles

def parse_site():
	N_articles = 0
	f = open('DailyStar_articles_data.txt','w')
	for year in range(2003,2016):

		for month in range(1,13):
			month = '%02d' % month

			for day in range(1,32):
				day = '%02d' % day

				# first try to access the site with the old url format
				date_archive = '{}/{}/{}'.format(year,month,day)
				url_archive = 'http://archive.thedailystar.net/{}/index.htm'.format(date_archive)

				try:
					html = urlopen(url_archive)
					soup = BeautifulSoup(html, 'html.parser')
					N_articles = get_links_archive(f,soup,date_archive,N_articles)

				except:
					print 'Bad link ...'
					# try to access the site with the new url format
					date_current = '{}-{}-{}'.format(year,month,day)
					url_current = 'http://www.thedailystar.net/newspaper?date={}'.format(date_current)

					try:
						html = urlopen(url_current)
						soup = BeautifulSoup(html, 'html.parser')
						N_articles = get_links_current(f,soup,date_current,N_articles)

					except:
						print 'Bad link ...'

	print 'Number of articles = %d' %N_articles
	f.close()


def parse_site_beta(year_start,year_end,month_start,month_end,day_start,day_end):
	N_articles = 0
	f = open('DailyStar_articles_2008_20012_data.txt','a')
	for year in range(year_start,year_end):

		for month in range(month_start,month_end):
			month = '%02d' % month

			for day in range(day_start,day_end):
				day = '%02d' % day	

				# first try to access the site with the old url format
				date = '{}-{}-{}'.format(year,month,day)
				url_archive = 'http://archive.thedailystar.net/beta2/newspaper/?date={}'.format(date)

				try:
					html = urlopen(url_archive)
					soup = BeautifulSoup(html, 'html.parser')
					N_articles = get_links_beta2(f,soup,date,N_articles)

				except:
					print 'Bad link ...'

	print 'Number of articles = %d' %N_articles
	f.close()	

'http://archive.thedailystar.net/beta2/newspaper/?date=2013-03-06'

def parse_site_php(year_start,year_end,month_start,month_end,day_start,day_end):
	N_articles = 0
	f = open('DailyStar_articles_2008_20012_data.txt','a')
	for year in range(year_start,year_end):

		for month in range(month_start,month_end):
			month = '%02d' % month

			for day in range(day_start,day_end):
				day = '%02d' % day

				# first try to access the site with the old url format
				date = '{}-{}-{}'.format(year,month,day)
				url_archive = 'http://archive.thedailystar.net/newDesign/archive.php?date={}'.format(date)

				try:
					html = urlopen(url_archive)
					soup = BeautifulSoup(html, 'html.parser')
					N_articles = get_links_archive_php(f,soup,date,N_articles)

				except:
					print 'Bad link ...'

	print 'Number of articles = %d' %N_articles
	f.close()	

#------------------------------------------------------------------------#
reload(sys)  
sys.setdefaultencoding('utf8')
t0 = time.time()

parse_site_php(2007,2008,8,9,15,31)
parse_site_php(2007,2014,1,13,1,31)
parse_site_php(2013,2014,3,4,1,6)
parse_site_beta(2013,2014,3,4,6,32)
parse_site_beta(2013,2014,4,12,1,32)

print '\nProcessed The Daily Star in %.2f minutes.' % ((time.time()-t0)/60.0)


