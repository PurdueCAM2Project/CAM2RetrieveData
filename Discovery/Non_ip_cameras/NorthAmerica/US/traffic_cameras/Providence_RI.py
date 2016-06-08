""" 
--------------------------------------------------------------------------------
Descriptive Name     : Providence_RI.py
Author               : Mai Kanchanabul		
Contact Info         : cwengyan@purdue.edu (Chan Weng Yan) 
Description          : Parse cameras on the City of Providence traffic camera website
Command to run script: python Providence_RI.py
Output               : output urls, country, city and latitude, longitude to a 
                       textfile <list_ProvidenceRI>
Other files required by : N/A
this script and where 
located
----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://dot.ri.gov/travel/cameras_metro.php
In database (Y/N)    : Y 
Date added to Database : June 7, 2016
--------------------------------------------------------------------------------
"""

import urllib2
import json
import time
from bs4 import BeautifulSoup
import re

def getRegion():
    weburl="http://dot.ri.gov/travel/cameras_metro.php"
    baseurl="http://dot.ri.gov" #Set main url for camera images
    soup = BeautifulSoup(urllib2.urlopen(weburl).read())
    file = open('list_ProvidenceRI','w') #Open output file
    file.write("description#state#country#snapshot_url#latitude#longitude\n")
    for tag in soup.find_all("option"):
        region=tag.get('value')
        url = baseurl + region
        getProvidence(file,url)
    file.close()

def getProvidence(file,url):
    baseurl="http://dot.ri.gov" #Set main url for camera images
    soup = BeautifulSoup(urllib2.urlopen(url).read()) #Initialize bs4
    imagelist=[]
    streetlist=[]
    latlist=[]
    lnglist=[]
    for tag in soup.find_all("img"): #Finds all source code under "img"
        match=re.search('(.*)camimages/(.*).jpg',tag.get('src')) #Extract only source code desired
        if match:
            #Manipulate output to desired format
            imageurl=match.group().encode('utf-8')
            imageurl=imageurl.replace('..',baseurl)
            imagelist.append(imageurl)
            streetname=match.group(2).encode('utf-8')
            streetname=streetname.replace('@','at')
            streetlist.append(streetname)
    for street in streetlist:
        #Format Google API input
        street=street+' Providence'
        street=street.replace(" ","+")
        street=street.strip()
	#if encounter 'loc out of range error', after street add: +'&key=<google API key>'
        api='https://maps.googleapis.com/maps/api/geocode/json?address='+street
        response = urllib2.urlopen(api).read()
        #Load by json module
        parsed_json = json.loads(response)
        content = parsed_json['results']
        #Extract latitude and longitude from the API json code
        loc = content[0]
        geo = loc['geometry']
        location2 = geo['location']
        lat = location2['lat']
        lng = location2['lng']
        string_lat = str(lat)
        string_lng = str(lng)
        latlist.append(string_lat)
        lnglist.append(string_lng)
        time.sleep(0.1)

    #Write output to file
    iter=0
    while iter < len(imagelist):
        #Format the Url and output
	segment = imagelist[iter].split('/',imagelist[iter].count('/'))
	if segment[1] == 'img':
		output = streetlist[iter]+'#'+'Providence'+'#'+'RI'+'#'+'USA'+'#'+baseurl+imagelist[iter]+'#'+latlist[iter]+'#'+lnglist[iter]
        else:
		output = streetlist[iter]+'#'+'Providence'+'#'+'RI'+'#'+'USA'+'#'+imagelist[iter]+'#'+latlist[iter]+'#'+lnglist[iter]
	
	iter +=1
        #print output
        file.write(output.encode('utf-8')+'\n')

if __name__ == "__main__":
    getRegion()
