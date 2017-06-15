"""
--------------------------------------------------------------------------------
Descriptive Name     : TW_cam_parse
Author               : Kyle Martin
Contact Info         : marti716@purdue.edu
Date Written         : 05/30/2017
Description          : Parse cameras on Taiwanese traffic cam website
Command to run script: python3 TW_cam_parse.py
Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : www.1968.com.tw/1968MapV2/index.aspx#
In database (Y/N)    : 
Date added to Database :
--------------------------------------------------------------------------------
"""

from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
import sys
import time
import socket
import json

def tw_cam():

    # save the URL to the JSON file and then load and parse the file
    json_url = "http://www.1968.com.tw/1968MapV2/CCTV.json"
    json_data = urllib2.urlopen(json_url).read().decode('utf-8')
    #str_json_data = json_data.readall().decode('utf-8')
    parsed_data = json.loads(json_data)

    # open a data file
    f = open('tw_cam_list', 'w')

    # open a data file for failed links
    f_err = open('tw_cam_errs', 'w')

    # create the header line
    f.write("cam_id#snapshot_url#latitude#longitude#country#region#region2\n")

    # initialize counters for functional cameras and 404 cameras
    num_cams = 0
    num_404s = 0

    # extract camera info
    cams = parsed_data['features']
    tot_cams = len(cams)
    for cam in cams:
        # save properties, coordinates and link
        props = cam['properties']
        coord = cam['geometry']['coordinates']
        link = props['ScriptLink']

        # check camera link
        cam_avail = False
        num_attempts = 0
        while (cam_avail is False and num_attempts < 2):
            try:
                urllib2.urlopen(link, timeout=3)
                cam_avail = True
            except socket.timeout:
                cam_avail = True
            except:
                num_attempts += 1
                
        if (cam_avail):
            cam_id = props['cctv_id']
            lat = coord[1]
            lon = coord[0]
            reg = props['region']
            reg2 = props['region2']
            f.write("{0:s}#{1:s}#{2:f}#{3:f}#Taiwan#{4:s}#{5:s}\n"
                    .format(cam_id, link, lat, lon, reg, reg2))
            num_cams += 1
        else:
            num_404s += 1
            f_err.write("{0:s}\n".format(link))

        # display the current progress bar
        printProgressBar(num_cams + num_404s, tot_cams)
    
    # print out the number of cameras and the number of 404s
    print("found {0:d} cameras, {1:d} 404s".format(num_cams, num_404s))
    
    return

def printProgressBar(cur, tot, decimals = 2, length = 50):
    str_percent = ("{0:." + str(decimals) + "f}").format(
        100 * (cur / float(tot)))
    filled_length = int(length * cur // tot)
    bar = '#' * filled_length + '-' * (length - filled_length)
    print('\r|%s| %s%%\r' % (bar, str_percent), end='\r')
    if (cur == tot):
        print()

if __name__ == '__main__':
    tw_cam()
