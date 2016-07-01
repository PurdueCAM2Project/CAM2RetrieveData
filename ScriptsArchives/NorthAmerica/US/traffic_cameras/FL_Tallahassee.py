"""
--------------------------------------------------------------------------------
Descriptive Name     : FL_Tallahassee.py
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu
Date Written         : June 30, 2016
Description          : Parses cameras in the City of Tallahassee
Command to run script: python FL_Tallahassee.py
Usage                : None
Input file format    : N/A
Output               : list_FL_Tallahassee.txt
Note                 : 
Other files required by : Geocoding.py, WriteToFile.py located in 
this script and where     NetworkCameras/Discovery/Tools
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : https://www.talgov.com/you/you-traffic-cameras.aspx
In database (Y/N)    : Y
Date added to Database : June 30, 2016
--------------------------------------------------------------------------------
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from Geocoding import Geocoding
from WriteToFile import WriteToFile
import time

class FL:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.geo = Geocoding('Google', None)
        self.write = WriteToFile(True, 'list_FL_Tallahassee.txt')
        self.urlList = []

    def Navigate(self):
        self.driver.get('https://www.talgov.com/you/you-traffic-cameras.aspx')
        time.sleep(1)
        camPage = self.driver.find_elements_by_xpath('//table/tbody/tr/td/a')
        numPages = len(camPage)
        count = 0

        while count < numPages:
            camPage = self.driver.find_elements_by_xpath('//table/tbody/tr/td/a')
            try:
                camPage[count].click()
                time.sleep(0.5)
                self.getInfo()
                self.driver.back()
                time.sleep(0.5)
            except:
                pass
            count += 1

        self.driver.close()

    def getInfo(self):
        info = self.driver.find_elements_by_xpath('//div[@id = "center_column_threecol"]/p')
        url = info[0].find_element_by_tag_name('img').get_attribute('src')
        if url in self.urlList:
            pass
        else:
            self.urlList.append(url)
            location = info[1].text
            location = location.split('ImgDateTime')[0]
            location = location.replace("Intersection: ", "")
            location = location.replace("\n", "")
            location = location.replace("@", "and")
            try:
                self.geo.locateCoords(location, "Tallahassee", "FL", "USA")
                self.write.writeInfo("USA", "FL", "Tallahassee", url, self.geo.latitude, self.geo.longitude)
            except:
                print location
        

if __name__ == '__main__':
    Florida = FL()
    Florida.Navigate()
