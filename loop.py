
""" 
--------------------------------------------------------------------------------
Descriptive Name     : loop.py
Author               : Minghao Guo (Mina)								      
Contact Info         : guo288@purdue.edu
Date Written         : June 22, 2017
Description          : Used for looping through all the earthcamURLs and transferred them into m3u8 urls by using fetchstreamsrc.py
Command to run script: python3 loop.py
Usage                : Can be imported into another script or run from the command line
Input file format    : N/A
Output               : A list of m3u8 urls
Note                 : This is only the initial script for getting all the m3u8 urls, it will stuck everytime it encounters an url of 				RTMP type, so I had to run fetchstreamsrc.py manually to get the information of those urls with issues. The 				next step is to identify the urls of RTMP type and deal with them specifically.
Other files required by : fetchstreamsrc.py (written by Caleb)
this script and where 
located
--------------------------------------------------------------------------------
"""

import streamlink
from bs4 import BeautifulSoup
from fetchstreamsrc import get_stream_src_from_url
import re
import sys
import string
import traceback
#from urllib.parse import urlparse
#url_type = urlparse(http://www.earthcam.com/usa/colorado/breckenridge/)
#read lines from earthcamURL

#read lines from earthcamURL
with open('opentopia.csv') as f:
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
		src_url = []
		src_url = get_stream_src_from_url(line.rstrip())
		print(src_url)
#print("m3u8 url: %s", src_url)
