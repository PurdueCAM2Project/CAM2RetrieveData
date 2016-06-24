"""
--------------------------------------------------------------------------------
Descriptive Name     : BBC Traffic Cameras
Author               : Ryan Dailey                                   
Contact Info         : dailey1@purdue.edu
Description          : This script creates a file that holds the title,url,latitude,longitude,country, and city seperated by #
Command to run script: Python BBC_UK.py
Input file format    : This script takes in a file named "BBC_JSON_LIST" which is a list of JSon files associated with the camera data.
                       This was found manually by loading the page and monitering for JSon files. 
Output               : UK_BBC_list
Note                 :
Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : https://www.bbc.co.uk/travel/northwestwales/incidents/road
In database (Y/N)    : Yes 
--------------------------------------------------------------------------------
Contents of BBC_JSON_LIST:

gcx.json
gcw.json
gcy.json
u12.json
gcr.json
gcq.json
gcm.json
gct.json
gcj.json
gcn.json
gbu.json
gbg.json
gch.json
gbv.json
gcp.json
u10.json
u12.json
u13.json
gby.json
gbw.json
gcd.json
gce.json
gcv.json
gcg.json
gcu.json
gf7.json
gfk.json
gf5.json
gfh.json
gfj.json
gck.json
gcz.json
--------------------------------------------------------------------------------
"""
from bs4 import BeautifulSoup
import urllib2
import re
import sys
import time
import json
from Geocoding import Geocoding

def uk():
    # Map URL : https://www.bbc.co.uk/travel/northwestwales/incidents/road
    jason_url = 'https://travel.files.bbci.co.uk/travel-tcam-parser/live/map-cells/'
    camera_url = "https://ichef.bbci.co.uk/traveluk/provider/cam_id/large"
    
    # Opens a list of files that contain the camera info json files on the bbc website 
    f_list = open('BBC_JSON_LIST','r')
    files = list(f_list)
    f_list.close()

    # create and open a file named UK_ls to write as output
    f = open('list_UK_BBC.txt','wb')

    # Define Geocoder
    GAPI = Geocoding("Google", "None")
    API_num = 0 # Keeps track of which key we are using

    f.write("description#snapshot_url#latitude#longitude#country#city\n")
    print "Running UK_BBC..."
    # After making a list of files that hold the GPS information and camera data manually by going through the website and putting the URL's in a file 
    # we parse the jason and extract the information we need before sending it to the GAPI to get the city and country information as it is not in the Json file
    for onefile in files:
        try:
            response = urllib2.urlopen(jason_url + onefile.replace("\n", "")).read()
        except:
            print("\"%s\" did not load" % onefile.replace("\n", ""))
            pass
        
        parsed_json= json.loads(response)
        for camera in parsed_json:
            cam_id = camera['id']
            provider = camera['provider']
            title = camera['title']
            latitude = str(camera['latitude'])
            longitude = str(camera['longitude'])
            url = camera_url.replace("provider/cam_id", provider+"/"+cam_id)
            try:
                GAPI.reverse(latitude, longitude)
                city = str(GAPI.city)
                country = str(GAPI.country)
                if len(city) == 0 or len(country) == 0:
                    raise Exception('City or Country Not Found!')
                    pass
                f.write(title+"#"+url+"#"+str(latitude)+"#"+str(longitude)+"#"+country+"#"+city+"\n") # Write all the data to the text file
            except Exception as error:
                if str(error) == "Your request was denied.":
                    print("Over GAPI limit, switching to API"+str(API_num + 1))
                    API_num = API_num + 1
                    if API_num == 1:
                        GAPI = Geocoding("Google", "AIzaSyC96cLzfPJJU6JJ9fzJ1kXykB6GMpb9fN4")
                    elif API_num == 2:
                        GAPI = Geocoding("Google", "AIzaSyCmrSFG2GCAnTKh7EtY0obD4_YnwSbjGxQ")
                    elif API_num == 3:
                        GAPI = Geocoding("Google", "AIzaSyDRb6HaVtHDbpHkJq8a3MEODFZlmkBt7f4")
                    else:
                        print "<<<ERROR:"+str(error)+">>>"
                        print "API list exhausted, stopped on:"
                        print title+"#"+url+"#"+str(latitude)+"#"+str(longitude)+"#"+"ERROR"+"#"+"ERROR"
                        return
                else:
                    print "<<<Error:"+str(error)+">>>"+" For:\n"+title+"#"+url+"#"+str(latitude)+"#"+str(longitude)+"#"+"ERROR"+"#"+"ERROR"
            pass

    f.close()             
              
if __name__ == '__main__':
    uk()    
