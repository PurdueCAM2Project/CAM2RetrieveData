"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for traffic cameras in Idaho's gov website
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 15 June 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python Idaho_gov.py
Usage                : N/A
Input file format    : N/A
Output               : list_Idaho_traffic
Note                 : 
Other files required by : It requires Selenium and BeautifulSoup4 to be installed
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://lb.511.idaho.gov/idlb/cameras/routeselect.jsf?view=state&textOnly=false
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

class Idaho:
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://lb.511.idaho.gov"
        self.traffic_url = "http://lb.511.idaho.gov/idlb/cameras/routeselect.jsf?view=state&textOnly=false"
        self.country = "USA"
        self.state = "ID"

        # open the file to store the list and write the format of the list at the first line
        self.f = open('list_Idaho_gov.txt', 'w')
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
        descrip = self.get_token(descrip, ":", "").strip()

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
        soup_cam = self.get_soup(self.home_url + link)

        # get the description and city name of the camera
        descrip = self.get_descrip(soup_cam)
        city = descrip
        img_src = self.get_img_src(soup_cam)

        return descrip, city, img_src
    
    def main(self):
        # get parser for the traffic page
        variable = Geocoding('Nominatim', None)
        soup = self.get_soup(self.traffic_url)

        # store the href of each camera
        for div_tag in soup.findAll("div", {"id" : "j_idt120"}):
            # get the link to the camera if href of each link doesn't start with character "/", ignore it
            link = div_tag.find("a").get('href')
            if link[0] != "/":
                continue

            # get the description, city name, and image url for given camera
            descrip, city, img_src = self.get_data(link)
            print(descrip, img_src)

            try:
                variable.locateCoords(descrip, city, self.state, self.country)
                result = variable.city.replace(" ", "").title() + "#" + variable.country + "#" + variable.state + "#" + img_src + "#" + variable.latitude + "#" + variable.longitude + "\n"
                result = result.replace("##", "#")
                self.f.write(result)
            except:
                print("can't find")

if __name__ == '__main__':
    Idaho = Idaho()
    Idaho.main()
