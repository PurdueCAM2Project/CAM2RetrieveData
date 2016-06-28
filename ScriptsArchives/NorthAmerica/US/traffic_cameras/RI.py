""" 
--------------------------------------------------------------------------------
Descriptive Name     : RI.py
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu
Date Written         : June 28, 2016
Description          : Parse cameras on the RI DOT website
Command to run script: python RI.py
Usage                : None
Input file format    : N/A
Output               : list_RI.txt
Note                 : 
Other files required by : Geocoding.py, Clean.py, WriteToFile.py all located in
this script and where     NetworkCameras/Discovery/Tools
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.dot.ri.gov/travel/cameras_metro.php
In database (Y/N)    : Y 
Date added to Database : June 28, 2016
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

class RI:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.geo = Geocoding('Google', None)
        self.write = WriteToFile(True, 'list_RI.txt')
    
    def Navigate(self):
        self.driver.get('http://www.dot.ri.gov/travel/cameras_metro.php')
        time.sleep(1)
        dropdown = self.driver.find_element_by_id('customDropdown')
        selectArea = Select(dropdown)
        numOptions = len(dropdown.find_elements_by_tag_name('option'))
        count = 1

        while count < numOptions:
            dropdown = self.driver.find_element_by_id('customDropdown')
            selectArea = Select(dropdown)
            selectArea.select_by_index(count)
            time.sleep(0.5)
            tabs = self.driver.find_elements_by_xpath('//div[@class = "section-container auto"]/section/p[@class = "title"]/a')
            for tab in tabs:
                tab.click()
                time.sleep(0.5)
                self.getInfo()
            count += 1

        self.driver.close()

    def getInfo(self):
        cams = self.driver.find_elements_by_xpath('//section[@class = "active"]/div[@class = "content"]/ul[@class = "small-block-grid-1 medium-block-grid-2 large-block-grid-3 gray-boxes"]/li/a/img')
        for cam in cams:
            url = cam.get_attribute('src')
            locat = cam.get_attribute('alt')
            locat = locat.replace("Camera at", "")
            cleanLocat = Clean(locat)
            cleanLocat.suite()
            try:
                self.geo.locateCoords(cleanLocat.textString, "", "RI", "USA")
                time.sleep(1)
                self.write.writeInfo("USA", "RI", self.geo.city, url, self.geo.latitude, self.geo.longitude)
            except:
                print cleanLocat.textString

if __name__ == '__main__':
    RhodeIsland = RI()
    RhodeIsland.Navigate()