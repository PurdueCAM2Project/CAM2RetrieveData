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
from state_code import states
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
        self.home_url = "http://www.meteosurfcanarias.com"
        self.traffic_url = "http://www.meteosurfcanarias.com/en/webcams"

        # open the file to store the list and write the format of the list at the first line
        self.us = open('list_WorldWebcam_US.txt', 'w')
        self.us.write("city#country#state#snapshot_url#latitude#longitude" + "\n")

        self.ot = open('list_WorldWebcam_Other.txt', 'w')
        self.ot.write("city#country#snapshot_url#latitude#longitude" + "\n")

        # country code list
        self.countries = {}
        for country in pycountry.countries:
            self.countries[country.name] = country.alpha2


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

    def get_data(self, cam):
        """ Get the country-code, state-code, city name, image URL, and description about the given camera

            The cam contains all the information about one camera.
            This function extracts the needed data from cam.

            Args:
                cam: BeautifulSoup4 element that contains all the information about one camera

            Return:
                country:    The 2-letter country code of the given camera
                state:      The 2-letter state code of the given camera
                city:       The city name of the given camera
                img_src:    The image URL of the given camera
                descrip:    The description of the given camera

        """
        # extract the description text
        text = cam.find("p", {"class" : "description"}).text.encode("UTF-8")

        # extract the image URL of the camera
        img_src = cam.find("img").get('src')
        if img_src[0] == '/':
            img_src = self.home_url + img_src

        # extract the country name and convert it to the 2-letter code
        country, state = self.get_country_state(text)

        # extract the city name
        city = cam.find("p", {"class" : "one-webcam-header"}).text.strip()
        descrip = ""

        return country, state, city, img_src, descrip

    def get_country_state(self, text):
        """ Get the country and state code of a camera
            
            The text is the description text of a camera.
            This function extracts the country and state name.
            Since only USA has the state, it first checks the country name and assigns the state code based on the country name

            Args:
                text: description text of a camera
        """
        country = self.get_token(text, "Country:", "Webcam").strip()

        if country == "United States":
            country = "USA"
            try:
                state = states[self.get_token(text, "state:", "Country").strip()]
            except:
                state = states[self.get_token(text, "Region:", "Country").strip()]
        else:
            country = self.countries.get(country, 'Unknown code')
            state = ""

        return country, state

    def write_to_file(self, geo, country, state, city, img_src, descrip):
        """ Writes the extracted data into the list files
            
            It locates the GPS with the Geocoding module.
            If success, it writes the result into the files.
            Since the format of US file and other countries' file, check the country name before writing.

            Args:
                geo:        A Geocoding object to locate the GPS location
                country:    The 2-letter country code of the given camera
                state:      The 2-letter state code of the given camera
                city:       The city name of the given camera
                img_src:    The image URL of the given camera
                descrip:    The description of the given camera
        """
        geo.locateCoords(descrip, city, state, country)
        result = geo.city + "#" + geo.country + "#" + geo.state + "#" + img_src + "#" + geo.latitude + "#" + geo.longitude + "\n"
        result = result.replace("##", "#")

        if country == "USA":
            self.us.write(result)
        else:
            self.ot.write(result)

        print(country, state, city, img_src, descrip)

    def main(self):
        geo = Geocoding('Nominatim', None)

        # loop through each continent category
        soup_traffic = self.get_soup(self.traffic_url)
        for continent in soup_traffic.findAll("area"):

            # loop through each country from the continent
            soup_continent = self.get_soup(self.home_url + continent.get('href'))
            for country in soup_continent.findAll("div", {"class" : "country-button"}):

                # loop through the camears of each country
                soup_country = self.get_soup(self.home_url + country.find("a").get('href'))
                for cam in soup_country.findAll("div", {"class" : ["display-webcams-peq", "display-webcams-med"]}):

                    # try to extract the data and write them into the files, if fails, ignore it and move to the next camera
                    try:
                        country, state, city, img_src, descrip = self.get_data(cam)
                        self.write_to_file(geo, country, state, city, img_src, descrip)
                    except:
                        print("ERROR")

if __name__ == '__main__':
    WorldWebcam = WorldWebcam()
    WorldWebcam.main()
