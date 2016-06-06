#!/usr/bin/python
""" 
--------------------------------------------------------------------------------
Descriptive Name     : MA.py
Author               : unknown							      
Contact Info         : ssui@purdue.edu (Shengli Sui)
Description          : Parse cameras on the 511 Massachusetts traffic camera website
Command to run script: python MA.py
Output               : output MA.xml 
Other files required by : N/A
this script and where 
located
----For Parsing Scripts---------------------------------------------------------
URL Parse	     : http://www1.eot.state.ma.us/xmltrafficfeed/camsXML.aspx
In database (Y/N)    : Y
--------------------------------------------------------------------------------
"""
import urllib2
import httplib

def getMA():	
	URL= 'http://www1.eot.state.ma.us/xmltrafficfeed/camsXML.aspx'
	xml = urllib2.urlopen(URL)
	
	#output file
	out = open('MA.xml',"w")
	out.write(xml.read())
	out.close()

getMA()
