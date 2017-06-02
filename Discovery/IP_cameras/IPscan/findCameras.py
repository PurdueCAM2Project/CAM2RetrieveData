#!/usr/bin/python
#
# This program takes a file that contains ranges of IP addresses and
# checks whether the IP addresses are likely to be IP cameras
# 
# The program takes one command-line argument as the name of the file
#
import os
import sys
import smtplib
import socket

import readKnownCameras
import generateIP
import checkOneIP

# read the paths of cameras
cameras = {} # create a dictionary
readKnownCameras.readPaths("knowncameras", cameras)

# read the list of IP addresses
arg = sys.argv[1]
fptr = open(arg, 'r')
numthread = 64
for oneline in fptr:
    # checkOneIP.check(oneline, cameras)
    generateIP.generateAllIP(oneline, cameras, numthread)
fptr.close()

