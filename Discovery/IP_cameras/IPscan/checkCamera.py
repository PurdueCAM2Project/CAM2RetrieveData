#!/usr/bin/python
#
# This function takes three arguments: an IP address, a port number,
# and a map of cameras (path-brand)
#
# The function goes through each possible path and sends the GET
# command to the IP address and the port.  If the response is 200
# (HTTP OK), this function thinks the IP address is a network camera.
# For unknown reasons, this function has many false positive (the
# function thinks an IP address is camera but it is actually not a
# camera). 
# 
import httplib
import re
import getImage
from camera import IPCamera
from getImage import archiver
from checkLogin import loginRequired
import printXML
def isCamera(address, port, cameras):
    for path in sorted(cameras.keys()):
       #print("These are the paths that looped through:\n")
       #print(path)
       #print("These are the cameras: \n")
       #print(cameras.keys()) #\video2.mjpeg
       #print("These are the sorted cameras: \n")
       #print(sorted(cameras.keys())) #\MJPEG.CGI
       #Only goes once through the loop, unless the first path.resp.status != 200 -> Once 200, returns
       #it gets a 200 response with the first key no matter what
       #bc it redirects to html.login
       try:
          conn = httplib.HTTPConnection(address, port, timeout = 5)
          conn.request("GET", path)
          resp = conn.getresponse()
       except Exception:
          # print "exception HTTPConnect"
          return "Not Found"
       if (resp.status == 200):
           try:
               if(loginRequired(address) == 0): #no login is found
                   camera = IPCamera(1, 1, address, path)
                   archiver(camera)
                   return path
                   #This needs more improvement.
                   #What if more than 1 path?
                   #continue with finally, then return path?
               else:
                   file = open("Ip_Requires_Login.txt", 'a')
                   file.write("<camera>\n")
                   printXML.out(file, "ip", address)
                   printXML.out(file, "path", path)
                   printXML.out(file, "brand", cameras[path])
                   file.write("</camera>\n")
                   file.close()
                   return path
           except Exception:
               return "Not Found"
    return "Not Found"

