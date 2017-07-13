# """
# --------------------------------------------------------------------------------
# Descriptive Name     : <Opentopia whole database parser>
# Author               : Ryan Schlueter
# Contact Info         : rschluet@gmail.com
# Date Written         : July 5, 2017
# Description          : Parse the entirety of opentopia's database. Find relevant geographical data and include that
#                       in a csv output file. This is slower, but gets more links than just going through the
#                       "most viewed" or "highest rated" links on opentopia's website, as some of the links not on those
#                       lists still give valid cameras, but are broken on opentopia's website
# Command to run script: python opentopia_bs4.py
# Usage                : (extra requirements to run the script: eg. have to be run within dev server)
# Input file format    : (eg. url#description (on each line))
# Output               : <whole_opentopia_output.txt>
# Note                 :
# Other files required by : N/A
# this script and where
# located
#
# ----For Parsing Scripts---------------------------------------------------------
# Website Parsed       : <opentopia.com>
# In database (Y/N)    :
# Date added to Database :
# --------------------------------------------------------------------------------
# """


import urllib2
from bs4 import BeautifulSoup as BS
from Geocoding import Geocoding

f=open("whole_opentopia_output.txt", 'w')

def parseOpentopia():
  for x in range(0, 17000):
    print(str(x))
    still_url = "http://www.opentopia.com/webcam/" + str(x) + "?viewmode=savedstill"
    vid_url   = "http://www.opentopia.com/webcam/" + str(x) + "?viewmode=livevideo"

    try:
      # Try to open the opentopia site with the saved still
      soup = BS(urllib2.urlopen(still_url), 'html.parser')
      a = soup.find_all("img")[1].get("src")

      # Only continue if the still image is not the stock "no image found" placeholder
      if(a!="/images/nosnapshot-715x536.jpg"):
        try:
          # Try to open the opentopia site with the live feed
          soup2 = BS(urllib2.urlopen(vid_url), 'html.parser')
          wholeURL = soup2.find_all("img")[1].get("src")
          cutUrl=wholeURL.split("/")
          ipAddress=cutUrl[2]
          # Store the ip address as something that can be opened by a web-browser with appropriate url tails
          ipAddress = "http://"+ipAddress

          try:
            # Try to open the url link of the feed located on the livefeed opentopia website
            # soup3 = BS(urllib2.urlopen(ipAddress, timeout=15), 'html.parser') # Full website
            soup3 = BS(urllib2.urlopen(ipAddress, timeout=2), 'html.parser') # Quick parse

            # Initialize geo info as none in case it's not found
            country = "none"
            state = "none"
            city = "none"
            location = "none"
            lat = "none"
            lon = "none"
            brand = "none"

            # Find all HTML elements with label types (all opentopia geo info data is stored as lables)
            b = soup.find_all("label")
            info=[0]*len(b)

            # Parse Geo Data assuming findign url went well. Split all label elements along their > and < characters.
            # Geo info is stored as <blahblahblah>RELEVENT_INFO<blahblahblah>. This pulls out the relevant info.
            # Special care is needed for lat and lon
            for y in range(0,len(b)):
              c = b[y]
              c = str(c)
              c=c.split(">")
              # print c
              if "latitude" in str(c):
                lat = c[2].split("<")[0]
                lon = c[4].split("<")[0]
              else:
                d=str(c[1])
                d=d.split("<")
                if ((len(d[0])==0)or(d[0][len(d[0])-1]==" ")):
                  # cut off last char if it's a space
                  temp=d[0][:-1]
                  info[y]=temp
                else:
                  # not needed
                  info[y]=d[0]

            # Pull out text for geo info from the extracted html strings if the category is present
            for n in range(2, len(info)):
              if (info[n - 1] == "Country:"):
                country = info[n]
              if (info[n - 1] == "State/Region:"):
                state = info[n]

              if (info[n - 1] == "Brand:"):
                brand = info[n]

              # Extra code is needed for city and location, as these sometimes contain commas within the text strings
              # which needs to be replaced
              if (info[n - 1] == "City:"):
                if "," in info[n]:
                  city2 = info[n]
                  city2 = city2.split(',')
                  city=city2[0]
                  for i in range(1,len(city2)):
                    city += " -"
                    city += city2[i]
                else:
                  city = info[n]

              if (info[n - 1] == "Facility:"):
                if "," in info[n]:
                  location2 = info[n]
                  location2 = location2.split(',')
                  location=location2[0]
                  for i in range(1,len(location2)):
                    location += " -"
                    location += location2[i]
                else:
                  location = info[n]

            # Only use geocoding.py is the GPS coords were not provided on the website
            if (lat=="none" or lon=="none"):
              newGeo = Geocoding("Google", "AIzaSyBZYcy365bFEbW1Qar5ij4EmUkaCdmbbBc")
              newGeo.locateCoords(location, city, state, country)
              lat=newGeo.latitude
              lon=newGeo.longitude

            # printOutput = ("Cam ID:\t\t" + str(x) + "\nLat:\t\t" + lat + "\nLon:\t\t" + lon + "\nCountry:\t" + country + "\nState:\t\t" + state + "\nCity:\t\t" + city + "\nLocation:\t" + location + "\nBrand:\t\t" + brand + "\nURL:\t\t" + ipAddress + "\n")
            output = (str(x) + "," + lat + "," + lon + "," + country + "," + state + "," + city + "," + location + "," + brand + "," + ipAddress + "," + wholeURL + "\n")
            # print (printOutput)
            f.write(output)
            print  ("good camera")
          except Exception as e:
            print e
            print ("Connection to IP camera failed")
            pass
        except:
          pass
    except (KeyboardInterrupt, SystemExit):
      raise
    except:
      pass

  f.close()

if __name__ == "__main__":
    parseOpentopia()
