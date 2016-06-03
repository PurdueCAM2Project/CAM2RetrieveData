
#!/usr/bin/python

import urllib2
import httplib

#This program is to receive XML feed from Ohio state
def getMA():	
	URL= 'http://www1.eot.state.ma.us/xmltrafficfeed/camsXML.aspx'
	xml = urllib2.urlopen(URL)
	
	#output file
	out = open('MA.xml',"w")
	out.write(xml.read())
	out.close()

getMA()