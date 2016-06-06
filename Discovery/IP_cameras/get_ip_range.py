#!/usr/bin/python
""" 
--------------------------------------------------------------------------------
Descriptive Name     : get_ip_range.py
Author               : unknown								      
Contact Info         : ssui@purdue.edu (Shengli Sui)
Description          : Take a host name (a URL) and find the range of IP addresses that 
                       belongs to the same organization
Command to run script: python get_ip_range.py <url textfile>
Input file format    : url
Output               : Information output to screen
Other files required by : N/A
this script and where 
located
--------------------------------------------------------------------------------
"""

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
