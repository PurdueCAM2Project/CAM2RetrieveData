"""
--------------------------------------------------------------------------------
Descriptive Name     : PA.py
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu
Date Written         : June 28, 2016
Description          : Parse cameras on the Pennsylvania 511 site
Command to run script: python PA.py
Usage                : None
Input file format    : N/A
Output               : list_PA.txt
Note                 : This script is incomplete. Navigation is done but the image
                       links return a 403 Forbidden error. Until we are able to get
                       to the images, we cannot parse this website.
Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.511pa.com/CameraListing.aspx
In database (Y/N)    : N
Date added to Database :
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

class PA:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.geo = Geocoding('Google', None)
        self.write = WriteToFile(True, 'list_PA.txt')

    def Navigate(self):
        self.driver.get('http://www.511pa.com/CameraListing.aspx')
        time.sleep(1)
        dropdown1 = self.driver.find_element_by_id('ddlRegions')
        selectRegion = Select(dropdown1)
        numOptions1 = len(dropdown1.find_elements_by_tag_name('option'))
        count1 = 1

        while count1 < numOptions1:
            dropdown1 = self.driver.find_element_by_id('ddlRegions')
            selectRegion = Select(dropdown1)
            selectRegion.select_by_index(count1)
            time.sleep(0.5)
            dropdown2 = self.driver.find_element_by_id('ddlRoutes')
            selectRoute = Select(dropdown2)
            numOptions2 = len(dropdown2.find_elements_by_tag_name('option'))
            count2 = 1

            while count2 < numOptions2:
                dropdown2 = self.driver.find_element_by_id('ddlRoutes')
                selectRoute = Select(dropdown2)
                selectRoute.select_by_index(count2)
                time.sleep(0.5)

                count2 += 1
                
            count1 += 1
        self.driver.close()

if __name__ == '__main__':
    Pennsylvania = PA()
    Pennsylvania.Navigate()