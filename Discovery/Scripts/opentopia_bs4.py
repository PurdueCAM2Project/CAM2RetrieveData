from selenium import webdriver
import urllib2
from bs4 import BeautifulSoup as BS
from Geocoding import Geocoding

f=open("bs_opentopia_out2_whole2.txt", 'w')

for x in range(0, 500):
  print(str(x))
  still_url = "http://www.opentopia.com/webcam/" + str(x) + "?viewmode=savedstill"
  vid_url   = "http://www.opentopia.com/webcam/" + str(x) + "?viewmode=livevideo"

  try:#will exit if a 404 error or something
    soup = BS(urllib2.urlopen(still_url), 'html.parser')
    a = soup.find_all("img")[1].get("src")
    if(a!="/images/nosnapshot-715x536.jpg"):

      try:
        soup2 = BS(urllib2.urlopen(vid_url), 'html.parser')
        wholeURL = soup2.find_all("img")[1].get("src")
        cutUrl=wholeURL.split("/")
        ipAddress=cutUrl[2]
        # print (ipAddress)
        ipAddress = "http://"+ipAddress

        try:
          soup3 = BS(urllib2.urlopen(ipAddress, timeout=15), 'html.parser')
          #Find Geo Data assuming findign url went well
          b = soup.find_all("label")
          country = "none"
          state = "none"
          city = "none"
          location = "none"
          lat = "none"
          lon = "none"
          brand = "none"
          info=[0]*len(b)
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
                # cut off last char
                temp=d[0][:-1]
                info[y]=temp
              else:
                # it's good
                info[y]=d[0]
          # print (info)
          for n in range(2, len(info)):
            if (info[n - 1] == "Country:"):
              country = info[n]
            if (info[n - 1] == "State/Region:"):
              state = info[n]

            if (info[n - 1] == "City:"):
              if "," in info[n]:
                city2 = info[n]
                city2 = city2.split(',')
                city=city2[0]
                for i in range(1,len(city2)):
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

            if (info[n - 1] == "Brand:"):
              brand = info[n]
	  

          if (lat=="none" or lon=="none"):
            newGeo = Geocoding("Google", "AIzaSyBZYcy365bFEbW1Qar5ij4EmUkaCdmbbBc")
            newGeo.locateCoords(location, city, state, country)
            lat=newGeo.latitude
            lon=newGeo.longitude


          printOutput = ("Cam ID:\t\t" + str(x) + "\nLat:\t\t" + lat + "\nLon:\t\t" + lon + "\nCountry:\t" + country + "\nState:\t\t" + state + "\nCity:\t\t" + city + "\nLocation:\t" + location + "\nBrand:\t\t" + brand + "\nURL:\t\t" + ipAddress + "\n")
          output = (str(x) + "," + lat + "," + lon + "," + country + "," + state + "," + city + "," + location + "," + brand + "," + ipAddress + "\n")
          print (printOutput)
          f.write(output)
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





