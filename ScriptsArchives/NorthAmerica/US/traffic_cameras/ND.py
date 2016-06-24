""" 
--------------------------------------------------------------------------------
Descriptive Name     : ND.py
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu
Date Written         : June 15, 2016
Description          : Parse traffic cameras in North Dakota
Command to run script: python ND.py
Usage                : Must be run on a machine with geopy installed
Input file format    : N/A
Output               : list_ND.txt
Note                 : 
Other files required by : Geocoding.py, WriteToFile.py, Clean.py all located in
this script and where     NetworkCameras/Discovery/Tools
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.dot.nd.gov/travel-info-v2/
In database (Y/N)    : Y
Date added to Database : June 16, 2016
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

class ND:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.geo = Geocoding('Google', None)
        self.write = WriteToFile(True, 'list_ND.txt')
        self.fail = 0
        self.url = ''

    def Navigate(self):
        self.driver.get('http://www.dot.nd.gov/travel-info-v2/')
        time.sleep(1)
        camList = self.driver.find_element_by_id('tab_maincontainer_tablist_tab_cameraimages')
        camList.click()
        time.sleep(1)
        cameras = self.driver.find_elements_by_class_name('camera')
        skipFirst = 0
        for cam in cameras:
            if skipFirst == 0:
                skipFirst = 1
            else:
                cam.click()
                time.sleep(1)
                self.getLocation()
                imgGroup = self.driver.find_element_by_css_selector('span.dojoxLightboxGroupText')
                numImages = re.sub(r"\([0-9]+\sof\s","",imgGroup.text)
                numImages = re.sub(r"\)$", "", numImages)
                print numImages
                try:
                    numImages = int(numImages)
                    noImages = 0
                except:
                    noImages = 1
                
                if noImages == 0:
                    countImages = 1
                    while countImages < numImages:
                        self.getURL()
                        if self.fail == 0:
                            self.write.writeInfo("USA", "ND", self.geo.city, self.url, self.geo.latitude, self.geo.longitude)
                        next = self.driver.find_element_by_css_selector('.dijitInline.LightboxNext')
                        next.click()
                        time.sleep(1.5)
                        countImages += 1
                    self.getURL()
                    if self.fail == 0:
                        self.write.writeInfo("USA", "ND", self.geo.city, self.url, self.geo.latitude, self.geo.longitude)
                else:
                    pass

                closeButton = self.driver.find_element_by_css_selector('.dijitInline.LightboxClose')
                closeButton.click()
                time.sleep(1.5)

        self.driver.close()
    
    def getURL(self):
        image = self.driver.find_element_by_css_selector('img.dojoxLightboxImage')
        self.url = image.get_attribute('src')
        self.url = self.url.split('?ts=')[0]
        print self.url

    def getLocation(self):
        location = self.driver.find_element_by_css_selector('.dojoxLightboxText')
        print location.text
        if location.text == "" or "Image not found." in location.text:
            self.fail = 1
        else:
            hwy = location.find_element_by_tag_name('strong').text
            city = location.find_element_by_tag_name('em').text
            location = location.text
            location = location.replace(hwy, "")
            location = location.replace(city, "")
            location = location.split(' - ')[0]
            city = city.split(' Area')[0]
            cleanHwy = Clean(hwy)
            cleanCity = Clean(city)
            cleanLoc = Clean(location)
            cleanHwy.suite()
            cleanCity.suite()
            cleanLoc.suite()
            hwy = cleanHwy.textString
            city = cleanCity.textString
            location = cleanLoc.textString

            self.fail = 0
            try:
                try:
                    self.geo.locateCoords(hwy + ',' + location, "", "ND", "USA")
                except:
                    self.geo.locateCoods(hwy, city, "ND", "USA")
            except:
                self.fail = 1
        
        

if __name__ == '__main__':
    NDakota = ND()
    NDakota.Navigate()