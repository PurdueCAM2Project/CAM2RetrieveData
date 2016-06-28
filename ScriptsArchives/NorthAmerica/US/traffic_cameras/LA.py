""" 
--------------------------------------------------------------------------------
Descriptive Name     : LA.py
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu
Date Written         : June 27, 2016
Description          : Parse traffic cameras on the 511 Louisiana site
Command to run script: python LA.py
Usage                : Must be run on a machine with geopy installed
Input file format    : N/A
Output               : list_LA.txt
Note                 : There are quite a few locations that the geocoder couldn't
                       find coordinates for.
Other files required by : Geocoding.py, WriteToFile.py, Clean.py all are located
this script and where     in NetworkCameras/Discovery/Tools
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://mb.511la.org/la3g/
In database (Y/N)    : Y
Date added to Database : June 27, 2016
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

class LA:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.geo = Geocoding('Google', None)
        self.write = WriteToFile(True, 'list_LA.txt')
        self.fail = 0

    def Navigate(self):
        self.driver.get('http://mb.511la.org/la3g/')
        time.sleep(1)
        self.driver.find_element_by_link_text('Cameras').click()
        self.driver.find_element_by_link_text('See Numbered Highways with Cameras').click()

        routes = self.driver.find_elements_by_class_name('most-popular-route')
        numRoutes = len(routes)
        countRoutes = 0

        while countRoutes < numRoutes:
            routes = self.driver.find_elements_by_class_name('most-popular-route')
            cameraPage = routes[countRoutes].find_element_by_css_selector('a')
            cameraPage.click()
            time.sleep(1)

            camera = self.driver.find_elements_by_css_selector('a')
            numCams = len(camera)
            countCam = 3

            while countCam < numCams-1:
                camera = self.driver.find_elements_by_css_selector('a')
                numCams = len(camera)
                if 'Map' not in camera[countCam].text and 'Cameras' not in camera[countCam].text and 'Menu' not in camera[countCam].text:
                    camera[countCam].click()
                    time.sleep(1)
                    self.getLoc()
                    try:
                        stopCycle = self.driver.find_element_by_id('stopCycling')
                        stopCycle.click()

                        dropdown = self.driver.find_element_by_id('imageSelection')
                        imgSelect = Select(dropdown)
                        numOptions = len(dropdown.find_elements_by_tag_name('option'))
                        countOptions = 0
                        while countOptions < numOptions:
                            imgSelect.select_by_index(countOptions)
                            time.sleep(0.5)
                            self.getInfo(countOptions)
                            countOptions += 1
                    except NoSuchElementException:
                        self.getInfo(0)

                    self.driver.back()
                    time.sleep(1)
                countCam += 1

            self.driver.back()
            time.sleep(1)
            countRoutes += 1

        self.driver.close()

    def getLoc(self):
        title = self.driver.find_elements_by_tag_name('table')[2]
        Location = title.find_elements_by_css_selector('div')
        loc1 = Location[0].text
        loc2 = Location[1].text
        clean1 = Clean(loc1)
        clean2 = Clean(loc2)
        clean1.suite()
        clean2.suite()
        locat1 = clean1.textString.replace(clean2.textString, "") #Remove redundant location info
        try:
            try:
                try:
                    self.geo.locateCoords(locat1 + " " + clean2.textString, "", "Louisiana", "USA")
                    self.fail = 0
                except:
                    self.geo.locateCoords(clean1.textString, "", "Louisiana", "USA")
                    self.fail = 0
            except:
                self.geo.locateCoords(clean2.textString, "", "Louisiana", "USA")
                self.fail = 0
        except:
            self.fail  = 1
            print locat1 + " " + clean2.textString
        
    def getInfo(self, camNumber):
        try:
            imageID = "cam-"+str(camNumber)+"-img"
            image = self.driver.find_element_by_id(imageID)
            url = image.get_attribute('src')
            if self.fail == 0:
                self.write.writeInfo("USA", "LA", self.geo.city, url, self.geo.latitude, self.geo.longitude)
                time.sleep(1)
        except:
            pass

if __name__ == '__main__':
    Louisiana = LA()
    Louisiana.Navigate()