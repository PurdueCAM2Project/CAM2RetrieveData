#!/usr/bin/python

# take a host name (an URL) and find the range of 
# IP addresses belonging to the same organization
import sys
import socket
import subprocess
import re

arg = sys.argv[1]
# read the list of URLs
fptr = open(arg, 'r')
for oneline in fptr:
    # remove the ending \n 
    oneline = oneline.rstrip('\n')
    try: 
        ipaddr = socket.gethostbyname(oneline)
    except Exception:
        pass # do nothing, ignore this exception
    # print ipaddr + " " + oneline
    result = subprocess.Popen(["whois", ipaddr], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    resout, reserr = result.communicate()
    print "=========================================="
    print ipaddr + " " + oneline
    print resout

fptr.close()
