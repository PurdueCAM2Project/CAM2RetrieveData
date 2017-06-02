#!/usr/bin/python
#
# find urls insdie an HTML page
#
import sys
import socket
import re

arg = sys.argv[1]
fptr = open(arg, 'r')
for oneline in fptr:
    data = oneline
    found = 1
    while (found == 1):
        mch = re.search("(.*?)(\"http://.*?\")(.*)", data)
        if mch:
            print mch.group(2)
            data = mch.group(3)
        else:
            found = 0
fptr.close()
