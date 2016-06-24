"""
--------------------------------------------------------------------------------
Descriptive Name     : London_UK.py
Author               : Pongthip Srivarangkul
Contact Info         : psrivara@purdue.edu
Date Written         :  June 9, 2016
Description          : Parse cameras on London, United Kingdom traffic camera
Command to run script: python London_UK.py
Usage                : Run on operating system with requests, bs4 and re installed
Input file format    : (eg. url#description (on each line))
Output               : (eg. <file name> or <on screen>)
Note                 :
Other files required by : N/A
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.trafficdelays.co.uk/london-traffic-cameras/
In database (Y/N)    :
Date added to Database :
--------------------------------------------------------------------------------
"""


import requests
import sys
from bs4 import BeautifulSoup
import re
from requests.packages.urllib3.connectionpool import xrange

# Defining fuction to retrive needed data from each camera
def scraping(address):
    r = requests.get(address)
    soup = BeautifulSoup(r.content, "html.parser")
    imgset = soup.find_all("img")
    for imglink in imgset:
        if "trafficdelay" not in imglink.get("src") : # clear out the one we dont need
            print("Snapshot's URL : " + imglink.get("src"))
            fo.write(imglink.get("src") + "#")
    locset = soup.find_all("br")
    for loclink in locset: # look for the line that contain geographical location
        if "Lat" in loclink.text:
            wantedtext = loclink.text
    parsedLoc = re.search(r"Lat: (?P<lat>[\d\.\-]*), Long: (?P<long>[\d\.\-]*)", wantedtext)
    lat = parsedLoc.group('lat')
    long = parsedLoc.group('long')
    print("Latitude : " + str(lat))
    fo.write(str(lat) + "#")
    print("Longitude : " + str(long))
    fo.write(str(long) + "\n")

if __name__ == '__main__':
    fo = open("list_London_UK.txt", "w")
    fo.write("country#city#snapshot_url#latitude#longitude\n")
    origin = "http://www.trafficdelays.co.uk/london-traffic-cameras/"
    for page_num in xrange(1, 27): #iterate through each page from 1 to 26
        print("\n" + "P." + str(page_num) + "\n")
        add_page_num = "?lcp_page0=" + str(page_num) + "#lcp_instance_0"
        r = requests.get(origin + add_page_num)
        soup = BeautifulSoup(r.content, "html.parser")
        linkset = soup.find_all("h4",{"class":"lcp_title"})
        for link in linkset: # for each page, this will go through every links to camera avaliable.
            print("Country : United Kingdom")
            fo.write("GB#");
            print("City : London")
            fo.write("London#")
            scraping(link.find_all("a")[0].get("href")) # utilize the scraping function
            print("Note : " + link.find_all("a")[0].get("title").replace('| London Jam Cams',''))
            print("Reference : " + link.find_all("a")[0].get("href") + "\n")
