"""
--------------------------------------------------------------------------------
Descriptive Name     : NewZealand.py
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu
Date Written         : June 29, 2016
Description          : Parse cameras on the New Zealand Transit Agency site
Command to run script: python NewZealand.py
Usage                : None
Input file format    : N/A
Output               : list_NewZealand.txt
Note                 : Many locations cannot be found by the geocoding API
Other files required by : Geocoding.py, Clean.py, WriteToFile.py all located in
this script and where     NetworkCameras/Discovery/Tools
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.nzta.govt.nz/traffic-and-travel-information/traffic-cameras/
In database (Y/N)    : Y
Date added to Database : June 29, 2016
--------------------------------------------------------------------------------
"""

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from Geocoding import Geocoding
from WriteToFile import WriteToFile
from Clean import Clean
import urllib
import time
import re

class NZ:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.geo = Geocoding('Google', None)
        self.write = WriteToFile(False, 'list_NewZealand.txt')

    def Navigate(self):
        self.driver.get('http://www.nzta.govt.nz/traffic-and-travel-information/traffic-cameras/')
        time.sleep(1)
        region = self.driver.find_elements_by_css_selector('i.i-arrow-r.i--dark-blue.small')
        numRegions = len(region)
        count = 0

        while count < numRegions:
            region = self.driver.find_elements_by_css_selector('i.i-arrow-r.i--dark-blue.small')
            region[count].click()
            time.sleep(1)
            cameras = self.driver.find_elements_by_class_name("traffic-cameras__thumbnail")
            numCams = len(cameras)
            countCams = 0
            while countCams < numCams:
                cameras = self.driver.find_elements_by_class_name("traffic-cameras__thumbnail")
                cameras[countCams].click()
                time.sleep(1)
                self.getInfo()
                time.sleep(1)
                self.driver.back()
                time.sleep(1)
                countCams += 1
            self.driver.back()
            time.sleep(1)
            count += 1
            

        self.driver.close()

    def getInfo(self):
        url = self.driver.find_element_by_css_selector("img.js__refresh-image.traffic-cameras__full").get_attribute("src")
        location = self.driver.find_element_by_css_selector("span.traffic-cameras__details--description").text
        location = location.split("looking")[0]
        location = location.split("along")
        if len(location) == 2:
            location = location[1]
        else:
            location = ' '.join(location)
        cleanLocat = Clean(location)
        cleanLocat.suite()
        
        try:
            self.geo.locateCoords(cleanLocat.textString, "", "", "NZ")
            self.write.writeInfo("NZ", "", self.geo.city, url, self.geo.latitude, self.geo.longitude)
        except:
            print cleanLocat.textString

if __name__ == '__main__':
    NewZealand = NZ()
    NewZealand.Navigate()