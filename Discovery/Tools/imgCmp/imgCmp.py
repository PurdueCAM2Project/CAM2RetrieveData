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


def main(args):
    """The main function for imgCmp.py

    The main implementation expects two command-line arguments, both filenames
    of images. The script then creates two Image objects, one for each
    filename, and compares them to get a list of squared differences. This list
    is then used to find the mean, median and standard deviation of the pixel-
    wise squared differences. These values are returned via a print statement.
    """
    img1 = cv2.imread(args[0])
    img2 = cv2.imread(args[1])
    diff_list = cmpMSE(img1, img2)
    mean = sum(diff_list) / len(diff_list)
    median = getMedian(diff_list)
    std_dev = getStdDev(diff_list, mean=mean)
    print("Mean = {0:0.2f}\nMedian = {1:0.2f}\nStandard Deviation = "\
          "{2:0.2f}".format(mean, median, std_dev))
    return

def cmpMSE(img1, img2):
    """Compare two images using the Means Squared Error method.
    
    arg: img1 - the first image to be compared
    arg: img2 - the second image to be compared
    
    return: A list of all the squared differences, one for each pixel
    """
    if (img1.shape[0] != img2.shape[0] or img1.shape[1] != img2.shape[1]):
        raise ValueError("img1 and img2 are not the same size.")
    if (img1.shape[2] != img2.shape[2]):
        raise ValueError("img1 and img2 must have the same grayscale value.")

    diff_list = []
    i = 0
    while i < img1.shape[0]:
        j = 0
        while j < img1.shape[1]:
            diff = 0
            k = 0
            while k < img1.shape[2]:
                diff += (int(img1[i][j][k]) - int(img2[i][j][k])) ** 2
                k += 1
            diff /= img1.shape[2]
            diff_list.append(diff)
            j += 1
        i += 1

    return diff_list

def getMedian(vals):
    """Get the median value of a list.
    
    arg: vals - a list of integer or float values

    returns: the median of vals
    """
    vals2 = copy.copy(vals)
    vals2.sort()
    list_len = len(vals2)
    if (list_len % 2 == 1):
        return vals2[int(list_len / 2)]
    return (vals2[int((list_len - 1) / 2)] + vals2[int(list_len / 2)]) / 2

def getStdDev(vals, mean=None):
    """Get the standard deviation of a list.

    arg: vals - a list of integer or float values
    arg: mean - optionally passed, the average of vals

    returns: the standard deviation of vals
    """
    if (mean is None):
        mean = sum(vals) / len(vals)
    std = 0
    for val in vals:
        std += (val - mean) ** 2
    std /= len(vals)
    return std ** 0.5

if __name__ == "__main__":
    main(sys.argv[1:])