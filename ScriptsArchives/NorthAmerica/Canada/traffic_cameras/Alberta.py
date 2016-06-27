""" 
--------------------------------------------------------------------------------
Descriptive Name     : Alberta.py
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu
Date                 : June 2, 2016
Description          : Parse cameras on the 511 Alberta traffic camera website
Command to run script: python Alberta.py
Output               : output urls, country, city and latitude, longitude to a 
                       textfile <list_Alberta_CA.txt>
Other files required by : Geocoding.py and WriteToFile.py both located in the 
this script and where     Tools directory in NetworkCameras/Discovery
located
----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://511.alberta.ca/cameras/
In database (Y/N)    : Y
--------------------------------------------------------------------------------
"""

from selenium import webdriver
from selenium.webdriver.support.select import Select
import urllib
from Geocoding import Geocoding
from WriteToFile import WriteToFile
import time

def Navigate():
    driver = webdriver.Firefox()
    driver.get("http://511.alberta.ca/cameras/")

    coords = Geocoding('Google', None)
    file = WriteToFile(False, 'list_Alberta.txt')

    option = Select(driver.find_element_by_id("highway_dropdown"))
    numOption = len(driver.find_elements_by_tag_name("option"))
    countOption = 0

    while countOption < numOption:
        option = Select(driver.find_element_by_id("highway_dropdown"))
        option.select_by_index(countOption)
        time.sleep(1.5)
        cameras = driver.find_elements_by_css_selector(".thumbnail.thumbnail-camera")
        numCam = len(cameras)
        countCam = 0
        while countCam < numCam:
            cameras = driver.find_elements_by_css_selector(".thumbnail.thumbnail-camera")
            if cameras[countCam].is_displayed():
                cameras[countCam].click()
                time.sleep(1)
                countAngles = 0
                try:
                    thumbnail = driver.find_elements_by_css_selector(".thumbnail")
                    if(len(thumbnail) == 0):
                        raise Exception('one image')
                    for angles in thumbnail:
                        countAngles += 1
                        angles.click()
                        time.sleep(1)
                        GetInfo(driver, coords, file)
                except:
                    try:
                        thumbnail = driver.find_elements_by_css_selector(".thumbnail.thumbnail-horizontal")
                        if(len(thumbnail) == 0):
                            raise Exception('one image')
                        for angles in thumbnail:
                            countAngles += 1
                            angles.click()
                            time.sleep(1)
                            GetInfo(driver, coords, file)
                    except:
                        if (countAngles == 0):
                            GetInfo(driver, coords, file)
                driver.back()
                time.sleep(1)
            countCam += 1
        countOption += 1
    driver.close()

def GetInfo(driver, coords, file):
    location = driver.find_element_by_xpath("//div[@class = 'panel-title']/h4").text
    city = driver.find_element_by_xpath("//div[@class = 'panel-title']/h4/small").text
    location = location.replace(city, "")
    city = city.replace("Near", "")
    url = urllib.quote(driver.find_element_by_xpath("//div[@id = 'displayImageContainer']/img").get_attribute("src"), safe = ':?,=/&')

    try:
        coords.locateCoords(location, city, "", "CA")
        file.writeInfo("CA", "", coords.city, url, coords.latitude, coords.longitude)
    except:
        pass    

if __name__ == "__main__":
    Navigate()
