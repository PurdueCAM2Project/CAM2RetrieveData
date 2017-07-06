"""
--------------------------------------------------------------------------------
Descriptive Name     : Image Comparison
Author               : Kyle Martin
Contact Info         : marti716@purdue.edu
Date Written         : 07/06/2017
Description          : Compare images to determine how different they are.
Command to run script: python imgCmp.py <filename1> <filename2>
Usage                : Get the mean, median and standard deviation of the
                       pixel-wise percent difference between two images.
Input file format    : N/A
Output               : A print statement with mean, median and standard
                       deviation.
Notes                : OpenCV must be installed to use the code.
                       The file works in python2 and python3.
Other files required by : N/A
this script and where 
located
--------------------------------------------------------------------------------
"""

import sys
import cv2
import numpy as np
import copy

class Image:
    """An image object."""
    
    def __init__(self, filename, grayscale=False):
        """Initialize an image object from a filename."""
        self.img = cv2.imread(filename)
        self.height = self.img.shape[0]
        self.width = self.img.shape[1]
        self.gray = grayscale

def main(args):
    img1 = Image(args[0])
    img2 = Image(args[1])
    diff_list = compare(img1, img2)
    mean = sum(diff_list) / len(diff_list)
    median = getMedian(diff_list)
    std_dev = getStdDev(diff_list, mean=mean)
    print("Mean = {0:0.2f}\nMedian = {0:0.2f}\nStandard Deviation = {0:0.2f}"\
          .format(mean, median, std_dev))
    return

def compare(img1, img2):
    """Compare two images of the same size."""
    if (img1.height != img2.height or img1.width != img2.width):
        raise ValueError("img1 and img2 are not the same size.")
    if (img1.gray != img2.gray):
        raise ValueError("img1 and img2 must have the same grayscale value.")

    diff_list = []
    i = 0
    j = 0
    k = 0
    while i < img1.height:
        while j < img1.width:
            diff = 0
            if img1.gray:
                diff = float(img1.img[i][j] - img2.img[i][j]) * 100 / 255
            else:
                while k < 3:
                    diff += float(img1.img[i][j][k] - img2.img[i][j][k])\
                            * 100 / 255
                    k += 1
                diff /= 3
            diff_list.append(diff)
            j += 1
        i += 1

    return diff_list

def getMedian(vals):
    """Get the median value of a list."""
    vals2 = copy.copy(vals)
    vals2.sort()
    list_len = len(vals2)
    if (list_len % 2 == 1):
        return vals2[int(list_len / 2)]
    return (vals2[int((list_len - 1) / 2)] + vals2[int(list_len / 2)]) / 2

def getStdDev(vals, mean=None):
    """Get the standard deviation of a list."""
    if (mean is None):
        mean = sum(vals) / len(vals)
    std = 0
    for val in vals:
        std += (val - mean) ** 2
    std /= len(vals)
    return std ** 0.5

if __name__ == "__main__":
    main(sys.argv[1:])
