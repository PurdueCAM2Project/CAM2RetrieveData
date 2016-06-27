"""
--------------------------------------------------------------------------------
Descriptive Name     : NM.py
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu
Date Written         : June 14, 2016
Description          : Parse traffic cameras in New Mexico
Command to run script: python NM.py
Usage                : Must be run on a machine with geopy installed
Input file format    : N/A
Output               : list_NM.txt
Note                 : 
Other files required by : Geocoding.py, WriteToFile.py, Clean.py
this script and where     all located in NetworkCameras/Discovery/Tools
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://nmroads.com/mapIndex_04211601.html#
In database (Y/N)    : Y
Date added to Database : June 14, 2016
--------------------------------------------------------------------------------
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from Geocoding import Geocoding
from WriteToFile import WriteToFile
from Clean import Clean
import urllib
import time

class NM:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.geo = Geocoding('Google', None)
        self.write = WriteToFile(True, 'list_NM.txt')

    def Navigate(self):
        self.driver.get('http://nmroads.com/mapIndex_04211601.html#')
        self.driver.find_element_by_id('cameraButton').click()
        self.driver.find_element_by_id('cameraListButton').click()
        
        cameraList= self.driver.find_element_by_id('cameraListList')
        cameras = cameraList.find_elements_by_tag_name('li')

        for cam in cameras:
            cam.click()
            time.sleep(0.2)
            self.getInfo()
        self.driver.close()
        
    def getInfo(self):
        img = self.driver.find_element_by_id('cameraListImage')
        url = img.find_element_by_tag_name('img').get_attribute('src')
        location = img.text.replace("\nCLOSE", "")
        cleanLocat = Clean(location)
        cleanLocat.suite()
        
        try:
            self.geo.locateCoords(cleanLocat.textString, "", "NM", "USA")
            self.write.writeInfo("USA", "NM", self.geo.city, url,  self.geo.latitude, self.geo.longitude)
        except Exception as e:
            print e
            print cleanLocat.textString

if __name__ == "__main__":
    NewMexico = NM()
    NewMexico.Navigate()