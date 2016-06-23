""" 
--------------------------------------------------------------------------------
Descriptive Name     : ilikephilly.py
Author               : unknown							      
Contact Info         : cwengyan@purdue.edu (Chan Weng Yan)
Date Written         : unknown
Description          : Parse cameras on the Philadelphia Live Traffic Cameras website)
Command to run script: python ilikephilly.py
Output               : output urls, country, city and latitude, longitude to a 
                       textfile <philly>
Note                 : 
Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.ilikephilly.com/traffic/
In database (Y/N)    : Y
Date added to Database : unknown
--------------------------------------------------------------------------------
"""
from bs4 import BeautifulSoup
import urllib2
import re
import sys
import json
import Queue
import time

source_url = 'http://www.ilikephilly.com/traffic/'
city = 'Philladelphia'
state = 'PA'
country = 'USA'
f = open('list_ilikephilly.txt', 'w')
dupe_check = []
f.write('country#state#city#description#snapshot_url#latitude#longitude\n')

#grab additional URLs from original URL
def geturl(queue, soup):
	for tag in soup('a'):
		try:
			link = str(tag['href'])
			if not link.__contains__('#') and not link.__contains__('http'):
				if check_duplicate(dupe_check, link) == 1:
					queue.put(source_url+link)
		except:
			continue
	return

#check link against array  
#1 -> No duplicate
#0 -> Duplicate
def check_duplicate(str_array, link):
	for l in str_array:
		if l in link:
			return 0
	str_array.append(link)
	return 1

#Grabs Description
def grabdef(soup):
	for tag in soup('title'):
		return tag.string
	return 

def grabimg(soup):
	for tag in soup('img'):
		if str(tag['src']).__contains__('.jpg'):
			return tag['src']
	return

#
def grabiframe(url, iframequeue, dqueue):
	time.sleep(0.2)
	iframe_url = ''
	try:
		response = urllib2.urlopen(url)
	except:
		return
	html = response.read()
	soup = BeautifulSoup(html)
	base = ''
	acount = 0
	icount = 0
	atags = []
	itags = []
	for tag in soup('a'):
		try:
			if tag.string is not None:
				if tag.string.__contains__('@'):
					temp = tag.string.split('@')
					temp = temp[0].replace(' ', '')
					acount = acount + 1
					if not temp:
						atags.append(base+tag.string)
					else:
						base = temp
						atags.append(tag.string)
		except KeyError:
			continue
	for tag in soup('iframe'):
		try:
			#if check_duplicate(dupe_check, tag['src']) == 1:
			icount = icount + 1
			itags.append(tag['src'])
			#elif check_duplicate(dupe_check, tag['src']) == 0:
				#print 'DUPLICATE: ' + tag['src']
		except KeyError:
			continue

	if len(atags) == len(itags):
		for i in range(0, len(atags)):
			dqueue.put(atags[i])
			iframequeue.put(itags[i])
	return

def process(url, description):
	time.sleep(0.2)
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html)
	queue = Queue.Queue()
	geturl(queue, soup)
	img = grabimg(soup)
	gAPI(description, city, state, country, img, f)
	return

def gAPI(locat, city, state, country, link, f): #Location is discription ,city, link is to URL, f is file
    time.sleep(0.2)
    locat = str(locat)
    description = locat
    description = description.replace('EB', '')
    description = description.replace('WB', '')
    description = description.replace('NB', '')    
    description = description.replace('SB', '')
    description = description.replace('@', 'and')
    description = description.replace('North of', '')
    description = description.replace('South of', '')
    description = description.replace('West of', '')
    description = description.replace('Easy of', '')
    description = description.replace('Before', '')
    description = description.replace('After', '')
    description = description.replace('Exit', '')
    description = description.replace('Approaching', '')
    description = description.replace('Ramp to', '')
    description = description.replace('Exp', '')
    description = description.replace('Midspan', '')
    description = description.split('/')[0]
    description = description.split('MM')[0]
    description = description.split('Curve')[0]
    #api = "https://maps.googleapis.com/maps/api/geocode/json?address=" + description + "," + city + "," + state +","+ country
    api = "https://maps.googleapis.com/maps/api/geocode/json?address=" + description + "," + state +","+ country
    api = api.replace(' ','')
    ''' use API to find the latitude and longitude'''
    response = urllib2.urlopen(api).read()
    #load by json module
    parsed_json= json.loads(response)
    content= parsed_json['results']
    #extract latitude and longitude from the API json code
    try:
    	loc= content[0]
    except IndexError:
    	print(locat + ' is not working')
    	return
    geo = loc['geometry']
    location2 = geo['location']
    lat = location2['lat']
    lng= location2['lng']
    #change lat and lng to string
    string_lat = str(lat)
    string_lng = str(lng)
    locat = locat.replace(' ', '')
    #print string_lat,string_lng
    locat = country+'#'+state+'#'+city+'#'+locat+'#'+link+'#'+string_lat+'#'+string_lng
    #locat = 'TX'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
    #file_lafa.write(link.encode('utf-8')+'\n')
    f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')
    return

response = urllib2.urlopen(source_url)
html = response.read()
soup = BeautifulSoup(html)
url_queue = Queue.Queue()
iframe_queue = Queue.Queue()
d_queue = Queue.Queue()
geturl(url_queue, soup)
while not (url_queue.empty()):
	grabiframe(url_queue.get(), iframe_queue, d_queue)
while not (iframe_queue.empty() and d_queue.empty()):
	process(iframe_queue.get(), d_queue.get())
f.close()
