#! /usr/bin/env python
'''
Author: epberry, Fall 2013
This is a program to read camera data from a few hundred html files
and convert it into an xml file which can then by read by the database
'''

import sys
import os
import re
import xml.etree.ElementTree as ET

# Read in every file in the directory
directory = sys.argv[1]
os.chdir(directory)
files = os.listdir(".")

ip_addr = ""
country = ""
state_region = ""
city = ""
latitude = ""
longitude = ""
hostname = ""

# create top root of XML tree
root = ET.Element("cameras")

'''
Iterate through a series of html files, then parse those files
looking for certain keywords (like "IP:") which indicate
that descriptive information for the camera follows.  After finding
each peice of information, add it to the XML tree.  At the end of the
inner for loop, add that entire element to the tree.  The tree requires
decoding into UTF-8'''

for i in files:
    element = ET.Element("camera")
    afile = open(i, "r")
    lines = afile.readlines()
    for j in lines:
        if j.find("   IP:") > 0:
            holder = j.strip().split(":")
            ip_addr = ET.SubElement(element, "ip_addr")
            ip_addr.text = holder[1].strip().decode("utf8")
        if j.find("   Hostname:") > 0:
            holder = j.strip().split(":")
            hostname = ET.SubElement(element, "hostname")
            hostname.text = holder[1].strip().decode("utf8")
        if j.find("Country:") > 0:
            holder = j.strip().split(":")
            country = ET.SubElement(element, "country")
            country.text = holder[1].strip().decode("utf8")
        if j.find("State/Region:") > 0:
            holder = j.strip().split(":")
            state_region = ET.SubElement(element, "state_region")
            state_region.text = holder[1].strip().decode("utf8")
        if j.find("City:") > 0:
            holder = j.strip().split(":")
            city = ET.SubElement(element, "city")
            city.text = holder[1].strip().decode("utf8")
        # for latitude and longitude, strip out unnessecary characters
        # using regex
        if j.find("Latitude:") > 0:
            holder = j.strip().split(":")
            latitude = ET.SubElement(element, "latitude")
            latitude.text = re.sub('[^A-Z0-9\. ]+', holder[1].strip()).decode("utf8")
        if j.find("Longitude:") > 0:
            holder = j.strip().split(":")
            longitude = ET.SubElement(element, "longitude")
            longitude.text = re.sub('[A-Z0-9\. ]+', holder[1].strip()).decode("utf8")
    root.append(element)
    afile.close()

# write completed tree to XML file
tree = ET.ElementTree(root)
tree.write("../rawcameradata.xml", "UTF-8")

'''
After the information has been written to an XML file, use a series
of commands documented in the big data wiki under /system/database to
convert the XML file into the mysql database.
This code could be improved by writing directly to the database but for
the purposes of speed and my own knowledge gaps I did it this way through
XML'''

sys.exit(0)
