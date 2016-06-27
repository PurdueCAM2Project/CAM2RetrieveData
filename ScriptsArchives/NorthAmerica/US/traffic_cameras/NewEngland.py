"""
--------------------------------------------------------------------------------
Descriptive Name     : NewEngland.py
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu 
Date Written         : June 23, 2016
Description          : Parse cameras on New England site
Command to run script: python NewEngland.py
Usage                : Must be run on machine with geopy installed
Input file format    : N/A
Output               : list_NewEngland.txt
Note                 : 
Other files required by : Geocoding.py, WriteToFile.py located in 
this script and where     NetworkCameras/Discovery/Tools
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://newengland511.org/traffic/getcameras
In database (Y/N)    : Y
Date added to Database : June 23, 2016
--------------------------------------------------------------------------------
"""
import urllib2
import json
from Geocoding import Geocoding
from WriteToFile import WriteToFile
import time

class NewEngland:
    def __init__(self):
        self.website = urllib2.urlopen('http://newengland511.org/traffic/getcameras').read()
        self.jsonInfo = json.loads(self.website)
        self.geo = Geocoding('Google', None)
        self.write = WriteToFile(True, 'list_NewEngland.txt')

    def getInfo(self):
        for location in self.jsonInfo:
            url = location["ImageUrl"]
            latitude = location["Latitude"]
            longitude = location["Longitude"]
            self.geo.reverse(str(latitude), str(longitude))
            time.sleep(2)
            self.write.writeInfo("USA", self.geo.state, self.geo.city, url, str(latitude), str(longitude))

if __name__ == '__main__':
    NE = NewEngland()
    NE.getInfo()