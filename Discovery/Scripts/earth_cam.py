"""
--------------------------------------------------------------------------------
Descriptive Name     : earthcam_parser
Author               : Kyle Martin				      
Contact Info         : marti716@purdue.edu
Date Written         : 06/02/17
Description          : Parse cameras on the earthcam network website
Command to run script: python3 earth_cam.py <link> <directory-for-cameras>
Usage                : No extra requirements
Input file format    : No input file necessary
Output               : Several .txt files stored in the directory specified on
                       the command line
Note                 : 
Other files required by : N/A
this script and where 
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : Designed for earthcam.com/network/
In database (Y/N)    : N
Date added to Database : N/A
--------------------------------------------------------------------------------
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import os
import re
import time

def get_earth_cams():
    
    # check that there is at least one argument
    if (len(sys.argv) != 3):
        raise Exception("Must have two arguments, a link and a directory")
    
    # create a new instance of a firefox web browser
    driver = webdriver.Firefox()
    driver_reg = webdriver.Firefox()
    driver_cam = webdriver.Firefox()
    
    # open the link
    driver.get(sys.argv[1])
    
    # create an output directory
    if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2])
        
    # find a list of elements with the class "locationLink"
    loc_links = driver.find_elements_by_class_name("locationLink")
        
    for loc_link in loc_links:
        # access the href
        href_reg = loc_link.get_attribute("href")
        
        # create the link for the region and go to that link in a new tab
        driver_reg.get(href_reg)
        
        # get a list of elements with the class "learnMore"
        cam_links = driver_reg.find_elements_by_class_name("regularTitleLink")
        
        for cam_link in cam_links:
            # access the href
            href_cam = cam_link.get_attribute("href")
            title_cam = cam_link.find_element_by_class_name(
                "regularTitle").get_attribute("innerHTML")
                        
            # go to the camera link in a new tab
            # try twice (sometimes a link times out the first time)
            num_attempts = 0
            while (num_attempts < 2):
                try:
                    num_attempts = 2
                    driver_cam.get(href_cam)
                except:
                    num_attempts += 1

            # if multiple attempts failed, skip this link
            if (num_attempts > 1):
                continue
                
            # get the HTML source
            html_source = driver_cam.page_source
            
            # create a file with the page title
            valid_title = make_valid_name(title_cam)
            f = open("./{0:s}/{1:s}.txt"
                     .format(sys.argv[2], valid_title), 'w')
            
            # update output file
            f.write(href_cam + "\n" + html_source)
            f.close()
                
            
    # close the drivers
    driver.close()
    driver_reg.close()
    driver_cam.close()

def make_valid_name(file_str):
    valid_file_str = re.sub(r' ', '_', file_str)
    valid_file_str = re.sub(r"[^\w-]", '', valid_file_str)
    return valid_file_str
    
if __name__ == "__main__":
    get_earth_cams()
