""" 
--------------------------------------------------------------------------------
Descriptive Name     : Traffic_Cameras_dotCom.py
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu
Date Written         : June 30, 2016
Description          : Parse the cameras on TrafficCameras.com
Command to run script: python Traffic_Cameras_dotCom.py
Usage                : None
Input file format    : N/A
Output               : list_Traffic_Cameras_dotCom.txt
Note                 : This site has many more cameras than can be checked by the
                       geocoder in 24 hours. Use an API key or split up the work
                       over the course of several days
Other files required by : Geocoding.py, WriteToFile.py located in
this script and where     NetworkCameras/Discovery/Tools
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.trafficcameras.com/
In database (Y/N)    : Y
Date added to Database : July 1, 2016
--------------------------------------------------------------------------------
"""
from selenium import webdriver
from Geocoding import Geocoding
from WriteToFile import WriteToFile
import urllib2
import json
import time

class traffic:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.geo = Geocoding('Google', None) #Insert Google API key instead of None to parse more cameras
        self.write = WriteToFile(True, 'list_Traffic_Cameras_dotCom.txt')
        self.numURLsOverMax = 0

    def getInfo(self):
        self.driver.get('http://www.trafficcameras.com/')
        time.sleep(1)
        list_of_locations = []
        cities = self.driver.find_elements_by_xpath('//ul[@id = "Nav"]/li/a')
        for item in cities:
            location = item.get_attribute("href")
            location = location.split("/")[3]
            jsonlink = "http://www.trafficcameras.com/api/trafficcameras/" + str(location)
            list_of_locations.append(jsonlink)

        self.driver.close()

        for item in list_of_locations[0:]: #Change the list index in this line to specify which cities you want to parse. Check the website to find out what each city's index is
            print "Parsing: ", item
            website = urllib2.urlopen(item).read()
            jsonInfo = json.loads(website)
            for camera in jsonInfo:
                latitude = camera['lat']
                longitude = camera['lon']
                url = "http://www.trafficcameras.com" + camera['link']
                if len(url) > 200: #Many URLs are over the max character limit allowed for the database
                    self.numURLsOverMax += 1
                else:
                    try:
                        self.geo.reverse(latitude, longitude)
                        self.write.writeInfo("USA", self.geo.state, self.geo.city, url, latitude, longitude)
                        time.sleep(0.5)
                    except:
                        print latitude, longitude
                        print url

        print self.numURLsOverMax
                

if __name__ == '__main__':
    cams = traffic()
    cams.getInfo()