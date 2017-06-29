"""
--------------------------------------------------------------------------------
Descriptive Name     : <BeachCamUsa all cameras parser.py>
Author               : Ryan Schlueter
Contact Info         : rschluet@gmail.com
Date Written         : June 20, 2017
Description          :
Command to run script: python beachcamsusa.py
Usage                : (extra requirements to run the script: eg. have to be run within dev server)
Input file format    : (none)
Output               : <beachcamsusa_output.txt>
Note                 :
Other files required by : N/A
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : <insert url>
In database (Y/N)    :
Date added to Database :
--------------------------------------------------------------------------------
"""

# Necessary Import Statements, selenium allows for web-crawling. Maybe switch to Beautiful Soup for faster performance
import selenium
from selenium import webdriver
from selenium.webdriver.support.select import Select
import urllib
import time




def main():
  driver = webdriver.Firefox()
  driver.set_page_load_timeout(45)
  f=open('beachcams_output.txt', 'w')

  url="http://www.beachcamsusa.com/"
  driver.get(url)
  data = driver.find_elements_by_xpath("//section[@class = 'block block-views block-even block-count-8 block-region-sidebar-first']/div/div/div/div/div/ul/li")
  time.sleep(1)


  # Finds the current states with cameras on the databse and how many cameras each state has
  states=[0]*(len(data))
  nums=[0]*(len(data))
  for x in range(0,len(data)):
    data2 = data[x].text
    data2 = data2.split(' ')
    state = str(data2[0])
    num = str(data2[1])
    num=num[1:]#Cut off first char
    num=num[:-1]#Cut off last char
    num=int(num)
    states[x]=state
    nums[x]=num

  print(sum(nums))
  webAddresses=[0]*sum(nums)
  count=0
  for x in range(0,len(states)):
    for y in range(0,(nums[x]/10)+1):
      url = "https://www.beachcamsusa.com/states/" + str(states[x]) + "?page=" + str(y)
      # print(url)
      driver.get(url)
      links = driver.find_elements_by_xpath("//section[@id = 'main-content']/div/div/div/div/div/div/div/div")
      # print (len(links))
      for z in range(0,len(links)):
        links2=links[z].find_elements_by_xpath("//div[@class = 'views-field views-field-title']/span/a")
        links3=links2[z].get_attribute("href")
        print (links3)
        webAddresses[count]=links3
      time.sleep(0.5)




















  # for state in states:
  #   url = "http://www.beachcamsusa.com/states/" + str(state)
  #   driver.get(url)
  #
  #   # streams = driver.find_element_by_xpath("//div[@class='view-content']/div/div/div").get_attritube("href")
  #   data = driver.find_elements_by_xpath("//div[@class = 'view-content']")
  #   streams = data[1].find_elements_by_xpath("//div[@class = 'views-field views-field-title']")
  #   print (len(streams))
  #
  #   # print(str(state) + " " + str(len(streams)))


if __name__ == "__main__":
    main()