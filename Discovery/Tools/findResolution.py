""" ****add / remove fields where appropriate, delete this line when done****
--------------------------------------------------------------------------------
Descriptive Name     : findResolution.py
Author               : Ryan Dailey                                    
Contact Info         : dailey1@purdue.edu
Date Written         : 6/13/16
Description          : Given a folder of snapshots this will find and output the resolutions
Command to run script: python findResolution.py
Usage                : It must be in the directory above a folder called "snapshots" that contains the snapshot images
Input file format    : N/A
Output               : ID \t resolution_width \t resolution_height \n
Note                 : 
Other files required by : snapshot files located in snapshots/<camera id>.jpeg
this script and where 
located
"""


import sys

from PIL import Image


def findResolution(args):
    f = open("resolutions.txt", "w")
    for cam_id in xrange(1,145655):
        try:
            image_filename = "snapshots/"+str(cam_id)+".jpg"
            im = Image.open(image_filename)
            width, height = im.size
            f.write(str(cam_id)+"\t"+str(width)+"\t"+str(height)+"\n")
            pass
        except:
            pass
        pass

    f.close()

if __name__ == '__main__':
    findResolution(sys.argv)
