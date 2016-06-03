#JScript method calls containing information
from bs4 import BeautifulSoup
import urllib2
import re
import sys
import json

f = open('nycdot', 'w')

#connect to target URL and retrieve HTML
url = 'http://nyctmc.org/'
response = urllib2.urlopen(url)
html = response.read()
soup = BeautifulSoup(html)
llresult = []
nresult = []
uresult = []
f.write('country#state#city#description#snapshot_url#latitude#longitude\n')
for tag in soup.find_all('script'):
	if tag.string and tag.string.__contains__('c_marker'):
		parse = tag.string.splitlines()
		for s in parse:
			if s and s.__contains__('GLatLng'):
				regex = '\"(.*)\"'
				if(re.findall(regex, s)):
					llresult.append(re.findall(regex, s))
				#print(llresult)
			elif s and s.__contains__('img src'):
				regex = '\"(.*)<br '
				nresult.append(re.findall(regex, s))
				regex = '\'(http.*jpg)\''
				uresult.append(re.findall(regex, s))
				#print (uresult)
		for x in range (0, len(llresult)):
			if(uresult[x]):
				latlng = str(llresult[x])
				regex = '\'(.*)\''
				latlng = re.findall(regex, latlng)[0]
				latlng = latlng.replace('\"', '')
				lat = latlng.split(',')[0].strip()
				lng = latlng.split(',')[1].strip()
				regex = '\'(.*)\''
				locat = 'USA#' + 'NY#' + 'New York City#' + re.findall(regex, str(nresult[x]))[0] + '#' + re.findall(regex, str(uresult[x]))[0] + '#' + lat + '#' + lng + '\n'
				f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')
f.close()


