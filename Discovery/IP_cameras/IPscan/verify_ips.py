#!/usr/bin/python
import checkOneIP
import readKnownCameras
import sys

# read the paths of cameras
cameras = {} # create a dictionary
readKnownCameras.readPaths("knowncameras", cameras)
src = sys.argv[1]
dst = sys.argv[2]

# read the list of IP addresses
fptr = open(src, 'r')

def isValid(ipaddr):
    path = checkOneIP.check(ipaddr, cameras)
    # print path
    if (path == "Not Found"):
        return 0
    return 1

with open(dst, 'w') as f:
	for oneline in fptr:
		# remove the ending \n 
		oneline = oneline.rstrip('\n')
		print oneline
		if (isValid(oneline) == 1):
			f.write(oneline + '\n')
