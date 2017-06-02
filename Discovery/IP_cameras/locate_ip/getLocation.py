#!/usr/bin/python
#
# This function needs lynx (text mode web browser). Please make sure it
# is installed.
#
# The function takes a file pointer and and IP address.  The function
# sends a query to the web site whatismyipaddress.com to find the
# geographical location of the IP address (it is an approximation) and
# saves the result in the file.
#
# whatismyipaddress.com allows only 56 queries each hour. after
# responding to 56 queries, the web site will send a message asking to
# wait for an hour
# 
#
import httplib
import sys
import subprocess
import re

import printXML

def matchPrint(fptr, keyword, data):
    # print keyword
    pattern = keyword + ":\s+(.*)"
    # print pattern
    mch = re.search(pattern, data)
    if mch:
       printXML.out (fptr, keyword, mch.group(0))

def locate(fptr, address):
    query = "http://whatismyipaddress.com/ip/" + address;
    result = subprocess.Popen(["lynx", "-dump", query], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    resout, reserr = result.communicate()
    fptr.write(resout)
    """
    matchPrint(fptr, "IP", resout)
    matchPrint(fptr, "Hostname", resout)
    matchPrint(fptr, "ISP", resout)
    matchPrint(fptr, "Organization", resout)
    matchPrint(fptr, "Type", resout)
    matchPrint(fptr, "Country", resout)
    matchPrint(fptr, "State/Region", resout)
    matchPrint(fptr, "City", resout)
    matchPrint(fptr, "Latitude", resout)
    matchPrint(fptr, "Longitude", resout)
    """


