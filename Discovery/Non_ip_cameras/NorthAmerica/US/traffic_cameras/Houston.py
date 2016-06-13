from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib2
import urllib
import sys
import re
import json
import time


#Script utilizes selenium to extract links to image urls
#output will be the image urls and descriptions in file list_Houston

def main():
    driver = webdriver.Firefox()
    #driver = webdriver.Chrome()
    #driver = webdriver.PhantomJS()
    driver.get("http://traffic.houstontranstar.org/cctv/txdot/txdot_regional_cameras.html?rd=FM-105")
    driver.implicitly_wait(15)
    time.sleep(2);
    ls = []
    lat = []
    lon = []
    locat = " "
    numregions = 0
    city = "Houston"
    #File was already created because each individual tab was run as a separate link
    f = open('list_Houston', 'a')
    highway=driver.find_elements_by_css_selector(".roadbut.img-rounded")
    numhighway=len(highway)

    number=0
    while number < numhighway:
        highway=driver.find_elements_by_css_selector(".roadbut.img-rounded")
        highway[number].click()
        
    #Write format of output so it can be uploaded - Only needed to be written once
    #f.write("country#state#city#snapshot_url#latitude#longitude\n")
        for i in driver.find_elements_by_tag_name('option'):
            
            #print i.text
            #Link is full URL, doesn't need to be added to the host site
            link = i.get_attribute('value').split(';', 1)[0];
            locat = urllib.quote(i.text, safe='?,=/&');
            try:
                gAPI(locat, city, link, f)
                pass
            except Exception as e:
                try:
                    gAPI_city(locat, city, link, f)
                    pass
                except Exception as i:
                    print i
                    print "Error generating location information"
        number+=1
    driver.close();
    return;


def gAPI(locat, city, link, f): #Location is discription ,city, link is to URL, f is file
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

main()
