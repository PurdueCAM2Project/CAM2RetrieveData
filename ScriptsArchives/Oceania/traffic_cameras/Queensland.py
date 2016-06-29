# encoding=utf8
""" 
--------------------------------------------------------------------------------
Descriptive Name     : Queensland.py
Author               : Shengli Sui								      
Contact Info         : ssui@purdue.edu
Date Written         : June 29,0216
Description          : Parse cameras on the Queensland, AUS traffic camera website
Command to run script: python Queensland.py
Output               : list_Queensland.txt
Note                 : 
Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.tmr.qld.gov.au/Traffic-cameras-by-location.aspx
In database (Y/N)    : Y
Date added to Database : June 29, 2016
--------------------------------------------------------------------------------
"""
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
import urllib
import urllib2

import re
import json
import time
import codecs



class Brisbane:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.f = open('list_Queensland.txt', 'w')
    
    def gAPI(self, locat, city, link, f):
        time.sleep(0.2);
        api = "https://maps.googleapis.com/maps/api/geocode/json?address=" + locat + ", " + city + ",Queensland, Australia"
        api = api.replace(' ','')
        ''' use API to find the latitude and longitude'''
        response = urllib2.urlopen(api).read()
        #load by json module
        parsed_json= json.loads(response)
        content= parsed_json['results']
        #extract latitude and longitude from the API json code
        loc= content[0]
        geo = loc['geometry']
        location2 = geo['location']
        lat = location2['lat']
        lng = location2['lng']
        #change lat and lng to string
        string_lat = str(lat)
        string_lng = str(lng)
        #print string_lat,string_lng
        locat = 'AU'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
        f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')
    
    def gAPI_city(self, locat, city, link, f):
        time.sleep(0.2)
        api = "https://maps.googleapis.com/maps/api/geocode/json?address=" + city + ",Queensland, Australia"
        api = api.replace(' ','')
        ''' use API to find the latitude and longitude'''
        response = urllib2.urlopen(api).read()
        #load by json module
        parsed_json= json.loads(response)
        content= parsed_json['results']
        #extract latitude and longitude from the API json code
        loc= content[0]
        geo = loc['geometry']
        location2 = geo['location']
        lat = location2['lat']
        lng= location2['lng']
        #change lat and lng to string
        string_lat = str(lat)
        string_lng = str(lng)
        #print string_lat,string_lng
        locat = 'AU'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
        f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')
    
    def getData(self):
        self.driver.get("http://www.tmr.qld.gov.au/Traffic-cameras-by-location.aspx")
        place=self.driver.find_elements_by_css_selector("a[href*='/Traffic-cameras-by-location/Traffic-cameras.aspx?region']")
        numplace=len(place)
        countplace=0
        while countplace<numplace:
            place=self.driver.find_elements_by_css_selector("a[href*='/Traffic-cameras-by-location/Traffic-cameras.aspx?region']")
            place[countplace].click()
            time.sleep(0.5)
            cam=self.driver.find_elements_by_css_selector("a[href*='/Traffic-cameras-by-location/Traffic-cameras?region']")
            numcamera=len(cam)
            countcamera=0
            while countcamera<=numcamera:
                camera=self.driver.find_elements_by_css_selector("a[href*='/Traffic-cameras-by-location/Traffic-cameras?region']")
                
                camera[countcamera].click()
                time.sleep(0.5)
                img=self.driver.find_element_by_id("camTCImage")
                url=img.get_attribute("src")
                location=self.driver.find_element_by_xpath("//div[@id = 'camDetails']/h2").text
                
                if len(location.split('-'))!=1:
                    location = location.split('-')
                    city=location[0]
                    loc = location[1]
                
                elif len(location.split('–'))!=1:
                    #location = self.driver.find_element_by_xpath("//div[@id = 'camDetails']/h2").text
                    location=location.split('–')
                    city=location[0]
                    loc = location[1]
                
                else:
                    #location = self.driver.find_element_by_xpath("//div[@id = 'camDetails']/h2").text
                    location=location.split()
                    city=location[0]
                    loc = str(location[1:3])
                
#                print(city)
#                print(loc)
                try:
                    self.gAPI(loc, city, url, self.f)
                except Exception("Location not found") as e:
                    self.gAPI_city(loc, city, url, self.f)
                
                countcamera+=1
            
            
            for i in range(countcamera):
                self.driver.back()
            countplace+=1
            time.sleep(1)

if __name__ == '__main__':
    BrisbaneData = Brisbane()
    
    BrisbaneData.getData()
