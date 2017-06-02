#!/usr/bin/python
# 
# read the paths and brands of known IP cameras
#
import re

def readPaths(filename, cameras):
    fptr = open(filename, 'r')
    for oneLine in fptr:
        mch = re.search("\s*(.*)\s*#\s*(.*)\s*", oneLine)
        # match is a python command so I use mch
        path = mch.group(1)
        brand = mch.group(2)
        path = path.rstrip(' ')
        brand = brand.rstrip(' ')
        # print "path = " + path + "--brand = " + brand + "---"
        cameras[path] = brand
    fptr.close()
