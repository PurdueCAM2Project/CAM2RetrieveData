"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for traffic cameras in New Australia of Canada traffic camera website
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 22 June 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python Australia_weather.py
Usage                : N/A
Input file format    : N/A
Output               : list_Australia_weather.txt
Note                 : 
Other files required by : It requires Selenium and BeautifulSoup4 to be installed
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.weathercamnetwork.com.au/index.html
In database (Y/N)    : Y
Date added to Database : 23 June 2016
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

class Australia:
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://www.weathercamnetwork.com.au"
        self.traffic_url = "http://www.weathercamnetwork.com.au/index.html"
        self.country = "AU"
        self.state = ""

        # open the file to store the list and write the format of the list at the first line
        self.f = open('list_Australia_weather.txt', 'w')
        self.f.write("city#country#snapshot_url#latitude#longitude" + "\n")

        # open the webbrowser
        self.driver = webdriver.Firefox()

        # gps moduel
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

    def get_data(self, string):
        """ Get the description, image url, and city name of the given camera

            The string contains the location infomation about one camera
            This function extracts the description and city name from the string
            Also, it gets the img_src from the current webpage

            ArgsderLeft:
                string: the location infomation about one camera

            Return:
                city: city name of the given camera
                img_src: image url of the given camera
                descrip: description about the given camera
        """
        img_src = self.driver.find_element_by_xpath("//div[@align='center']/img").get_attribute('src')
        city = self.get_token(string, "-", "(").strip()
        descrip = city + ", " + self.get_token(string, "", " ")

        return img_src, city, descrip

    def main(self):
        # get parser for the traffic page
        self.driver.get(self.traffic_url)

        # lists to store description and link to the image of each camera
        descrips = []
        links_to_img = []

        # loop through each link
        for div_tag in self.driver.find_elements_by_xpath("//div[@id='pageContent']/div"):

            # try to get description and link to the image of a camera. if fails, it means that it reached the end so breaks out of the loop
            try:
                descrip = div_tag.find_element_by_class_name("webcamHeaderLeft").text
                link_to_img = div_tag.find_element_by_tag_name("a").get_attribute('href')

                descrips.append(descrip)
                links_to_img.append(link_to_img)
            except:
                break

        # loop through the stored links
        for i in range(len(links_to_img)):

            # move to the link
            self.driver.get(links_to_img[i])

            # get the data about one camera
            img_src, city, descrip = self.get_data(descrips[i])
            print(descrip, img_src, city)

            # try to get the GPS data and write it to the file. if fails, move to the next camera
            try:
                self.gps.locateCoords(descrip, city, self.state, self.country)
                input_format = self.gps.city + "#" + self.gps.country + "#" + self.gps.state + "#" + img_src + "#" + self.gps.latitude + "#" + self.gps.longitude + "\n"
                input_format = input_format.replace("##", "#")
                self.f.write(input_format)
            except:
                print("can't find")

if __name__ == '__main__':
    Australia = Australia()
    Australia.main()
