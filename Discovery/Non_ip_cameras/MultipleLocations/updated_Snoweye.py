###############################################################################
# Descriptive Name for File: Snoweye website parser
#
# Written by: Thomas Norling									      
# Contact Info: thomas.l.norling@gmail.com
#
# URL of website being parsed: Snoweye.com
# Command to Run Script: python Snoweye.py
# Other files required by this script and where located: None
#
# Description:
#   This parsing script will first call the Navigate function which is designed
#   to navigate the website by clicking the tabs and drilling down into each
#   sub-tab until it reaches a page of cameras. When a page is loaded, the getData
#   function is called where the script then checks to see whether or not each 
#   camera has a button to see more cameras, if it does that button is clicked
#   and a new page is loaded. If this is the case, getMoreData is called and 
#   the location data is used to call gAPI where the location is plugged into
#   the google API and it will attempt to find the latitude and longitude 
#   coordinates. If they are found, the information is written to the file.
#   If there is no "more" button the script stays in getData and the same process
#   is used to try to find coordinates and write to a file. When all cameras
#   on the page have been parsed the script returns to the Navigate function where
#   it navigates to a new page of cameras and the process repeats until all cameras
#   have been parsed.
#
#   Note: This script uses the geopy library to perform the geocoding on the 
#   addresses given. Geopy is not installed on the development server as of this 
#   writing. This will not run on the development machine and thus will need to 
#   be run on a machine with geopy installed.
#
#   Also Note: There are more cameras on this website than can be parsed in one 
#   day with the google API. You will need to either use several geocoders or 
#   parse different sections of the website on different days. In order to parse
#   on multiple days update the countTabs variable in the Navigate function to
#   the tab number where you last parsed cameras so that the script will start
#   on that tab rather than from the beginning.
#
#
#
#
# DO NOT PUT USERNAMES/PASSWORDS IN CODE
###############################################################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
import urllib2
import urllib
from geopy.geocoders import GoogleV3
import sys
import re
import json
import time


