"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for traffic cameras in theweathernetwork website from Canada
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 21 July 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python Weather_Network.py
Usage                : N/A
Input file format    : N/A
Output               : list_Canada_weatherNetwork.txt
Note                 : It goes to the webpage that has json data about the cameras.
                       It extracts the json data into a string and parses the string with json module.
Other files required by : Useful.py in NetworkCameras/Discovery/Tools
this script and where     It requires Selenium to be installed
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : https://www.theweathernetwork.com
In database (Y/N)    : Y
Date added to Database : 21 July 2016
--------------------------------------------------------------------------------
"""

# -*- coding: utf-8 -*-

import selenium.webdriver.support.ui as ui
import time
import re
import traceback
import json
from Useful import Useful
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException

class WeatherNetwork(Useful):
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url   = "https://www.theweathernetwork.com"
        self.json_url   = "https://www.theweathernetwork.com/api/maps/trafficcameras/9/43.84598317236631/-80.71453475531251/43.048384299427234/-78.72600936468751"
        self.country    = "CA"
        self.state      = ""

        # open the file to store the list and write the format of the list at the first line
        self.list_file = open('list_Canada_weatherNetwork.txt', 'w')
        self.list_file.write("city#country#snapshot_url#latitude#longitude" + "\n")

        # open the browser
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference("javascript.enabled", False)

        self.driver = webdriver.Firefox(firefox_profile=firefox_profile)

    def get_camera_data_in_input_format(self, camera_data_in_json):
        img_src     = camera_data_in_json['img']
        city        = camera_data_in_json['city']
        latitude    = camera_data_in_json['lat']
        longitude   = camera_data_in_json['lng']
        country     = self.country
        state       = self.state

        input_format = city + "#" + country + "#" + state + "#" + img_src + "#" + str(latitude) + "#" + str(longitude) + "\n"
        input_format = input_format.replace("##", "#")    # if no state exists, state == ""

        return input_format 

    def get_json_data_into_string(self):
        self.driver.get(self.json_url)
        json_string = self.driver.find_element_by_tag_name("body").text
        self.driver.close()

        return json_string

    def main(self):
        json_string = self.get_json_data_into_string()
        parsed_json = json.loads(json_string)

        for camera_data_in_json in parsed_json:
            try:
                input_format = self.get_camera_data_in_input_format(camera_data_in_json)
                self.write_to_file(input_format)
            except:
                traceback.print_exc()

if __name__ == '__main__':
    WeatherNetwork = WeatherNetwork()
    WeatherNetwork.main()
