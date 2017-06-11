import json
import re

from bs4 import BeautifulSoup
from urllib2 import urlopen


url = 'http://www.wcpm.com'

html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

data = soup.prettify()
print data
