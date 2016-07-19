"""
--------------------------------------------------------------------------------
Descriptive Name     : IE_dublincity.py
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 19 July 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python IE_dublincity.py
Usage                : N/A
Input file format    : N/A
Output               : list_Ireland_dublincity.txt
Note                 : 
Other files required by : Geocoding.py, CameraData.py, and Useful.py in NetworkCameras/Discovery/Tools
this script and where     It requires Selenium and BeautifulSoup4 to be installed.
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : https://www.dublincity.ie/dublintraffic/
In database (Y/N)    : Y
Date added to Database : 19 July 2016
--------------------------------------------------------------------------------
"""

# -*- coding: utf-8 -*-

import selenium.webdriver.support.ui as ui
import time
import re
import traceback
import pycountry
from CameraData import CameraData
from Useful import Useful
from Geocoding import Geocoding
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class Ireland(Useful):
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url       = "https://www.dublincity.ie"
        self.traffic_url    = "https://www.dublincity.ie/dublintraffic/"
        self.country        = "IE"
        self.state          = ""

        # open the file to store the list and write the format of the list at the first line
        self.list_file = open('list_Ireland_dublincity.txt', 'w')
        self.list_file.write("city#country#snapshot_url#latitude#longitude" + "\n")

        # gps module
        self.gps = Geocoding('Google', None)
    
    def get_camera_data(self, cam):
        img_tag = cam.find("img")

        img_src     = img_tag.get("src")
        description = img_tag.get("alt")
        city        = self.get_city(description)
        state       = self.state
        country     = self.country

        camera_data = CameraData(img_src, country, state, city, description)

        return camera_data

    def get_city(self, description):
        city = description
        if "-" in city:
            city = Useful.get_token_between(self, city, "-", "")
        if "/" in city:
            city = Useful.get_token_between(self, city, "/", "")

        return city.strip()

    def convert_parsed_data_into_input_format(self, camera_data):
        self.gps.locateCoords(camera_data.get_description(),
                              camera_data.get_city(),
                              camera_data.get_state(),
                              camera_data.get_country())

        input_format = self.gps.city + "#" + self.gps.country + "#" + self.gps.state + "#" + camera_data.get_img_src() + "#" + self.gps.latitude + "#" + self.gps.longitude + "\n"
        input_format = input_format.replace("##", "#")    # if no state exists, state == ""

        return input_format

    def write_to_file(self, input_format):
        self.list_file.write(input_format)

    def main(self):
        # loop through each camera
        parser_for_traffic_webpage = Useful.get_parser_with_soup(self, self.traffic_url)
        for cam in parser_for_traffic_webpage.findAll("span", {"class" : "detContent"}):
            try:
                camera_data     = self.get_camera_data(cam)
                input_format    = self.convert_parsed_data_into_input_format(camera_data)

                self.write_to_file(input_format)
            except:
                traceback.print_exc()

if __name__ == '__main__':
    Ireland = Ireland()
    Ireland.main()
