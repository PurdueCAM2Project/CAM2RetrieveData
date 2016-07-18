"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for traffic cameras in New Brunswick of Canada traffic camera website
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 22 June 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python NewBrunswick.py
Usage                : N/A
Input file format    : N/A
Output               : list_NewBrunswick.txt
Note                 : 
Other files required by : Geocoding.py from in NetworkCameras/Discovery/Tools
this script and where     It requires Selenium and BeautifulSoup4 to be installed
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www2.gnb.ca/content/gnb/en/departments/dti/highways_roads/content/highway_cameras/nb_cameras.html
In database (Y/N)    : Y
Date added to Database : 22 June 2016
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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class NewBrunswick:
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://www2.gnb.ca"
        self.traffic_url = "http://www2.gnb.ca/content/gnb/en/departments/dti/highways_roads/content/highway_cameras/nb_cameras.html"
        self.country = "CA"
        self.state = ""

        # open the file to store the list and write the format of the list at the first line
        self.f = open('list_NewBrunswick.txt', 'w')
        self.f.write("city#country#snapshot_url#latitude#longitude" + "\n")

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

    def get_data(self, a_tag):
        """ Get the description, image url, and city name of the given camera

            The a_tag is a BeautifulSoup element that contains the infomation about one camera in <a> tag
            This function extracts the description, image url, and city name of the given data

            Args:
                a_tag: BeautifulSoup element that contains the infomation about one camera in <a> tag

            Return:
                descrip: description about the given camera
                img_src: image url of the given camera
                city: city name of the given camera
        """
        img_tag = a_tag.find("img")

        img_src = img_tag.get('src')
        city    = "New Brunswick"
        descrip = img_tag.get('alt')

        return descrip, img_src, city

    def main(self):
        # get parser for the traffic page
        geo = Geocoding('Google', None)
        soup_traffic = self.get_soup(self.traffic_url)

        # loop through each link
        for a_tag in soup_traffic.findAll("a", {"class" : "thumbnail"}):

            # get the data about the camera
            descrip, img_src, city = self.get_data(a_tag)
            print(descrip, img_src, city)

            try:
                geo.locateCoords(descrip, city, self.state, self.country)
                result = geo.city + "#" + geo.country + "#" + geo.state + "#" + img_src + "#" + geo.latitude + "#" + geo.longitude + "\n"
                result = result.replace("##", "#")
                self.f.write(result)
            except:
                print("can't find")

if __name__ == '__main__':
    NewBrunswick = NewBrunswick()
    NewBrunswick.main()
