"""
-----------------------------------------------------------------------------
Descriptive Name: PA_turnpike.py
Author          : Chan Weng Yan  
Contact Info    : cwengyan@purdue.edu
Date Written    : July 12,2016
Description     : Parse several Pennsylvania traffic cameras
Command to run  : python PA_turnpike.py
script
Output          : country#state#city#snapshot_url#latitude#longitude to <list_PA_turnpike.txt>
Other files required by : script reads from PA_turnpike.kml rather than from the website
this script and where 
located

----For Parsing Scripts-----------------------------------------------------
Website Parsed       : https://www.paturnpike.com/cameras/
In database (Y/N)    : Y
Date added to Database : July 12, 2016
----------------------------------------------------------------------------
"""

import re
import sys
import json
import urllib2
import time
from bs4 import BeautifulSoup


def getData():
	
	kmlFile = open('PA_turnpike.kml').read() #read from kml file
	soup =  BeautifulSoup(kmlFile)
	outputFile = open("list_PA_turnpike.txt",'w')
	outputFile.write('country#state#city#snapshot_url#latitude#longitude'+'\n')
	url = []
	latitude = []
	longitude = []

	#get image url by regex
	for placemark in soup.find_all('description'): 
		if 'src' in str(placemark):
			src = str(placemark).split('src="')
			src = str(src[1]).split('jpg')
			url.append(src[0]+'jpg')
	
	#get coordinates by regrex
	for coordinates in soup.find_all('coordinates'):
		coordinates = str(coordinates).replace('<coordinates>','').replace('</coordinates>','')
		coordinates = coordinates.split(',')
		longitude.append(coordinates[0])
		latitude.append(coordinates[1])
	
	iter = 0
	for url in url:
		api = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + latitude[iter] + ','+ longitude[iter]
		print api
		response = urllib2.urlopen(api).read()
		#Load by json module
		parsed_json = json.loads(response)
		content = parsed_json['results']
		loc = content[0]
		add_com = loc['address_components']
		
		for item in add_com:
			types = item['types']
			if types[0] == 'locality':
				city = item['long_name']
			elif types[0] == 'administrative_area_level_1':
				stateCode = item['short_name']

		output = 'USA#'+stateCode+'#'+city+'#'+url+'#'+latitude[iter]+'#'+longitude[iter]
		outputFile.write(output.encode('utf-8')+'\n')
		iter += 1
		time.sleep(0.5)


if __name__ == "__main__":
	getData()
