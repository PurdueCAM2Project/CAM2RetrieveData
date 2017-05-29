""" 
--------------------------------------------------------------------------------
Descriptive Name     : youtubeDownloader.py
Author               : Vikrant Satheesh Kumar
Email Id             : vsathees@purdue.edu
Date Written         : 5 / 28 / 17
Description          : This program downloads images from YouTube videos and
		       saves it in a format given by the user.
Command to run script: python youtubeDownloader.py
Input file format    : .csv
Output               : Output depends on what the user wants. (eg: jpeg, bmp, etc)
Other files required by : ffmpeg, youtube-dl
--------------------------------------------------------------------------------

Note:

1. To install youtube-dl:	sudo pip install youtube-dl
2. To install ffmpeg (Linux):   sudo apt-get install ffmpeg

INPUT CSV FILE FORMAT: 

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+ FOLDER NAME +	DURATION(S) + OUTPUT FORMAT + OUTPUT NAME + LINK +
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Additional: Code tested:	python2.7
	    Operating SystemL	Ubuntu 16.04
"""

# Checking for import.
try:
	from subprocess import Popen, PIPE, STDOUT
	import os
	import csv
	import argparse
except:
	print "Import Failed! Please satisfy all dependencies!"
	raise SystemExit


def youtubeDownloader(filename):
	#Check for the given file rtmpstreams.csv
	# Please make sure to read the documentation and create a proper CSV file.
	
	csv_handle = open(filename, 'rb')
	myreader = csv.reader(csv_handle,delimiter=",")
	
	# Necessary Fields
	folder     = []
	duration   = []
	out_format = []
	out_name   = []
	link       = []

	k = 0;

	# Get the necessary information
	try:
		for row in myreader:
			folder.append(row[0])
			duration.append(row[1])
			out_format.append(row[2])
			out_name.append(row[3])
			link.append(row[4])
	except:
		print("Invalid entries in csv. Most likely the wrong fields were filled! Please use readme for instructions to fill csv")
		raise SystemExit
        
	del folder[0]
	del duration[0]
	del out_format[0]
	del out_name[0]
	del link[0]
	
	#Run commands in bash 1 by 1
	# Sample BASH command executed in one iteration of the for loop.
	# youtube-dl "https://www.youtube.com/watch?v=MwhqdVICTA0" -o - | ffmpeg -i pipe:0 -t 2 image%0d.jpg
	
	try:
		for i in range(len(link)):
			
			try:
				# Check if the folder already exists. If no, create one.
				if(os.path.isfile(folder[i]) != True):
					makeDirectory = "mkdir " + folder[i] + "; cd " + folder[i]
					event = Popen(makeDirectory,shell = True)
					(output,err)=event.communicate()
				else:
					changeDirectory = "cd " + folder[i]
					event = Popen(changeDirectory,shell = True)
					(output,err)=event.communicate()
		
				shell_command = 'youtube-dl ' + link[i] + ' -o - | ffmpeg -i pipe:0 -t ' 
				shell_command += duration[i] + ' '
				shell_command += "./" + folder[i] + "/" + out_name[i] + "%0d." + out_format[i]
 
				# Open the shell
				event = Popen(shell_command,shell = True)
				(output,err) = event.communicate()
 
				backToWorkingDirectory = ".."
				event = Popen(backToWorkingDirectory,shell = True)
				(output,err) = event.communicate()
			except:
				print ("Failed while Downloading. Please try again.")
				raise SystemExit
	except:
		print ("Incorrect entries in CSV file! Please fill the file according to the documentation!")
		raise SystemExit

# Create a new file with given name.
def createnewfile(newfile,optioncreate):
    try:
        if optioncreate.lower() == "yes":
            if(os.path.isfile(newfile)):
                print "File Exists! Exiting"      
                    
            else:
                # open a file
                csv_handle = open(newfile, 'wb')
                mywriter = csv.writer(csv_handle)
                mywriter.writerow(["FOLDER NAME","DURATION(S)","OUTPUT FORMAT","OUTPUT NAME","LINK"])

                #close file
                csv_handle.close()
                print "File created with name ",newfile
        else:
            print "File not found! Exiting"
    except():
            print "Unable to create file! Exiting!"
            csv_handle.close()

if __name__ == '__main__':

	# Parsing the given input arguments.
	parser = argparse.ArgumentParser()
	help_f = "Name of CSV file containing info with .csv extension (should be in same directory as program)"
	help_n = "Takes a string to create new csv file(must have .csv extension)"
	help_c = "Yes to create new file is file with filename does not exist"

	parser.add_argument('-f', '--filename', help = help_f, type = str)
	parser.add_argument('-c','--createnew', help = help_c, type = str, default = "no")
    	parser.add_argument('-n', '--newfile',  help = help_n, type = str, default = "Temp.csv")
	args = parser.parse_args()
	
	# File creation check
	if args.filename == None and args.createnew.lower() == "no":
		print "Enter a filename or create a new file! Exiting!"

	# Check for the existence of given input file.
	if(args.filename == None or os.path.isfile(args.filename) != True):
        	createnewfile(args.newfile, args.createnew)
    	else:        
		youtubeDownloader (args.filename)
	
