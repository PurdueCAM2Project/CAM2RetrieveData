from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib2
import urllib
import sys
import re
import json
import time


#output will be image url, country, state, city, lat, long, description

def getFL():
    FLORIDA_URL = "http://www.fl511.com/Cameras.aspx"
    driver = webdriver.Firefox()
    driver.get(FLORIDA_URL)
    driver.implicitly_wait(15)
    ls = []
    lat = []
    lon = []
    locat = " "
    j = 4;
    k = 1;

    #f = open('list_FL', 'w')
    #f.write("snapshot_url#country#state#city#latitude#longitude#description")

    #Sorts table by image availability
    for i in driver.find_elements_by_tag_name('a'):
        if(i.text == "Still Image"):
           for j in range(0,2):
               i.click();
        break
    
    time.sleep(2)        
    print "Extracting urls to images..."
    while True:
        time.sleep(2)
        for i in driver.find_elements_by_class_name('traffic-camera-image'):
            print driver.find_elements_by_tag_name('td')[j].text;
            j = j+6;
            try:
                print i.get_attribute("src")
            except Exception as e:
                break;
        #    for i in range(0, 10):
            if(j >= 60):
                break;
           
        j = 4;
        if k > 205:
            break;
        else:
            k = k+1;
        driver.find_element_by_id('MainContent_MainContent_CameraGridView_NextLinkButton').click()


    #driver.find_elements_by_css_selector('scope')[5].click()
    #i.click()
    
getFL()