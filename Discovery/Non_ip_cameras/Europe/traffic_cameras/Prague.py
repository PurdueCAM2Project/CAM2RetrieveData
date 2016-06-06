from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
import urllib2
import urllib
import sys
import re
import json
import time

#Written by Thomas Norling
#Will parse the cameras on the Prague traffic camera website and output urls, country, city and latitude, longitude to a text file

class Prague:
    def __init__(self):
        #Open up Firefox and the file to be written to
        self.driver = webdriver.Firefox()
        self.f = open('list_Prague', 'w')

    def gAPI(self, locat, city, link, f):
        time.sleep(0.2);
        api = "https://maps.googleapis.com/maps/api/geocode/json?address=" + locat + ", " + city + ", Czech Republic"
        api = api.replace(' ','%20')
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
        locat = 'CZ'+'#'+city.decode("utf-8")+'#'+link+'#'+string_lat+'#'+string_lng
        f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')

    def gAPI_city(self, locat, city, link, f):
        time.sleep(0.2)
        api = "https://maps.googleapis.com/maps/api/geocode/json?address=" + city + ", Czech Republic"
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
        locat = 'CZ'+'#'+city.decode("utf-8")+'#'+link+'#'+string_lat+'#'+string_lng
        f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')
    
    def getData(self):

        #Write format of output so it can be uploaded
        self.f.write("country#city#snapshot_url#latitude#longitude\n")

        #Open the Prague traffic camera website
        self.driver.get("http://www.dpp.cz/en/webcams/")
        time.sleep(2)

        titles = {} #This dictionary will be used to ensure duplicate cameras are not added more than once
        images = self.driver.find_elements_by_class_name("kamera")
        for image in images:
            url = image.find_element_by_css_selector("a").get_attribute("href")
            location = image.find_element_by_css_selector("a").get_attribute("title")
            if location in titles: #If the camera already exists in the dictionary, it has already been added and therefore the current camera should be skipped
                pass
            else:
                titles[location] = {} #Add location to dictionary

                #Clean up the location information so that the google API can obtain reliable results
                location = location.replace("TSK", "")
                location = location.replace("-", "")
                location = location.replace("VO", "")
                location = location.replace("BUS", "")
                location = location.replace("MHD", "")
                location = location.replace("DP", "")
                location = location.replace("5.", "")
                location = location.replace("web", "")
                location = location.replace("/", "")
                location = location.replace(" . ", " ")
                location = location.replace("  ", " ")
                location = location.strip()
                
                #Use the google API to obtain coordinate information
                try:
                    self.gAPI(location.encode("utf-8"), "Prague", url, self.f)
                except:
                    self.gAPI_city(location.encode("utf-8"), "Prague", url, self.f)

        self.driver.close() #Close the browser


if __name__ == '__main__':
    PragueData = Prague()

    PragueData.getData()
