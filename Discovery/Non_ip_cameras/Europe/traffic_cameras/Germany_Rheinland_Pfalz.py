""" 
--------------------------------------------------------------------------------
Descriptive Name     : Germany_Rheinland_Pfalz.py
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu
Date                 : June 6, 2016
Description          : Parse cameras on the Rheinland-Pfalz, Germany traffic camera website
Command to run script: python Germany_Rheinland_Pfalz.py
Output               : output urls, country, city and latitude, longitude to a 
                       textfile <list_Germany_Rheinland_Pfalz>

Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.verkehr.rlp.de/index.php?lang=20&menu1=50&menu2=10&menu3=
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
#Will parse the cameras on the Rheinland-Pfalz, Germany traffic camera website and output urls, country, city and latitude, longitude to a text file

class Germany_Rheinland:
    def __init__(self):
        #Open up Firefox and the file to be written to
        self.driver = webdriver.Firefox()
        self.f = open('list_Germany_Rheinland_Pfalz', 'w')

    def gAPI(self, locat, city, link, f):
        time.sleep(0.2);
        api = "https://maps.googleapis.com/maps/api/geocode/json?address=" + locat + ", " + city + ", Germany"
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
        locat = 'DE'+'#'+city.decode("utf-8")+'#'+link+'#'+string_lat+'#'+string_lng
        #file_lafa.write(link.encode('utf-8')+'\n')
        f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')

    def gAPI_city(self, locat, city, link, f):
        time.sleep(0.2)
        api = "https://maps.googleapis.com/maps/api/geocode/json?address=" + city + ", Germany"
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
        locat = 'DE'+'#'+city.decode("utf-8")+'#'+link+'#'+string_lat+'#'+string_lng
        #locat = 'TX'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
        #file_lafa.write(link.encode('utf-8')+'\n')
        f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')
    
    def getData(self):

        #Write format of output so it can be uploaded
        self.f.write("country#city#snapshot_url#latitude#longitude\n")

        #Open the Rheinland-Pfalz traffic camera website
        self.driver.get("http://www.verkehr.rlp.de/index.php?lang=20&menu1=50&menu2=10&menu3=")
        time.sleep(2)

        #webcam_info will include both the camera and description elements, the for loop below will separate them
        webcam_info = self.driver.find_elements_by_css_selector('tr[class*=webcam_]')
        
        for entry in webcam_info:
            #The webcam_as_row class contains the city descriptors
            if entry.get_attribute('class') == "webcam_as_row":
                city = entry.find_element_by_class_name("webcam_as").text

                #replace all the directional words in the city name
                city = city.replace("-", " ")
                city = city.replace("West", "")
                city = city.replace("Ost", "")
                city = city.replace("Nord", "")
                #Replace the German umlaut character so it can be found in the South directional word and removed
                city = city.replace(unichr(252), "ue")
                city = city.replace("Sued", "")
                #Put the German umlaut character back on actual city names
                city = city.replace("ue", unichr(252))
                city = city.replace("AD ", "")
                city = city.replace("AS ", "")
 
            #The webcam_img_row class contains the camera image information
            elif entry.get_attribute('class') == "webcam_img_row":
                #Get the specific location information
                location = entry.find_element_by_class_name("webcam_bab").text
                #Remove the city name from location to avoid redundance
                location = location.replace(city, "")
                #Extract the URL
                url = urllib.quote(entry.find_element_by_class_name("webcam_thumbnail_small").get_attribute("src"), safe = '?:,=/&')
                print location + " " + city + ": " + url
                
                #Try to find the coordinates through the google API
                try:
                    self.gAPI(location.encode("utf-8"), city.encode("utf-8"), url, self.f)
                except:
                    try:
                        self.gAPI_city(location.encode("utf-8"), city.encodue("utf-8"), url, self.f)
                    except:
                        pass
                    
        
        self.driver.close() #Close the browser


if __name__ == '__main__':
    RheinlandData = Germany_Rheinland()

    RheinlandData.getData()
