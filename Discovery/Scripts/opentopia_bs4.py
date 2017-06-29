from selenium import webdriver
import urllib2
from bs4 import BeautifulSoup as BS
from Geocoding import Geocoding

f=open("bs_opentopia_out2_0to5k.txt", 'w')

for x in range(0,5000):
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
          soup3 = BS(urllib2.urlopen(ipAddress, timeout=4), 'html.parser')
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
              city2 = info[n]
              city2 = city2.split(',')
              city = city2[0]+city2[1]
            if (info[n-1]=="Facility:"):
              location = info[n]
            if (info[n - 1] == "Brand:"):
              brand = info[n]

          if (lat=="none" or lon=="none"):
            newGeo = Geocoding("Google", "AIzaSyBZYcy365bFEbW1Qar5ij4EmUkaCdmbbBc")
            newGeo.locateCoords(location, city, state, country)
            lat=newGeo.latitude
            lon=newGeo.longitude


          output = (str(x) + "," + lat + "," + lon + "," + country + "," + state + "," + city + "," + location + "," + brand + "," + ipAddress + "\n")
          print (output)
          f.write(output)
        except Exception as e:
          print e
          print ("Connection to IP camera failed")
          pass
      except:
        pass
  except:
    pass

f.close()





