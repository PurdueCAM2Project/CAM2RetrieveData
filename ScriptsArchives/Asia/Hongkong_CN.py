"""
--------------------------------------------------------------------------------
Descriptive Name     : Hongkong_CN
Author               : Ryan Dailey					      
Contact Info         : dailey1@purdue.edu
Date                 : 5/18/16
Description          : Imports traffic cameras from Hongkong
Command to run script: python Hongkong_CN.py
Input file format    : N/A
Output               : list_Hongkong_CN.txt
Note                 :
Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://data.one.gov.hk
In database (Y/N)    : Yes 5/18/16
--------------------------------------------------------------------------------
"""

from bs4 import BeautifulSoup
import urllib
import urllib2
import re
import sys
import string
import time
import json

def gAPI(locat, f):
    time.sleep(0.2);
    api = "https://maps.googleapis.com/maps/api/geocode/json?address=" + locat + ", " + "HK"
    api = api.replace(' ','')
    ''' use API to find the latitude and longitude'''
    response = urllib2.urlopen(api).read()
    #load by json module 
    parsed_json= json.loads(response)
    content= parsed_json['results']
    #extract latitude and longitude from the API json code
    loc= content[0]
    geo = loc['geometry']
    location2 = geo['location']
    lat = location2['lat']
    lng = location2['lng']
    #change lat and lng to string
    string_lat = str(lat)
    string_lng = str(lng)
    #print string_lat,string_lng
    locat = string_lat+'#'+string_lng
    #file_lafa.write(link.encode('utf-8')+'\n')
    f.write(locat.encode('utf-8'))
   
#get the camera info from hong kong (180 cameras)

def getHK():
	url = 'http://data.one.gov.hk/code/td/imagelist.xml' # link to the XML document with cameara data
	opener = urllib2.build_opener() 
	opener.addheaders = [('User-agent', 'Mozilla/5.0')] # Add header information
	response = opener.open(url)
	page = response.read()
	soup = BeautifulSoup(page) # Create soup
	f = open('list_Hongkong_CN.txt','w') # Create file for output
	f.write('snapshot_url#description#latitude#longitude#country#city')
	f.write('\n')
	for tag in soup.find_all('image'):
		f.write('http://tdcctv.data.one.gov.hk/'+str(tag.key.string)+'.JPG'+'#') # Write the snapshot URL
		description = str(tag.find("english-description").string) # Get the description string from the XML
		description = description.replace("\'", "") # Remove ' (database doesn't like it)
		f.write(description + '#') # Write the descritpion to the file.
		locat = description.replace("Interchange", "")  # Remove Interchange (Google API doesnt like it)
		locat = locat.replace("Side", "") # Remove Side (Google API gets better results)
		locat = locat.replace("near", "and") # Remove near and replace it with and (Google API gets better resaults)
		locat = locat.replace("-", "and") # Remove insert an and in place of a hyphon (Google API doesnt like it, and gets better resaults)
		locat = locat.replace(" ", "+") # Insert + in place of space (Google API formatting)
		gAPI(locat, f) # Send location information to the (Google API function - will write latitude and longitude data to file)
		f.write("#HK#Hong Kong") # Write country and City Data
		f.write("\n") # Write new line char at the end of line
	f.close()

if __name__ == __main__:
	getHK()