class Snoweye:
    def __init__(self):
        #Open up Firefox and the file to be written to
        self.driver = webdriver.Firefox()
        self.f = open('list_Snoweye.txt', 'w')
        self.g = open('list_Snoweye_US.txt', 'w')

    def gAPI(self, locat, region, main_location, country, link, f, g):
        time.sleep(0.2);
        geolocator = GoogleV3(api_key = 'AIzaSyDRb6HaVtHDbpHkJq8a3MEODFZlmkBt7f4')
        if country != 'USA':
            try:
                searchTerm = str(locat + region + ',' + country)
                location = geolocator.geocode(searchTerm)
            except:
                searchTerm = str(main_location + ',' + country)
                location = geolocator.geocode(searchTerm)
            extractCity = location.raw['address_components'] #Get the raw JSON information so that the city name can be extracted
            city = locat
            for item in extractCity:
                types = item['types']
                if types[0] == "locality":
                    city = item['long_name']
            locat = country+'#'+str(city).decode("utf-8")+'#'+link+'#'+str(location.latitude)+'#'+str(location.longitude)
            f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')
        else:
            try:
                searchTerm = str(locat + region + ',' + main_location)
                location = geolocator.geocode(searchTerm)
            except:
                raise Exception
            extractCityState = location.raw['address_components'] #Get the raw JSON information so that the city name can be extracted
            city = locat
            state = ""
            for item in extractCityState:
                types = item['types']
                if types[0] == "locality":
                    city = item['long_name']
                elif types[0] == "administrative_area_level_1":
                    state = item['short_name']
            if state == "":
                raise Exception('No State!')
            locat = 'USA#'+str(state)+'#'+str(city).decode("utf-8")+'#'+link+'#'+str(location.latitude)+'#'+str(location.longitude)
            g.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')

    
    def Navigate(self):

        #Write format of output so it can be uploaded
        self.f.write("country#city#snapshot_url#latitude#longitude\n")
        self.g.write("country#state#city#snapshot_url#latitude#longitude\n")

        #Open the Snoweye Ski camera website
        self.driver.get("http://www.snoweye.com")
        time.sleep(2)

        #Find the country tabs and count them
        tabs = self.driver.find_elements_by_xpath("//div[@id = 'menu']/ul/li")
        numTabs = len(tabs)

        #Start with the first country tab (Home tab is at index 0)
        countTabs = 1
        while countTabs < numTabs:
            #Find the tab elements again as this needs to be found each time the page changes or refreshes
            tabs = self.driver.find_elements_by_xpath("//div[@id = 'menu']/ul/li")
            #Find the sub-page menu items
            pages = tabs[countTabs].find_elements_by_xpath(".//ul/li")
            numPages = len(pages)

            #Reset the count to 0 each time a new tab is clicked
            countPages = 0

            while countPages < numPages:
                #Find the tab and page elements again as these need to be found each time the page changes or refreshes
                tabs = self.driver.find_elements_by_xpath("//div[@id = 'menu']/ul/li")
                pages = tabs[countTabs].find_elements_by_xpath(".//ul/li")
                
                #Get the country code information from the tab id and if it returns blank, get it from the page id
                try:
                    country = tabs[countTabs].get_attribute("id")
                except:
                    country = ""

                if country == "":
                    try:
                        country = pages[countPages].get_attribute("id")
                    except:
                        country = ""
                country = country[:2] #Trim the country code to only the first 2 characters
                if country == "us": 
                    country = "usa" #Turn "us" into "usa"
                country = country.upper() #Uppercase country code
                print "country = " + country
                
                try: #If the page menu item has other sub-pages, iterate through these as well
                    subPages = pages[countPages].find_elements_by_xpath(".//ul/li")
                    numSubPages = len(subPages)
                    if numSubPages == 0: #If there are no sub-pages force except statement
                        raise Exception('No Sub Pages')
                    
                    countSubPages = 0
                    while countSubPages < numSubPages:
                        #Find the tab, page and subpage elements each time the page changes or refreshes
                        tabs = self.driver.find_elements_by_xpath("//div[@id = 'menu']/ul/li")
                        pages = tabs[countTabs].find_elements_by_xpath(".//ul/li")
                        subPages = pages[countPages].find_elements_by_xpath(".//ul/li")

                        #Navigate to the desired page
                        tabs[countTabs].click()
                        time.sleep(1)
                        pages[countPages].click()
                        time.sleep(1)
                        subPages[countSubPages].click()
                        time.sleep(1)
                        #Get the data from the page by calling function
                        self.getData(country) 
                    
                        countSubPages += 1
                        
                    countPages += numSubPages
                except Exception as e: #Page element does not have sub-page elements
                    #Navigate to the desired page
                    print e
                    tabs[countTabs].click()
                    time.sleep(1)
                    pages[countPages].click()
                    time.sleep(1)
                    #Get the data from the page by calling function
                    self.getData(country)
                time.sleep(2)
                countPages += 1
            countTabs += 1
                    
        
        self.driver.close() #Close the browser

    def getData(self, country):
        
        mainLocation = self.driver.find_element_by_tag_name("h1").text #Save the overall area information from the header
        cameras = self.driver.find_elements_by_class_name("cambox") #Find the camera elements
        numCams = len(cameras) - 2 #Subtracting 2 accounts for the 2 advertisements at the end of the page

        countCams = 0

        while countCams < numCams:
            #Find the camera elements again, as this needs to be found each time the page changes or refreshes
            cameras = self.driver.find_elements_by_class_name("cambox")
            try: 
                #Make sure what you are trying to find the information for is not an advertisement
                advert = cameras[countCams].find_element_by_class_name("camboxadwide")
            except:
                try:
                    #If there is a more button click it
                    more = cameras[countCams].find_element_by_class_name("more")
                    more.click()
                    time.sleep(2)
                    #Get the data from the other data extracting function
                    self.getMoreData(country, mainLocation)
                    self.driver.back()
                    time.sleep(1.5)
                except:
                    #Get the url information
                    try:
                        url = urllib.quote(cameras[countCams].find_element_by_class_name("fancybox").get_attribute("href"), safe = '?:,=/&')
                    except:
                        url = urllib.quote(cameras[countCams].find_element_by_tag_name("img").get_attribute("src"), safe = '?:,=/&')
                    regex = re.match('^.+\.jpg$', url) #Ensure the image is a jpg, some images are not and cannot be parsed into our website
                    if regex is not None:
                        resort = cameras[countCams].find_element_by_class_name("resort").text #Get location information
                        try:
                            region = cameras[countCams].find_element_by_class_name("region").text #Get secondary location information if available, otherwise leave blank
                        except:
                            region = ""

                        try:
                            self.gAPI(resort.encode("utf-8"), region.encode("utf-8"), mainLocation.encode("utf-8"), country.encode("utf-8"), url, self.f, self.g) #Try to find location
                        except Exception as e:
                            print("Failed") #Print a message for each location that was not found through the google API
                            print e
                            print(resort.encode("utf-8"), region.encode("utf-8"))
                    else:
                        pass

            countCams += 1 
        self.driver.refresh() #Refresh when done so that the next tab can be clicked
        time.sleep(1)

    def getMoreData(self, country, mainLocation):
        
        cameras = self.driver.find_elements_by_class_name("cambox-resort") #Find the camera elements
        numCams = len(cameras) - 2 #Subtracting 2 accounts for the 2 advertisements at the end of the page
        countCams = 0

        while countCams < numCams:
            cameras = self.driver.find_elements_by_class_name("cambox-resort") #Find the camera elements each time the page changes or refreshes
            try: #Get the url information
                url = urllib.quote(cameras[countCams].find_element_by_class_name("fancybox").get_attribute("href"), safe = '?:,=/&')
            except:
                url = urllib.quote(cameras[countCams].find_element_by_tag_name("img").get_attribute("src"), safe = '?:,=/&')
            regex = re.match('^.+\.jpg$', url) #Only use jpgs
            if regex is not None:
                resort = cameras[countCams].find_element_by_class_name("resort").text #Get location information
                try:
                    region = cameras[countCams].find_element_by_class_name("region").text #Get secondary location information if available
                except:
                    region = ""

                try:
                    self.gAPI(resort.encode("utf-8"), region.encode("utf-8"), mainLocation.encode("utf-8"), country.encode("utf-8"), url, self.f, self.g) #Try to find location
                except Exception as e:
                    print("Failed") #Print a message for each location that was not found through the google API
                    print e
                    print(resort.encode("utf-8"), region.encode("utf-8"))
            else:
                pass

            countCams += 1

if __name__ == '__main__':
    SnoweyeData = Snoweye()

    SnoweyeData.Navigate()
