#!/usr/bin/python
"""
--------------------------------------------------------------------------------
Descriptive Name     : BritishColumbia.py
Author               : Chan Weng Yan					      
Contact Info         : cwengyan@purdue.edu
Date Written         : June 16,2016
Description          : Parse cameras on the British Columbia, Canada traffic camera
Command to run script: python BritishColumbia.py
Output               : country#city#snapshot_url#latitude#longitude to <list_BritishColumbia.txt>
Note                 : 
Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://images.drivebc.ca/bchighwaycam/pub/html/www/index.html
In database (Y/N)    : Y
Date added to Database : June 16, 2016
--------------------------------------------------------------------------------
"""

from bs4 import BeautifulSoup
import urllib2
import re
import sys
import json
import time

def BChighway():
	#obataining all image urls
	BC_URL = "http://images.drivebc.ca/bchighwaycam/pub/html/www/index.html"
	baseurl = 'http://images.drivebc.ca'
	soup = BeautifulSoup(urllib2.urlopen(BC_URL).read())
	f = open('list_BritishColumbia.txt','w')
	f.write('country#city#snapshot_url#latitude#longitude'+'\n')
	imgurl = []
	titlelist = []
	latlist = []
	lnglist = []
	for img in soup.find_all('img',{'class':'thumbnail2'}):
		desc = img['title'].replace('Webcam Image: ', '')
		titlelist.append(desc)
		imgurl.append(baseurl + img['src'])
	
	iter = 0
	for street in titlelist:
		#Format Google API input
		street=street+' British Columbia'
		street=street.replace(" ","+")
		street=street.strip()
		print street
		api='https://maps.googleapis.com/maps/api/geocode/json?address='+street+'&key=AIzaSyBvfN0TyrWPbYb2Cj2IoXCMs8qyaqCqJfs'
		response = urllib2.urlopen(api).read()
		#Load by json module
		parsed_json = json.loads(response)
		content = parsed_json['results']
		#Extract latitude and longitude from the API json code
		loc = content[0]
		add_com = loc['address_components']

		most_exact = 4
		for item in add_com:
			types = item['types']
			if types[0] == "locality" and most_exact > 1:
				city = item['long_name']
				most_exact = 1
			elif types[0] == "postal_town" and most_exact > 2:
				city = item['long_name']
				most_exact = 2
			elif types[0] == "administrative_area_level_2" and most_exact > 3:
				city = item['long_name']
				most_exact = 3
			
		geo = loc['geometry']
		location2 = geo['location']
		lat = location2['lat']
		lng = location2['lng']
		string_lat = str(lat)
		string_lng = str(lng)
		output=('CA#'+city+'#'+imgurl[iter]+'#'+string_lat+'#'+string_lng)
		f.write(output.encode('utf-8')+'\n')
		time.sleep(0.1)
		iter += 1

	f.close()

if __name__ == "__main__":
	BChighway()

		
		
         
			
	
	

