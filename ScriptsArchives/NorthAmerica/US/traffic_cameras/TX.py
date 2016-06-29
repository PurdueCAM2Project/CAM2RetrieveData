""" 
---------------------------------------------------------------------------
Name		: TX.py
Author		: Thomas Norling
Contact Info: tnorling@purdue.edu
Date Written: June 2016
Description : Parse cameras on the TXdot traffic camera website)
Command to run script: python TX.py
Output      : (eg. <file name> or <on screen>)
Note        : 
Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------
Website Parsed       : http://its.txdot.gov/ITS_WEB/FrontEnd/default.html?r=AMA&p=Amarillo&t=cctv
In database (Y/N)    : Y
Date added to Database : June 2016
--------------------------------------------------------------------------
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib2
import urllib
import sys
import re
import json
import time

#Location 4, Corpus Christi, does not get proper API Information and is excluded
def main():
    driver = webdriver.Firefox()
	#driver = webdriver.Chrome() 
    #driver = webdriver.PhantomJS()
    driver.get("http://its.txdot.gov/ITS_WEB/FrontEnd/default.html?r=AMA&p=Amarillo&t=cctv")
    driver.implicitly_wait(15)
    time.sleep(2);
    ls = []
    lat = []
    lon = []
    locat = " "
    numregions = 0
    f = open('list_TX.txt', 'w')

    #Write format of output so it can be uploaded
    f.write("country#state#city#snapshot_url#latitude#longitude\n")

    try:
        for regions in driver.find_elements_by_tag_name('option'):
            numregions = numregions + 1
    except Exception as e:
        driver.navigate().refresh()
        for regions in driver.find_elements_by_tag_name('option'):
            numregions = numregions + 1
        
    
    #Range for Regions/Cities
    for i in range(11, numregions-1):
        time.sleep(2);
        try:
            driver.find_elements_by_tag_name('option')[i].click()
            city = driver.find_elements_by_tag_name('option')[i].text
            driver.implicitly_wait(15)
        except Exception as e:
                try:
                    for i in range(0,10):
                        driver.reload()
                        driver.find_elements_by_id('doesnt-matter')
                        break
                except Exception as e:
                    print e
                    print "Error opening next region"
    
        #Sets link to maxiumum size
        driver.implicitly_wait(15)
        time.sleep(2);
        driver.find_element_by_xpath("//*[@type='radio' and @value='200']").click()
        
    
        #Gets the images in the roadway by default opened:
        for camera in driver.find_elements_by_class_name('CameraElement'):
            try:
                camera.click()
                link = driver.find_element_by_id('currentSnap').get_attribute("src")
                if(link.find("NoSnapshot") == -1):
                   locat =  urllib.quote(driver.find_element_by_id('snapTitle').text, safe = '?,=/&')
                   locat.replace("CCTV", "")
                   gAPI(locat, city, link, f)
                   writeOut(locat)
            except Exception as e:
                try:
                    gAPI_city(locat, city, link, f)
                except Exception as i:
                    print i
                    print "Error generating location information"
                    

           #Simulates click on each roadway which have class roadway
        for roadway in driver.find_elements_by_class_name('roadway'):
            roadway.click()
            #All cameras have class CameraElement, simulates clicking each element and then extracts the enlarged image url
            for camera in driver.find_elements_by_class_name('CameraElement'):
                try:
                    camera.click()
                    #time.sleep(1.5)
                    link = driver.find_element_by_id('currentSnap').get_attribute("src")
                    if(link.find("NoSnapshot") == -1):
                        locat =  urllib.quote(driver.find_element_by_id('snapTitle').text, safe = '?,=/&')
                        locat.replace("CCTV","")
                        gAPI(locat, city, link, f)
                except Exception as e:
                    try:
                        gAPI_city(locat, city, link, f)
                    except Exception as i:
                        print i
                        print "Error generating location information"
    driver.close()
    return;


def gAPI(locat, city, link, f):
    time.sleep(0.2);
    api = "https://maps.googleapis.com/maps/api/geocode/json?address=" + locat + "," + city + ",TX,USA"
    api = api.replace(' ','')
    ''' use API to find the latitude and longitude'''
    response = urllib2.urlopen(api).read()
    #load by json module 
    parsed_json= json.loads(response)
    content= parsed_json['results']
    #print content
    #extract latitude and longitude from the API json code
    loc= content[0]
    geo = loc['geometry']
    location2 = geo['location']
    lat = location2['lat']
    lng= location2['lng']
    #change lat and lng to string
    string_lat = str(lat)
    string_lng = str(lng)
    #print string_lat,string_lng
    locat = 'USA'+'#'+'TX'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
    #locat = 'TX'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
    #file_lafa.write(link.encode('utf-8')+'\n')
    f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')
    return;


def gAPI_city(locat, city, link, f):
    time.sleep(0.2)
    api = "https://maps.googleapis.com/maps/api/geocode/json?address=" + city + ",TX,USA"
    api = api.replace(' ','')
    ''' use API to find the latitude and longitude'''
    response = urllib2.urlopen(api).read()
    #load by json module 
    parsed_json= json.loads(response)
    content= parsed_json['results']
    #print content
    #extract latitude and longitude from the API json code
    loc= content[0]
    geo = loc['geometry']
    location2 = geo['location']
    lat = location2['lat']
    lng= location2['lng']
    #change lat and lng to string
    string_lat = str(lat)
    string_lng = str(lng)
    #print string_lat,string_lng
    locat = 'USA'+'#'+'TX'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
    #locat = 'TX'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
    #file_lafa.write(link.encode('utf-8')+'\n')
    f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')
    return;
    
if __name__ == '__main__':
	main()
