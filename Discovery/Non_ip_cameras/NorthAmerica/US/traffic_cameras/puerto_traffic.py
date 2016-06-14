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
Other files required by : It requires Selenium to be installed
this script and where
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
from Geocoding import Geocoding
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException

class Puerto:
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://its.dtop.gov.pr/es/"
        self.traffic_url = "http://its.dtop.gov.pr/es/TrafficCameras.aspx?"
        self.country = "USA"
        self.state = "PR"

        # open web browser for selenium
        self.driver = webdriver.Firefox()

        # open the file to store the list and write the format of the list at the first line
        self.f = open('list_puerto_traffic', 'w')
        self.f.write("city#country#state#snapshot_url#latitude#longitude" + "\n")

    def get_data(self, link):
        """ Get the url to the img_src of the given link
                the detailed location information
                the city name about one camera

            The arguement link is a Selenium element that contains the html data about one camera.
            This function extracts the needed data in the <a href=""> tag.

            Args:
                link: Selenium element that contains the html data about one camera

            Return:
                cam_src: the extracted link url from <a href=""> tag
                desc: the detailed location information
                city: the city name about one camera
        """
        cam_src = link.get_attribute('href')
        city = link.text.split("-")[0]
        desc = self.get_token(link.text.encode("UTF-8"), "(", ")").strip()

        return cam_src, city, desc
    
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
            Moves to that webpage and get the img_src on the page.
            Then, moves back and returns the img_src

            Args:
                cam_src: the link to the webpage that has img_src

            Return:
                img_src: image url of one camera
        """
        self.driver.get(cam_src)

        img_tag = self.driver.find_element_by_id("Image")
        img_src = img_tag.get_attribute("src").split("?")[0]

        self.driver.back()

        return img_src
    
    def main(self):
        # get parser for the homepage
        self.driver.get(self.traffic_url)
        variable = Geocoding('Nominatim', None)

        # list to store cam_src, city name, and descriptioon about each camera
        cam_srcs = []
        cities = []
        descrips = []

        # Selenium element that contains a list of links of all cameras
        link_container = self.driver.find_element_by_id("bodyContent_bodyContent_cctv")

        # loop through the links of cameras to get the data
        for link in link_container.find_elements_by_tag_name("a"):
            cam_src, city, desc = self.get_data(link)

            # store the parsed data into the list
            cam_srcs.append(cam_src)
            cities.append(city)
            descrips.append(desc)

        # loop through the parsed data of cameras to write to the file
        for i in range(len(cam_srcs)):
            img_src = self.get_img_src(cam_srcs[i])
            city = cities[i]
            descrip = descrips[i]
            
            print(city, descrip, img_src)
            
            try:
                variable.locateCoords(descrip, city, self.state, self.country)
                self.f.write(variable.city.replace(" ", "").title() + "#" + variable.country + "#" + variable.state + "#" + img_src + "#" + variable.latitude + "#" + variable.longitude + "\n")
            except:
                print("can't find")

if __name__ == '__main__':
    Puerto = Puerto()
    Puerto.main()
