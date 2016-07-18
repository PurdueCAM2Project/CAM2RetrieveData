"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for traffic cameras in Wyoming travel service website
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 15 June 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python WY_wyroad.py
Usage                : N/A
Input file format    : N/A
Output               : list_WY_wyroad.txt
Note                 : 
Other files required by : Geocoding.py from in NetworkCameras/Discovery/Tools
this script and where     It requires Selenium and BeautifulSoup4 to be installed
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.wyoroad.info/highway/webcameras/webcameras.html
In database (Y/N)    : Y
Date added to Database : 15 June 2016
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

class Wyoming:
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://www.wyoroad.info"
        self.traffic_url = "http://www.wyoroad.info/highway/webcameras/webcameras.html"
        self.country = "USA"
        self.state = "WY"

        # open the file to store the list and write the format of the list at the first line
        self.f = open('list_WY_wyroad.txt', 'w')
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

    def get_data(self, cam):
        """ Get the description, image url, and city name of the given camera

            The cam is a BeautifulSoup element that contains the infomation about one camera in <a href=""> tag
            This function extracts the description, image url, and city name of the given data

            Args:
                cam: BeautifulSoup element that contains the infomation about one camera in <a href=""> tag

            Return:
                descrip: description about the given camera
                img_src: image url of the given camera
                city: city name of the given camera
        """
        # create parser for a camera
        soup_cam = self.get_soup(self.home_url + cam.get('href'))

        # create img_src, city, descrip for Geocoding
        descrip = ""
        img_src = soup_cam.find("img", {"class" : "photolarge"}).get('src')
        city = cam.text

        # complete the img_src
        if img_src[0] == "/":
            img_src = self.home_url + img_src

        return descrip, img_src, city

    def main(self):
        # get parser for the traffic page
        soup_traffic = self.get_soup(self.traffic_url)

        # loop through each link
        link_table = soup_traffic.find("table", {"class" : "table"})
        for a_tag in link_table.findAll("a"):

            # create parser for each link
            soup_link = self.get_soup(self.home_url + a_tag.get('href'))
            cam_table = soup_link.find("table", {"class" : "table"})

            # loop through each camera in a link
            for cam in cam_table.findAll("a"):
                descrip, img_src, city = self.get_data(cam)
                
                print(img_src, city)

                try:
                    self.gps.locateCoords(descrip, city, self.state, self.country)
                    input_format = self.gps.city + "#" + self.gps.country + "#" + self.gps.state + "#" + img_src + "#" + self.gps.latitude + "#" + self.gps.longitude + "\n"
                    input_format = input_format.replace("##", "#")
                    self.f.write(input_format)
                except:
                    print("can't find")

if __name__ == '__main__':
    Wyoming = Wyoming()
    Wyoming.main()
