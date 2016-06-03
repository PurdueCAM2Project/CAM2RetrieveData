#!/usr/bin/env python
"""
    Author: Tao Tian
    Date: July 8, 2014
    This script checks if the cameras parsed have been added to database.
    Things you need to make sure before using this script:
    1. The script has to be placed on develop machine along with the output file of your parsing script.
    2. To run his script:
       python check_camera_exist.py <filename>
       
       <filename> is the file that contains a list of urls you want to check
    3. If the camera has not been added into database, the url of that camera will be stored in filename_need_added file
    
    The input file should have the format:
    url#description
    on each line.
    
"""
import MySQLdb
import sys

#Input validation
if(len(sys.argv) != 2):
    print "Usage: check_camera.py <filename>"
    sys.exit(1)

#Load links from your output file
input_file = sys.argv[1]
fin = open(input_file, 'r')
links = []
for line in fin:
    line = line.strip()
    data = line.split('#')
    links.append(data[0])
fin.close()

#Logon to database
db = MySQLdb.connect("localhost", "root","a9L&uC$qu@R3F", "cam2")
cursor = db.cursor()
#Get camera links that have been added in database
query = "Select camera_key from camera"
result = cursor.execute(query)
links_database = []
for row in cursor.fetchall():
    links_database.append(row[0])
#check if the links from output file is in the database
links_to_be_added = []
for link in links:
    if(not (link in links_database)):
        links_to_be_added.append(link)

#Output the links still need to be added if neccessary
if len(links_to_be_added) != 0:
    print "Some of the cameras have not been added to the database! Those camera links are stored in the _need_added file."
    fout = open(input_file + "_need_added", 'w')
    for link in links_to_be_added:
        fout.write(link + '\n')
    fout.close()
else:
   print "Cameras are already in the database"
