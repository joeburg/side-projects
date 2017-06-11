import codecs


def load_html_file(html_file):
	# load the html document
	f = codecs.open(html_file, 'r')
	html = f.read()
	f.close()
	return html