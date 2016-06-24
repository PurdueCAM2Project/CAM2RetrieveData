"""
--------------------------------------------------------------------------------
Descriptive Name     : Parsing Script for Wisconsin Traffic Cameras
Author               : Thomas Norling (based off a script written by Otavio De Moraes Neto)							      
Contact Info         : thomas.l.norling@gmail.com
Date                 : June 8, 2016
Description          : Script uses selennium to acquire links to the images
Command to run script: python WI.py
Usage                : 
Input file format    : N/A
Output               : list_WI
Note                 : This script uses the geopy library to perform the geocoding on the 
                       addresses given. Geopy is not installed on the development server 
                       as of this writing. This will not run on the development machine 
                       and thus will need to be run on a machine with geopy installed.
Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.511wi.gov/web/traffic/cameras.aspx
In database (Y/N)    : Y
--------------------------------------------------------------------------------
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from geopy.geocoders import GoogleV3
import urllib2
import urllib
import sys
import re
import json
import time

def main():
    driver = webdriver.Firefox()
    driver.get("http://www.511wi.gov/web/traffic/cameras.aspx")
    driver.implicitly_wait(15)
    time.sleep(2)
    f = open ('list_WI.txt','w')
    #Format of output
    att = []
    ls = []
    lat = []
    lon = []
    locat = " "
    hwy = " "
    city = " "
    count = 0
    j = 0
    
    #Write format of output so it can be uploaded
    f.write("country#state#city#snapshot_url#latitude#longitude\n")
    
    
    #Loop used to stop when there is no more next buttons to click
    while(j == 0):
        #Resets Attribute list
        del att[:]
        #Creates attribute list from the current list of cameras, trys so there are no errors at the end of the list
        try:
            for v in driver.find_elements_by_xpath("//*[starts-with(@id, 'ctl00_ctl00_ctl00_ContentPlaceHolder_Column2PlaceHolder_ListPlaceHolder_ListGridView_ctl')]"):
                att.append(v.text)
        except:
            m = 0
        
        count = 0
        i = driver.find_elements_by_class_name('cctv')
        num_images = len(i)
        while count < num_images:
            b = 1
            i = driver.find_elements_by_class_name('cctv')
            try:
                link = i[count].get_attribute('src')
                print link
            except Exception as w:
                b = 0
                print "Image link isn't up"
            
            if b == 1:
                city = att[count * 4]
                locat = att[(4*count) + 2]
                locat = locat.replace("WIS", "Hwy")
                locat = locat.replace("@", "and")
                locat = locat.replace("at", "and")
                hwy = att[(4*count) + 1]
                hwy = hwy.replace("WIS", "Hwy")
                print city + " " + hwy + " " + locat
                try:
                    gAPI(locat, hwy, city, link, f)
                except Exception as e:
                    print e
                    print "Error generating location information"
            count += 1
        #Catches when it reaches the end of the list of cameras
        try:
            driver.find_element_by_link_text('Next').click()
        except NoSuchElementException:
            j = 1
            break;
        driver.implicitly_wait(30)
        time.sleep(6)
    driver.close();
    return;

def gAPI(locat,hwy, city, link, f): #Location is discription ,city, link is to URL, f is file
    time.sleep(0.2);
    geolocator = GoogleV3()
    try:
        searchTerm = str(locat + ',' + city + ', WI, US') #Search for location and city
        location = geolocator.geocode(searchTerm)
    except:
        try:
            searchTerm = str(hwy + ',' + city + ', WI, US') #Search for hwy and city
            location = geolocator.geocode(searchTerm)
        except:
            searchTerm = str(city + ', WI, US') #Search for only city
            location = geolocator.geocode(searchTerm)

    extractCity = location.raw['address_components'] #Get the raw JSON information so that the city name can be extracted
    for item in extractCity:
        types = item['types']
        if types[0] == "locality":
            city = item['long_name']
# print locat, hwy, city
# print location.latitude, location.longitude
    locat = 'USA'+'#'+'WI'+'#'+str(city)+'#'+link+'#'+str(location.latitude)+'#'+str(location.longitude)
    f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')
    return;


main()
