#!/usr/bin/python
"""
-------------------------------------------------------------------------------
Descriptive Name     : NewSouthWales_AU.py
Author               : unknown						      
Contact Info         : cwengyan@purdue.edu (Chan Weng Yan)
Date Written         : unknown
Description          : Parse cameras on the New South Wales, Australia traffic camera website)
Command to run script: python NewSouthwales.py
Output               : description#city#country#longitude#latitude#snapshot_url to <AU.list>
Note                 : 
Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://data.livetraffic.com/cameras/traffic-cam.json
In database (Y/N)    : Y
Date added to Database : June 9, 2016
--------------------------------------------------------------------------------
"""
import urllib2
import httplib
import json

#This program is to receive JSON feed from AU NSW
def getAU():	
	URL= 'http://data.livetraffic.com/cameras/traffic-cam.json'  #NSW
	req = urllib2.Request(URL)
	req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1')
	res = urllib2.urlopen(req)
	js = json.load(res)
	#in_ = open('AU.json','r')
	#js = json.load(in_)
	out =open("AU.list",'w')
	#sort jason
	results = js['features']
	out.write('description#city#country#longitude#latitude#snapshot_url'+'\n')
	for result in results:
		#description
                out.write(result['properties']['title'].encode(encoding='UTF-8')+'#')
		#city and country
		out.write('New South Wales#AU#')
		#write longitude
		out.write(str(result['geometry']['coordinates'][0])+'#')
		#write latitude
		out.write(str(result['geometry']['coordinates'][1])+'#')
		
		#Image link
		out.write(result['properties']['href'].encode(encoding='UTF-8')+'\n')
	out.close();

if __name__ == '__main__':
	getAU()
