""" 
--------------------------------------------------------------------------------
Descriptive Name     : EarthCamParser.py
Author               : Ajay Gopakumar and Vikrant Satheesh Kumar
Email Id             : agopakum@purdue.edu, vsathees@purdue.edu
Date Written         : March 30, 2017
Description          : Downloads video from EarthCam webiste based on the 
		       CSV file inputted.
Command to run script: python EarthCamParser.py
Input file format    : .csv
Output               : .avi

Other files required by : ffmpeg.exe (https://ffmpeg.org/download.html)

--------------------------------------------------------------------------------

Format of Input CSV File:

(Sample CSV File available on Github)

RTMP STREAMS | URLS | SWF streams | FLV names | Output filename (no extension) | Duration

"""

from subprocess import Popen,PIPE,STDOUT
import os
import csv

#Check for the given file rtmpstreams.csv
# Please make sure to read the documentation and create a proper CSV file.
filename = raw_input ('Enter the input csv file name: ')

try:
	csv_handle = open(filename, 'rb')
	myreader = csv.reader(csv_handle,delimiter=",")
	
	# Necessary Fields
	rtmps=[]
	urls=[]
	swfs=[]
	outputfiles=[]
	durations=[]
	flvnames=[]

	k = 0;

	#get required info
	for row in myreader:
		rtmps.append(row[0])
		urls.append(row[1])
		swfs.append(row[2])
		flvnames.append(row[3])
		outputfiles.append(row[4])
		durations.append(row[5])
        
	del urls[0]
	del outputfiles[0]
	del swfs[0]
	del durations[0]
	del flvnames[0]	
	del rtmps[0]
	
	#run commands in bash 1 by 1
	for i in range(len(urls)):
		shell_command = 'rtmpdump -r ' + rtmps[i]+' -p "' + urls[i] 
		shell_command += '" -s "' + swfs[i] + '" -v -y ' + flvnames[i]
		shell_command += '.flv -R -o - | ffmpeg -i pipe:0 -t '+durations[i]+' '+ outputfiles[i]+'.avi'
		print shell_command
		event = Popen(shell_command,shell=True)
		(output,err)=event.communicate()

except:
	# Create a new csv file with the required info for easier access.
	option = raw_input("The file you specified does not exist! Create a new one? (Y/N): ")
        if option == 'Y' or option =="y":
		
		newFilename = raw_input ("\nEnter the file name: ")
		
		print "\nYour file has been successfully created! Please fill in the required info!"      	
        	
		# open a file
        	csv_handle = open('rtmpstreams.csv', 'wb')
        	mywriter = csv.writer(csv_handle)
        	mywriter.writerow(["RTMP STREAMS","URLS",
		"SWF streams","FLV names","Output filename (no 	extension)","Duration"])

        	#close file
        	csv_handle.close()
        else:
		# User did not want to create new file!
        	print "Closing program - Do not want to create file!"







