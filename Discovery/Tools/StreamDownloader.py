""" 
--------------------------------------------------------------------------------
Descriptive Name     : StreamDownloader.py
Author               : Thomas Norling								      
Contact Info         : thomas.l.norling@gmail.com
Date Written         : December 2, 2016
Description          : Takes 4 input arguments. A link to a camera stream, an 
                       output filename without extension, a desired runtime and 
                       the desired output frames per second.
                       The output filename specified with a .avi extension will be
                       created containing the downloaded video. Then individual frames
                       will be saved based on the number of frames per second specified
                       at runtime.
Command to run script: python StreamDownloader.py <url> <filename> <runtime (secs)> <fps>
Usage                : Can be imported into another script or run from the command line
Input file format    : N/A
Output               : AVI video, JPG images
Note                 : The disadvantage to this is that everytime you want updated
                       images/videos you will need to run this script.
Other files required by : ffmpeg.exe (https://ffmpeg.org/download.html)
this script and where 
located
--------------------------------------------------------------------------------
"""

import urllib2
import sys
import time
from subprocess import call

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

    def saveFrames(self, framesPerSec):
        #Function to save individual frames of the downloaded video
        #OpenCV and ffmpeg are capable of doing this
        #This function uses ffmpeg. In order for this to work, the filepath to ffmpeg.exe needs to be the first argument unless ffmpeg.exe is
        #located in the same directory as this script.
        #The -y option allows output file to be overwritten if it already exists. Remove this option if you would like to keep all outputs
        call(["ffmpeg", "-i", self.filename + ".avi", "-vf", "fps=" + framesPerSec, "-y", self.filename + "%d.jpg"])

if __name__ == '__main__':
    print "Saving Video"
    download = StreamDownloader(sys.argv[1], sys.argv[2], sys.argv[3])
    download.saveStream()
    print "Video Saved"
    download.saveFrames(sys.argv[4])