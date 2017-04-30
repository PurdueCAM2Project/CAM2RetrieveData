"""
    --------------------------------------------------------------------------------
    Descriptive Name     : EarthCam_GPS.py
    Author               : Shengli Sui
    Contact Info         : ssui@purdue.edu
    Date Written         : April 1st, 2017
    Description          : Get the GPS coordinates of the camera from EarthCam
    Command to run script: python EarthCam_GPS.py
    Output               : gpsinfo.txt (latitude, longitude)
    Note                 :
    Other files required by : N/A
    this script and where
    located
    --------------------------------------------------------------------------------
    """
# Import the necessary python modules
from selenium import webdriver
import sys
import time

#Script utilizes selenium to extract links to image urls
#output will be the image urls and descriptions in file list_Houston
class getGPSinfo:
    def __init__(self):
        self.driver = webdriver.Firefox()  #Here we are using Firefox browser
    
    def extractinfo(self):
        my_file = open("gpsinfo.txt", "w")  #Open the website list file
        with open('websites.txt') as f:
            content = f.read().splitlines()  #Go through each line in the website list file
            for i in range(0,len(content)):
                self.driver.get(content[i])  #Go to the current website
                time.sleep(1);               #Wait for 1 second
                element=self.driver.find_element_by_xpath("//img[@id='static_map_image']")  #Locate the element
                element_attribute_value = element.get_attribute('src')  #Extract the GPS information
                start = 'center='
                end = '&zoom='
                s = element_attribute_value
                #print s[s.find(start)+len(start):s.rfind(end)]
                my_file.write(s[s.find(start)+len(start):s.rfind(end)]+'\n')  #Write the GPS information into the external file
        my_file.close()  #Close the file
        self.driver.quit();  #Close the broswer
        return;

if __name__ == '__main__':
    GPSinfo = getGPSinfo()
    GPSinfo.extractinfo()
