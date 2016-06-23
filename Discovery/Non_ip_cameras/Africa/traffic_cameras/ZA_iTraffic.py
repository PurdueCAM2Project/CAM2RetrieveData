"""
--------------------------------------------------------------------------------
Descriptive Name     : Script to parse cameras in South Africa
Author               : Thomas Norling								      
Contact Info         : thomas.l.norling@gmail.com
Date                 : June 8, 2016
Description          : This script will first get all the information it needs from
                       the first page, clean up the location data, and then search
                       for coordinates with several different search queries. Then
                       it will navigate to the next page and repeat the process
                       until the entire site has been parsed.
Command to run script: python South_Africa.py
Usage                : Needs to be run on personal machine with geopy installed
Input file format    : N/A
Output               : list_South_Africa.txt
Note                 : This script uses the geopy library to perform the geocoding
                       on the addresses given. Geopy is not installed on the 
                       development server as of this writing.
                       This will not run on the development machine and thus will 
                       need to be run on a machine with geopy installed.
Other files required by : Geocoding.py and WriteToFile.py located in 
this script and where       NetworkCameras/Discovery/Tools
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : https://www.i-traffic.co.za/traffic/cameras.aspx
In database (Y/N)    : Y
--------------------------------------------------------------------------------
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from Geocoding import Geocoding
from WriteToFile import WriteToFile
import urllib2
import urllib
import sys
import re
import json
import time

def main():
    driver = webdriver.Firefox()
    driver.get("https://www.i-traffic.co.za/traffic/cameras.aspx")
    driver.implicitly_wait(15)
    time.sleep(2)
    #Format of output
    att = []
    ls = []
    lat = []
    lon = []
    locat = " "
    hwy = " "
    city = " "
    count = 0
    j = 0

    #Write format of output so it can be uploaded
    geoCode = Geocoding('Google', None)
    file = WriteToFile(False, 'list_ZA_iTraffic.txt')

    
    #Loop used to stop when there is no more next buttons to click
    while(j == 0):
        #Resets Attribute list
        del att[:]
        #Creates attribute list from the current list of cameras, trys so there are no errors at the end of the list
        try:
            for v in driver.find_elements_by_xpath("//*[starts-with(@id, 'ctl00_ctl00_ctl00_ContentPlaceHolder_Column2PlaceHolder_ListPlaceHolder_ListGridView_ctl')]"):
                att.append(v.text)
        except:
            m = 0

        count = 0
        i = driver.find_elements_by_class_name('cctv')
        num_images = len(i)
        while count < num_images:
            b = 1
            i = driver.find_elements_by_class_name('cctv')
            try:
                link = i[count].get_attribute('src')
                
            except Exception as w:
                b = 0
                print "Image link isn't up"
                   
            if b == 1:    
                city = att[count * 4]
                locat = att[(4*count) + 2]
                #Clean up the location info
                locat = locat.replace("traffic closer to the camera is traveling", "")
                locat = locat.replace("Inbound", "")
                locat = locat.replace("Outbound", "")
                locat = locat.replace("IB", "")
                locat = locat.replace("OB", "")
                locat = locat.replace("EB", "")
                locat = locat.replace("WB", "")
                locat = locat.replace("NB", "")
                locat = locat.replace("SB", "")
                locat = locat.replace("Ib", "")
                locat = locat.replace("Ob", "")
                locat = locat.replace("Eb", "")
                locat = locat.replace("Wb", "")
                locat = locat.replace("Nb", "")
                locat = locat.replace("Sb", "")
                locat = locat.replace("Northbound", "")
                locat = locat.replace("Southbound", "")
                locat = locat.replace("Eastbound", "")
                locat = locat.replace("Westbound", "")
                locat = locat.replace("Onramp", "")
                locat = locat.replace("on-ramp", "")
                locat = locat.replace("onramp", "")
                locat = locat.replace("off-ramp", "")
                locat = locat.replace("oframp", "")
                locat = locat.replace("offramp", "")
                locat = locat.replace("Offramp", "")
                locat = locat.replace("behind", "")
                locat = locat.replace("before", "")
                locat = locat.replace("Before", "")
                locat = locat.replace("after", "")
                locat = locat.replace("After", "")
                locat = locat.replace("Between", "")
                locat = locat.replace("between", "")
                locat = locat.replace("just", "")
                locat = locat.replace("Near", "")
                locat = locat.replace("near", "")
                locat = locat.replace("opposite", "")
                locat = locat.replace("at", "")
                locat = locat.replace("At", "")
                locat = locat.replace("Interchange", "")
                locat = locat.replace("interchange", "")
                locat = locat.replace("center median", "")
                locat = locat.replace("Centre median", "")
                locat = locat.replace("Median", "")
                locat = locat.replace("Security_Cam", "")
                locat = locat.replace("Security camera", "")
                locat = locat.replace("warehouse", "")
                locat = locat.replace("Four level ", "")
                locat = locat.replace("footbridge", "")
                locat = locat.replace("/", " ")
                locat = locat.replace(hwy, "")
                locat = locat.replace("I/C", "")
                locat = locat.replace("IC", "")
                locat = locat.replace("I C", "")
                locat = locat.replace("()", "")
                locat = locat.replace("( )", "")
                locat = locat.replace("\n", "")
                locat = locat.replace("  ", " ")
                locat = locat.strip()
                
                hwy = att[(4*count) + 1]
                try:
                    try:
                        if locat.startswith("CCTV"):
                            raise Exception("CCTV Location")
                        geoCode.locateCoords(locat + ',' + city,'', '', 'ZA')
                        file.writeInfo('ZA', '', geoCode.city, link, geoCode.latitude, geoCode.longitude)
                    except:
                        try:
                            try:
                                if locat.startswith("CCTV"):
                                    raise Exception("CCTV Location")
                                geoCode.locateCoords(locat + ',','', '', 'ZA')
                                file.writeInfo('ZA', '', geoCode.city, link, geoCode.latitude, geoCode.longitude)
                            except:
                                
                                geoCode.locateCoords(hwy + ',' + city,'', '', 'ZA')
                                file.writeInfo('ZA', '', geoCode.city, link, geoCode.latitude, geoCode.longitude)
                        except:
                            if city == "":
                                raise Exception("City is empty")
                            geoCode.locateCoords(city,'', '', 'ZA')
                            file.writeInfo('ZA', '', geoCode.city, link, geoCode.latitude, geoCode.longitude)
                except Exception as e:
                    if locat.startswith("CCTV"):
                        pass
                    else:
                        print e
                        print locat + " " + city + " " + ', ZA'
                        print "Error generating location information"
                
            count += 1
        #Catches when it reaches the end of the list of cameras
        try:
            driver.find_element_by_link_text('Next').click()
        except NoSuchElementException:
            j = 1
            break;
        driver.implicitly_wait(30)
        time.sleep(6)
    driver.close();
    return;  
   
if __name__ == "__main__":
  main()
