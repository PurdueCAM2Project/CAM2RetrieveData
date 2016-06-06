#!/usr/bin/python
""" 
--------------------------------------------------------------------------------
Descriptive Name     : MD.py
Author               : unknown							      
Contact Info         : ssui@purdue.edu (Shengli Sui)
Description          : Parse cameras on the Maryland Dept of Transportation traffic camera website
Command to run script: python MD.py
Output               : output MD.xml 
Other files required by : N/A
this script and where 
located
----For Parsing Scripts---------------------------------------------------------
URL Parse	     : http://www.chart.state.md.us/rss/ProduceRss.aspx?Type=VIDEOXML&filter=all
In database (Y/N)    : Y
--------------------------------------------------------------------------------
"""
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
