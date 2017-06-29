"""
--------------------------------------------------------------------------------
Descriptive Name     : <parse_opentopia.py>
Author               : Ryan Schlueter
Contact Info         : rschluet@gmail.com
Date Written         : June 20, 2017
Description          : Parse cameras on opentopia's datbase of open ip cameras. Opentopia has a collection of worldwide
                       free, open ip cameras. According to their service, the owner of any camera can contact them and
                       opentopia will stop allowing access to that particular camera.
Command to run script: python opentopia_camera_finder.py
Usage                : (extra requirements to run the script: eg. have to be run within dev server)
Input file format    : (eg. url#description (on each line))
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
    # Initializes the selenium webdriver as Firefox, stable and fast w/ plugins available
    driver = webdriver.Firefox()
    # PhantomJS

    driver.set_page_load_timeout(30)#Set to 5 for testing, 30 for actual runs

    # Open and write header for output file
    f=open('opentopia_output.txt', 'w')
    f.write("feedNumber#lat#lon#country#state/region#city#specific_location#URL_feed"+'\n')
    # Image URL that will be received if there is no live stream. This was an assumption, as it is very unlikely the
    # feed would be live while not haveing a screenshot saved. This greatly decreases loading time, as the crawler
    # does not try to load the stream if it receives this as the screenshot
    noSnap="http://www.opentopia.com/images/nosnapshot-715x536.jpg"

    # Set the starting and ending points for the main lopo
    numCams = 100
    currentCam = 0

    # Main searching loop
    while currentCam < numCams:
        print(currentCam)# Testing purposes only

        # url is the page to load to look for streams, stillUrl is the page to load to check for the dead camera image
        url = "http://www.opentopia.com/webcam/" + str(currentCam) + "?viewmode=livevideo"
        stillUrl = "http://www.opentopia.com/webcam/" + str(currentCam) + "?viewmode=savedstill"

        # Crawler tries to receive the screenshot, if there's an error, assume the link is dead
        try:
            driver.get(stillUrl)
            time.sleep(0.05)
            hasStill = urllib.quote(driver.find_element_by_xpath("//div[@class = 'big']/img").get_attribute("src"),
                                    safe = ':?,=/&')
        except:
            hasStill = "http://www.opentopia.com/images/nosnapshot-715x536.jpg"
            pass

        # If the screenshot is the same as the no snapshot image, assume the live feed is dead as well
        if(hasStill==noSnap):
            goodFeed=False
        else:
            goodFeed=True

        # If the feed is assumed to be live, continue, else move on to the next link
        if(goodFeed):
            print("Has still")#Testing purposes only

            try:
                driver.get(url)
            except selenium.common.exceptions.TimeoutException:
                print ("Timeout"+'\n')
                currentCam += 1
                continue
            time.sleep(0.05)

            try:
                geoInfo=GetInfo(driver, currentCam)
                # print(geoInfo)
                f.write(geoInfo)
            except:
                pass
        currentCam += 1


    driver.close()
    f.close()

# Gets the geo and camer information from the current url in the driver. Returns as a string to be entered into the
# output file
def GetInfo(driver, currentCam):
    print("getting info"+'\n')#testing purposes only
    try:
        feedUrl = urllib.quote(driver.find_element_by_xpath("//div[@class = 'big']/div/img").get_attribute("src"),safe = ':?,=/&')
    except:
        feedUrl="none"
        pass
    feedUrl=str(feedUrl)

    try:
        country = driver.find_element_by_xpath("//label[@class = 'right country-name']").text
    except:
        country="none"
        pass
    country=str(country)

    try:
        state_region = driver.find_element_by_xpath("//label[@class = 'right region']").text
    except:
        state_region="none"
        pass
    state_region=str(state_region)

    try:
        city = driver.find_element_by_xpath("//label[@class = 'right locality']").text
    except:
        city="none"
        pass
    city=str(city)

    try:
        location = driver.find_element_by_xpath("//label[@class = 'right']").text
    except:
        location="none"
        pass
    location=str(location)

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


    # try:
    #     brand = []
    #     brand = driver.find_elements_by_xpath("//label[@class = 'right']")
    # except:
    #     pass

    geoInfo=str(currentCam) + '\t' +'#' + str(lat) + '#' +  str(lon) + '#' +  str(country) + '#' +  str(state_region) + '#' +   str(city) + '#' +  str(location) + '#' +   str(feedUrl) + '\n'
    return(geoInfo)


if __name__ == "__main__":
    main()
