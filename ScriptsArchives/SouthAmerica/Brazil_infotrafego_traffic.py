"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for cameras in http://infotrafego.pbh.gov.br
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 12 July 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python Brazil_infotrafego_traffic.py
Usage                : N/A
Input file format    : N/A
Output               : list_infotrafego_traffic.txt
Note                 : 
Other files required by : It requires Selenium and BeautifulSoup4 to be installed.
                          It requires Geocoding.py from the Tools directory
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://infotrafego.pbh.gov.br/info_trafego_cameras.html
In database (Y/N)    : Y
Date added to Database : 12 July 2016
--------------------------------------------------------------------------------
"""

# -*- coding: utf-8 -*-

import selenium.webdriver.support.ui as ui
import time
import urllib
import urllib2
import re
import traceback
import sys  
from Geocoding import Geocoding
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class WorldWebcam:
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://infotrafego.pbh.gov.br"
        self.traffic_url = "http://infotrafego.pbh.gov.br/info_trafego_cameras.html"
        self.country = "BR"
        self.state = ""

        # open the file to store the list and write the format of the list at the first line
        self.list_file = open("list_infotrafego_traffic.txt", "w")
        self.list_file.write("city#country#snapshot_url#latitude#longitude" + "\n")

        # get the webdriver of the opened firefox and open the url
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference("javascript.enabled", False)

        self.driver = webdriver.Firefox(firefox_profile=firefox_profile)

        # gps module
        self.gps = Geocoding('Google', None)

        reload(sys)  
        sys.setdefaultencoding('utf8')

    def get_soup(self, url):
        """ Create beautifulSoup object with the given url and return it

            Args:
                url: the URL address of the webpage to be parsed

            Return:
                soup: beautifulSoup object to parse the given URL
        """

        opener = urllib2.build_opener() 
        opener.addheaders = [('User-agent', 'Mozilla/5.0')] # Add header information
        response = opener.open(url)
        page = response.read()
        soup = BeautifulSoup(page, "html.parser")           # Create soup

        return soup

    def get_token(self, string, front, end):
        """ Extract the substring between <front> and <end> string
            
            The string contains string or html element
            This function extract the substring between <front> and <end> string
            If front string is empty, return string from the first character to the split of end string
            If end string is empty, return string from the end character to the split of the front string

            Args:
                string: string or html element
                front: string at the left of the wanted substring
                end: string at the right of the wanted substring

            Return:
                token: the string between <front> and <end> string OR if DNE, return empty string
        """
        try:
            s = str(string.encode('UTF-8'))
            if front == "":
                token = s.split(end)[0]
            elif end == "":
                token = s.split(front)[1]
            else:
                front_split = s.split(front)[1]
                token = front_split.split(end)[0]
        except:
            print("get_token error")
            traceback.print_exc()
            token = ""

        return token

    def write_to_file(self, country, state, city, img_src, descrip):
        """ Writes the extracted data into the list files
            
            It locates the gps with the Geocoding module.
            If success, it writes the result into the files.
            Since the format of US file and other countries' file, check the country name before writing.

            Args:
                country:    The 2-letter country code of the given camera
                state:      The 2-letter state code of the given camera
                city:       The city name of the given camera
                img_src:    The image URL of the given camera
                descrip:    The description of the given camera
        """
        self.gps.locateCoords(descrip, city, state, country)
        result = self.gps.city.encode("UTF-8") + "#"
        result = result + self.gps.country + "#"
        result = result + self.gps.state + "#"
        result = result + img_src + "#"
        result = result + self.gps.latitude + "#" + self.gps.longitude + "\n"
        #result = self.gps.city.encode("UTF-8") + "#" + self.gps.country + "#" + self.gps.state + "#" + img_src + "#" + self.gps.latitude + "#" + self.gps.longitude + "\n"
        result = result.replace("##", "#")

        self.list_file.write(result)

    def get_city(self, description):
        if ("/c" in description):
            city = self.get_token(description, "/c", "").strip()
        else:
            city = description

        return city

    def parse_cam(self, cam):
        img_src     = cam.get_attribute('src')
        description = self.get_token(cam.get_attribute('title'), "-", "").strip()
        city        = self.get_city(description)

        print(city, img_src, description)

        self.write_to_file(self.country, self.state, city, img_src, description)

    def main(self):
        self.driver.get(self.traffic_url)

        for cam in self.driver.find_elements_by_class_name("camThumb"):
            try:
                self.parse_cam(cam)
            except:
                traceback.print_exc()
                print("Error")

if __name__ == '__main__':
    WorldWebcam = WorldWebcam()
    WorldWebcam.main()
