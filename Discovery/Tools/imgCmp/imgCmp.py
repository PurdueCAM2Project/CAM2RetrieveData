"""
--------------------------------------------------------------------------------
Descriptive Name     : Image Comparison
Author               : Kyle Martin
Contact Info         : marti716@purdue.edu
Date Written         : 07/06/2017
Description          : Compare images to determine how different they are.
Command to run script: python imgCmp.py
Usage                :
Input file format    : N/A
Output               : 
Note                 : 
Other files required by : N/A
this script and where 
located
--------------------------------------------------------------------------------
"""

import sys
import cv2
import numpy as np

class Image:
    """An image object."""
    
    def __init__(self, filename, grayscale=False):
        """Initialize an image object from a filename."""
        self.arr = cv2.imread(filename)
        self.height = self.arr.shape[0]
        self.width = self.arr.shape[1]
        self.gray = grayscale


def compare(img1, img2):
    pass

def main(args):
    pass

if __name__ == "__main__":
    main(sys.argv[1:])
