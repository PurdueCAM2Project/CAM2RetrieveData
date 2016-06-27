"""
--------------------------------------------------------------------------------
Descriptive Name     : MO.py
Author               : Thomas Norling  								      
Contact Info         : tnorling@purdue.edu
Date Written         : June 16, 2016
Description          : Parse traffic cameras on the Missouri dot site
Command to run script: python MO.py
Usage                : Must be run on a machine with geopy installed
Input file format    : N/A
Output               : list_MO.txt
Note                 : 
Other files required by : Geocoding.py, WriteToFile.py, Clean.py all located in
this script and where     NetworkCameras/Discovery/Toolslocated
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.modot.org/mobileweb/trafficcam.html
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

class MO:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.geo = Geocoding('Google', None)
        self.write = WriteToFile(True, 'list_MO.txt')

    def Navigate(self):
        self.driver.get('http://www.modot.org/mobileweb/trafficcam.html')
        time.sleep(1)
        hwyList = self.driver.find_element_by_css_selector('.ui-listview')
        hwyLinks = self.driver.find_elements_by_css_selector('.ui-link-inherit')
        numHwys = len(hwyLinks)
        countHwys = 0

        while countHwys < numHwys:
            hwyLinks = self.driver.find_elements_by_css_selector('.ui-link-inherit')
            hwyLinks[countHwys].click()
            time.sleep(1)
            self.getInfo()
            self.driver.back()
            time.sleep(1)
            countHwys += 1
        
        self.driver.close()

    def getInfo(self):
        locations = self.driver.find_elements_by_css_selector('div.ui-content')[2:]

        for loc in locations:
            url = loc.find_element_by_tag_name('img').get_attribute('src')
            loc = loc.text.split(',')
            hwy = loc[0]
            city = loc[-1]
            city = city.replace("near", "")
            city = city.strip()
            
            try:
                self.geo.locateCoords(str(hwy), str(city), "MO", "USA")
                self.write.writeInfo("USA", "MO", self.geo.city, url, self.geo.latitude, self.geo.longitude)
            except Exception as e:
                print e
                print hwy, city

if __name__ == '__main__':
    Missouri = MO()
    Missouri.Navigate()