"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for cameras in WorldCamera website
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 30 June 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python WorldCameras.py
Usage                : N/A
Input file format    : N/A
Output               : list_WorldCamera_Other.txt list_WorldCamera_US.txt
Note                 : This website contains a lot of cameras all over the world.
                        For this reason, it has two output files, one for US and the other for non-US countries.
Other files required by : It requires Selenium and BeautifulSoup4 to be installed.
                            It also requires to install pycountry
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.meteosurfcanarias.com/en/webcams
In database (Y/N)    : Y
Date added to Database : 30 June 2016
--------------------------------------------------------------------------------
"""

# -*- coding: utf-8 -*-

import selenium.webdriver.support.ui as ui
import time
import urllib
import urllib2
import re
import traceback
import pycountry
from CameraData import CameraData
from state_code import states
from Geocoding import Geocoding
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class WorldCamera:
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://www.meteosurfcanarias.com"
        self.traffic_url = "http://www.meteosurfcanarias.com/en/webcams"

        # open the file to store the list and write the format of the list at the first line
        self.us_file = open('list_WorldCamera_US.txt', 'w')
        self.us_file.write("city#country#state#snapshot_url#latitude#longitude" + "\n")

        self.non_us_file = open('list_WorldCamera_Other.txt', 'w')
        self.non_us_file.write("city#country#snapshot_url#latitude#longitude" + "\n")

        # country code list
        self.countries = {}
        for country in pycountry.countries:
            self.countries[country.name] = country.alpha2

    def get_soup(self, url):
        """ Get beautifulSoup object with the given url

            Args:
                url: the URL address of the webpage to be parsed

            Return:
                soup: beautifulSoup object to parse the given URL
        """
        opener = urllib2.build_opener() 
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]     # Add header information
        response = opener.open(url)
        page = response.read()
        soup = BeautifulSoup(page, "html.parser")               # Create soup

        return soup

    def get_token_between(self, string, front, end):
        """ Get the substring between <front> and <end> string
            
            The string contains string or html element
            This function get the substring between <front> and <end> string
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
            print("get_token_between error")
            traceback.print_exc()
            token = ""

        return token

    def parse_data(self, cam):
        """ Parse the country-code, state-code, city name, image URL, and description about the given camera

            The cam contains all the information about one camera.
            This function parse_datas the needed data from cam.

            Args:
                cam: BeautifulSoup4 element that contains all the information about one camera

            Return:
                camera_data: CameraData object containing the parsed data about the camera
        """
        description_text_of_cam = self.parse_data_descriptive_text(cam)

        img_src         = self.parse_data_img_src(cam)
        city            = self.parse_data_city_name(cam)
        country, state  = self.parse_data_country_state_two_letter_code(description_text_of_cam)
        descrip         = ""    # empty description

        camera_data = CameraData(img_src, country, state, city, descrip)    # Create CameraData object that contains all the data

        return camera_data

    def parse_data_descriptive_text(self, cam):
        return cam.find("p", {"class" : "description"}).text.encode("UTF-8")

    def parse_data_img_src(self, cam):
        img_src = cam.find("img").get('src')

        if img_src[0] == '/':
            img_src = self.home_url + img_src
        
        return img_src
    
    def parse_data_city_name(self, cam):
        return cam.find("p", {"class" : "one-webcam-header"}).text.strip()

    def parse_data_country_state_two_letter_code(self, description_text_of_cam):
        full_country_name = self.parse_data_full_country_name(description_text_of_cam)

        if full_country_name == "United States":
            country_code = "USA"
            state_code   = self.parse_data_state_two_letter_code(description_text_of_cam)
        else:
            country_code = self.convert_into_two_letter_code(full_country_name)
            state_code   = ""

        return country_code, state_code
    
    def parse_data_full_country_name(self, text):
        return self.get_token_between(text, "Country:", "Webcam").strip()

    def parse_data_state_two_letter_code(self, description_text_of_cam):
        try:
            full_state_name = self.get_token_between(description_text_of_cam, "state:", "Country").strip()
        except:
            full_state_name = self.get_token_between(description_text_of_cam, "Region:", "Country").strip()

        two_letter_state_code = states[full_state_name]

        return two_letter_state_code

    def convert_into_two_letter_code(self, country):
        return self.countries.get(country, 'Unknown code')

    def convert_parsed_data_into_input_format(self, gps_module, camera_data):
        description = camera_data.get_description()
        city        = camera_data.get_city()
        state       = camera_data.get_state()
        country     = camera_data.get_country()
        img_src     = camera_data.get_img_src()

        gps_module.locateCoords(description, city, state, country)
        input_format = gps_module.city + "#" + gps_module.country + "#" + gps_module.state + "#" + img_src + "#" + gps_module.latitude + "#" + gps_module.longitude + "\n"
        input_format = input_format.replace("##", "#")    # if no state exists, state == ""

        return input_format

    def write_to_file(self, country, input_format):
        if country == "USA":
            self.us_file.write(input_format)
        else:
            self.non_us_file.write(input_format)

        print(input_format)
    
    def main(self):
        gps_module = Geocoding('Nominatim', None)

        # loop through each continent category
        soup_traffic = self.get_soup(self.traffic_url)
        for continent in soup_traffic.findAll("area"):

            # loop through each country from the continent
            soup_continent = self.get_soup(self.home_url + continent.get('href'))
            for country in soup_continent.findAll("div", {"class" : "country-button"}):

                # loop through the camears of each country
                soup_country = self.get_soup(self.home_url + country.find("a").get('href'))
                for cam in soup_country.findAll("div", {"class" : ["display-webcams-peq", "display-webcams-med"]}):

                    try:
                        camera_data     = self.parse_data(cam)
                        input_format    = self.convert_parsed_data_into_input_format(gps_module, camera_data)

                        self.write_to_file(country, input_format)
                    except:
                        print("ERROR")

if __name__ == '__main__':
    WorldCamera = WorldCamera()
    WorldCamera.main()
