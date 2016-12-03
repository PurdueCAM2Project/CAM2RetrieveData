""" 
--------------------------------------------------------------------------------
Descriptive Name     : StreamDownloader.py
Author               : Thomas Norling								      
Contact Info         : thomas.l.norling@gmail.com
Date Written         : December 2, 2016
Description          : Takes 3 input arguments. A link to a camera stream, an 
                       output filename without extension, and a desired runtime.
                       The output filename specified with a .avi extension will be
                       created containing the downloaded video. A function can be
                       written to save individual frames of the saved video.
Command to run script: python StreamDownloader.py <url> <filename> <runtime (secs)>
Usage                : Can be imported into another script or run from the command line
Input file format    : N/A
Output               : AVI video
Note                 : The disadvantage to this is that everytime you want updated
                       images/videos you will need to run this script.
Other files required by : N/A
this script and where 
located
--------------------------------------------------------------------------------
"""

import urllib2
import sys
import time

class StreamDownloader:
    def __init__(self, link, filename, runtime):
        self.url = urllib2.urlopen(link)
        self.filename = filename
        self.f = open(filename +".avi", 'wb')
        self.runtime = int(runtime) #In seconds
    
    def saveStream(self):
        buffer = 4 * 1024 #Can use 8 or 16 instead of 4 to make video run smoother
        start = time.time()
        end = time.time()
        while (end - start) < self.runtime:
            self.f.write(self.url.read(buffer))
            end = time.time()
        self.f.close()

    def saveFrames(self):
        #Write function to save individual frames of the downloaded video
        #Sounds like OpenCV and ffmpeg are capable of doing this
        pass

if __name__ == '__main__':
    print "Saving Video"
    download = StreamDownloader(sys.argv[1], sys.argv[2], sys.argv[3])
    download.saveStream()
    print "Video Saved"