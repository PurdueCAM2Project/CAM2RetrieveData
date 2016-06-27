"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for cameras in insecam.org
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 27 June 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python insecam.py
Usage                : N/A
Input file format    : N/A
Output               : list_insecam_US.txt list_insecam_Other.txt
Note                 : This website contains a lot of cameras all over the world.
                        For this reason, it has two output files, one for US and the other for non-US countries.
                        Also, since it contains many private cameras, this script parses only the cameras in the following categories to not violate the privacy
                        ['City', 'Village', 'River' 'Square', 'Construction', 'Bridge', 'Nature', 'Mountain', 'Traffic', 'Street', 'Road', 'Architecture', 'Port', 'Beach']
Other files required by : It requires Selenium and BeautifulSoup4 to be installed
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.insecam.org/
In database (Y/N)    : 
Date added to Database : 
--------------------------------------------------------------------------------
"""

# -*- coding: utf-8 -*-

import selenium.webdriver.support.ui as ui
import time
import urllib
import urllib2
import re
import traceback
from state_code import states
from Geocoding import Geocoding
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class Insecam:
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://www.insecam.org"
        self.traffic_url = "http://www.insecam.org/"

        # open the file to store the list and write the format of the list at the first line
        self.us = open('list_insecam_US.txt', 'w')
        self.us.write("city#country#state#snapshot_url#latitude#longitude" + "\n")

        self.ot = open('list_insecam_Other.txt', 'w')
        self.ot.write("city#country#snapshot_url#latitude#longitude" + "\n")

        # open the web-driver
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference("javascript.enabled", False)

        self.driver = webdriver.Firefox(firefox_profile=firefox_profile)

        # list of categories that it will parse
        self.categories = ['City', 'Village', 'River' 'Square', 'Construction', 'Bridge', 'Nature', 'Mountain', 'Traffic', 'Street', 'Road', 'Architecture', 'Port', 'Beach']
        self.invalid = ['http://admin:@50.30.102.221:85/videostream.cgi',
                        'http://198.1.4.43:80/mjpg/video.mjpg?COUNTER',
                        'http://97.76.101.212:80/mjpg/video.mjpg?COUNTER',
                        'http://24.222.206.98:1024/img/video.mjpeg?COUNTER',
                        'http://71.43.210.90:80/SnapshotJPEG?Resolution=640x480&amp;amp;Quality=Clarity&amp;amp;1467044876',
                        'http://61.149.161.158:82/mjpg/video.mjpg?COUNTER',
                        "http://213.126.67.202:1024/oneshotimage1",
                        "http://71.90.110.144:8080/img/video.mjpeg?COUNTER",
                        "http://95.63.206.142:80/mjpg/video.mjpg?COUNTER",
                        "http://201.229.94.197:80/mjpg/video.mjpg?COUNTER"
                       ]

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

    def valid_type(self, category):
        """ Check if the given category is OK to parse or not

            Since some categories of cameras are private, we have to check if it is OK to parse.
            This function checks if the given category is safe to parse.

            Args:
                category: the category of cameras

            Return:
                result: the boolean value whether it is safe or not
        """
        split = category.get('href').split("/")                 # split to get the string value of category
        result = split[len(split) - 2] in self.categories       # check if the category if in the valid category list 

        return result

    def get_page_num(self, soup_cate):
        """ Get the maximum page number of given category of cameras

            Args:
                soup_cate: the BeautifulSoup object to parse the pages of the given category
            
            Return:
                page_num: the maximum page number of given category of cameras
        """
        pages = soup_cate.find("div", {"id" : "navbar"})
        page_num = int(self.get_token(pages, ",", ","))

        return page_num

    def get_data(self, cam):
        """ Get the data for each camera such as country, city, etc.

            The cam has a URL to one camera.
            This function parse the camera's webpage to get the data such as country, city, and so on.

            Args:
                cam: a BeautifulSoup element that contains a URL to one camera
            
            Return:
                country: the country code of the camera
                state: the state code of the camera
                city: the city name of the camera
                lat: the latitude of the camera
                lon: the longitude of the camera
                img_src: the image URL of the camera 
        """
        # get parser for the camera webpage AND get the table that has all the data
        soup_cam = self.get_soup(self.home_url + cam.find("a").get('href'))
        rows = soup_cam.find("table").findAll("tr")

        # extract the data from the table
        country = rows[1].findAll("td")[1].text.strip()
        state   = rows[2].findAll("td")[1].text.strip().title()
        city    = rows[3].findAll("td")[1].text.split(".")[0].strip()
        lat     = rows[4].findAll("td")[1].text.strip()
        lon     = rows[5].findAll("td")[1].text.strip()

        # get the img_src and update the country code and state code
        img_src = cam.find("img", {"class" : "thumbnailimg"}).get('src')
        country, state = self.update_country_state(country, state)

        return country, state, city, lat, lon, img_src

    def update_country_state(self, country, state):
        """ Update the country/state code

            If country is "US", change it to "USA" and find the 2 letter state_code
            If not, change the state_code as ""

            Args:
                country: the country code in 2 letter abbreviation
                state: the region name of the camera (if country is US, it is the state name)
            
            Return:
                country_code: the correct country code
                state_code: the correct 2 letter state code
        """
        if country == "US":
            country_code = "USA"
            state_code = states[state]
        else:
            country_code = country
            state_code = ""

        return country_code, state_code

    def write_to_file(self, country, state, city, lat, lon, img_src):
        """ Write the parsed data into the file

            Since the file format of US and non-US countries are different, write the data into two different files.

            Args:
                country: the country code of a camera
                state: the state code of a camera 
                city: the city name of a camera
                lat: the latitude of a camera
                lon: the longitude of a camera
                img_src: the image URL of a camera
        """
        if state == "" and not city == "-":
            self.ot.write(city + "#" + country + "#" + img_src + "#" + lat + "#" + lon + "\n")
        elif country == "USA" and not city == "-":
            self.us.write(city + "#" + country + "#" + state + "#" + img_src + "#" + lat + "#" + lon + "\n")

        print(country, state, city, lat, lon, img_src)

    def main(self):
        # get parser for the traffic page
        self.driver.get(self.traffic_url)
        soup_traffic = BeautifulSoup(self.driver.page_source, "html.parser")
        
        # loop through the categories
        soup_traffic_categories = soup_traffic.find("ul", {"id" : "tagsul"})
        for category in soup_traffic_categories.findAll("a"):

            # if the given category is NOT valid, ignore it and move to the next category
            if not self.valid_type(category):
                continue

            # if valid category, move to the pages of the given category and loop through the pages
            category_url = self.home_url + category.get('href')
            soup_cate = self.get_soup(category_url)
            for i in range(self.get_page_num(soup_cate)):

                # For each page, loop through all the cameras to parse them
                soup_page = self.get_soup(category_url + "?page=" + str(i + 1))
                for cam in soup_page.findAll("div", {"class" : "thumbnail"}):
                    
                    # try to extract the data and write them into the files. if fails, move to the next camera
                    try:
                        country, state, city, lat, lon, img_src = self.get_data(cam)
                        if (img_src in self.invalid): # if the img_src is one of unsafe url, ignore it and move to the next
                            continue
                        self.write_to_file(country, state, city, lat, lon, img_src)
                    except:
                        print("next")

if __name__ == '__main__':
    Insecam = Insecam()
    Insecam.main()
