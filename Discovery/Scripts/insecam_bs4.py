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
import sys




def main():
  f=open("insecam_output.txt", 'w')
  hdr = {'User-Agent': 'Mozilla/5.0'}

  pages=500
  camsPerPage=6
  urls = [0]*((pages-1)*(camsPerPage))
  count=0
  print ("Loading pages")
  for x in range(1, pages):
    sys.stdout.write('.')
    sys.stdout.flush()
    url = ("http://www.insecam.org/en/byrating/?page="+str(x))
    req = urllib2.Request(url, headers=hdr)
    page = urllib2.urlopen(req, timeout=15)
    try:
      soup = BS(page, 'html.parser')
    except Exception as e:
      print e
      pass

    for a in soup.find_all('a', href=True):
      if ("view" in a['href']):
        urls[count] = str("http://www.insecam.org/" + a['href'])
        count+=1

  print ("\nPages loaded\n")
  # Find the stream and geo info from each of the links found earlier
  print ("Finding ip camera information\n")
  for x in range(0, len(urls)):
    print (str(x+1) + " out of " + str((pages-1)*(camsPerPage)))
    try:
      print (urls[x])
      req = urllib2.Request(urls[x], headers=hdr)
      page=urllib2.urlopen(req, timeout=15)
      soup=BS(page, 'html.parser')

      a = soup.find_all("div")
      if (a[18].text.strip()=="Country:"):
        country = a[19].text.strip()
        region = a[25].text.strip()
        city = a[28].text.strip()
        lat = a[31].text.strip()
        lon = a[34].text.strip()
        brand = a[43].text.strip()
      else:
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

      printOutput = ("Lat:\t\t" + str(lat) + "\nLon:\t\t" + str(lon) + "\nCountry:\t" + str(country) + "\nState:\t\t" + str(region) + "\nCity:\t\t" + str(city) + "\nBrand:\t\t" + str(brand) + "\nURL:\t\t" + str(stream) + "\n")
      output = (str(lat) + "," + str(lon) + "," + str(country) + "," + str(region) + "," + str(city) + "," + str(brand) + "," + str(stream) + "\n")
      print printOutput
      f.write(output)
    except Exception as e:
      print (e)
      pass
  f.close()

if __name__ == "__main__":
    main()
