"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for traffic cameras in WeatherBug website from Ohio 
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 5 July 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python OH_Cleveland.py
Usage                : N/A
Input file format    : N/A
Output               : list_Cleveland_Ohio.txt
Note                 : 
Other files required by : It requires Selenium and BeautifulSoup4 to be installed.
                          It requires to have Geocoding.py and CameraData.py in the same directory
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://web.live.weatherbug.com/LiveCameras/2/LiveCameras.aspx?no_cookie_zip=43215&no_cookie_stat=CLMTS&no_cookie_world_stat=&zcode=Z5264&camera_group=1&show_list=1&lid=CENLIST
In database (Y/N)    : Y
Date added to Database : 5 July 2016
--------------------------------------------------------------------------------
"""

# -*- coding: utf-8 -*-

import selenium.webdriver.support.ui as ui
import time
import urllib
import re
import traceback
from CameraData import CameraData
from Geocoding import Geocoding
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class Cleveland:
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://web.live.weatherbug.com/LiveCameras/2/LiveCameras.aspx"
        self.traffic_url = "http://web.live.weatherbug.com/LiveCameras/2/LiveCameras.aspx?no_cookie_zip=43215&no_cookie_stat=CLMTS&no_cookie_world_stat=&zcode=Z5264&camera_group=1&show_list=1&lid=CENLIST"
        self.country = "USA"
        self.state = "OH"

        # open the file to store the list and write the format of the list at the first line
        self.file = open('list_Cleveland_Ohio.txt', 'w')
        self.file.write("city#country#state#snapshot_url#latitude#longitude" + "\n")

        # gps module
        self.gps = Geocoding('Google', None)

    def get_soup(self, url):
        """ Create beautifulSoup object with the given url and return it

            Args:
                url: the URL address of the webpage to be parsed

            Return:
                soup: beautifulSoup object to parse the given URL
        """
        soup_url = urllib.urlopen(url.encode("UTF-8")).read()
        soup = BeautifulSoup(soup_url, "html.parser")

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
            s = str(string)
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

    def get_camera_data(self, cam_element):
        img_src     = self.get_img_src(cam_element)
        description = self.get_description(cam_element)
        city        = self.get_city(cam_element, description)
        state       = self.state
        country     = self.country

        camera_data = CameraData(img_src, country, state, city, description)

        return camera_data

    def get_img_src(self, cam_element):
        return cam_element.find("img").get('src')

    def get_description(self, cam_element):
        description_text = cam_element.find("a").text
        description_text = self.multiple_spaces_into_single_space(description_text)

        return description_text

    def get_city(self, cam_element, description):
        location_name = cam_element.find("a").find("a").text
        city = description[len(location_name):].split(",")[0].strip()

        return city

    def multiple_spaces_into_single_space(self, string):
        return ' '.join(string.split())

    def convert_parsed_data_into_input_format(self, camera_data):
        self.gps.locateCoords(camera_data.get_description(),
                              camera_data.get_city(),
                              camera_data.get_state(),
                              camera_data.get_country())

        input_format = self.gps.city + "#" + self.gps.country + "#" + self.gps.state + "#" + camera_data.get_img_src() + "#" + self.gps.latitude + "#" + self.gps.longitude + "\n"
        input_format = input_format.replace("##", "#")    # if no state exists, state == ""

        return input_format

    def write_to_file(self, input_format):
        self.file.write(input_format)

    def main(self):
        # get parser for the traffic page
        parser_for_traffic_website = self.get_soup(self.traffic_url)

        parser_for_traffic_website_table = parser_for_traffic_website.find("table", {"class" : "wxForecastBox"})
        for cam_element in parser_for_traffic_website_table.findAll("td", {"class" : "wx"}):
            try:
                camera_data     = self.get_camera_data(cam_element)
                input_format    = self.convert_parsed_data_into_input_format(camera_data)

                self.write_to_file(input_format)
            except:
                traceback.print_exc()
                print("ERROR")

if __name__ == '__main__':
    Cleveland = Cleveland()
    Cleveland.main()
