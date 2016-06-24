#!/usr/bin/python
'''
--------------------------------------------------------------------------------
Descriptive Name     : LafayetteLA.py
Author               : Chan Weng Yan (Adapted from unknown author) 
Contact Info         : cwengyan@purdue.edu
Date Written         : June 13, 2016
Description          : Parse cameras on the Lafayette, Louisiana traffic camera website
Command to run script: python Lafayatte_LA.py
Output               : country#state#description#url#lat#long to <list_LafayetteLA.txt>
Note                 : 
Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.lafayettela.gov/trafficcameras/Traffic_Cameras.aspx
In database (Y/N)    : Y
Date added to Database : June 3, 2016
--------------------------------------------------------------------------------
'''

from bs4 import BeautifulSoup
import urllib2
import re
import sys
import json
import time

def Lafayette():
    Lafa_url = 'http://www.lafayettela.gov/trafficcameras/Traffic_Cameras.aspx'
    soup = BeautifulSoup(urllib2.urlopen(Lafa_url).read())
    linkls=[]
    iter = 0

    #create a file named file_lafa and creat Lf_ls txt file to be output
    file_lafa = open('list_LafayetteLA.txt','w')
    file_lafa.write('country#state#city#description#snapshot_url#latitude#longitude'+'\n')

    #get list of links to append to url to create different soup
    urllist=[]
    urllist.append('Traffic_Cameras.aspx')
    for table in soup.find_all('input',{'type':'image'}):
        camLinks=re.split('"',table['onclick'],flags=re.I)
        urllist.append(camLinks[7])

    for url in urllist:
        Lafa_url = 'http://www.lafayettela.gov/trafficcameras/' + str(urllist[iter])
        soup = BeautifulSoup(urllib2.urlopen(Lafa_url).read())
        for ls in soup.find_all('div',{'id':'ctl00_ContentPlaceHolder1_upnlMain'}):
            for src in ls.find_all('img'):
                name='USA'+'+'+'Louisiana'+'+'+'Lafayette'+'+'+src['alt'].encode('utf-8')
                name1 = name.replace(" ","+")
                name2 = name1.replace("AMBASSADOR","Ambassador+Caffery+Pkwy")

                #use API to find the latitude and longitude
                api = 'http://maps.googleapis.com/maps/api/geocode/json?address='+name1+'&sensor=true_or_false'
                response = urllib2.urlopen(api).read()

                #load by json module 
                parsed_json= json.loads(response)
                content= parsed_json['results']

                #extract latitude and longitude from the API json code
                loc= content[0]
                geo = loc['geometry']
                location2 = geo['location']
                lat = location2['lat']
                lng= location2['lng']

                #change lat and lng to string
                string_lat = str(lat)
                string_lng = str(lng)
                link = 'USA'+'#'+'LA'+'#'+'Lafayette'+'#'+src['alt']+'#'+src['src']+'#'+string_lat+'#'+string_lng
                print(link)
                file_lafa.write(link.encode('utf-8')+'\n')
                time.sleep(0.5)
        iter += 1
    file_lafa.close()

if __name__ == '__main__':
    soup = Lafayette()
