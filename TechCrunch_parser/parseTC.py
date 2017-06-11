import sys  
import time
import yaml

from bs4 import BeautifulSoup
from urllib2 import urlopen


#------------------------------------------------------------------------#
reload(sys)  
sys.setdefaultencoding('utf8')
t0 = time.time()

# get all of the links to TechCrunch articles 
# 632 pages of startup articles
page_number = 0
N_articles = 0
f = open('TC_startup_articles_data3.txt','w')
while True:
	page_number += 1
	print 'Page number = %d' %page_number

	url = 'http://techcrunch.com/startups/page/{}/'.format(page_number)

	try:
		html = urlopen(url)
		soup = BeautifulSoup(html, 'html.parser')

		stories = soup.find_all('li', class_='river-block ')

		if stories:
			for story in stories:
				# get the url from the article 
				link = story.get('data-permalink')

				# get the date from the link
				if link:
					baseurl = 'http://techcrunch.com/'
					date = link[len(baseurl): len(baseurl) + 10]
				else:
					continue

				# get the title of the article 
				title = story.get('data-sharetitle')

				# try to open the link and grab the text
				try:
					# some stories are removed
					html_l = urlopen(link)
				except:
					continue

				soup_l = BeautifulSoup(html_l, 'html.parser')

				article_entry = soup_l.find_all('p')
				if article_entry:
					article_text = ''
					for data in article_entry:
						article_text += data.text+' '
				else:
					continue

				# write the data to a file
				if link and title and date and article_text:
					N_articles += 1
					print 'Article Number = %d' %N_articles
					f.write('<!--\n%s\n%s\n%s\n%s\n--!>\n' %(link, title, date, article_text))
		else:
			continue
	except:
		break
f.close()

print 'Number of articles = %d' %N_articles
print '\nProcessed TechCrunch in %.2f minutes.' % ((time.time()-t0)/60.0)

# for each link, process the article and write to a yaml file

# url = 'http://techcrunch.com/2015/09/16/todoist-updates-its-web-app-with-new-features-and-design/'
# url = 'http://techcrunch.com/2015/09/16/dostuff/'
# url = 'http://techcrunch.com/2015/09/16/learnup-a-startup-closing-the-skills-gap-for-entry-level-job-seekers-raises-8m-from-nea-shasta/'
# url = 'http://techcrunch.com/2015/09/16/vinebox-offers-wine-by-the-glass-as-a-monthly-subscription/'
# url = 'http://techcrunch.com/2015/09/16/a-case-study-of-startup-failure/'
# url = 'http://techcrunch.com/2011/05/20/turntable-fm/'
# url = 'http://techcrunch.com/2011/06/02/founder-stories-from-paul-newman-to-paul-graham-with-alexis-ohanian-tctv/'


# url = 'http://techcrunch.com/2015/06/09/vine-updates-search-results-to-include-actual-vines-not-just-hashtags-and-people/'
# html = urlopen(url)
# soup = BeautifulSoup(html, 'html.parser')
# article_text = ''
# article_entry = soup.find_all('p')
# for data in article_entry:
# 	article_text += data.text+' '
# print article_text


# article_data = []
# if article_entry:
# 	article_text = ''
# 	for data in article_entry:
# 		# if data.find('p'):
# 		# 	print data
# 		# 	print '\n\n\n\n\n'			
# 		if not data.find('div'):
# 			article_data.append(data)

# 			if data.find('p'):
# 				print data
# 				print '\n\n\n\n\n'
# 				article_text += data.text+' '

# print article_text


# # f = open('TC_startup_articles_data.yml','w')
# f = open('TC_startup_articles_data.txt','w')
# for link_title_date in tc_data:
# 	# get the url, title and date of article
# 	url, title, date = link_title_date 
# 	# url = link_title_date[0].encode('utf-8')
# 	# title = link_title_date[1].encode('utf-8')
# 	# date = link_title_date[2].encode('utf-8')

# 	# get the text of the article
# 	html = urlopen(url)
# 	soup = BeautifulSoup(html, 'html.parser')

# 	article_entry = soup.find('div', class_='article-entry text')

# 	article_text = ''
# 	for data in article_entry:
# 		if not data.find('div'):
# 			article_text += data.text+' '

# 	# article_text = article_text.encode('utf-8')

# 	# write the data to a file
# 	f.write('<!--\n%s\n%s\n%s\n%s\n--!>\n' %(url, title, date, article_text))
# 	# f.write('%s : { title : %s, date : %s, text : %s }\n' %(url, title, date, article_text))
# 	# f.write('%s : %s\n' %(url, article_text))
# 	# f.write('%s : load\n' %(url))
# 	# f.write('%s\n\n' %article_text)

# f.close()


# # test opening and reading the file
# with open('TC_startup_articles_data.yml') as f:
# 	data = yaml.load(f)

# for url in data:
# 	print url
# 	# print data[url]['title']
# 	# print data[url]['date']
# 	# print data[url]['text']
# 	# print data[url]

# f = open('TC_startup_articles_data.txt')
# # while True:
# # 	line = f.readline()
# # 	print line
# # 	print ''
# for line in f:
# 	line = line.strip()
# 	if line == '<!--':
# 		print line







