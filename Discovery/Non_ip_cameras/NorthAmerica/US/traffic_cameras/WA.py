#!/usr/bin/python

import urllib2
import httplib
from xml.dom import minidom
from xml.dom.minidom import Node
import re

#This program is to receive XML feed from WA

def getWA():	
	URL= 'http://www.wsdot.wa.gov/traffic/api/HighwayCameras/kml.aspx'
	xml = urllib2.urlopen(URL)
	
	#output file for xml
	out = open('WA.xml',"w")
	out.write(xml.read())
	out.close()
	#output file for DB
	listFile = open("WA.list","w")

	xmldoc = minidom.parse("WA.xml")
	folder_list = xmldoc.getElementsByTagName('Folder') #extract folder section from xml
	for folders in folder_list:
		for pid in folders.getElementsByTagName("Placemark"):
			listFile.write(pid.attributes['id'].value.encode("utf-8")+'#')   #ID
			listFile.write(pid.getElementsByTagName("name")[0].firstChild.nodeValue.encode("utf-8")+"#") #place name 
			listFile.write(str(pid.getElementsByTagName("description")[0].firstChild.nodeValue.encode("utf-8")).split('"')[5]+'#') #URL 
			listFile.write(pid.getElementsByTagName("Point")[0].getElementsByTagName("coordinates")[0].firstChild.nodeValue.split(",")[0].encode("utf-8")+'#') #long
			listFile.write(pid.getElementsByTagName("Point")[0].getElementsByTagName("coordinates")[0].firstChild.nodeValue.split(",")[1].encode("utf-8")+'\n') #lat

	listFile.close()


getWA()

