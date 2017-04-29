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
    import StreamDownloader
    import argparse
except:
    print("Import failed! Check Requiremnets")
    raise SystemExit

class ErrorinCSV(Exception):
   pass


def usearchiverdatabase(filename):
    try:
        import csv        
        import urllib2
        import archiver
    except:
        print("Import failed! Check Requiremnets")
        raise ErrorinCSV("Import failed! Check Requiremnets")
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
        raise ErrorinCSV("Invalid entries in csv. Most likely the wrong fields were filled! Please use readme for instructions to fill csv") 

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
            raise ErrorinCSV("Invalid entries in csv. Most likely the wrong fields were filled! Please use readme for instructions to fill csv")
            
def useStreamdownloader(filename):
    try:
        import csv        
        import StreamDownloader
        import urllib2       
    except:
        print("Import failed! Check Requiremnets")
        raise ErrorinCSV("Import failed! Check Requiremnets")
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
        raise ErrorinCSV("Invalid entries in csv. Most likely the wrong fields were filled! Please use readme for instructions to fill csv") 
    j = 0
    del cam_urls[0]
    del filenames[0]
    csv_handle.close()
    for i in cam_urls:
        try:
            download = StreamDownloader.StreamDownloader(i, filenames[j])
        except:
            print("Invalid entries, please check the csv file fields")
            raise ErrorinCSV("Invalid entries, please check the csv file fields")  
                
    j+=1
    download.saveStream(runtime)
    print "Video Saved"
    download.saveFrames(fps)


def usearchiverurl(filename):
    try:
        import csv
        import urllib2
        import archiver_url
    except:
        print("Import failed! Check Requiremnets")
        raise ErrorinCSV("Import failed! Check Requiremnets")
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
        raise ErrorinCSV("Invalid entries, please check the csv file fields")

def createnewfile(newfile,optioncreate):
    try:
        import csv        
    except:
        print("Import failed! Check Requiremnets")
        raise ErrorinCSV("Import failed! Check Requiremnets")
    try:
        if optioncreate == 'Yes':
            if(os.path.isfile(newfile)):
                print "File Exists! Exiting"      
                    
            else:
                # open a file
                csv_handle = open(newfile, 'wb')

                mywriter = csv.writer(csv_handle)
                mywriter.writerow(["Camera_ID","is_video","Duration(secs)","Interval","StoreCAM_ID","URL","O/P Filename","Runtime(secs)","FPS"])

                #close file
                csv_handle.close()
                print "File created with name",newfile
        else:
            print "File not found! Ending"
    except():
            print "Unable to create file"
            csv_handle.close()
            raise ErrorinCSV("Unable to create file")
           
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--filename',help="Name of CSV file containing camera info with .csv extension(should be in same directory as program)",type = str)
    parser.add_argument('-o','--option',help="Enter 1 to use wrapper_info file to grab camera images from URL, 2 to grab video data or 3 to search camera database to grab images",type = int)
    parser.add_argument('-u','--urloption',help="use wrapper_info file to grab camera images from URL",action='store_true')
    parser.add_argument('-v','--videooption',help="grab video data", action='store_true')
    parser.add_argument('-d','--database',help="search camera database to grab images",action='store_true')    
    parser.add_argument('-c','--createnew',help="Yes to create new file is file with filename does not exist",type = str,default = "No")
    parser.add_argument('-n','--newfile',help="takes a string to create new csv file(must have .csv extension)",type = str,default = "Temp.csv")
    args = parser.parse_args()
    if(os.path.isfile(args.filename) != True):
        createnewfile(args.newfile,args.createnew)
    else:
        print args.urloption
        if(args.urloption):
            usearchiverurl(args.filename)
        elif(args.videooption):
            useStreamdownloader(args.filename)
        elif(args.database):            
            usearchiverdatabase(args.filename)
        else:
            print "Wrong options specified"
    
            
