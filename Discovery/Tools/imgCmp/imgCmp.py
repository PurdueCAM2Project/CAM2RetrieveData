"""
--------------------------------------------------------------------------------
Descriptive Name     : Image Comparison
Author               : Kyle Martin
Contact Info         : marti716@purdue.edu
Date Written         : 07/06/2017
Description          : Compare images to determine how different they are.
Command to run script: python imgCmp.py <filename1> <filename2>
Usage                : Get the mean, median and standard deviation of the
                       pixel-wise squared difference between two images.
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
import math


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
    #diff_list = cmpMSE(img1, img2)
    #mean = sum(diff_list) / len(diff_list)
    #median = getMedian(diff_list)
    #std_dev = getStdDev(diff_list, mean=mean)
    #print("Mean = {0:0.2f}\nMedian = {1:0.2f}\nStandard Deviation = "\
    #      "{2:0.2f}".format(mean, median, std_dev))
    arr1 = copy.copy(img1).flatten()
    arr2 = copy.copy(img2).flatten()
    best_fit = getBestFit(arr1, arr2)
    r_squared = getRSquared(arr1, arr2, best_fit)
    print("r squared = {0:0.2f}".format(r_squared))
    return

def getPMF(img):
    """Get the Probability Mass Function of an image."""
    img_flat = copy.copy(img).flatten()
    pmf = [0 for ind in range(256)]
    for pix in img_flat:
        try:
            pmf[int(pix)] += float(1) / len(img_flat)
        except Exception as e:
            print(int(pix))
            raise e
    return pmf

def getJointPMF(img1, img2):
    """Get the Joint Probability Mass Function of two images."""
    img1_flat = copy.copy(img1).flatten()
    img2_flat = copy.copy(img2).flatten()
    pmf = [[0 for col in range(256)] for row in range(256)]
    for pix1 in img1_flat:
        for pix2 in img2_flat:
            pmf[int(pix1)][int(pix2)] += float(1) \
                                         / (len(img1_flat) * len(img2_flat))
    return pmf

def getMutInf(pmf1, pmf2, j_pmf):
    """Get the Mutual Information of two random variables."""
    mi = 0
    for a in range(len(pmf1)):
        for b in range(len(pmf2)):
            mi += j_pmf(a, b) * math.log(j_pmf(a, b) / (pmf(a) * pmf(b)))
    return mi

def getRSquared(arr1, arr2, best_fit):
    """Find the correlation between two arrays."""
    m = best_fit[0]
    b = best_fit[1]
    arr2_bar = float(sum(arr2)) / len(arr2)
    ss_tot = sum([(arr2[i] - arr2_bar) ** 2 for i in range(len(arr2))])
    f = [arr1[i] * m + b for i in range(len(arr1))]
    ss_res = sum([(arr2[i] - f[i]) ** 2 for i in range(len(f))])
    return 1 - float(ss_res) / ss_tot

def getBestFit(arr1, arr2):
    """Get the line of best fit between arr2 (on y axis) vs arr1 (x axis)."""
    arr1_bar = float(sum(arr1)) / len(arr1)
    arr2_bar = float(sum(arr2)) / len(arr2)
    num = sum([(arr1[i] - arr1_bar) * (arr2[i] - arr2_bar)\
               for i in range(len(arr1))])
    den = sum([(arr1[i] - arr1_bar) ** 2 for i in range(len(arr1))])
    m = float(num) / den
    b = arr2_bar - m * arr1_bar
    return (m, b)

def cmpMSE(img1, img2):
    """Compare two images using the Means Squared Error method.
    
    arg: img1 - the first image to be compared
    arg: img2 - the second image to be compared
    
    returns: A list of all the squared differences, one for each pixel
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
