""" 
--------------------------------------------------------------------------------
Descriptive Name     : wrapper.py
Author               : Ajay Gopakumar and Vikrant Sateesh
Email Id             : agopakum@purdue.edu, vsatees@purdue.edu
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
try:
    import sys
    import os.path
    import csv
    import archiver_url
    import StreamDownloader
    import urllib2
    import archiver
    import argparse
except:
    print("Import failed! Check Requiremnets")
    raise SystemExit

class ErrorinCSV(Exception):
   pass

def wrapper(filename,option):
    filename = str(filename)
    
    if(os.path.isfile(filename)):
        
   
        if option == 1:

            csv_handle = open(filename, 'rb')
            myreader = csv.reader(csv_handle,delimiter=",")
            cam_ids =[]
            cam_urls =[]
            k = 0;
        
            try:
                for row in myreader:
                    k += 1
                    if(k==2):
                        duration = int(row[2])
                        interval = int(row[3])
                    cam_id = row[0]
                    cam_ids.append(cam_id)
                    cam_url = row[5]
                    cam_urls.append(cam_url)
            except:               
               raise ErrorinCSV("Invalid entries in csv. Most likely the wrong fields were filled! Please use readme for instructions to fill csv")
              
               
               
            print cam_ids,"  ",cam_urls
            csv_handle.close()
            j=1
            cams = {}
            for i in range(1,len(cam_ids)):
                cams[cam_ids[i]] = cam_urls[j]
                j += 1
                print
            print cams
            try:
                archiver_url.main([cams,duration,interval])
            except:
                print("Invalid entries, please check the csv file fields")
                raise SystemExit 
        
        elif option == 2:   
            print "Saving Video"
            csv_handle = open(filename, 'rb')
            myreader = csv.reader(csv_handle,delimiter=",")
            cam_urls = []
            filenames = []
            k = 0
            try:
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
            except:
               print("Invalid entries in csv. Most likely the wrong fields were filled! Please use readme for instructions to fill csv")
               raise SystemExit 
            j = 0
            del cam_urls[0]
            del filenames[0]
            csv_handle.close()
            for i in cam_urls:
                try:
                    download = StreamDownloader.StreamDownloader(i, filenames[j])
                except:
                    print("Invalid entries, please check the csv file fields")
                    raise SystemExit 
                
            j+=1
            download.saveStream(runtime)
            print "Video Saved"
            download.saveFrames(fps)
        elif option == 3:
            csv_handle = open(filename, 'rb')
            myreader = csv.reader(csv_handle,delimiter=",")
            cam_ids =[]
            cam_isvideolist =[]
            k = 0;
            try:
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
            except:
                print("Invalid entries in csv. Most likely the wrong fields were filled! Please use readme for instructions to fill csv")
                raise SystemExit 

            j = 0
            del cam_ids[0]
            del cam_isvideolist[0]
       
            csv_handle.close()
            j=1
            cams = {}
            for i in cam_ids:
                try:
                    archiver.main([i,cam_isvideolist[j],duration,interval])
                    j+=1
                except:
                    print("Invalid entries, please check the csv file fields")
                    raise SystemExit 
        
            print "DONE!" 
        else:
            print "Wrong option specified"
            
            
    else:
        try:
          option = raw_input("File does not exist. Would you like to create it?(Yes/No) ")
          if option == 'Yes':
      
                # open a file
                csv_handle = open(filename, 'wb')

                mywriter = csv.writer(csv_handle)
                mywriter.writerow(["Camera_ID","is_video","Duration(secs)","Interval","StoreCAM_ID","URL","O/P Filename","Runtime(secs)","FPS"])

                #close file
                csv_handle.close()
        except():
            print "Unable to create file"
            csv_handle.close()
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--filename',help="Name of CSV file containing camera info with .csv extension(should be in same directory as program)",type = str)
    parser.add_argument('-o','--option',help="Enter 1 to use wrapper_info file to grab camera images from URL, 2 to grab video data or 3 to search camera database to grab images",type = int)
    args = parser.parse_args()
    wrapper(args.filename,args.option)
