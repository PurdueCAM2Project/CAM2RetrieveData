#!/usr/bin/python

import urllib2
import httplib

#This program is to receive XML feed from MD
def getMD():	
	URL= 'http://www.chart.state.md.us/rss/ProduceRss.aspx?Type=VIDEOXML&filter=all'
	xml = urllib2.urlopen(URL)
	
	#output file
	out = open('MD.xml',"w")
	out.write(xml.read())
	out.close()

getMD()