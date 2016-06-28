"""
--------------------------------------------------------------------------------
Descriptive Name     : Oahu_HI
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu
Date Written         : June 28, 2016
Description          : Parse cameras on the goAkamai website for traffic cameras
                       on O'ahu island Hawaii
Command to run script: python Oahu_HI
Usage                : None
Input file format    : N/A
Output               : list_Oahu_HI.txt
Note                 : 
Other files required by : Geocoding.py, Clean.py, WriteToFile.py all located in
this script and where     NetworkCameras/Discovery/Tools
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://goakamai.org/icx/pages/cameras.aspx
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

class Oahu:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.geo = Geocoding('Google', None)
        self.write = WriteToFile(True, 'list_Oahu_HI.txt')

    def Navigate(self):
        self.driver.get('http://goakamai.org/icx/pages/cameras.aspx')
        time.sleep(1)
        dropdown = self.driver.find_element_by_id('tourSelector')
        selectArea = Select(dropdown)
        numOptions = len(dropdown.find_elements_by_tag_name('option'))
        count = 0

        while count < numOptions:
            selectArea.select_by_index(count)
            time.sleep(1)
            self.getInfo()
            time.sleep(1)
            count += 1

        self.driver.close() 

    def getInfo(self):
        cameras = self.driver.find_elements_by_class_name('camera')
        for cam in cameras:
            location = cam.get_attribute('title')
            cleanLocat = Clean(location)
            cleanLocat.suite()
            url = cam.get_attribute('src')

            try:
                self.geo.locateCoords(cleanLocat.textString, "", "HI", "USA")
                self.write.writeInfo("USA", "HI", self.geo.city, url, self.geo.latitude, self.geo.longitude)
            except:
                print cleanLocat.textString
            

if __name__ == '__main__':
    Hawaii = Oahu()
    Hawaii.Navigate()