""" 
--------------------------------------------------------------------------------
Descriptive Name     : WA_SeattleDOT
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu
Date Written         : June 17, 2016
Description          : parse traffic cameras on the Seattle, WA DOT site
Command to run script: python WA_SeattleDOT.py
Usage                : Must be run on a machine with geopy installed
Input file format    : N/A
Output               : list_WA_SeattleDOT.txt
Note                 : 
Other files required by : Geocoding.py, WriteToFile.py located in 
this script and where     NetworkCameras/Discovery/Tools
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.seattle.gov/trafficcams/
In database (Y/N)    : Y
Date added to Database : June 17, 2016
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

class SEA:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.geo = Geocoding('Google', None)
        self.write = WriteToFile(True, 'list_WA_SeattleDOT.txt')

    def getInfo(self):
        self.driver.get('http://www.seattle.gov/trafficcams/')
        time.sleep(1)

        cameras = self.driver.find_elements_by_xpath('//div/table/tbody/tr/td/div/a')

        for cam in cameras:
            link = cam.get_attribute("href")
            location = cam.text
            
            try:
                self.geo.locateCoords(location.encode("utf-8"), "Seattle", "WA", "USA")
                self.write.writeInfo("USA", "WA", "Seattle", link, self.geo.latitude, self.geo.longitude)
            except:
                print location.encode("utf-8")
                print link
    

        self.driver.quit()
        
if __name__ == '__main__':
    Seattle = SEA()
    Seattle.getInfo()
