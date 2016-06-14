"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for Germany Traffic Camera website http://www.svz-bw.de/ 
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : June 14 2016
Description          : Parse cameras on Germany Traffic Camera website
Command to run script: python Germany_svz.py
Usage                : N/A
Input file format    : N/A
Output               : list_germany_traffic
Note                 : No single camera is parsed because every camera fails on Geocoding
Other files required by : It requires Selenium to be installed
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.svz-bw.de/verkehrskameras.html#filter_bereich=ALL&filter_strasse=ALL&showresult=1&
In database (Y/N)    : N
Date added to Database : 
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

class Germany:
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://www.svz-bw.de/"
        self.traffic_url = "http://www.svz-bw.de/verkehrskameras.html#filter_bereich=ALL&filter_strasse=ALL&showresult=1&"
        self.country = "DE"
        self.state = ""

        # open web browser for selenium
        self.driver = webdriver.Firefox()

        # open the file to store the list and write the format of the list at the first line
        self.f = open('list_germany_traffic', 'w')
        self.f.write("city#country#state#snapshot_url#latitude#longitude" + "\n")

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
            token = ""

        return token

    def get_desc(self, location):
        """ Get the description AND city name of the given location
            
            The location contains street name, location name, and sight name of one camera
            This function extracts them from the location string

            Args:
                location: string that contains street name, location name, and sight name of one camera

            Return:
                desc: description of location about one camera
                sight: city name of location about one camera
        """
        location = location.encode("UTF-8")

        street = self.get_token(location, "e:", "Standort").strip()
        locat = self.get_token(location, "Standort:", "Blickrichtung").strip()
        sight = self.get_token(location, "Blickrichtung:", "").strip()

        desc = street + " " + locat + " " + sight

        return desc, sight
    
    def main(self):
        # get parser for the homepage
        variable = Geocoding('Nominatim', None)
        self.driver.get(self.traffic_url)
        time.sleep(1)

        # click the view_all button to see all cameras
        view_all = self.driver.find_element_by_id("showAll")
        view_all.click()
        time.sleep(1)

        # get all Selenium elements of each camera
        table = self.driver.find_element_by_id("cam_result_table")
        cams = table.find_elements_by_tag_name("tr")

        for i in range(len(cams)):
            # skip the first row of table because it contains category name of each column
            if i == 0:
                continue

            # get the descrip and city name of a camera
            location = cams[i].find_elements_by_tag_name("td")[1].text
            descrip, city = self.get_desc(location)

            print(i, descrip, city)

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
