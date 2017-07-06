"""
--------------------------------------------------------------------------------
Descriptive Name     : <Opentopia popular cameras parser.py>
Author               : Ryan Schlueter
Contact Info         : rschluet@gmail.com
Date Written         : June 20, 2017
Description          : Parse cameras on opentopia's datbase of open ip cameras. Opentopia has a collection of worldwide
                       free, open ip cameras. According to their service, all cameras are unsecured and the owner of any
                       camera can contact them and opentopia will stop allowing access to that particular camera.
Command to run script: python opentopia.py
Usage                : (extra requirements to run the script: eg. have to be run within dev server)
Input file format    : (none)
Output               : <opentopia_output.txt>
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
import urllib2
import urllib
from bs4 import BeautifulSoup as BS
from Geocoding import Geocoding
import time




def main():
  f=open("insecam_output.txt", 'w')
  driver = webdriver.Firefox()
  driver.set_page_load_timeout(30)

  pages=2
  camsPerPage=6
  urls = [0]*((pages-1)*(camsPerPage))
  count=0
  for x in range(1, pages):

    url = ("http://www.insecam.org/en/byrating/?page="+str(x))
    driver.get(url)

    data = driver.find_elements_by_xpath("//div[@class = 'col-xs-12 col-sm-6 col-md-4 col-lg-4']/div/a/div/img")
    insecamlink=driver.find_elements_by_xpath("//div[@class = 'col-xs-12 col-sm-6 col-md-4 col-lg-4']/div/a")
    for y in range(0, len(data)):
      urls[count]=str(insecamlink[y].get_attribute("href"))
      count+=1
      # data2=data[x].get_attribute("src")
      # insecamlinks=insecamlink[x].get_attribute("href")
      # print (data2)
      # print (insecamlinks)
  driver.close()



  hdr = {'User-Agent': 'Mozilla/5.0'}
  # Find the stream and geo info from each of the links found earlier
  for x in range(0, 2):#len(urls)):
    try:
      print (urls[x])
      req = urllib2.Request(urls[x], headers=hdr)
      page=urllib2.urlopen(req)
      soup=BS(page, 'html.parser')
      time.sleep(1)


      a = soup.find_all("div")
      country = a[18].text.strip()
      region = a[24].text.strip()
      city = a[27].text.strip()
      lat = a[30].text.strip()
      lon = a[33].text.strip()
      brand = a[42].text.strip()

      b = soup.find_all("img")
      tempStream = b[0].get("src")
      tempStream=tempStream.split("/")
      stream = "http://" + tempStream[2]

      printOutput = ("Lat:\t\t" + str(lat) + "\nLon:\t\t" + str(lon) + "\nCountry:\t" + str(country) + "\nState:\t\t" + str(region) + "\nCity:\t\t" + str(city) + "\nBrand:\t\t" + str(brand) + "\nURL:\t\t" + str(stream))
      output = (str(lat) + "," + str(lon) + "," + str(country) + "," + str(region) + "," + str(city) + "," + str(brand) + "," + str(stream))
      print printOutput
      f.write(output)
    except Exception as e:
      print (e)
      pass






  # Works with Selenium
  # for x in range(0,len(urls)):
  #   print(x)
  #   driver.get(urls[x])
  #   try:
  #     streamHTML = driver.find_element_by_xpath("//div[@class = 'grid-container']/a/img")
  #     tempStream=streamHTML.get_attribute("src")
  #     tempStream=tempStream.split("/")
  #     stream = "http://" + tempStream[2]
  #     # print ("Stream: " + str(stream))
  #   except Exception as e:
  #     print e
  #     pass
  #
  #   for y in range(0,9):
  #     temp = driver.find_elements_by_xpath("//div[@class = 'camera-details__cell']")
  #     country = temp[0].text
  #     state = temp[2].text
  #     city = temp[3].text
  #     lat = temp[4].text
  #     lon = temp[5].text
  #     brand = temp[8].text
  #     f.write(str(lat)+","+str(lon)+","+str(country)+","+str(state)+","+str(city)+","+str(brand)+","+str(stream)+"\n")
  #   # print (len(details))
  f.close()

if __name__ == "__main__":
    main()
