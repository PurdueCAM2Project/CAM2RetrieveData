#JSON in script tag style
""" 
--------------------------------------------------------------------------------
Descriptive Name     : ddot.py
Author               : unknown								      
Contact Info         : cwengyan@purdue.edu (Chan Weng Yan)
Date Written         : unknown
Description          : Parse cameras on the Washington,DC traffic camera website
Command to run script: python ddot.py
Output               : country#state#city#description#snapshot_url#latitude#longitude to textfile  
Note                 : 
Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://app.ddot.dc.gov/
In database (Y/N)    : Y
Date added to Database : June 8, 2016
--------------------------------------------------------------------------------
"""
from bs4 import BeautifulSoup
import urllib2
import re
import sys
import json

f = open('list_ddot.txt', 'w')

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
