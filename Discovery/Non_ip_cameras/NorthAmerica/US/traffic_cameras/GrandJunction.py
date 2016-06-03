#!/usr/bin/python
'''
This program will parse camera information from the City of Grand Junction website. This simple code will utilize
Beautiful Soup 4 to extract the relevant information including image url and street address of each camera. The street
address will then be processed by Google API to fetch the corresponding geographical information. It will then  output
the results in a text file.
'''

import urllib2
import json
import time
from bs4 import BeautifulSoup

#This website separates its camera feeds into road ways they belong to where each road way is a link that will lead to
#the said camera feeds. These links have the same url (stored in baseroadurl) followed by the road way name. We first
#extract all the road way names then pass them to the getCams() function as a url for the camera feeds in each road way.
def getGJ():
    #Generate base urls for links to relevant pages
    baseroadurl='http://publicweb-fs.ci.grandjct.co.us/e-net/PublicWorks/TrafficCam/'
    #Open main page where all road ways are listed
    base='http://www.gjcity.org/TrafficVolumeCameras.aspx'
    file = open('GrandJunction_output.txt','w') #Open output file
    roadlist=[]
    #Extract links which lead to camera feed pages of each road way
    soup = BeautifulSoup(urllib2.urlopen(base).read())
    for tag in soup.find_all("a",{"class":"MakeLink"}):
        roadurl=tag.get('href').encode('utf-8')
        if baseroadurl in roadurl:
            roadlist.append(roadurl)
    #Go through the list of links extracted and parse camera information from them
    for roadurl in roadlist:
        getCams(roadurl,file)
    file.close()

#This function extracts the relevant information such as the camera's image url and its street location. The street
#location is processed by Google API which returns geographical locations of the cameras. Google API is accurate on
#these locations because the website only has cameras that are located in main roads and highways that is recognizable
#by the api.
def getCams(road,file):
    weburl='http://publicweb-fs.ci.grandjct.co.us'
    soup = BeautifulSoup(urllib2.urlopen(road).read())
    streetlist=[]
    latlist=[]
    lnglist=[]
    urllist=[]
    #Parse camera url in each page where each image will have a width of 350
    for tag in soup.find_all("img",{"width":"350"}):
        url=tag.get('src')
        #Deal with inconsistent formats the website stores cameras in
        if '/e-net/PublicWorks/TrafficCam/' not in url:
            url='/e-net/PublicWorks/TrafficCam/'+url
        url=weburl+url
        urllist.append(url)
    #Parse camera street address in each page
    for tag in soup.find_all("td",{"class":"hdrsub"}):
        add=tag.get_text().encode('utf-8')
        #Deal with NULL/junk information the website did not clean up
        if add != '\xc2\xa0':
            streetlist.append(add)
    #Pass each street address into Google API to fetch geo-locations
    for street in streetlist:
        #Generate the right address for the stadium camera
        if 'Sign' in street:
            street=street.replace('Sign','')
        street=street.replace(" ","+")
        street=street.strip()
        street=street+'+GrandJunction'
        api='http://maps.googleapis.com/maps/api/geocode/json?address='+street
        response = urllib2.urlopen(api).read()
        #Load by json module
        parsed_json = json.loads(response)
        content = parsed_json['results']
        #Extract latitude and longitude from the API json code
        loc = content[0]
        geo = loc['geometry']
        location2 = geo['location']
        lat = location2['lat']
        lng = location2['lng']
        string_lat = str(lat)
        string_lng = str(lng)
        latlist.append(string_lat)
        lnglist.append(string_lng)
        time.sleep(0.1)
    #Write output to file
    iter=0
    while iter < len(urllist):
        #Format the output
        output = streetlist[iter]+'#'+'Grand Junction'+'#'+'CO'+'#'+'USA''#'+urllist[iter]+'#'+latlist[iter]+'#'+lnglist[iter]
        iter +=1
        #print output
        file.write(output.encode('utf-8')+'\n')


if __name__ == "__main__":
    getGJ()

