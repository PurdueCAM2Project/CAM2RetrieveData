"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for the traffic camera websites of Philadelphia
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 8 July 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python PA_phillytraffic.py
Usage                : N/A
Input file format    : N/A
Output               : list_Philadelphia_PA.txt
Note                 : The output of this script doesn't include the GPS location data.
                       It will use the GPS data from the website http://www.511pa.com/ which is parsed by intercepting the JSON file not by the script.
                       Ask Ryan Dailey who parsed http://www.511pa.com/
Other files required by : It requires Selenium and BeautifulSoup4 to be installed.
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.phillytraffic.com/#!traffic-updates/cjn9
In database (Y/N)    : N/A
Date added to Database : N/A
--------------------------------------------------------------------------------
"""

# -*- coding: utf-8 -*-

import selenium.webdriver.support.ui as ui
import time
import urllib
import re
import traceback
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class Philadelphia:
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://www.phillytraffic.com"
        self.traffic_url = "http://www.phillytraffic.com/#!traffic-updates/cjn9"
        self.country = "USA"
        self.state = "PA"

        # open the file to store the list and write the format of the list at the first line
        self.file = open('list_Philadelphia_PA.txt', 'w')
        self.file.write("city#country#state#snapshot_url#latitude#longitude" + "\n")

        # open the brwoser
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference("javascript.enabled", False)

        self.driver = webdriver.Firefox(firefox_profile=firefox_profile)
        self.wait = ui.WebDriverWait(self.driver, 10)

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

    def write_to_file(self, description, img_src):
        self.file.write(description + "#" + img_src + "\n")

    def get_parser_for_link(self, link_to_street):
        self.driver.get(link_to_street)
        parser_for_link = BeautifulSoup(self.driver.page_source, "html.parser")
        self.driver.get(parser_for_link.find('iframe').get('src'))
        parser_for_link = BeautifulSoup(self.driver.page_source, "html.parser")

        return parser_for_link

    def main(self):
        # get parser for the traffic page
        gps_module = Geocoding('Google', None)
        self.driver.get(self.traffic_url)

        # store the link addresses to camera webpage of each street
        links = []
        for street in self.driver.find_elements_by_xpath("//a[@target='_self'][@class='s6link']"):
            links.append(street.get_attribute('href'))

        # loop through the camera webpage of each street
        for link_to_street in links:
            parser_for_link = self.get_parser_for_link(link_to_street)

            for cam in parser_for_link.findAll("img"):
                description = cam.get('name')
                img_src     = cam.get('src')

                self.write_to_file(description, img_src)
            
if __name__ == '__main__':
    Philadelphia = Philadelphia()
    Philadelphia.main()
