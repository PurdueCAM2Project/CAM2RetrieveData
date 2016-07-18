"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for Puerto Rico Traffic Camera website http://its.dtop.gov.pr/es/TrafficCameras.aspx
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : June 13 2016
Description          : Parse cameras on Puerto Rico traffic camera website
Command to run script: python puerto_traffic.py
Usage                : N/A
Input file format    : N/A
Output               : list_puerto_traffic
Note                 : Do not use Google API for Geocoding. It gives wrong latitude and longitude
                       It only parse two cameras out of about 50 or more cameras because it fails on geocoding
Other files required by : Geocoding.py from in NetworkCameras/Discovery/Tools
this script and where     It requires Selenium and BeautifulSoup4 to be installed
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://its.dtop.gov.pr/es/TrafficCameras.aspx
In database (Y/N)    : Y
Date added to Database : June 13 1026
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

class Puerto:
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://its.dtop.gov.pr"
        self.parent_url = "http://its.dtop.gov.pr/es/"
        self.traffic_url = "http://its.dtop.gov.pr/es/TrafficCameras.aspx?"
        self.country = "USA"
        self.state = "PR"

        # open the file to store the list and write the format of the list at the first line
        self.f = open('list_puerto_traffic.txt', 'w')
        self.f.write("city#country#state#snapshot_url#latitude#longitude" + "\n")
        
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

    def get_data(self, a_tag):
        """ Get the img_src of the given camera 
                the detailed location information
                the city name about one camera

            The arguement link is a BeautifulSoup element that contains the html data about one camera.
            This function extracts the needed data in the <a href=""> tag.

            Args:
                a_tag: Selenium element that contains the html data about one camera

            Return:
                img_src: the img_src of the given camera
                desc: the detailed location information
                city: the city name about one camera
        """
        link_to_cam = a_tag.get('href')

        img_src = self.get_img_src(self.parent_url + link_to_cam)
        city = a_tag.text.split("-")[0]
        desc = self.get_token(a_tag.text.encode("UTF-8"), "(", ")").strip()

        return img_src, city, desc
    
    def get_token(self, camera, front, end):
        """ Extract the substring between <front> and <end> string
            
            The str(camera) contains html string about one camera
            This function extract the substring between <front> and <end> string

            Args:
                camera: html element or string that contains the information of one camera
                front: string at the left of the wanted substring
                end: string at the right of the wanted substring

            Return:
                token: the string between <front> and <end> string OR if DNE, return empty string
        """
        cam_str = str(camera)
        front_split = cam_str.split(front)[1]
        try:
            token = front_split.split(end)[0]
        except:
            token = ""

        return token

    def get_img_src(self, cam_src):
        """ Get the img_src of one camera
            
            The cam_src contains the link to the webpage that has img_src.
            Create parser for that webpage and get the img_src on the page.
            Then, return the img_src

            Args:
                cam_src: the link to the webpage that has img_src

            Return:
                img_src: image url of one camera
        """
        soup_cam = self.get_soup(cam_src)

        img_tag = soup_cam.find("img")
        img_src = img_tag.get("src").split("?")[0]
        img_src = self.home_url + img_src

        return img_src
    
    def main(self):
        # create parser for the traffic webpage
        soup_traffic = self.get_soup(self.traffic_url)
        geo = Geocoding('Nominatim', None)

        # loop through the a_tag about each camera
        soup_traffic_links = soup_traffic.find("div", {"id" : "bodyContent_bodyContent_cctv"})
        for a_tag in soup_traffic_links.findAll("a", {"target" : "_blank"}):

            # get the im_src, city name, and description about the camera
            img_src, city, descrip = self.get_data(a_tag)
            print(city, descrip, img_src)
            
            try:
                geo.locateCoords(descrip, city, self.state, self.country)
                self.f.write(geo.city + "#" + geo.country + "#" + geo.state + "#" + img_src + "#" + geo.latitude + "#" + geo.longitude + "\n")
            except:
                print("can't find")

if __name__ == '__main__':
    Puerto = Puerto()
    Puerto.main()
