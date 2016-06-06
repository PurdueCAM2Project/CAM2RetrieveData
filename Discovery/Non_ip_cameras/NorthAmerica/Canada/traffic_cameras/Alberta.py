""" 
--------------------------------------------------------------------------------
Descriptive Name     : Alberta.py
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu
Date                 : June 2, 2016
Description          : Parse cameras on the 511 Alberta traffic camera website
Command to run script: python Alberta.py
Output               : output urls, country, city and latitude, longitude to a 
                       textfile <list_Alberta>
Other files required by : N/A
this script and where 
located
----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://511.alberta.ca/cameras/
In database (Y/N)    : Y
--------------------------------------------------------------------------------
"""
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
#Will parse the cameras on the 511 Alberta traffic camera website and output urls, country, city and latitude, longitude to a text file

class Alberta:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.f = open('list_Alberta', 'w')

    def gAPI(self, locat, city, link, f):
        time.sleep(0.2);
        api = "https://maps.googleapis.com/maps/api/geocode/json?address=" + locat + ", " + city + ", Alberta, Canada"
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
        locat = 'CA'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
        #file_lafa.write(link.encode('utf-8')+'\n')
        f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')

    def gAPI_city(self, locat, city, link, f):
        time.sleep(0.2)
        api = "https://maps.googleapis.com/maps/api/geocode/json?address=" + city + ",Alberta, Canada"
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
        locat = 'CA'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
        #locat = 'TX'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
        #file_lafa.write(link.encode('utf-8')+'\n')
        f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')
    
    def getData(self):

        #Write format of output so it can be uploaded
        self.f.write("country#city#snapshot_url#latitude#longitude\n")

        #Open the Alberta traffic camera website
        self.driver.get("http://511.alberta.ca/cameras/")

        option = Select(self.driver.find_element_by_id("highway_dropdown")) #"option" is the dropdown menu object on the page which allows the user to select a highway
        numOption = len(self.driver.find_elements_by_tag_name("option")) #count the number of options on the dropdown menu
        countOption = 0 #iteration variable for the dropdown menu

        #iterate through each option on the dropdown menu
        while countOption < numOption:
            option = Select(self.driver.find_element_by_id("highway_dropdown")) #Need to do this again as the page will be "new" each time you reach this statement
            option.select_by_index(countOption) #Select the option that corresponds to the current count
            time.sleep(1.5) #Ensure the page has loaded
            cameras = self.driver.find_elements_by_css_selector(".thumbnail.thumbnail-camera") #Returns a list of the camera links on the page
            numCam = len(cameras) #counts the number of cameras (includes hidden cameras, i.e. cameras under other options on the dropdown)

            countCam = 0 #iteration variable for the cameras

            #iterate through each camera on the page
            while countCam < numCam:
                cameras = self.driver.find_elements_by_css_selector(".thumbnail.thumbnail-camera") #Need to do this again as the page will be "new" each time you reach this statement
                if cameras[countCam].is_displayed(): #Only perform the following actions on cameras that are currently displayed on the page
                    cameras[countCam].click() #Click a camera
                    time.sleep(1) #Ensure the page loads

                    location = self.driver.find_element_by_xpath("//div[@class = 'panel-title']/h4").text #Extract location data from the header
                    city = self.driver.find_element_by_xpath("//div[@class = 'panel-title']/h4/small").text #City information seems to be in the small text in the header
                    location = location.replace(city, "") #Remove the city from the location so we have two seperate variables for location and city
                    city = city.replace("Near", "") #Remove the word "Near" from the city variable

                    if city == "": #If there is no city, make the location the city
                        city = location
                        location = ""
    
                    #Each camera page has one or more camera angles. Sometimes they show up vertically on the left hand side and sometimes underneath the image. The following checks both conditions
                    countAngles = 0 #Control variable
                    try:
                        thumbnail = self.driver.find_elements_by_css_selector(".thumbnail") #Find all the angles on the camera page
                        if(len(thumbnail) == 0): #If there is only one image, raise an exception to move to the except state
                            raise Exception('one image')

                        for angles in thumbnail: #Iterate through each camera angle
                            countAngles += 1 #Count the number of camera angles
                            angles.click() #Click each angle
                            time.sleep(1) #Allow time for the image to load
                            url = urllib.quote(self.driver.find_element_by_xpath("//div[@id = 'displayImageContainer']/img").get_attribute("src"), safe = '?,=/&') #Extract the URL information from the image
                            try:
                                self.gAPI(location, city, url, self.f) #Try to find GPS coordinates with location and city
                            except Exception("Location not found") as e:
                                self.gAPI_city(location, city, url, self.f) #If the above failed, find GPS coordinates through city only
    
                    except Exception as e:
                        try:
                            thumbnail = self.driver.find_elements_by_css_selector(".thumbnail.thumbnail-horizontal") #Find all the angles on the camera page
                            if(len(thumbnail) == 0): #If there is only one image, raise an exception to move to the except state
                                raise Exception('one image')

                            for angles in thumbnail: #Iterate through each camera angle
                                countAngles += 1 #Count the number of camera angles
                                angles.click() #Click each angle
                                url = urllib.quote(self.driver.find_element_by_xpath("//div[@id = 'displayImageContainer']/img").get_attribute("src"), safe = '?,=/&') #Extract the URL information from the image
                                try:
                                    self.gAPI(location, city, url, self.f) #Try to find GPS coordinates with location and city
                                except Exception("Location not found") as e:
                                    self.gAPI_city(location, city, url, self.f) #If the above failed, find GPS coordinates through city only
    
                        except Exception as e:
                            if (countAngles == 0): #If there is only one image on the page, don't click through the angles and only find url for the one
                                url = urllib.quote(self.driver.find_element_by_xpath("//div[@id = 'displayImageContainer']/img").get_attribute("src"), safe = '?,=/&') #Extract the URL information from the image
                                try:
                                    self.gAPI(location, city, url, self.f) #Try to find GPS coordinates with location and city
                                except Exception("Location not found") as e:
                                    self.gAPI_city(location, city, url, self.f) #If the above failed, find GPS coordinates through city only

                    self.driver.back() #Go back to the camera selection page and choose another camera or a new highway from the dropdown
                    time.sleep(1.5) #Allow the page to load
                countCam += 1 #Increment the camera iteration variable
            countOption += 1 #Increment the dropdown menu iteration variable
        self.driver.close() #Close the browser


if __name__ == '__main__':
    AlbertaData = Alberta()

    AlbertaData.getData()
