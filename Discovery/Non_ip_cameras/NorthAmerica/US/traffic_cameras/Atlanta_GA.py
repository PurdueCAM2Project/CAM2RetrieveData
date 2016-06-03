#author: Honey Singh
#date: 10/23/2014

''' The script was written to parse the data for traffic 
cameras in Atlanta, Georgia. The original website url 
http://www.511ga.org/#zoom=4&lat=33.71641&lon=-84.37597&traffic_speeds_layer&Construction_control&Message_Signs_control&Major_Incidents_control&Other_Incidents_control&General_Info_control&Special_Event_control.

The file link used here is a resource file used by the website
 for camera data. The file is a geojson type. The data from 
the file is separated into each camera geometry and properties.

The required details are extracted using regular expressions.
The geometry tag had the required latitudes and longitudes 
and properties tag had the description and url.'''

import urllib2
import re
import sys
import json

def finding():
	
	url = "http://files0.iteriscdn.com/WebApps/GA/SafeTravel4/data/geojson/icons.cctv.geojsonp"
	soup = urllib2.urlopen(url).read()
	#opening the file to write
	f = open('Atlanta_GA','w')
	
	#using regular expression to split data
	dat = re.split("}},",soup)
	#looping over each split object list
	for i in range(0,len(dat)-1):
		# using regex to find geolocation from the list
		geoloc = re.findall("(?:(-\d+.\d+|\d+.\d+))",dat[i])
		#finding the url for each snapshot
		data = re.findall("http.*jpg",dat[i])
		# finding the location description
		ner = re.findall("\"location_description\":\".*\"",dat[i])
		# editing the location description
		loc_des = str(ner[0]).replace('location_description','').replace(':','').replace('\"','').replace('#','')
		 
		link = str(data).replace('[','').replace('\'','').replace(']','')
		#replacing the url address with public accessible address
		link = link.replace('navigator-c2c.dot.ga.gov/snapshots','cdn.511ga.org/cameras')
		# checking for any camera with bad data
		if not link or not geoloc:
			continue
		else:
			output = loc_des+"#Atlanta#GA#USA#"+link+"#"+geoloc[1]+"#"+geoloc[0]+"\n"			
			f.write(output.encode('utf-8'))
	f.close()
finding()
