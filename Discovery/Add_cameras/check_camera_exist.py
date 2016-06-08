#!/usr/bin/env python
""" 
--------------------------------------------------------------------------------
Descriptive Name     : check_camera_exist.py
Author               : Tao Tian								      
Contact Info         : N/A
Date                 : July 8, 2014
Description          : This script checks if the cameras parsed have been added to database. 
Command to run script: python check_camera_exist.py <filename>
Usage                : 1) The script has to be placed on develop machine along with the
                          output file of your parsing script.
                       2) <filename> is the file that contains a list of urls you want to check
                       3) If the camera has not been added into database, the url of that camera 
                          will be stored in <filename_need_added> file
Input file format    : url#description (on each line)

Other files required by : N/A
this script and where 
located
--------------------------------------------------------------------------------
"""

import MySQLdb
import sys
import getpass
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
password = getpass.getpass()
#Logon to database
db = MySQLdb.connect("localhost", "root",password, "cam2")
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
