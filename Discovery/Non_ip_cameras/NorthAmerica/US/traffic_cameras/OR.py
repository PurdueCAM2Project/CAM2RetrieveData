#!/usr/bin/python

import urllib2
import httplib
from xml.dom import minidom
from xml.dom.minidom import Node
#This program is to receive XML feed from OR
def getOR():	
	URL= 'http://www.tripcheck.com/ttipv2/Documents/SampleData/cctvInventory.xml'
	xml = urllib2.urlopen(URL)
	
	#output file
	out = open('OR.xml',"w")
	out.write(xml.read())
	out.close()
	listFile = open("OR.list","w")

	xmldoc = minidom.parse("OR.xml")
	root = xmldoc.getElementsByTagName('cCTVInventory') #extract cCTVInventory section from xml
	for cctv in root:
		listFile.write(cctv.getElementsByTagName('device-id')[0].firstChild.nodeValue.encode('utf-8')+'#') #ID
		listFile.write(cctv.getElementsByTagName('device-name')[0].firstChild.nodeValue.encode('utf-8')+'#') #address
		latitude = (cctv.getElementsByTagName('latitude')[0].firstChild.nodeValue)
		latitude = float(latitude)/(10**(len(latitude)-2))
		listFile.write(str(latitude)+'#')
		longitude =(cctv.getElementsByTagName('longitude')[0].firstChild.nodeValue)
		longitude = float(longitude)/(10**(len(longitude)-4))
		listFile.write(str(longitude)+'#') 
		listFile.write(cctv.getElementsByTagName('cctv-url')[0].firstChild.nodeValue.encode('utf-8')+'\n')



	listFile.close()

getOR()