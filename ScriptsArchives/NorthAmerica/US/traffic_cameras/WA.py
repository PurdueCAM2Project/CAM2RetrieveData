#!/usr/bin/python
""" 
--------------------------------------------------------------------------------
Descriptive Name     : WA.py
Author               : unknown							      
Contact Info         : dailey1@purdue.edu (Ryan Dailey)
Date Written         : unknown
Description          : Parse cameras on the Washington state DOT traffic camera website
Command to run script: python WA.py
Usage                : downloads WA.xml to be parsed instead of parsing on the web
Output               : output urls, country, city and latitude, longitude to a 
                       textfile <WA.list>
Note                 : This program is to receive XML feed from WA
Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.wsdot.wa.gov/traffic/api/HighwayCameras/kml.aspx
In database (Y/N)    : Y
Date added to Database : unknown
--------------------------------------------------------------------------------
"""
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

if __name__ == __main__:
	getWA()

