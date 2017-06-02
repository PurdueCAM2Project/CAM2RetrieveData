#!/usr/bin/python
import checkCamera
import getLocation
import canConnect
import printXML
import checkOneIP
import readKnownCameras
import sys
import socket
import time

# read the paths of cameras
cameras = {} # create a dictionary
readKnownCameras.readPaths("knowncameras", cameras)
arg = sys.argv[1]

# read the list of IP addresses
fptr = open(arg, 'r')
namecount = 1000
location  = 0

def isValid(ipaddr):
    path = checkOneIP.check(ipaddr, cameras)
    # print path
    if (path == "Not Found"):
        return 0
    """
    try: 
        hostname, alias, addrlist = socket.gethostbyaddr(ipaddr)
    except Exception:
        return 0
    """
    return 1
    
for oneline in fptr:
    # remove the ending \n 
    oneline = oneline.rstrip('\n')
    if (isValid(oneline) == 1):
        filename = "cam" + str(namecount) + ".html"
        htmlfptr = open(filename, 'w')
        htmlfptr.write("<title>" + oneline + "</title>\n")
        htmlfptr.write("<!---\n")
        printXML.out (htmlfptr, "id", oneline)
        address, colon, port = oneline.partition(':')
        if (location == 1):
            getLocation.locate(htmlfptr, address)
        htmlfptr.write("--->\n")
        htmlfptr.write("<h2> IP: " + oneline + "</h2>\n")
        try: 
            path = checkOneIP.check(oneline, cameras)
            # printXML.out (htmlfptr, "path", path)
            # printXML.out (htmlfptr, "brand", cameras[path])
            htmlfptr.write("<h2> Brand: " + cameras[path] + "</h2>\n")
            hostname, alias, addrlist = socket.gethostbyaddr(oneline)
            htmlfptr.write("<h2> Hostname: " + hostname + "</h2>\n")
        except Exception:
            pass
        htmlfptr.write("<a href=\"http://" + oneline + path + "\">\n")
        htmlfptr.write("<img height=300 src=\"http://" + oneline + path + "\"></a>") 
        htmlfptr.write("\n\n")
        # create the Back and Next links
        htmlfptr.write("<p><a href=\"cam" + str(namecount - 1) + ".html\">")
        htmlfptr.write("Back</a>\n")
        htmlfptr.write("<p><a href=\"cam" + str(namecount + 1) + ".html\">")
        htmlfptr.write("Next</a>\n")
        namecount = namecount + 1
        if ((namecount % 50) == 0):
            if (location == 1):
                # whatismyipaddress allows 56 queries each hour
                # sleep for one hour
                time.sleep(3601);
        htmlfptr.close();
fptr.close()
