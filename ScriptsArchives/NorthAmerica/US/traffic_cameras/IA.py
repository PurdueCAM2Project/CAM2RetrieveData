"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for traffic cameras in Iowa's traffic website
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 16 June 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python IA.py
Usage                : N/A
Input file format    : N/A
Output               : list_IA.txt
Note                 : N/A
Other files required by : Geocoding.py and Useful.py in NetworkCameras/Discovery/Tools
this script and where     It requires Selenium and BeautifulSoup4 to be installed
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://lb.511.Iowa.gov/idlb/cameras/routeselect.jsf
In database (Y/N)    : Y
Date added to Database : 15 July 2016
--------------------------------------------------------------------------------
"""

# -*- coding: utf-8 -*-

import selenium.webdriver.support.ui as ui
import time
import urllib
import re
import traceback
from Geocoding import Geocoding
from selenium import webdriver
from Useful import Useful
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class Iowa(Useful):
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://lb.511ia.org"
        self.traffic_url = "http://lb.511ia.org/ialb/cameras/routeselect.jsf"
        self.country = "USA"
        self.state = "IA"

        # open the file to store the list and write the format of the list at the first line
        self.f = open('list_IA.txt', 'w')
        self.f.write("city#country#state#snapshot_url#latitude#longitude" + "\n")

        # gps module
        self.gps = Geocoding('Google', None)

    
    def get_descrip(self, soup_cam):
        """ Get the description of location about a camera

            The soup_cam is the parser for webpage of one camera.
            This function parses the description data from it.

            Args:
                soup_cam: parser for webpage of one camera
            
            Return:
                descrip: the description of the location about one camera
        """
        descrip = soup_cam.find("div", {"class" : "panelTitle"}).text
        descrip = ' '.join(descrip.split())
        descrip = Useful.get_token_between(self, descrip, "@", "(").strip()

        return descrip

    def get_img_src(self, soup_cam):
        """ Get the image url for one camera

            The img tag for cameras are two: cam-1-img and cam-0-img.
            This function tries both of them to get the img_src of all cameras.

            Args:
                soup_cam: parser for webpage of one camera

            Return:
                img_src: the image url for the camera with the given webpage parser
        """
        img_src = ""
        for arg in [{"id" : "cam-1-img"}, {"id" : "cam-0-img"}]:
            try:
                img_src = soup_cam.find("img", arg).get('src')
                break
            except:
                continue

        return img_src

    def get_data(self, link):
        """ Get the description, city name, and the image url of the given camera

            The link is url to a camera.
            This function creates parser for that and extracts the needed data.

            Args:
                link: url to a camera webpage that contains more detailed info about the camera

            Return:
                descrip: description about the given camera
                city: city name of the given camera
                img_src: image url of the given camera
        """
        # create html parser for the camera
        soup_cam = Useful.get_parser_with_soup(self, self.home_url + link)

        # get the description, city name, and img_src of the camera
        descrip = self.get_descrip(soup_cam)
        city = ""
        img_src = self.get_img_src(soup_cam)

        return descrip, city, img_src

    def main(self):
        # get parser for the traffic page
        soup = Useful.get_parser_with_soup(self, self.traffic_url)

        # loop through each camera to parse
        for div_tag in soup.findAll("div", {"id" : "j_idt126"}):
            # get the link to the camera. If href of each link doesn't start with character "/", ignore it
            link = div_tag.find("a").get('href')
            if link[0] != "/":
                continue

            # get the description, city name, and image url for given camera
            descrip, city, img_src = self.get_data(link)
            print(descrip, img_src)

            try:
                self.gps.locateCoords(descrip, city, self.state, self.country)
                input_format = self.gps.city + "#" + self.gps.country + "#" + self.gps.state + "#" + img_src + "#" + self.gps.latitude + "#" + self.gps.longitude + "\n"
                input_format = input_format.replace("##", "#")
                self.f.write(input_format)
            except:
                traceback.print_exc()
                print("can't find")

if __name__ == '__main__':
    Iowa = Iowa()
    Iowa.main()
