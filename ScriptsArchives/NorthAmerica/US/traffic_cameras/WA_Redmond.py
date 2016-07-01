"""
--------------------------------------------------------------------------------
Descriptive Name     : WA_Redmond.py
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu 
Date Written         : June 30, 2016
Description          : Parse cameras on City of Redmond site
Command to run script: python WA_Redmond.py
Usage                : None
Input file format    : N/A
Output               : list_WA_Redmond.txt
Note                 : 
Other files required by : Geocoding.py, WriteToFile.py located in 
this script and where     NetworkCameras/Discovery/Tools
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://gis.redmond.gov/arcgis/rest/services/TrafficCameras/MapServer/1/query?f=json&where=1%3D1&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=*&outSR=102100
In database (Y/N)    : Y
Date added to Database : June 30, 2016
--------------------------------------------------------------------------------
"""
import urllib2
import json
from Geocoding import Geocoding
from WriteToFile import WriteToFile
from Clean import Clean
import time

class Redmond:
    def __init__(self):
        self.website = urllib2.urlopen('http://gis.redmond.gov/arcgis/rest/services/TrafficCameras/MapServer/1/query?f=json&where=1%3D1&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=*&outSR=102100').read()
        self.jsonInfo = json.loads(self.website)
        self.geo = Geocoding('Google', None)
        self.write = WriteToFile(True, 'list_WA_Redmond.txt')

    def getInfo(self):
        features = self.jsonInfo['features']
        for item in features:
            attributes = item['attributes']
            if attributes['d_Jurisdiction'] == 'WSDOT': #We have another script that parses these cameras
                pass
            else:
                ImagePath = attributes['ImagePath']
                Description = attributes['Description']
                Description = Description.replace("&", "and")
                Description = Description.replace("@", "and")
                Description = Description.replace("south", "")
                Description = Description.replace("west", "")
                Description = Description.replace(" - Northeast corner", "")
                Description = Description.replace("facing West", "")
                Description = Description.replace("facing North", "")
                Description = Description.replace(" - North side", "")
                Description = Description.replace("East facing", "")
                Description = Description.replace("over the", "")

                cleanLocat = Clean(Description)
                cleanLocat.suite()
                
                if attributes['d_Jurisdiction'] == 'City of Bellevue': 
                    city = 'Bellevue'
                elif attributes['d_Jurisdiction'] == 'City of Seattle': 
                    city = 'Seattle'
                elif attributes['d_Jurisdiction'] == 'Sammamish':
                    city = 'Sammamish'
                else:
                    city = ""
 
                try:
                    self.geo.locateCoords(cleanLocat.textString, city, "WA", "USA")
                    self.write.writeInfo("USA", "WA", self.geo.city, ImagePath, self.geo.latitude, self.geo.longitude)
                except:
                    print cleanLocat.textString
                    print ImagePath

if __name__ == '__main__':
    WA = Redmond()
    WA.getInfo()
