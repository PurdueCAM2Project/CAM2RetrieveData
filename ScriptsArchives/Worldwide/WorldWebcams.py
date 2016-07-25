"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for cameras in WorldWebcam website
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 30 June 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python WorldWebcams.py
Usage                : N/A
Input file format    : N/A
Output               : list_WorldWebcam_Other.txt list_WorldWebcam_US.txt
Note                 : This website contains a lot of cameras all over the world.
                       For this reason, it has two output files, one for US and the other for non-US countries.
Other files required by : Geocoding.py in NetworkCameras/Discovery/Tools
this script and where     It requires Selenium and BeautifulSoup4 to be installed.
located                   It requires to install pycountry.

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.meteosurfcanarias.com/en/webcams
In database (Y/N)    : Y
Date added to Database : 30 June 2016
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
from state_code import states
from Geocoding import Geocoding
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class WorldWebcam(Useful):
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url       = "http://www.meteosurfcanarias.com"
        self.traffic_url    = "http://www.meteosurfcanarias.com/en/webcams"
        self.country        = ""

        # open the file to store the list and write the format of the list at the first line
        self.us = open('list_WorldWebcam_US.txt', 'w')
        self.us.write("city#country#state#snapshot_url#latitude#longitude" + "\n")

        self.ot = open('list_WorldWebcam_Other.txt', 'w')
        self.ot.write("city#country#snapshot_url#latitude#longitude" + "\n")

        # country code list
        self.countries = {}
        for country in pycountry.countries:
            self.countries[country.name] = country.alpha2
        
        # gps module
        self.gps = Geocoding('Google', None)
    
    def get_data(self, cam):
        """ Get the country-code, state-code, city name, image URL, and description about the given camera

            The cam contains all the information about one camera.
            This function extracts the needed data from cam.

            Args:
                cam: BeautifulSoup4 element that contains all the information about one camera

            Return:
                camera_data: CameraData instance that contains the parsed information of a camera
        """
        # extract the description text
        text = cam.find("p", {"class" : "description"}).text.encode("UTF-8")

        img_src         = self.get_img_src(cam)
        descrip         = ""
        city            = cam.find("p", {"class" : "one-webcam-header"}).text.strip()
        country, state  = self.get_country_state(text)

        camera_data = CameraData(img_src, country, state, city, descrip)

        return camera_data

    def get_img_src(self, cam):
        img_src = cam.find("img").get('src')
        if img_src[0] == '/':
            img_src = self.home_url + img_src
        
        return img_src

    def get_country_state(self, text):
        """ Get the country and state code of a camera
            
            The text is the description text of a camera.
            This function extracts the country and state name.
            Since only USA has the state, it first checks the country name and assigns the state code based on the country name

            Args:
                text: description text of a camera
        """
        country = Useful.get_token_between(self, text, "Country:", "Webcam").strip()

        if country == "United States":
            country = "USA"
            try:
                state = states[Useful.get_token_between(self, text, "state:", "Country").strip()]
            except:
                state = states[Useful.get_token_between(self, text, "Region:", "Country").strip()]
        else:
            country = self.countries.get(country, 'Unknown code')
            state = ""

        self.country = country

        return country, state

    def write_to_file(self, input_format):
        if self.country == "USA":
            self.us.write(input_format)
        else:
            self.ot.write(input_format)

        print(input_format)

    def main(self):
        # loop through each continent category
        soup_traffic = self.get_parser_with_soup(self.traffic_url)
        for continent in soup_traffic.findAll("area"):

            # loop through each country from the continent
            soup_continent = self.get_parser_with_soup(self.home_url + continent.get('href'))
            for country in soup_continent.findAll("div", {"class" : "country-button"}):

                # loop through the camears of each country
                soup_country = self.get_parser_with_soup(self.home_url + country.find("a").get('href'))
                for cam in soup_country.findAll("div", {"class" : ["display-webcams-peq", "display-webcams-med"]}):

                    # try to extract the data and write them into the files, if fails, ignore it and move to the next camera
                    try:
                        camera_data     = self.get_data(cam)
                        input_format    = self.convert_parsed_data_into_input_format(camera_data)

                        self.write_to_file(input_format)
                    except:
                        traceback.print_exc()

if __name__ == '__main__':
    WorldWebcam = WorldWebcam()
    WorldWebcam.main()
