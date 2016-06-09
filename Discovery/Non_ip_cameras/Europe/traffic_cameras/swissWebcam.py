"""
--------------------------------------------------------------------------------
Descriptive Name     :  Parser for traffic cameras in SwissWebcam website
Author               :  Sanghyun Joo
Contact Info         :  joos@purdue.edu OR toughshj@gmail.com
Date                 :  7 June 2016
Description          :  parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script:  python3 swissWebcam.py
Usage                :  Parsing traffic cameras in SwissWebcam website
Input file format    :  N/A
Output               :  list_swissWebcam_traffic file
Note                 :  it sometimes gives "TypeError: object of type 'NoneType' has no len()" error. If so, just re-run the script
Other files required by : This code requires to install Selenium
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       :  yes
In database (Y/N)    :  yes
--------------------------------------------------------------------------------
"""

# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.ui as ui

class SwissWebcam:
    def __init__(self):
        # disable the js of firefox to speed up. it is not necessary to run
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference("javascript.enabled", False)

        # get the webdriver of the opened firefox and open the url
        self.driver = webdriver.Firefox(firefox_profile=firefox_profile)
        self.driver.get("http://en.swisswebcams.ch/verzeichnis/traffic/schweiz/beliebt")

        # open the file to store the list and write the format of the list at the first line
        self.f = open('list_SwissWebcam_traffic', 'w')
        self.f.write("country#city#snapshot_url#latitude#longitude" + "\n")

        # wait object to use
        self.wait = ui.WebDriverWait(self.driver, 10)

    def handle_alert(self):
        """ handle the alert that randomly pops up
        """
        #alert = self.driver.switch_to_alert()
        #alert.send_keys('8080')
        #alert.dismiss()
        time.sleep(1)       # waits until the alert is removed

    def click_all_button(self):
        """ click the button that redirects to the list of all webcams

            Raises:
                UnexpectedAlertPresentException: it occurs when a ramdom alert dialog pops up
                TimeoutException: it occurs when the element we want is never loaded
        """
        try:
            # wait until the element is loaded
            self.wait.until(lambda driver: driver.find_element_by_id("VERZEICHNIS-button_alle"))

            # get the button element and click it
            button = self.driver.find_element_by_id("VERZEICHNIS-button_alle")
            button.click()

        except UnexpectedAlertPresentException:
            self.handle_alert()
            self.click_all_button()

        except:
            self.driver.refresh()
            self.click_all_button()

    def get_tabs(self, tabs):
        """ get the list of link addresses of the alphabet tabs that

            extract the elements of the tabs of the alphabet which categorize the cameras by alphabet

            Returns:
                tabs: the list of link addresses of all the alphabet in the tabs

            Raises:
                UnexpectedAlertPresentException: it occurs when a ramdom alert dialog pops up
                TimeoutException: it occurs when the element we want is never loaded
                Sometimes tabs returns None type object and I don't know why
        """
        try:
            # wait until the element is loaded
            self.wait.until(lambda driver: self.driver.find_element_by_id("VERZEICHNIS-pagination_top"))

            # get the tabs' elements
            tabs_container = self.driver.find_element_by_id("VERZEICHNIS-pagination_top")
            hrefs = tabs_container.find_elements_by_tag_name("a")

            # loop through all the tabs to get the href source of them
            for href in hrefs:
                tabs.append(href.get_attribute("href"))

        except UnexpectedAlertPresentException:
            self.handle_alert()
            self.get_tabs()

        except:
            self.driver.refresh()
            self.get_tabs()

    def get_cctvs(self, cctvs):
        """ get the list of link addresses of the cameras in the selected alphabet tab

            extract the elements of the cameras of the selected alphabet

            Returns:
                cctvs: the list of link addresses of all the cameras in the selected tab
                
            Raises:
                UnexpectedAlertPresentException: it occurs when a ramdom alert dialog pops up
        """
        try:
            # wait until the element is loaded AND get the cameras' elements
            self.wait.until(lambda driver: self.driver.find_elements_by_class_name("thumbnail"))
            images = self.driver.find_elements_by_class_name("thumbnail")

            # loop throught all the cameras to get the href source of them
            for img in images:
                cctvs.append(img.get_attribute("href"))

            return cctvs
        
        except UnexpectedAlertPresentException:
            self.handle_alert()
            self.get_cctvs(cctvs)

        except:
            self.driver.refresh()
            self.get_cctvs()

    def print_city(self):
        """ get the city name and put it into the file opened

            Raises:
                UnexpectedAlertPresentException: it occurs when a ramdom alert dialog pops up
        """
        try:
            # wait until the element is loaded AND get the city name in the element
            self.wait.until(lambda driver: self.driver.find_element_by_class_name("h1"))
            city_token = self.driver.find_element_by_class_name("h1").text.split(":")[0]
            city = city_token.split()[0]

            # write the city name in the file
            self.f.write("Switzerland#" + city + "#")

            print(city)

        except UnexpectedAlertPresentException:
            self.handle_alert()
            self.print_city()

        except:
            self.driver.refresh()
            self.print_city()

    def print_image_src(self):
        """ get the camera image url and put it into the file opened

            Raises:
                UnexpectedAlertPresentException: it occurs when a ramdom alert dialog pops up
                TimeoutException: if occurs when the the element is never loaded (the element has different id)
        """
        try:
            # wait until the element is loaded AND get the image src in the element
            self.wait.until(lambda driver: self.driver.find_element_by_id("WEBCAM-bild"))
            src = self.driver.find_element_by_id("WEBCAM-bild").get_attribute("src")

            # write the image src in the file
            self.f.write(src + "#")

            print(src)

        except UnexpectedAlertPresentException:
            self.handle_alert()
            self.print_image_src()

        except TimeoutException:
            link_to_img = self.driver.find_element_by_id("WEBCAM-daylight")
            link_to_img.click()

            self.wait.until(lambda driver: self.driver.find_element_by_id("WEBCAM_ZOOM-bild"))
            src = self.driver.find_element_by_id("WEBCAM_ZOOM-bild").get_attribute("src")

            self.f.write(src + "#")

            print(src)

            self.driver.back()

        except:
            self.driver.refresh()
            self.print_image_src()

    def move_to_location_webpage(self):
        """ move to the location webpage of the selected camera

            each webpage of camera has a link to their location
            extract the url of the webpage and move to it

            Raises:
                UnexpectedAlertPresentException: it occurs when a ramdom alert dialog pops up
        """
        try:
            # wait until the element is loaded AND get the link to the location webpage in the element
            self.wait.until(lambda driver: self.driver.find_element_by_link_text("Location"))
            location = self.driver.find_element_by_link_text("Location").get_attribute("href")

            # move to the location webpage
            self.driver.get(location)

        except UnexpectedAlertPresentException:
            self.handle_alert()
            self.move_to_location_webpage()

        except:
            self.driver.refresh()
            self.move_to_location_webpage()

    def print_geocoord(self):
        """ get the location information of the camera and put it into the file opened

            when moved to the location webpage, it has the latitude and longitude information in degree/minute/second format
            extract it, convert it into the decimal format, and put it into the file

            Raises:
                UnexpectedAlertPresentException: it occurs when a ramdom alert dialog pops up
        """
        try:
            # wait until the element is loaded AND get the location information in dms format
            self.wait.until(lambda driver: self.driver.find_element_by_xpath("//div[@style='width: 180px; border: 1px solid black; background-color: white; color: black; text-align: center; font: 12px Arial,sans-serif; padding: 1px 3px; z-index: 0; position: absolute; top: 0px; right: 0px;']"))
            dms = self.driver.find_element_by_xpath("//div[@style='width: 180px; border: 1px solid black; background-color: white; color: black; text-align: center; font: 12px Arial,sans-serif; padding: 1px 3px; z-index: 0; position: absolute; top: 0px; right: 0px;']").text

            # convert the dms format into the decimal format
            lat, lon = self.convert_DMS_to_decimal(dms)

            # write the latitute and longitude in the file
            self.f.write(str(lat) + "#")
            self.f.write(str(lon) + "\n")

            print(lat, lon)

        except UnexpectedAlertPresentException:
            self.handle_alert()
            self.print_geocoord()

        except:
            self.driver.refresh()
            self.print_geocoord()

    def convert_DMS_to_decimal(self, dms):
        """ converts the latitude and longitude from DMS format to decimal format

            Args:
                dms: the latitude and longitude in DMS format which extracted from the location webpage
                        eg. 46°55' 45" N 8°34' 16" E'

            Returns:
                lat: the converted latitude in decimal format
                lon: the converted latitude in decimal format 
        """
        # loop through the dms to remove the unnecessary characters
        s = ""
        for char in dms:
            if char.isdigit():
                s += char
            else:
                s += " "

        # split it by the white space
        geocoord = s.split()

        # convert it into decimal format
        lat = float(geocoord[0]) + float(geocoord[1])/60 + float(geocoord[2])/3600
        lon = float(geocoord[3]) + float(geocoord[4])/60 + float(geocoord[5])/3600

        return lat, lon

    def main(self):
        """ main function to run the script
        """
        self.click_all_button()                             # click to move

        tabs = []
        self.get_tabs(tabs)                                     # get the list of link addresses of the alphabet tabs
        current_url = self.driver.current_url               # get the current webpage's url

        for i in range(len(tabs)):
            self.driver.get(tabs[i])                        # move to the next alphabet tab

            cctvs = []
            self.get_cctvs(cctvs)                           # get the list of link addresses of the cameras in the selected alphabet tab

            for j in range(len(cctvs)):
                self.driver.get(cctvs[j])                   # move to the next camera

                self.print_city()                           # scrap the city name and print it
                self.print_image_src()                      # scrap the snapshot_url and print it
                self.move_to_location_webpage()             # move to the webpage that has the geocoordinate information
                self.print_geocoord()                       # scrap the lat/long and print it

if __name__ == '__main__':
    SwissWebcam = SwissWebcam()
    SwissWebcam.main()
