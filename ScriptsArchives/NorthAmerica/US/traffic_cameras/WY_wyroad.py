"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for traffic cameras in Wyoming travel service website
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 15 June 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python WY_wyroad.py
Usage                : N/A
Input file format    : N/A
Output               : list_WY_wyroad.txt
Note                 : 
Other files required by : Geocoding.py and Useful.py from in NetworkCameras/Discovery/Tools
this script and where     It requires Selenium and BeautifulSoup4 to be installed
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.wyoroad.info/highway/webcameras/webcameras.html
In database (Y/N)    : Y
Date added to Database : 15 June 2016
--------------------------------------------------------------------------------
"""

# -*- coding: utf-8 -*-

import selenium.webdriver.support.ui as ui
import time
import re
import traceback
from CameraData import CameraData
from Geocoding import Geocoding
from Useful import Useful
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class Wyoming(Useful):
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url       = "http://www.wyoroad.info"
        self.traffic_url    = "http://www.wyoroad.info/highway/webcameras/webcameras.html"
        self.country        = "USA"
        self.state          = "WY"

        # open the file to store the list and write the format of the list at the first line
        self.list_file = open('list_WY_wyroad.txt', 'w')
        self.list_file.write("city#country#state#snapshot_url#latitude#longitude" + "\n")

        # gps module
        self.gps = Geocoding('Google', None)

    def get_camera_data(self, cam):
        """ Get the description, image url, and city name of the given camera

            The cam is a BeautifulSoup element that contains the infomation about one camera in <a href=""> tag
            This function extracts the description, image url, and city name of the given data

            Args:
                cam: BeautifulSoup element that contains the infomation about one camera in <a href=""> tag

            Return:
                camera_data: CameraData instance that contains the parsed information about a camera
        """
        # create parser for a camera
        soup_cam = self.get_parser_with_soup(self.home_url + cam.get('href'))

        # create img_src, city, descrip for Geocoding
        img_src     = self.get_img_src(soup_cam)
        description = ""
        city        = cam.text
        state       = self.state
        country     = self.country

        camera_data = CameraData(img_src, country, state, city, description)

        return camera_data

    def get_img_src(self, soup_cam):
        img_src = soup_cam.find("img", {"class" : "photolarge"}).get('src')

        # complete the img_src
        if img_src[0] == "/":
            img_src = self.home_url + img_src
        
        return img_src

    def main(self):
        # get parser for the traffic page
        soup_traffic = Useful.get_parser_with_soup(self, self.traffic_url)

        # loop through each link
        link_table = soup_traffic.find("table", {"class" : "table"})
        for a_tag in link_table.findAll("a"):

            # create parser for each link
            soup_link = Useful.get_parser_with_soup(self, self.home_url + a_tag.get('href'))
            cam_table = soup_link.find("table", {"class" : "table"})

            # loop through each camera in a link
            for cam in cam_table.findAll("a"):
                try:
                    camera_data     = self.get_camera_data(cam)
                    input_format    = self.convert_parsed_data_into_input_format(camera_data)

                    self.write_to_file(input_format)
                except:
                    traceback.print_exc()

if __name__ == '__main__':
    Wyoming = Wyoming()
    Wyoming.main()
