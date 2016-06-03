#JSON in script tag style
from bs4 import BeautifulSoup
import urllib2
import re
import sys
import json

f = open('ddot', 'w')

#connect to target URL and retrieve HTML
url = 'http://app.ddot.dc.gov/'
response = urllib2.urlopen(url)
html = response.read()
soup = BeautifulSoup(html)
f.write('country#state#city#description#snapshot_url#latitude#longitude\n')
#search through script tags for specific tag containing 'LoadCameras'
for tag in soup.find_all('script'):
	if tag.string and tag.string.__contains__('LoadCameras'):
		regex = '\[{.*}\]'
		#results are JSON formatted information on each camera
		result = re.findall(regex, tag.string)[0]
		decoded = json.loads(result)
		for d in decoded:
			locat = 'USA#' + 'DC#' + 'Washington#' + d['name'] + '#' + d['image'] + '#' + str(d['lat']) + '#' + str(d['lng']) + '\n'
			f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')
f.close()
