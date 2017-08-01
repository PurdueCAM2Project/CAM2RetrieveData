"""
--------------------------------------------------------------------------------
Descriptive Name     : <Livestream.com popular streams parser>
Author               : Ryan Schlueter
Contact Info         : rschluet@gmail.com
Date Written         : June 27, 2017
Description          : Parse every camera on livestream.com's database. Outputs a list of URL's to be run through
                        Caleb/Mina's code to find the stream url. Streams are all high quality (most are 720p 30fps),
                        but are subject to being cut off whenever the event ends. Also potentially copywritten.
Command to run script: python livestream.py
Usage                : (extra requirements to run the script: eg. have to be run within dev server)
Input file format    : (none, base url included in code)
Output               : <livestream_output.txt>
Note                 : urls in output file have new line characters after each one. Maybe switch to BS4 for performance
Other files required by : N/A
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : <livestream.com> (Parses popular streams)
In database (Y/N)    : N
Date added to Database :
--------------------------------------------------------------------------------
"""

import selenium
from selenium import webdriver
import time




def main():
    # Open output file
    f=open('livestream_output.txt', 'w')

    # Initializes the selenium webdriver
    driver = webdriver.Firefox()# PhantomJS
    driver.set_page_load_timeout(5)#Set to 5 for testing, 30 for actual runs
    url="https://livestream.com/watch/popular"
    driver.get(url)
    time.sleep(0.5)


    # Load every page on the "popular" homepage. Loading the first 20 pages, (540 streams) on the popular page should
    # retrieve high amounts of high quality streams. Loads each additional page of info below the current one by
    # clicking the load more button. Should get 20 links per page. First and final pages are where 540 comes from 25*20
    pages=25
    for x in range(0, pages):
        driver.find_element_by_id('load_more').click()
        time.sleep(1.5)#Can decrease if using a headless browser, or for actual runs. Delay is there to load thumbnails

    #Finds the links of every thumbnail loaded on the page
    data = driver.find_elements_by_xpath("//div[@class = 'each_event_card js-event_card js-card']")
    data2=data[1].find_elements_by_xpath("//div[@class = 'event_card_bottom']/a")
    for x in range(0, len(data2)):
        data3=data2[x].get_attribute("href")
        f.write(str(data3) + "\n")
        time.sleep(0.01)


if __name__ == "__main__":
    main()
