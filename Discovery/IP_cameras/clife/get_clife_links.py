import urllib2

TOTAL_NUMBER_OF_CAMERAS = 1818

def get_clife_links():
	"""Gets the links for the cameras in c-life.de. Stores the list in a file.
	"""
	urls = []
	next_result_index = 0
	while True:
		downloaded_data  = urllib2.urlopen('http://www.c-life.de/all.php?type=next&total=' + str(TOTAL_NUMBER_OF_CAMERAS) + '&start=' + str(next_result_index))
		urls.extend([item.split('&')[0] for item in downloaded_data.read().split('openurl=')[1:]])
		print len(urls), '/', TOTAL_NUMBER_OF_CAMERAS

		next_result_index += 8
		if next_result_index > TOTAL_NUMBER_OF_CAMERAS:
			break

	with open('urls.txt', 'w') as urls_file:
		for url in urls: urls_file.write(url + '\n')

if __name__ == '__main__':
	get_clife_links()
