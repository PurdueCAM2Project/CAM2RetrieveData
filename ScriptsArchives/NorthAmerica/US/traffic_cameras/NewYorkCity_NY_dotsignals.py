"""
--------------------------------------------------------------------------------
Descriptive Name     : NewYorkCity_NY_dotsignals
Author               : Ryan Dailey				      
Contact Info         : dailey1@purdue.edu
Description          : Parses the New York City Camera Website http://dotsignals.org/
Command to run script: NewYorkCity_NE_dotsignals.py
Input file format    : N/A
Output               : NewYorkCity_NY_dotsignals_list
Note                 :
Other files required by : This code requires PhantomJS a headless web browser found at https://nodejs.org/en/
this script and where 	  to be located in the same directory as the script.
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://dotsignals.org
In database (Y/N)    : Yes (6/8/16)
--------------------------------------------------------------------------------
"""
from bs4 import BeautifulSoup
import urllib2
import re
import sys
import time
import json
from selenium import webdriver
import platform


def nycdot():

	if platform.system() == 'Windows':
	    PHANTOMJS_PATH = './phantomjs.exe'
	else:
	    PHANTOMJS_PATH = './phantomjs'

	browser = webdriver.PhantomJS(PHANTOMJS_PATH)

	
	JSonURL = "http://dotsignals.org/new-data.php" # URL to the JSon File Containing Map Data
	CameraPopupURL = "http://dotsignals.org/google_popup.php?cid=" # URL to access the cameara URL
	f = open('list_NewYorkCity_NY_dotsignals','w') # Open an output file for writing
    
    # Write the header info into the file
	f.write("description#snapshot_url#latitude#longitude#country#state#city\n")

    # Load JSon file into responce
	response = urllib2.urlopen(JSonURL).read()
    # Parse the JSon file with the json module
	parsed_json= json.loads(response)

	cameras = parsed_json['markers'] # Navigate to the "markers" key

	for camera in cameras:
		cam_id = camera['id']
		content = camera['content']
		latitude = camera['latitude']
		longitude = camera['longitude']
		url = CameraPopupURL+cam_id

		browser.get(url) # Load the URL with Selenium in the PhantomJS browser
		soup = BeautifulSoup(browser.page_source) # Extract the page source and send it to BeautifulSoup

		snapshot_url = soup.find('img').get('src') # Use BeautifulSoup to parse the page and find all the image source tags

		
		if re.search(r'img/inactive', snapshot_url) == None:
			snapshot_url = re.search(r'(?P<URL>[\w\.\/:\\]*)', snapshot_url).group('URL')
			f.write(content+"#"+str(snapshot_url)+"#"+latitude+"#"+longitude+"#"+"USA#NY#New York\n") 
		pass

	browser.quit()
	f.close()
	return


if __name__ == '__main__':
	nycdot()
