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

class Germany:
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://lb.511.idaho.gov"
        self.traffic_url = "http://lb.511.idaho.gov/idlb/cameras/routeselect.jsf?view=state&textOnly=false"
        self.country = "USA"
        self.state = "ID"

        # open the file to store the list and write the format of the list at the first line
        self.f = open('list_Idaho_traffic', 'w')
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
    
    def main(self):
        # get parser for the traffic page
        variable = Geocoding('Nominatim', None)
        soup = self.get_soup(self.traffic_url)


        # store the href of each camera
        links = []
        for div_tag in soup.findAll("div", {"id" : "j_idt120"}):
            links.append(div_tag.find("a").get('href'))

        # loop through each camera to parse
        soup_cam = None
        for link in links:
            # if href of each link doesn't start with character "/", ignore it
            if link[0] != "/":
                continue

            # create html parser for the camera
            soup_cam = self.get_soup(self.home_url + link)

            # get the description and city name of the camera
            descrip = soup_cam.find("div", {"class" : "panelTitle"}).text
            descrip = self.get_token(descrip, ":", "").strip()
            city = descrip

            # get the img_src
            for arg in [{"id" : "cam-1-img"}, {"id" : "cam-0-img"}]:
                try:
                    img_src = soup_cam.find("img", arg).get('src')
                    break
                except:
                    continue

            print(descrip, img_src)

            try:
                variable.locateCoords(descrip, city, self.state, self.country)
                result = variable.city.replace(" ", "").title() + "#" + variable.country + "#" + variable.state + "#" + img_src + "#" + variable.latitude + "#" + variable.longitude + "\n"
                result = result.replace("##", "#")
                self.f.write(result)
            except:
                print("can't find")

if __name__ == '__main__':
    Germany = Germany()
    Germany.main()
