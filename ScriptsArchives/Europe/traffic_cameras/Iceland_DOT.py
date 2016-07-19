"""
--------------------------------------------------------------------------------
Descriptive Name     : Iceland_DOT.py
Author               : Pongthip Srivarangkul
Contact Info         : psrivara@purdue.edu
Date Written         :  June 13, 2016
Description          : Parse cameras on Florida traffic camera
Command to run script: python Iceland_DOT.py
Usage                : Run on operating system with requests, bs4 and re installed
Input file format    : (eg. url#description (on each line))
Output               : list_Iceland.txt
Note                 : This code can only parse aound 1/4 of it. 
                        Reason:
                        Reverse geocoding cannot return city name.
Other files required by : N/A
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       :http://www.road.is
In database (Y/N)    :
Date added to Database : 
--------------------------------------------------------------------------------
"""
from logging import exception
import geopy
from geopy.geocoders import GoogleV3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
import urllib
import sys
import re
import json
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import functools
from bs4 import BeautifulSoup
import time

def greater(a,b):
    if int(a.get_attribute("x")) > int(b.get_attribute("x")) :
        return 1
def getv(x):
    return int(x.get_attribute("x"))

if __name__ == '__main__':
    fo = open("list_Iceland.txt", "w")
    fo.write("country#city#snapshot_url#latitude#longitude\n")
    allinks = 0
    parsable = 0
    driver = webdriver.Firefox()
    address = ["http://vegasja.vegagerdin.is/eng/?xmin=315811&ymax=438600&xmax=419011&ymin=365280",
               "http://vegasja.vegagerdin.is/eng/?xmin=378961&ymax=435900&xmax=553861&ymin=311640",
               "http://vegasja.vegagerdin.is/eng/?xmin=488641&ymax=514920&xmax=765811&ymin=318000",
               "http://vegasja.vegagerdin.is/eng/?xmin=251581&ymax=550650&xmax=450121&ymin=409590",
               "http://vegasja.vegagerdin.is/eng/?xmin=572131&ymax=573390&xmax=790261&ymin=418410",
               "http://vegasja.vegagerdin.is/eng/?xmin=244111&ymax=670260&xmax=427501&ymin=539970",
               "http://vegasja.vegagerdin.is/eng/?xmin=383221&ymax=665370&xmax=596401&ymin=513930",
               "http://vegasja.vegagerdin.is/eng/?xmin=553951&ymax=674145&xmax=796741&ymin=501675"
               ]
    for element in address:
        driver.get(element)
        imagelist = driver.find_elements_by_tag_name("image")
        time.sleep(3)
        imagelist.sort(key = lambda x: int(x.get_attribute("x")))
        countclo = 0
        #countcli = 0
        for link in imagelist:
                try:
                    # Click Each Camera
                    link.click()
                    print(link.get_attribute("x") + " " + link.get_attribute("y") + "  clickable")
                    time.sleep(0.5)
                    try:
                        # Determine Number of Images in the Pop up
                        poptitle = driver.find_element_by_class_name("title")
                        html = poptitle.get_attribute("outerHTML")
                        soup = BeautifulSoup(html, "html.parser")
                        needtxt = soup.find("span", id = "popupVefmyndavelTitle").next_sibling
                        strtxt = str(needtxt)
                        first = strtxt.find("f ")
                        last = strtxt.find(")")
                        numimg = strtxt[first + 2:last] #number of images in a popup
                    except Exception as e:
                        print(e)
                        continue
                    #Geting Geographical Coordinates
                    action = webdriver.ActionChains(driver)
                    action.move_to_element(link)
                    geotxt =  driver.find_element_by_id("hnit").text
                    geosp = geotxt.split(", ") # geo SPlit
                    la = str(geosp[0])
                    lo = str(geosp[1])
                    latitude = float(la[0:la.index('°')]) + float(la[la.index(' ') + 1:la.index("'")]) / 60.0
                    longitude = (float(lo[0:lo.index('°')]) + float(lo[lo.index(' ') + 1:lo.index("'")]) / 60.0) * (-1)
                    print(latitude, longitude)
                    print(geosp)

                    #Geting City Name
                    geolocator = GoogleV3()
                    location = geolocator.reverse(str(latitude) + " , " + str(longitude))

                    city = ""
                    flag = 0
                    for choice in location:
                        extractCity = choice.raw['address_components']
                        for item in extractCity:
                            types = item['types']
                            #print("doing")
                            for t in types:
                                #print(str(choice) + " " + str(item) + " " + str(t))
                                if t == "locality":
                                    city = item['long_name']
                                    print("got it")
                                    flag = 1
                                    break
                            if flag == 1:
                                break
                        if flag == 1:
                            break
                    print("city : " + str(city))

                    #Getting Images Links
                    for p in range(1,int(numimg) + 1):
                        imagepop = driver.find_element_by_xpath("//*[@id='popupVefmyndavel']/img")
                        print(imagepop.get_attribute("src")) # SNAPSHOT URL
                        if city != "":
                            fo.write("IS#" + str(city) + "#" + str(imagepop.get_attribute("src")) + "#" + str(latitude) + "#" + str(longitude) + "\n")
                        # Clicking 'Next' Button
                        if p != int(numimg):
                            elementnxt = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, "//*[@id='mapDiv_root']/div[3]/div[1]/div[1]/div/div[4]")));
                            elementnxt.click();

                    #Counting links
                    allinks += int(numimg)
                    if flag == 1:
                        parsable += int(numimg)
                    # Closing Pop Up Window
                    element = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[@id='mapDiv_root']/div[3]/div[1]/div[1]/div/div[6]")));
                    element.click();
                    print("closed")
                    countclo+=1
                    time.sleep(2)
                except Exception as e:  # catch *all* exceptions
                    1+1
                    #print(e)
                    print(link.get_attribute("x") + " " + link.get_attribute("y") + "  unclickable")

        print("All links = " + str(allinks))
        print("Link with City Name = " + str(parsable))
    """
    for link in imagelist :
        try :
            print(link.get_attribute("x") + " " + link.get_attribute("y") )
            element = WebDriverWait
            link.click()
            time.sleep(4)
            print("click")
            time.sleep(4)
            closeb = driver.find_element_by_xpath("//*[@id='mapDiv_root']/div[3]/div[1]/div[1]/div/div[6]")
            closeb.click()
            time.sleep(4)
            print("close window\n")
        except Exception as e:
            #print(e)
            print("unclick")
            time.sleep(4)
            continue
    """
