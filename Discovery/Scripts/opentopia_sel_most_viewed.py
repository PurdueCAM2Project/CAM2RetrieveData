"""
--------------------------------------------------------------------------------
Descriptive Name     : <Opentopia popular cameras parser.py>
Author               : Ryan Schlueter
Contact Info         : rschluet@gmail.com
Date Written         : June 20, 2017
Description          : Parse cameras on opentopia's datbase of open ip cameras. Opentopia has a collection of worldwide
                       free, open ip cameras. According to their service, all cameras are unsecured and the owner of any
                       camera can contact them and opentopia will stop allowing access to that particular camera.
Command to run script: python opentopia.py
Usage                : (extra requirements to run the script: eg. have to be run within dev server)
Input file format    : (none)
Output               : <opentopia_output.txt>
Note                 :
Other files required by : N/A
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : <insert url>
In database (Y/N)    :
Date added to Database :
--------------------------------------------------------------------------------
"""

# Necessary Import Statements, selenium allows for web-crawling. Maybe switch to Beautiful Soup for faster performance
import selenium
from selenium import webdriver
from selenium.webdriver.support.select import Select
import urllib
import time




def main():
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(30)
    f=open('opentopia_most_viewed_output.txt', 'w')
    f.write("feedNumber#lat#lon#country#state/region#city#specific_location#URL_feed"+'\n')
    noSnap="http://www.opentopia.com/images/nosnapshot-715x536.jpg"

    pages=87
    camsPerPage=15# DO NOT CHANGE
    urlList=[0]*((pages)*camsPerPage)
    print (str(len(urlList)) + " cameras")

    i=0
    for page in range(1,pages+1):
        print ("Pulling links from page: " + str(page) + " out of " + str(pages))
        url = "http://www.opentopia.com/hiddencam.php?showmode=standard&country=*&seewhat=oftenviewed&p="
        url += str(page)
        driver.get(url)
        time.sleep(0.5)

        data = driver.find_elements_by_xpath("//ul[@class = 'camgrid camgrid3']/li/a")

        openUrls=[]
        for x in range(0,camsPerPage):
            openUrls=data[x].get_attribute("href")
            splitUrls=openUrls.split('/')
            num=(int(splitUrls[-1]))
            urlList[i]=num
            i += 1

    time.sleep(2)
    print ("Finding Data")
    for n in range(0, len(urlList)):
        findUrl = "http://www.opentopia.com/webcam/" + str(urlList[n]) + "?viewmode=livevideo"
        try:
            print (str(n) + ": " + str(urlList[n]))
            driver.get(findUrl)
        except selenium.common.exceptions.TimeoutException:
            print ("Timeout" + '\n')
            continue
        time.sleep(0.05)

        try:
            f.write(GetInfo(driver, urlList[n]))
        except:
            pass

def GetInfo(driver, currentCam):
    try:
        feedUrl = urllib.quote(driver.find_element_by_xpath("//div[@class = 'big']/div/img").get_attribute("src"),safe = ':?,=/&')
    except:
        feedUrl="none"
        pass
    feedUrl=str(feedUrl)

    try:
        country = driver.find_element_by_xpath("//label[@class = 'right country-name']").text
        country = str(country)
    except:
        country="none"
        pass

    try:
        state_region = driver.find_element_by_xpath("//label[@class = 'right region']").text
        state_region=str(state_region)
    except:
        state_region="none"
        pass

    try:
        city = driver.find_element_by_xpath("//label[@class = 'right locality']").text
        city = str(city)
    except:
        city="none"
        pass

    try:
        location = driver.find_element_by_xpath("//label[@class = 'right']").text
        location = str(location)
    except:
        location="none"
        pass

    try:
        gpsCoord = driver.find_element_by_xpath("//div[@id = 'map_canvas']/img").get_attribute("src")
        gpsCoord=gpsCoord[gpsCoord.index('%') + 3:len(gpsCoord)]
        lat,lon = gpsCoord.split(',')
    except:
        lat=0
        lon=0
        pass
    lat=str(lat)
    lon=str(lon)


    try:
        brand = []
        brand = driver.find_elements_by_xpath("//label[@class = 'right']")[2]
    except:
        brand = "none"
        pass

    geoInfo=str(currentCam) +'#' + str(lat) + '#' +  str(lon) + '#' +  str(country) + '#' +  str(state_region) + '#' +   str(city) + '#' +  str(location) + '#' + brand + '#' + str(feedUrl) + '\n'
    return(geoInfo)


if __name__ == "__main__":
    main()
