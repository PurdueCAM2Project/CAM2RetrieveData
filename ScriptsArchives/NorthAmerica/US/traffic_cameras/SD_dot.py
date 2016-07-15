"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for traffic cameras in SouthDakota dot website
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 16 June 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python SD_dot.py
Usage                : N/A
Input file format    : N/A
Output               : list_SD_doc.txt
Note                 : 
Other files required by : It requires Selenium and BeautifulSoup4 to be installed
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.safetravelusa.com/sd/cameras/
In database (Y/N)    : Y
Date added to Database : 16 June 2016
--------------------------------------------------------------------------------
"""

# -*- coding: utf-8 -*-

import selenium.webdriver.support.ui as ui
import time
import urllib
import re
import traceback
import urlparse
from Geocoding import Geocoding
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class SouthDakota:
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://www.safetravelusa.com"
        self.traffic_url = "http://www.safetravelusa.com/sd/cameras/"
        self.country = "USA"
        self.state = "SD"

        # open the file to store the list and write the format of the list at the first line
        self.f = open('list_SD_dot.txt', 'w')
        self.f.write("city#country#state#snapshot_url#latitude#longitude" + "\n")

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
    
    def main(self):
        # get parser for the traffic page
        soup_traffic = self.get_soup(self.traffic_url)

        # loop through each camera
        for div_tag in soup_traffic.findAll("div", {"class" : "city"}):
            # get href of each camera's url. If it is empty string, ignore it
            href = self.get_token(div_tag, 'href="', '"')
            if href == "":
                continue

            # get the img_src and city name of each camera
            img_src = urlparse.urljoin(self.traffic_url, href)
            city = div_tag.find("span", {"class" : "name"}).text
            descrip = ""

            print(img_src, city)

            try:
                self.gps.locateCoords(descrip, city, self.state, self.country)
                input_format = self.gps.city + "#" + self.gps.country + "#" + self.gps.state + "#" + img_src + "#" + self.gps.latitude + "#" + self.gps.longitude + "\n"
                input_format = input_format.replace("##", "#")
                self.f.write(input_format)
            except:
                print("can't find")

if __name__ == '__main__':
    SouthDakota = SouthDakota()
    SouthDakota.main()
