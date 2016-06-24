"""
--------------------------------------------------------------------------------
Descriptive Name     :  Parser for cameras in SwissWebcam website
Author               :  Sanghyun Joo
Contact Info         :  joos@purdue.edu OR toughshj@gmail.com
Date                 :  10 June 2016
Description          :  parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script:  python swissWebcam_non_traffic.py
Usage                :  Parsing cameras in SwissWebcam website
Input file format    :  N/A
Output               :  list_SwissWebcam_non_traffic
Note                 :  This website's pictures are all from the http://www.webcams.travel/ which we already have. Do not use to parse
Other files required by : This code requires to install BeautifulSoup4 and Geocoding.py file from NetworkCameras/Discovery/Tools/Geocoding.py
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       :  http://en.swisswebcams.ch
In database (Y/N)    :  Y
--------------------------------------------------------------------------------
"""

# -*- coding: utf-8 -*-

import urllib
import re
import time
import traceback
import selenium.webdriver.support.ui as ui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from Geocoding import Geocoding

class SwissWebcam:
    def __init__(self):
        # store the url of homepage and the country code
        self.home_url = "http://en.swisswebcams.ch"
        self.geo_url = "http://map.topin.travel/?p=swc&id="
        self.country = "CH"

        # open the file to store the list and write the format of the list at the first line
        self.f = open('list_swissWebcam.txt', 'w')
        self.f.write("country#city#snapshot_url#latitude#longitude" + "\n")

        # open the Firefox
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference("javascript.enabled", False)

        self.driver = webdriver.Firefox(firefox_profile=firefox_profile)

        # wait object to use
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
    
    def get_img_src(self, camera):
        """ Extract the img_src on the webpage

            The argument camera is one element containing information about one camera.
            This function extracts the image url in the <img src=""> tag.

            Args:
                camera: beautiful soup's html element that contains the information of one camera

            Return:
                img_src: the extracted image url from <img src=""> tag
        """
        soup_img = self.get_soup(self.home_url + camera.get('href'))
        try:
            img_src = soup_img.find("img", {"id" : "WEBCAM-bild"}).get('src')
        except AttributeError:
            img_src = self.home_url + soup_img.find("iframe").get('src')

        return img_src

    def get_descrip(self, camera):
        """ Extract the detailed location information about one camera

            The argument camera is one element containing information about one camera.
            This function extracts the detailed location data
            
            Args:
                camera: beautiful soup's html element that contains the information of one camera

            Return:
                desc: the extracted detailed location data
        """
        soup_desc = self.get_soup(self.home_url + camera.get('href'))
        desc = soup_desc.find("b", class_="h1").text
        
        return desc

    def get_city(self, camera):
        """ Extract the city name abou one camera

            The argument camera is one element containing information about one camera.
            This function extracts the city name of the camera
            
            Args:
                camera: beautiful soup's html element that contains the information of one camera

            Return:
                token: the extracted city name
        """
        city = self.get_token(camera, '<b>', '<').strip()

        return city

    def get_cam_id(self, img_src):
        cam_id = self.get_token(img_src, "original/", ".jpg")

        return cam_id
    
    def get_token(self, camera, front, end):
        """ extract the substring between <front> and <end> string
            
            The str(camera) contains html string about one camera
            This function extract the substring between <front> and <end> string

            Args:
                camera: beautiful soup's html element that contains the information of one camera
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

    def print_geocoord(self):
        """ return the location information of the camera

            when moved to the location webpage, it has the latitude and longitude information in degree/minute/second format
            extract it, convert it into the decimal format, and return it

            Sometimes, the find_element_by_xpath cannot find the element we want.
            In that situation, try print_geocoord_help to find it in another way

            Return:
                lat: latitude of the camera
                lon: longitude of the camera

            Raises:
                UnexpectedAlertPresentException: it occurs when a ramdom alert dialog pops up
                TimeoutException: it occurs when the wait.until() can't find the element we want
        """
        try:
            # wait until the element is loaded AND get the location information in dms format
            self.wait.until(lambda driver: self.driver.find_element_by_xpath("//div[@style='width: 180px; border: 1px solid black; background-color: white; color: black; text-align: center; font: 12px Arial,sans-serif; padding: 1px 3px; z-index: 0; position: absolute; top: 0px; right: 0px;']"))
            time.sleep(0.5)
            dms = self.driver.find_element_by_xpath("//div[@style='width: 180px; border: 1px solid black; background-color: white; color: black; text-align: center; font: 12px Arial,sans-serif; padding: 1px 3px; z-index: 0; position: absolute; top: 0px; right: 0px;']").text

            # convert the dms format into the decimal format
            lat, lon = self.convert_DMS_to_decimal(dms)

            return lat, lon

        except UnexpectedAlertPresentException:
            time.sleep(1)
            return self.print_geocoord()

        except TimeoutException:
            self.driver.refresh()
            return self.print_geocoord_help()

    def print_geocoord_help(self):
        """ do the exact same thing as the print_geocoord() does

            sometimes, the find_element_by_xpath can't find the element
            for this reason, try to find the element in another way

            Return:
                lat: latitude of the camera
                lon: longitude of the camera

            Raises:
                UnexpectedAlertPresentException: it occurs when a ramdom alert dialog pops up
        """
        try:
            # wait until the element is loaded AND get the location information in dms format
            self.wait.until(lambda driver: self.driver.find_element_by_class_name("gm-style"))
            div_container = self.driver.find_element_by_class_name("gm-style")
            divs = div_container.find_elements_by_xpath("./div")
            dms = divs[7].text

            # convert the dms format into the decimal format
            lat, lon = self.convert_DMS_to_decimal(dms)

            return lat, lon

        except UnexpectedAlertPresentException:
            time.sleep(1)
            return self.print_geocoord_help()

    def convert_DMS_to_decimal(self, dms):
        """ converts the latitude and longitude from DMS format to decimal format

            Args:
                dms: the latitude and longitude in DMS format which extracted from the location webpage

            Returns:
                lat: the converted latitude in decimal format
                lon: the converted latitude in decimal format 
        """
        # loop through the dms to remove the unnecessary characters
        s = ""
        for char in dms:
            if char.isdigit():
                s += char
            else:
                s += " "

        # split it by the white space
        geocoord = s.split()

        # convert it into decimal format
        lat = float(geocoord[0]) + float(geocoord[1])/60 + float(geocoord[2])/3600
        lon = float(geocoord[3]) + float(geocoord[4])/60 + float(geocoord[5])/3600

        return lat, lon
    
    def main(self):
        # get parser for the homepage
        soup_home = self.get_soup(self.home_url)
        geo = Geocoding('Nominatim', None)

        i = 1

        # loop through all the categories
        for link in soup_home.find_all("a", class_="kategorie"):
            if "Traffic" in link.text:
                continue
            
            soup_cate = self.get_soup(self.home_url + link.get('href'))                                 # create parser for each category
            
            all_button_url = soup_cate.find("input", {"id" : "VERZEICHNIS-button_alle"}).get('onclick') # get the url of all_button of the category
            all_button_url = self.get_token(all_button_url, "'", "'")

            soup_cate = self.get_soup(self.home_url + all_button_url)                                   # get parser for the webpage after the all_button clicked
            soup_cate_tabs = soup_cate.find("div", {"class" : "main top"})

            # loop through all the alphabet tabs
            for tab in soup_cate_tabs.find_all("a"):
                # try to create parser. if fails, move to next alphabet tab.
                try:
                    soup_tab = self.get_soup(self.home_url + tab.get('href'))
                except:
                    continue

                # loop through all the cameras of the selected tab
                for camera in soup_tab.find_all("a", {"class" : "thumbnail"}):
                    try:
                        img_src = self.get_img_src(camera)
                        print(i, img_src)
                        i += 1
                        if "images.webcams.travel" in img_src:
                            continue

                        descrip = camera.get('title')
                        city    = self.get_city(camera)
                        cam_id  = self.get_cam_id(img_src)

                        print(img_src, descrip, city)

                        # try to get the geological information and write it into the file. if fails, move to the next camera
                        self.driver.get(self.geo_url + cam_id)
                        lat, lon = self.print_geocoord()

                        self.f.write("CH#" + city.replace(" ", "").title() + "#" + img_src + "#" + str(lat) + "#" + str(lon) + "\n")
                    except:
                        print("error")
                        traceback.print_exc()
                        continue

if __name__ == '__main__':
    SwissWebcam = SwissWebcam()
    SwissWebcam.main()
