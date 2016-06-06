#!/usr/bin/python
""" 
--------------------------------------------------------------------------------
Descriptive Name     : OH.py
Author               : unknown								      
Contact Info         : ssui@purdue.edu (Shengli Sui)
Description          : Parse cameras on the Ohio Dept of Transportation traffic camera website
Command to run script: python OH.py
Output               : output urls, country, city and latitude, longitude to a 
                       textfile <OH_cams>
Other files required by : N/A
this script and where 
located
----For Parsing Scripts---------------------------------------------------------
URL Parse	     : http://www.buckeyetraffic.org/services/Cameras.aspx
In database (Y/N)    : Y
--------------------------------------------------------------------------------
"""
import urllib2
import httplib
import xml.etree.ElementTree as ET

#This program is to receive XML feed from Ohio state
# Their xml categorize cameras into camera sites. Each camera site may contain more than one camera.
def getOH():
    URL= 'http://www.buckeyetraffic.org/services/Cameras.aspx'
    xml_string = urllib2.urlopen(URL).read()

    root = ET.fromstring(xml_string)
    
    # The output file is OH_cams
    out = open('OH_cams',"w")

    for camera_site in root:
    	
    	# get the parameters of the camera site
        address = camera_site.find('Location').text
        latitude = camera_site.find('Latitude').text
        longitude = camera_site.find('Longitude').text
        feeds = camera_site.find('CameraFeeds')
        
        # get the parameters of each camera in the camera site.
        for camera in feeds:
            direction = camera.find('Direction').text
            camtype = camera.find('Type').text
            description = camera.find('Description').text
            small_snapshot_url = camera.find('SmallImage').text
            snapshot_url = camera.find('LargeImage').text
            update_interval = camera.find('ImageUpdateInterval').text

		# for some cameras, they provide only small_snapshot.
            if snapshot_url is None:
                snapshot_url = small_snapshot_url

	# output the information of one camera (information of camera site + information of camera itself)
        out.write(str(snapshot_url) + "#" + str(latitude) + "#" + str(longitude)+ "#" + str(direction) + "#" + str(address) + "#" + str(camtype) + "#" + str(description) + "#" + str(small_snapshot_url) + "#" + str(update_interval) + "\n")

    out.close()
    
if __name__ == '__main__':
	getOH()
