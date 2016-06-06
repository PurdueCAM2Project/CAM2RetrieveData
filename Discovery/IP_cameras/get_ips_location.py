""" 
--------------------------------------------------------------------------------
Descriptive Name     : get_ips_location.py
Author               : unknown								      
Contact Info         : ssui@purdue.edu (Shengli Sui)
Description          : Prints the approximate GPS locations of a list of IP addresses
Command to run script: python get_ips_location.py <IP_address textfile>
Usage                : For each IP, the function sends a query to the web site 
		       whatismyipaddress.com to find the geographical location of the 
		       IP address (it is an approximation) and prints the location on the screen.

		       whatismyipaddress.com allows only 56 queries each hour. after
		       responding to 56 queries, the funtion will wait for an hour
Input file format    : IP address (on each line)
Note		     : This function needs lynx (text mode web browser). Please make sure it is installed.
 
Other files required by : N/A
this script and where 
located

--------------------------------------------------------------------------------
"""

import subprocess
import re
import time
import sys

def get_ips_locations(ips_file_name):
	with open(ips_file_name, 'r') as ips_file:
		ips = ips_file.read().splitlines()

	with open(ips_file_name + '_locations', 'w') as locationsfile:
		for index, address in enumerate(ips):
			if ":" in address:
				address = address.split(':')[0]

			query = "http://whatismyipaddress.com/ip/" + address;
			result = subprocess.Popen(["lynx", "-dump", query], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			resout, reserr = result.communicate()

			if resout.strip()[0:3] == "Too":
				time.sleep(3601)
				result = subprocess.Popen(["lynx", "-dump", query], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				resout, reserr = result.communicate()
	
			latmatch = re.search("Latitude:\s*([\d\.]+)\s*\(", resout)
			lonmatch = re.search("Longitude:\s*([\-\d\.]+)\s*\(", resout)

			if (latmatch and lonmatch):
				lat = latmatch.group(1)
				lon = lonmatch.group(1)
				print str(index + 1), str(lat), str(lon)
				locationsfile.write(str(index + 1) + ' ' + str(lat) + ' ' + str(lon) + '\n')
			else:
				print "Not Found"
				locationsfile.write("Not Found\n")

if __name__ == '__main__':
	get_ips_locations(sys.argv[1])
