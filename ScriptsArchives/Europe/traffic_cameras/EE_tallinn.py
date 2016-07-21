"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for traffic cameras in tallinn, Estonia
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 21 July 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python EE_tallinn.py
Usage                : N/A
Input file format    : N/A
Output               : list_Estonia_tallinn.txt
Note                 : 
Other files required by : Geocoding.py, CameraData.py, and Useful.py in NetworkCameras/Discovery/Tools
this script and where     It requires Selenium and BeautifulSoup4 to be installed
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://ristmikud.tallinn.ee/cams.php
In database (Y/N)    : Y
Date added to Database : 21 July 2016
--------------------------------------------------------------------------------
"""

# -*- coding: utf-8 -*-

import selenium.webdriver.support.ui as ui
import time
import re
import traceback
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

class Cleveland(Useful):
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://ristmikud.tallinn.ee"
        self.traffic_url = "http://ristmikud.tallinn.ee/cams.php/"
        self.country = "EE"
        self.state = ""

        # open the file to store the list and write the format of the list at the first line
        self.list_file = open('list_Estonia_tallinn.txt', 'w')
        if self.country == "USA":
            self.list_file.write("city#country#state#snapshot_url#latitude#longitude" + "\n")
        else:
            self.list_file.write("city#country#snapshot_url#latitude#longitude" + "\n")

        # gps module
        self.gps = Geocoding('Google', None)

    def get_camera_data(self, cam_element):
        img_src     = self.get_img_src(cam_element)
        description = self.get_description(cam_element)
        city        = "tallinn"
        state       = self.state
        country     = self.country

        camera_data = CameraData(img_src, country, state, city, description)

        return camera_data

    def get_img_src(self, cam_element):
        return self.home_url + cam_element.find("img").get('src')

    def get_description(self, cam_element):
        h3_tag      = cam_element.find("h3")
        a_tag       = h3_tag.find("a")

        description = a_tag.text.strip()

        return description

    def main(self):
        parser_for_traffic_website = self.get_parser_with_soup(self.traffic_url)

        for cam_element in parser_for_traffic_website.findAll("article", {"class" : "box"}):
            try:
                camera_data     = self.get_camera_data(cam_element)
                input_format    = self.convert_parsed_data_into_input_format(camera_data)

                self.write_to_file(input_format)
            except:
                traceback.print_exc()

if __name__ == '__main__':
    Cleveland = Cleveland()
    Cleveland.main()
