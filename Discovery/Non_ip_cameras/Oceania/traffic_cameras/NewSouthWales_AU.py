#!/usr/bin/python

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
	for result in results:
		#write longitude
		out.write(str(result['geometry']['coordinates'][0])+'#')
		#write latitude
		out.write(str(result['geometry']['coordinates'][1])+'#')
		#title
		out.write(result['properties']['title'].encode(encoding='UTF-8')+'#')
		#description
		out.write(result['properties']['view'].encode(encoding='UTF-8')+'#')
		#camera direction
		out.write(result['properties']['direction'].encode(encoding='UTF-8')+'#')
		#Image link
		out.write(result['properties']['href'].encode(encoding='UTF-8')+'\n')

	out.close();


getAU()