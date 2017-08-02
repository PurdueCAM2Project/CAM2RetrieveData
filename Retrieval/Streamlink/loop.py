
""" 
--------------------------------------------------------------------------------
Descriptive Name     : loop.py
Author               : Minghao Guo (Mina)								      
Contact Info         : guo288@purdue.edu
Date Written         : June 22, 2017
Description          : Used for looping through all the streaming webcam urls and transferring them into m3u8 urls by using fetchstreamsrc.py
Command to run script: python3 loop.py
Usage                : Can be imported into another script or run from the command line
Input file format    : N/A
Output               : A list of m3u8 urls
--------------------------------------------------------------------------------
"""

import streamlink
from bs4 import BeautifulSoup
from fetchstreamsrc import get_stream_src_from_url
import re
import sys
import string
import traceback
import logging
#from urllib.parse import urlparse
#url_type = urlparse(http://www.earthcam.com/usa/colorado/breckenridge/)
#read lines from earthcamURL

#read lines from earthcamURL

with open('earthcamURL.txt') as f:
    page_url = []
    page_url = f.readlines()
#loop through every line in the list  
    for line in page_url:
#parse the type of urls
		#url_type = urlparse(line.rstrip())
		#print(url_type)
		#scheme = url_type.scheme
			#print(scheme)
#transform the original urls into m3u8 ones using the function in fetchstreamsrc.py
        try:
            #src_url = []        
            src_url = get_stream_src_from_url(line.rstrip())
        #print(src_url)
        except Exception as e:
    #logging.error(traceback.format_exc())
            pass
        print(src_url)
#continue
#print(src_url)
#print("m3u8 url: %s", src_url)
