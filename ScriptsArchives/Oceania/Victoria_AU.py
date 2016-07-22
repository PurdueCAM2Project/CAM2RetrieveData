"""
--------------------------------------------------------------------------------
Descriptive Name     : Victoria_AU.py
Author               : Pongthip Srivarangkul
Contact Info         : psrivara@purdue.edu
Date Written         :  July 19, 2016
Description          : Parse cameras on Melburne, Traffic Camera traffic camera
Command to run script: python Victoria_AU.py
Usage                : Run on operating system with requests, bs4, re, Google API installed
Input file format    : NA
Output               : list_Victoria.txt
Note                 :
Other files required by : N/A
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://victoria.snarl.com.au/cams?p=1
In database (Y/N)    :
Date added to Database :
--------------------------------------------------------------------------------
"""


import requests
import sys
from bs4 import BeautifulSoup
import re
from requests.packages.urllib3.connectionpool import xrange
import geopy
from geopy.geocoders import GoogleV3


if __name__ == '__main__':
    geolocator = GoogleV3("AIzaSyAAv_bIqLj8KYPn91BMSqPsllYI4flKZgI")
    fo = open("list_Victoria.txt", "w")
    fo.write("country#city#snapshot_url#latitude#longitude\n")
    origin = "http://victoria.snarl.com.au/cams?p="
    for page_num in xrange(1, 5): #iterate through each page from 1 to 4
        print("\n" + "P." + str(page_num) + "\n")
        add_page_num = page_num
        r = requests.get(origin + str(add_page_num))
        soup = BeautifulSoup(r.content, "html.parser")
        linkset = soup.find_all("div",{"class":"col-md-4 col-sm-6 col-xs-12"})
        for link in linkset: # for each page, this will go through every links to camera avaliable.
            print("Country : Australia")
            fo.write("AU#");
            print("City : Melbourne")
            fo.write("Melbourne#")
            imgurl = link.find_all("img")[0].get("src")
            suburb = (link.find_all("label")[1].text).split(" ")[1]
            print("Suburb: " + suburb)
            print("URL: " + imgurl)
            fo.write(str(imgurl) + "#");
            # Google API to find GPS location
            location = geolocator.geocode(suburb + " " + "Melbourne" + " " + "Australia")
            print(location.latitude, location.longitude)
            fo.write(str(location.latitude) + "#" + str(location.longitude) + "\n")


