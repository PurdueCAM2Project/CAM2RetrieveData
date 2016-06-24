#!/usr/bin/python
"""
-----------------------------------------------------------------------------
Descriptive Name: eurocityNON_IP.py
Author          : (rewritten by Chan Weng Yan)					      
Contact Info    : cwengyan@purdue.edu
Date Written    : June 23,2016
Description     : Parse several european non traffic NON_IP cameras
Command to run  : python eurocityNON_IP.py > euroErrorNON_IP
script
Output          : country#city#snapshot_url#latitude#longitude to 
		  <list_eurocityNON_IP.txt>
		  urls that raise errors will be redirected to <euroError>
Note            : 1) this website uses a lot of non-ascii (unicode) characters.
		     urllib2.urlopen cannot open urls with unicode so used 
		     request.get instead. Some discriptions scraped cannot be 
		     understood by google API so any errors should be redirected
		     to <euroError> and fix manually
		  2) This script only gets all NON_IP cameras, another script
		     is written to get IP ones

Other files required by : N/A
this script and where 
located
----For Parsing Scripts-----------------------------------------------------
Website Parsed       : http://www.eurocitycam.com
In database (Y/N)    : Y
Date added to Database : June 23, 2016
----------------------------------------------------------------------------
"""

from bs4 import BeautifulSoup
import urllib2
import requests
import re
import sys
import json
import time

def eurocitycam():
	euro_URL = "http://www.eurocitycam.com"
	soup = BeautifulSoup(urllib2.urlopen(euro_URL).read())
	f = open('list_eurocityNON_IP.txt','w')
	f.write('country#city#snapshot_url#latitude#longitude'+'\n')

	countrylist = []
	countryname = []
	footer = soup.find('div',{'id':'rt-footer'})
	#obtain all country url
	for country in footer.find_all('a'):
		countrylist.append(euro_URL+country['href'])
	#obtain all country names
	for span in footer.find_all('span'):
		string = re.split('<|>| ',str(span))
		countryname.append(string[2])
	gotoCountry(euro_URL,countrylist,countryname,f)
	f.close()


def gotoCountry(baseurl,countrylist,countryname,f):
	#for each country get all city names and city urls
	iter_country = 0
	for country in countrylist:
		citylist = []
		cityname = []
		soup = BeautifulSoup(urllib2.urlopen(country).read())
		block = soup.find('div',{'class':'rt-grid-7 rt-omega'})

		for city in block.find_all('a'):
			citylist.append(baseurl+city['href']) #get all cityurl
			string = re.split('>|<| \d',str(city))
			string = str(string[2]).replace('.','')
			cityname.append(str(string))  #get all city names
		print countryname[iter_country]
		individualImage(cityname,citylist,countryname[iter_country],f)
		iter_country += 1

def individualImage(cityname,citylist,country,f):
	#get individual image
	iter_city = 0
	for cityurl in citylist:
		try:
			page =requests.get(cityurl)
			soup = BeautifulSoup(page.content) 
			img = soup.find('div',{'class':'rt-joomla'})
			imgurl = img.find('img')
			imgurl = imgurl['src']
		except:
			continue

		if 'mjpg' not in imgurl:#find only IP cameras
			#Format Google API input for every individual image
			location=cityname[iter_city]+' '+ country
			location=location.replace(" ","+")
			location=location.strip()
			api='https://maps.googleapis.com/maps/api/geocode/json?address='+location
			response = urllib2.urlopen(api).read()
			#Load by json module
			parsed_json = json.loads(response)
			content = parsed_json['results']
			#Extract latitude and longitude from the API json code
			try: 
				loc = content[0]
				geo = loc['geometry']
				location2 = geo['location']
				lat = str(location2['lat'])
				lng = str(location2['lng'])
				city = str(cityname[iter_city])
	
				#get country code
				add_com = loc['address_components']
				for item in add_com:
					types = item['types']
					if types[0] == 'country':
						countryCode = item['short_name']
					if types[0] == 'locality':
						city = item['long_name']

				output = countryCode+'#'+city+'#'+imgurl+'#'+lat+'#'+lng
				f.write(output.encode('utf-8')+'\n')

			#redirect problematic urls to separate textfile
			except:
				try:
					print('\n'+location.encode('utf-8'))
					print('\n'+cityurl.encode('utf-8'))
					e = sys.exc_info() 
					print '\n'+ str(e) + '\n'
				except:
					e = str(sys.exc_info())
					print '\n'+ str(e) + '\n'

		time.sleep(0.1)
		iter_city += 1

if __name__ == "__main__":
	eurocitycam()
