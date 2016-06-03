from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import urllib2
import urllib
import sys
import re
import json
import time

'''
WARNING:
The > button on the website is still clickable,  and visible when the script
reaches the end of the list. So the only way to check if it's at the end of the 
list is to check the last camera. So check the website first if it adds any cameras to 
the end. I'll tag that line in the code with a W.
'''

#Script uses selennium to acquire links to the images
#output will be the image urls and description in file list_LosAngelesDot


def main():
    driver = webdriver.Firefox()
    driver.get("http://fl511.com/Cameras.aspx")
    driver.implicitly_wait(15)
    time.sleep(2)
    f = open ('list_FloridaDot11','w')
    #Format of output
    att = []
    ls = []
    lat = []
    lon = []
    locat = []
    hwy = []
    city = []
    links = []
    count = 0
    j = 1


    
    #Cannot parce all 210 pages at once, ,must run script multiple times
    #With a 20 page intervals. These next few lines makes the script start
    #at different locations
    driver.find_element_by_link_text('10').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('20').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    
    driver.find_element_by_link_text('30').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('40').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    
    driver.find_element_by_link_text('50').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('60').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    
    driver.find_element_by_link_text('70').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('80').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    
    driver.find_element_by_link_text('90').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('100').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    
    driver.find_element_by_link_text('110').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('120').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    
    driver.find_element_by_link_text('130').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('140').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    
    driver.find_element_by_link_text('150').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('160').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    
    driver.find_element_by_link_text('170').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('180').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    
    driver.find_element_by_link_text('190').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('200').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    driver.find_element_by_link_text('>').click()
    driver.implicitly_wait(15)
    time.sleep(2)
    

    driver.implicitly_wait(30)
    time.sleep(4)

    


    #Write format of output so it can be uploaded - Only needed to be written once
    f.write("country#state#city#snapshot_url#latitude#longitude\n")


    #While Loop that goes through all pages
    while(j < 21):
        #Counters for finding locat, hwy, and city values
        locatC = 4
        hwyC = 2
        cityC = 1
        image = 5
        for i in driver.find_elements_by_class_name('traffic-camera-image'):
            #Skips the camera and its location
            try:
                while(driver.find_elements_by_tag_name('td')[image].text != ""):
                    print 'No image available'
                    locatC += 6
                    hwyC += 6
                    cityC += 6
                    image += 6
                links.append(i.get_attribute('src').split(';', 1)[0])
                city.append(driver.find_elements_by_tag_name('td')[cityC].text)
                hwy.append(driver.find_elements_by_tag_name('td')[hwyC].text)
                locat.append(driver.find_elements_by_tag_name('td')[locatC].text)
                #Gets the camera and its location
                print city[count] + " " + hwy[count] + " " + locat[count]
                print links[count]
                print count
                #Searches coordinates by locat first, then hwy, and finally the county/city
                locatC += 6
                hwyC += 6
                cityC += 6
                image += 6
                if(locat[count] == 'US-301 at Rhodine Rd'): #W
                    j = 22
                    break
                count += 1
            except Exception as e:
                print e
                print "Except Error"
        j += 1
            
        #Catches when it reaches the end of the list of cameras
        driver.find_element_by_link_text('>').click()
        driver.implicitly_wait(30)
        time.sleep(4)
    driver.close();
    for z in range (0,count):
            try:
                gAPI(locat[z],hwy[z], city[z], links[z], f)
            except Exception as e:
                try:
                    gAPI_hwy(locat[z],hwy[z], city[z], links[z], f)
                except Exception as e:    
                    try:
                        gAPI_city(locat[z],hwy[z],city[z],links[z],f)
                    except Exception as p:
                        print p
                        print "Error generating location information"
    return;


def gAPI(locat, hwy, city, link, f): #Location is discription ,city, link is to URL, f is file
    time.sleep(0.2);
    api = "https://maps.googleapis.com/maps/api/geocode/json?address=" + locat + "," + hwy + "," + city + ",FL,USA"
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
    locat = 'USA'+'#'+'FL'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
    #locat = 'FL'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
    #file_lafa.write(link.encode('utf-8')+'\n')
    f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')
    return;


def gAPI_hwy(locat, hwy, city, link, f):#Find location of camera by highway 
    time.sleep(0.2)
    api = "https://maps.googleapis.com/maps/api/geocode/json?address=" + hwy + "," + city + ",FL,USA"
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
    locat = 'USA'+'#'+'FL'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
    #locat = 'FL'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
    #file_lafa.write(link.encode('utf-8')+'\n')
    f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')
    return;

def gAPI_city(locat, hwy, city, link, f): #Find location by county/city
    time.sleep(0.2)
    api = "https://maps.googleapis.com/maps/api/geocode/json?address=" + city + ",FL,USA"
    api = api.replace(' ','')
    ''' use API to find the latitude and longitude'''
    response = urllib2.urlopen(api).read()
    #load by json module 
    parsed_json= json.loads(response)
    content= parsed_json['results']
    #print content
    #extract latitude and longitude from the API json code
    loc= content[0] # ERROR
    geo = loc['geometry']
    location2 = geo['location']
    lat = location2['lat']
    lng= location2['lng']
    #change lat and lng to string
    string_lat = str(lat)
    string_lng = str(lng)
    #print string_lat,string_lng
    locat = 'USA'+'#'+'FL'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
    #locat = 'FL'+'#'+city+'#'+link+'#'+string_lat+'#'+string_lng
    #file_lafa.write(link.encode('utf-8')+'\n')
    f.write(locat.encode('utf-8').replace(" ","").replace("\n",'')+'\n')
    return;
    
    
main()
