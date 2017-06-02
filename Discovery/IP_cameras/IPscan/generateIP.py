#!/usr/bin/python
#
# This program takes a range of IP addresses and scans all IP
# addresses in the range.  The program uses multiple threads. If an IP
# address is not used, the program will wait until timeout.  If the
# program uses only a single thread, the program will likely take very
# long waiting for timeout.  Multiple threads scan multiple IP
# addresses simultaneously and reduces the execution time.
#

import threading
# import re
import sys
import math
import datetime
from time import gmtime, strftime

import checkOneIP
import int2ip
import ip2int
import printXML

class checkIPThread (threading.Thread): 
    def __init__(self, threadID, stval, enval, cameras):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.stval = stval
        self.enval = enval
        self.cameras = cameras
        # print "stval " + int2ip.convert(self.stval)
        # print "enval " + int2ip.convert(self.enval)
    def run(self):
        counter = 0
        endvalue   = self.enval;
        valuerange = self.enval - self.stval + 1
        while (counter < valuerange):
            # randomize the order of the IP addresses
            nextip = (counter * 104729) % valuerange
            nextip = (counter * 104729) % valuerange + self.stval
            ipaddr = int2ip.convert(nextip);
            # print ipaddr
            path = checkOneIP.check(ipaddr, self.cameras)
            if (path != "Not Found"):
                print strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " " + ipaddr
                fptr = open(ipaddr, 'w')
                fptr.write("<camera>\n") #Add more information e.g. login page
                printXML.out (fptr, "id", ipaddr)
                printXML.out (fptr, "path", path)
                printXML.out (fptr, "brand", self.cameras[path])
                fptr.write("</camera>\n")
                sys.stdout.flush() #flush the output
                fptr.close()
            counter = counter + 1

def generateAllIP(oneline, cameras, numthread):
    start, dash, end = oneline.partition('-')
    start, slash, size = oneline.partition('/')
    # oneline should be something like
    # 128.40.30.0-128.40.30.255
    # or
    # 128.10.0.0/16 means the first 16 bits are fixed
    # and the rage is 128.10.0.0-128.10.255.255
    # 128.40.30.0/24 means the first 24 bits are fixed
    # and the range is 128.40.30.0-128.40.30.255
    #
    # print oneline
    # convert IP addresses to integers
    stval = ip2int.convert(start)
    enval = 0
    if (slash == ""): # not slash
        enval = ip2int.convert(end)
    else:
        range = 32 - int(size)
        numip = int(math.pow(2, range))
        # print range
        # print numip
        enval = stval + numip - 1
    # print "start = " + str(stval) + " " + int2ip.convert(stval)
    # print "end   = " + str(enval) + " " + int2ip.convert(enval)
    valgap = (enval - stval) / numthread
    threadlist = []
    while (numthread > 1):
        # create threads, each thread is responsible for 
        # a group of IP addresses
        thread = checkIPThread(numthread, stval, stval + valgap, cameras)
        thread.start()
        threadlist.append(thread)
        numthread = numthread - 1
        stval = stval + valgap + 1
    # make sure the last thread handles all remaining IP addresses
    thread = checkIPThread(numthread, stval, enval, cameras)
    thread.start()
    threadlist.append(thread)
    # wait for all threads finish
    for th in threadlist:
        th.join()
