"""
--------------------------------------------------------------------------------
Descriptive Name     : FI_kelikamerat.py
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 20 July 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python FI_kelikamerat.py
Usage                : N/A
Input file format    : N/A
Output               : list_Finland_kelikmerat.txt
Note                 : 
Other files required by : Geocoding.py, CameraData.py, and Useful.py in NetworkCameras/Discovery/Tools
this script and where     It requires Selenium and BeautifulSoup4 to be installed.
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.kelikamerat.info/kelikamerat
In database (Y/N)    : Y
Date added to Database : 20 July 2016
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
        self.home_url       = "http://www.kelikamerat.info"
        self.traffic_url    = "http://www.kelikamerat.info/kelikamerat/"
        self.country        = "FI"
        self.state          = ""

        # open the file to store the list and write the format of the list at the first line
        self.list_file = open('list_Finland_kelikmerat.txt', 'w')
        if self.country == "USA":
            self.list_file.write("city#country#state#snapshot_url#latitude#longitude" + "\n")
        else:
            self.list_file.write("city#country#snapshot_url#latitude#longitude" + "\n")

        # gps module
        self.gps = Geocoding('Google', None)

    def get_camera_data(self, cam, municipality):
        parser_for_cam_webpage = self.get_parser_with_soup(self.home_url + cam.get('href'))

        img_src     = self.get_img_src(parser_for_cam_webpage)
        description = self.get_description(cam)
        city        = municipality
        state       = self.state
        country     = self.country

        print(img_src, description, city)
        
        camera_data = CameraData(img_src, country, state, city, description)

        return camera_data

    def get_img_src(self, parser_for_cam_webpage):
        return parser_for_cam_webpage.find("img", {"id" : "gallery"}).get('src')

    def get_description(self, cam):
        description = cam.find("div").text.strip()
        description = self.take_first_two_tokens_off(description)
        description = self.take_last_token_off(description)

        return description

    def take_first_two_tokens_off(self, description):
        return' '.join(description.split(' ')[2:])

    def take_last_token_off(self, description):
        return ' '.join(description.split(' ')[:-1])

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
        # get BeautifulSoup4 parser for traffic_url
        parser_for_traffic_webpage = self.get_parser_with_soup(self.traffic_url)

        # loop through the list of the regions of Finland
        for region in parser_for_traffic_webpage.findAll("option"):
            parser_for_region_webpage = self.get_parser_with_soup(self.traffic_url + region.get('value'))
            municipalities = parser_for_region_webpage.find("ul", {"class" : "cities"})

            # loop through the list of municipalities of the given region
            for municipality in municipalities.findAll("a"):

                # if the municipality name is equal to "Kaikki kaupungit", skip it
                if "Kaikki kaupungit" in municipality:
                    continue

                municipality = municipality.text
                parser_for_municipality_webpage = self.get_parser_with_soup(self.home_url + municipality.get('href'))

                # loop through the list of roads of the given municipality
                for road in parser_for_municipality_webpage.findAll("div", {"class" : "road-camera"}):
                    parser_for_road_webpage = self.get_parser_with_soup(self.home_url + road.find("a").get('href'))
                    cameras = parser_for_road_webpage.find("div", {"class" : "middle-bar"})

                    # loop through the list of cameras of the given road
                    for cam in cameras.findAll("a"):
                        try:
                            camera_data     = self.get_camera_data(cam, municipality)
                            input_format    = self.convert_parsed_data_into_input_format(camera_data)

                            self.write_to_file(input_format)
                        except:
                            traceback.print_exc()

if __name__ == '__main__':
    Ireland = Ireland()
    Ireland.main()
