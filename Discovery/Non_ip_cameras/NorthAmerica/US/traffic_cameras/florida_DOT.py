"""
--------------------------------------------------------------------------------
Descriptive Name     : Florida_DOT.py 
Author               : Pongthip Srivarangkul
Contact Info         : psrivara@purdue.edu
Date Written         :  June 13, 2016
Description          : Parse cameras on Florida traffic camera
Command to run script: python Florida_DOT.py
Usage                : Run on operating system with requests, bs4 and re installed
Input file format    : (eg. url#description (on each line))
Output               : (eg. <file name> or <on screen>)
Note                 :
Other files required by : N/A
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://fl511.com/Cameras.aspx
In database (Y/N)    :
Date added to Database :
--------------------------------------------------------------------------------
"""
import geopy
from geopy.geocoders import GoogleV3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import urllib
import sys
import re
import json
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def scrapingFL():
    # setup
    fo = open("list_FL.txt", "w")
    # writing the header to the file
    fo.write("country#state#city#snapshot_url#latitude#longitude\n")
    driver = webdriver.Firefox()
    driver.get("http://fl511.com/Cameras.aspx")
    geolocator = GoogleV3("")
    # find elements in a page
    for p in xrange(1, 203):
        # printing page number
        print("        p." + str(p))
        for x in xrange(2, 12):
            try:
                #printing the order of the picture
                print("----" + str(x - 1))
                #getting the highway name
                highway = driver.find_element_by_xpath(
                    "//*[@id='MainContent_MainContent_CameraGridView']/tbody/tr[" + str(x) + "]/td[3]")
                #getting the county name
                county = driver.find_element_by_xpath(
                    "//*[@id='MainContent_MainContent_CameraGridView']/tbody/tr[" + str(x) + "]/td[2]")
                try:
                    image = driver.find_element_by_id("MainContent_MainContent_CameraGridView_ImageImage_" + str(x - 2))
                except NoSuchElementException:
                    #waiting for the Firefox to load
                    time.sleep(0.5)
                    continue
                #Printing to Screen is intended for debuging and mornitoring purposes only
                print(highway.text)
                print(county.text)
                citywant = county.text
                url = image.get_attribute("src")
                print(url)
                location = geolocator.geocode(highway.text + " " + county.text + "Florida")
                print(location.latitude, location.longitude)
                # waiting for the Firefox to load
                time.sleep(0.5)
            except StaleElementReferenceException:
                #showing which kind of error to the screen
                print("->>>>>>>>>--------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-__-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ Stale Error is here")
                continue
            except AttributeError:
                # showing which kind of error to the screen
                print(
                "->>>>>>>>>--------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-__-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_    AttributeError is here")
                continue
            except geopy.exc.GeocoderServiceError:
                # showing which kind of error to the screen
                print(
                    "->>>>>>>>>--------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-__-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_     Geopy error")
                continue
            except : # catch *all* exceptions:
                # showing which kind of error to the screen
                print(
                    "->>>>>>>>>--------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-__-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_      others error")
                continue
            fo.write("USA#FL#")
            try :
                # priting city name
                fo.write(citywant + "#")
            except StaleElementReferenceException:
                #showing the error
                fo.write("--------------------------------------------------------------------------------------------------------------->>>>>>\n")
                continue
            fo.write(url + "#" + str(location.latitude) + "#" + str(location.longitude) + "\n")
        # Search for the nextBotton... We will do it untill we found it.
        while True:
            try :
                nextBotton = driver.find_element_by_id("MainContent_MainContent_CameraGridView_NextLinkButton")
                nextBotton.click()
            except StaleElementReferenceException:
                time.sleep(0.5)
                continue
            break
        # wait for the browser to load
        time.sleep(4)
    driver.close()


if __name__ == '__main__':
    scrapingFL()
