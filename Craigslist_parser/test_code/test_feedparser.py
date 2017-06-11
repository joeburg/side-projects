import feedparser

url = 'http://sfbay.craigslist.org/search/sfc/apa?max_price=3000&format=rss'

listings = feedparser.parse(url)

# print len(listings)
print len(listings.entries)
# print listings.feed.image

# print type(listings)
# print type(listings.entries)
# print type(listings['entries'])

# print listings.feed.title
# print listings.feed.link
# print listings.feed.description

# for field in listings:
# 	print ''
	# print listings[field]
	# print '\n\n\n\n\n\n\n'

entries = listings['entries']
for entry in entries:
	print '#---------------------------------------------------------------------#'
	print entry['dc_source']
	print len(entry['summary'])


	# print '#---------------------------------------------------------------------#'
	# for field in entry:
	# 	print field
	# 	print ''
	# 	print entry[field]
	# 	print '\n\n'


# 	entry in listings.entries:
# 	if i < 2:
# 		print listings.entries[entry]
# 		i += 1


'''
fields in entries key of parsed object

dc_source
summary_detail
published_parsed
updated_parsed
links
title
rights
updated
summary
language
title_detail
link
published
rights_detail
enc_enclosure
id
dc_type
'''


''' 
fields in the parsed object

feed
status
updated
updated_parsed
encoding
bozo
headers
href
version
entries
namespaces
'''
