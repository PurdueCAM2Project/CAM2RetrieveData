###############################################################################
# Descriptive Name for File: Create Output Text File for Parsing Scripts
#
# Written by: Thomas Norling					 				      
# Contact Info: thomas.l.norling@gmail.com
#
# Command to Run Script: Should not be run from command line
# Other files required by this script and where located: None
#
# Description: 
#   1. Import Class: from WriteToFile import WriteToFile
#
#   2. Instatiate an instance of the class: variable = WriteToFile(states, filename)
#   where states is True/False whether you are parsing USA cameras or not
#   and filename is the filename/filepath of the file you want to write to
#
#   3. Call the function to write info each time you have new information to write:
#   variable.writeInfo(country, state, city, link, latitude, longitude)
#   where country, state, city, link, latitude, longitude are self explanitory
#   
#   Note: If the country is not USA call the function with state = ""
#
# DO NOT PUT USERNAMES/PASSWORDS IN CODE
###############################################################################

import time

class WriteToFile:
    def __init__(self,states,filename):
        self.f = open(filename, 'w')
        if states == True:  
            self.f.write("country#state#city#snapshot_url#latitude#longitude\n")
            time.sleep(0.5)
        else:
            self.f.write("country#city#snapshot_url#latitude#longitude\n")
            time.sleep(0.5)
    
    def writeInfo(self, country, state, city, link, latitude, longitude):
        info = str(country) + '#' + state + '#' + str(city) + '#' + link + '#' + latitude + '#' + longitude
        self.f.write(info.encode('utf-8').replace(" ","").replace("##", "#").replace("\n",'')+'\n')
        time.sleep(1)