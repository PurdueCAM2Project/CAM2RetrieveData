# script for parsing cams on http://hvo.wr.usgs.gov/cams/

import urllib2

import re

def getFromPage(page_url):

	Input = urllib2.urlopen(page_url).read()

	temp_url = re.findall("src='.*'></a>", Input)

	temp_url[0] = temp_url[0].replace("src='", "")

	temp_url[0] = temp_url[0].replace("'></a>", "")

	cam_url = base_url + temp_url[0]

	#print cam_url
	
	return cam_url

base_url = "http://hvo.wr.usgs.gov/cams"

Input = urllib2.urlopen(base_url).read()

f = open('list_HVO', 'w');

f.write('description#snapshot_url#country#state#City')

page_links = re.findall('<a href=.*><li>', Input)

titles = re.findall("<li>.*</li>", Input)

for i in range(0, len(page_links)):
	
	page_links[i] = page_links[i].replace('<a href="', '')
	
	page_links[i] = page_links[i].replace('"><li>', '')
	
	page_links[i] = base_url + '/' + page_links[i]
	
	url = getFromPage(page_links[i])
	
	titles[i] = titles[i].replace('<li>', '')
	
	titles[i] = titles[i].replace('</li>', '')
	
	titles[i] = titles[i].replace("&#299;", 'i')
	
	titles[i] = titles[i].replace("&#699;", "'")
	
	titles[i] = titles[i].replace("&#332;", "O")

	titles[i] = titles[i].replace("&#333;", "o")

	titles[i] = titles[i].replace("&#257;", "a")
	
	#print titles[i]

	f.write(titles[i] + '#' + url + '#' + 'US' + '#' + 'HI' + '#' + 'None' + '\n')

f.close()
