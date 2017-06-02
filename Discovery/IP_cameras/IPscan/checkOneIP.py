import checkCamera
#import getLocation
import canConnect
import printXML #move it
import sys

# check whether one IP address is a camera
# cameras is a map of paths and brands

def check(ipaddr, cameras): #cameras are all different image paths in knowncameras.txt
    # remove the ending \n
    ipaddr = ipaddr.rstrip('\n')
    # check whether a port number is specified
    address, colon, port = ipaddr.partition(':')
    if (port == ""):
        port = "80"
    if (canConnect.isOn(address, port) == 0):
       # print "cannot connect to " + ipaddr
       return "Not Found" # cannot connect to it
    path = checkCamera.isCamera(address, port, cameras) #address is a 200 response
    #pass image path and address to the camera
    #path returned is the full path(cameras is dictionary of paths)
    return path
