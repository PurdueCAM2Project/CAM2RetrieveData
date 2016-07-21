# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Descriptive Name     : CA_dot_map.py
Author               : Ali Cataltepe						      
Contact Info         : ali@cataltepe.com
Date Written         : July 21, 2016
Description          : Parses the snapshot urls and camera locations given in the cctvLocations[NUMBER].js file provided on the dot.ca.gov camera map
Command to run script: python ca511_mapfile_parser.py [cctv locations list file path]
Usage                : N/A
Input file format    : .txt
Output               : list_CA_dot_map.txt
Note                 :
Other files required by : Geocoding.py (NetworkCameras/Discovery/Tools/Geocoding.py)
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : dot.ca.gov
In database (Y/N)    : Y
Date added to Database : July 21, 2016
--------------------------------------------------------------------------------
"""

from selenium import webdriver
import urllib
from Geocoding import Geocoding
import time
import sys

GAPI_KEY = "AIzaSyDRb6HaVtHDbpHkJq8a3MEODFZlmkBt7f4" #YOUR GAPI KEY HERE

def ca511Parse(listfilepath):
	geocoder = Geocoding("Google", GAPI_KEY)
	profile = webdriver.FirefoxProfile()
	profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
	profile.set_preference("general.useragent.override","Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4")
	driver = webdriver.Firefox(profile)
	listfile = open(listfilepath, "r")
	writefile = open("list_CA_dot_map.txt", "w")
	writefile.write("country#state#city#snapshot_url#latitude#longitude\n")
	for line in listfile:
		try:
			geocoder.reverse(line[line.replace("ÿ","ü",3).index("ü")+2:line.replace("ÿ","ü",3).rindex("ü")].split("ÿ")[1],line[line.replace("ÿ","ü",3).index("ü")+2:line.replace("ÿ","ü",3).rindex("ü")].split("ÿ")[0])
			driver.get(line[line.index("= '")+3:line.index("ÿ")])
			print geocoder.country+"#"+geocoder.state+"#"+geocoder.city+"#"+urllib.quote(driver.find_element_by_id("cctvImage").get_attribute("src").split("?")[0], safe = ':?,=/&')+"#"+geocoder.latitude+"#"+geocoder.longitude+"\n"
			writefile.write(geocoder.country+"#"+geocoder.state+"#"+geocoder.city+"#"+urllib.quote(driver.find_element_by_id("cctvImage").get_attribute("src").split("?")[0], safe = ':?,=/&')+"#"+geocoder.latitude+"#"+geocoder.longitude+"\n")
		except Exception as error:
			print "ERROR: " + str(error)
			pass
	driver.close()
	writefile.close()
	listfile.close()

if __name__ == "__main__":
	ca511Parse(sys.argv[1])