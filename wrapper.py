""" 
--------------------------------------------------------------------------------
Descriptive Name     : wrapper.py
Author               : Ajay Gopakumar and Vikrant Sateesh								      
Date Written         : March 12, 2016
Description          : Uses a csv input file to call required function according to user
                       demands. Handles grabbing images from url, camera id and video stream.
Command to run script: python wrapper.py
Input file format    : .csv
Output               : JPG images, AVI video (if video stream)
Note                 : under development
Other files required by : ffmpeg.exe (https://ffmpeg.org/download.html)

--------------------------------------------------------------------------------
"""

import os.path
import csv
import archiver_url
import StreamDownloader
import urllib2
if(os.path.isfile("wrapper_info.csv")):
    option = input("Enter 1 to use wrapper_info file to grab camera images from URL, 2 to grab video data and 3 to search camera database to grab images ")
   
    if option == 1: #cameral images from url specified

        csv_handle = open('wrapper_info.csv', 'rb')
        myreader = csv.reader(csv_handle,delimiter=",")
        cam_ids =[]
        cam_urls =[]
	k = 0;
        
        for row in myreader:
	    k += 1
	    if(k==2):
	        duration = int(row[2])
	        interval = int(row[3])
            cam_id = row[0]
            cam_ids.append(cam_id)
            cam_url = row[5]
            cam_urls.append(cam_url)

        #print cam_ids,"  ",cam_urls
        csv_handle.close()
        j=1
        cams = {}
        for i in range(1,len(cam_ids)):
            cams[cam_ids[i]] = cam_urls[j]
            j += 1
            print
        print cams
        archiver_url.main([cams,duration,interval])
        print "DONE!" 
        
    elif option == 2:	#camera images from video
	print "Saving Video"
	csv_handle = open('wrapper_info.csv', 'rb')
        myreader = csv.reader(csv_handle,delimiter=",")
	cam_urls = []
	filenames = []
	k = 0 	
	for row in myreader:
	    k += 1
	    if(k==2):
	        runtime = int(row[7])
	        fps = row[8]
		print fps
            cam_url = row[5]
            cam_urls.append(cam_url)
	    filename1 = row[6]
	    filenames.append(filename1)

        j = 0
        del cam_urls[0]
	del filenames[0]
	csv_handle.close()
	for i in cam_urls:
	    download = StreamDownloader.StreamDownloader(i, filenames[j])
	    j+=1
        download.saveStream(runtime)
        print
        print "Video Saved"
        download.saveFrames(fps)
        print
        print "Images Saved"
        print "DONE!"
        
    elif option == 3:
        csv_handle = open('wrapper_info.csv', 'rb')
        myreader = csv.reader(csv_handle,delimiter=",")
        cam_ids =[]
        cam_isvideolist =[]
	k = 0;
        
        for row in myreader:
	    k += 1
	    if(k==2):
	        duration = int(row[2])
	        Interval = row[3]
		print Interval
            cam_id = row[0]
            cam_ids.append(cam_id)
	    cam_isvideo = row[1]
	    cam_isvideolist.append(cam_isvideo)

	j = 0
        del cam_ids[0]
	del cam_isvideolist[0]
       
        csv_handle.close()
        j=1
        cams = {}
        for i in cam_ids:
	    archiver.main([i,cam_isvideolist[j],duration,interval])
	    j+=1
	    
        print "DONE!" 
        
    else:
	print "Wrong option specified! Run program again and check csv file."
            
            
else:
    try:
       option = raw_input("File wrapper_info.csv does not exist. Would you like to create it?(Yes/No) ")
       if option == 'Yes' or option =="yes":
      
            # open a file
            csv_handle = open('wrapper_info.csv', 'wb')

            mywriter = csv.writer(csv_handle)
            mywriter.writerow(["Camera_ID","is_video","Duration(secs)","Interval","StoreCAM_ID","URL","O/P Filename","Runtime(secs)","FPS"])

            #close file
            csv_handle.close()
        else:
            print "Closing program"
    except():
        print "Unable to create file"
        csv_handle.close()

