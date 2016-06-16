"""
--------------------------------------------------------------------------------
Descriptive Name     :  Parser for cameras in SwissWebcam website
Author               :  Sanghyun Joo
Contact Info         :  joos@purdue.edu OR toughshj@gmail.com
Date                 :  10 June 2016
Description          :  parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script:  python swissWebcam_faster.py
Usage                :  Parsing cameras in SwissWebcam website
Input file format    :  N/A
Output               :  list_SwissWebcam_faster
Note                 :  This code is much faster than swissWebcam.py but fails on Geocoding part for many cameras.
                        If you want to parse every camera with more accuracy, run swissWebcam.py
Other files required by : This code requires to install BeautifulSoup4 and Geocoding.py file from NetworkCameras/Discovery/Tools/Geocoding.py
                          It is MUCH FASTER than swissWebcam_non_traffic.py but fails to get the geo-location information of some cameras.
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       :  http://en.swisswebcams.ch
In database (Y/N)    :  N
--------------------------------------------------------------------------------
"""

# -*- coding: utf-8 -*-

import urllib
import re
from bs4 import BeautifulSoup
from Geocoding import Geocoding

class SwissWebcam:
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://en.swisswebcams.ch"
        self.traffic_url = ""
        self.country = "CH"
        self.state = ""

        # open the file to store the list and write the format of the list at the first line
        self.f = open('list_SwissWebcam_faster', 'w')
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
    
    def get_img_src(self, camera):
        """ Extract the img_src on the webpage

            The argument camera is one element containing information about one camera.
            This function extracts the image url in the <img src=""> tag.

            Args:
                camera: beautiful soup's html element that contains the information of one camera

            Return:
                img_src: the extracted image url from <img src=""> tag
        """
        img_src = camera.find("img").get('src')
        img_src = img_src.replace("toenail", "original")

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
    
    def main(self):
        # get parser for the homepage
        soup_home = self.get_soup(self.home_url)
        variable = Geocoding('Nominatim', None)

        # loop through all the categories
        for link in soup_home.find_all("a", {"class" : "kategorie"}):
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
                    img_src = self.get_img_src(camera)
                    descrip = camera.get('title')   #self.get_descrip(camera)
                    city    = self.get_city(camera)

                    print(img_src, descrip, city)

                    # try to get the geological information and write it into the file. if fails, move to the next camera
                    try:
                        variable.locateCoords(descrip, city, self.state, self.country)
                        result = variable.city.replace(" ", "").title() + "#" + variable.country + "#" + variable.state + "#" + img_src + "#" + variable.latitude + "#" + variable.longitude + "\n"
                        result = result.replace("##", "#")
                        self.f.write(result)
                    except:
                        print("can't find")

if __name__ == '__main__':
    SwissWebcam = SwissWebcam()
    SwissWebcam.main()
