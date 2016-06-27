""" 
--------------------------------------------------------------------------------
Descriptive Name     : UT.py
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu
Date Written         : June 15, 2016
Description          : Parse traffic cameras on the Utah DOT website
Command to run script: python UT.py
Usage                : Must be run on machine with geopy installed
Input file format    : N/A
Output               : list_UT.txt
Note                 : It takes a while to parse all the cameras and it's not
                       perfect. Some cameras are gifs with multiple images
                       which we can't use. Others can't use the location
                       information given to get coordinates. Nonetheless,
                       many of the cameras parse successfully.
Other files required by : Geocoding.py, WriteToFile.py, Clean.py all located
this script and where     in NetworkCameras/Discovery/Tools
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.utahcommuterlink.com/
In database (Y/N)    : Y
Date added to Database : June 15, 2016
--------------------------------------------------------------------------------
"""
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from Geocoding import Geocoding
from WriteToFile import WriteToFile
from Clean import Clean
import urllib
import time
import re

class UT:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.geo = Geocoding('Google', None)
        self.write = WriteToFile(True, 'list_UT.txt')

    def Navigate(self):
        self.driver.get('http://www.utahcommuterlink.com/')
        time.sleep(1)
        overallAreaDropdown = Select(self.driver.find_element_by_id('ddlMapAreas'))
        overallAreaDropdown.select_by_visible_text('Statewide')
        time.sleep(1)
        cameraDropdown = self.driver.find_element_by_id('ddlCameras')
        cameraList = cameraDropdown.find_elements_by_tag_name('option')
        numCams = len(cameraList)

        cameras = Select(cameraDropdown)
        countCam = 0
        while countCam < numCams:
            cameras.select_by_index(countCam)
            self.getInfo(cameraList[countCam])
            countCam += 1

        self.driver.close()

    def getInfo(self, camera):
        location = camera.text
        location = re.sub(r"Local", "", location)
        location = re.sub(r"RWIS", "", location)
        location = re.sub(r"SR[0-9]+", "", location)
        location = re.sub(r"US[0-9]+", "", location)
        cleanLocation = Clean(location)
        cleanLocation.suite()
        cleanLocation.textString = re.sub(r"\s[A-Z]{2,3}$", "", cleanLocation.textString)
        cleanLocation.textString = re.sub(r"\s[A-Z]{3}\s", " ", cleanLocation.textString)
        cleanLocation.textString = re.sub(r"\sand$", "", cleanLocation.textString)
        cleanLocation.textString = re.sub(r"^and\s", "", cleanLocation.textString)
        
        url = camera.get_attribute('value')
        url = url.split("||")[0]
        
        try:
            self.geo.locateCoords(cleanLocation.textString, "", "UT", "USA")
            self.write.writeInfo("USA", "UT", self.geo.city, url, self.geo.latitude, self.geo.longitude)
        except Exception as e:
            print e
            print cleanLocation.textString

if __name__ == '__main__':
    Utah = UT()
    Utah.Navigate()