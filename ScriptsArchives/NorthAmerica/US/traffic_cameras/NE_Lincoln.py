"""
--------------------------------------------------------------------------------
Descriptive Name     : NE_Lincoln.py
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu
Date Written         : June 29, 2016
Description          : Parse cameras on the City of Lincoln Nebraska site
Command to run script: python NE_Lincoln
Usage                : None
Input file format    : N/A
Output               : list_NE_Lincoln.txt
Note                 : 
Other files required by : Geocoding.py, WriteToFile.py located in
this script and where     NetworkCameras/Discovery/Tools
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.lincoln.ne.gov/asp/city/pwcam.asp?ID=2
In database (Y/N)    : Y
Date added to Database : June 29, 2016
--------------------------------------------------------------------------------
"""

from selenium import webdriver
from Geocoding import Geocoding
from WriteToFile import WriteToFile
import time

class NE:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.geo = Geocoding('Google', None)
        self.write = WriteToFile(True, 'list_NE_Lincoln.txt')

    def Navigate(self):
        self.driver.get('http://www.lincoln.ne.gov/asp/city/pwcam.asp?ID=2')
        time.sleep(1)
        camlist = self.driver.find_element_by_id('camlist')
        cameras = camlist.find_elements_by_tag_name('a')
        numCameras = len(cameras)
        count = 0

        while count <= numCameras:
            camlist = self.driver.find_element_by_id('camlist')
            cameras = camlist.find_elements_by_tag_name('a')
            self.getInfo()
            time.sleep(1)
            if count < numCameras:
                cameras[count].click()
                time.sleep(1)
            count += 1

        self.driver.close()

    def getInfo(self):
        url = self.driver.find_element_by_xpath('//table/tbody/tr/td/img').get_attribute('src')
        location = self.driver.find_element_by_tag_name('h2').text
        try:
            self.geo.locateCoords(location, "Lincoln", "NE", "USA")
            self.write.writeInfo("USA", "NE", "Lincoln", url, self.geo.latitude, self.geo.longitude)
        except:
            print location


if __name__ == '__main__':
    Nebraska = NE()
    Nebraska.Navigate()