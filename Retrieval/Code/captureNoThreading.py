
# The program takes a file as input that contains sources to capture frames.
# Sources are media files such as .m3u8s.

import sys
import os
import argparse
import cv2
import time
import multiprocessing
from concurrent.futures import TimeoutError
from datetime import datetime
from pebble import ProcessPool
lock = multiprocessing.Lock()
# Path to save the frames
RESULTS_PATH = "/home/sara/CAM2RetrieveData/Retrieval/Code/results"

def parse_args(args):
    desc = 'Capture frames.'
    prog = 'captureNoThreading.py'
    parser = argparse.ArgumentParser(prog=prog, description=desc)
    parser.add_argument('-f','--filename',help="Name of file containing sources(file is mandatory and\
         should be in same directory as program)",type = str)
    parser.add_argument('-s', '--save', help='save image or not', type=int)
    parser.add_argument('-d', '--duration', help='Duration of time to capture frames from cameras', type=int)

    parser.add_argument('-i', '--interval', help='Interval between snapshots from each camera.', type=int)

    return parser.parse_args(args)

def checkCamera(source,duration,interval,save):
    #folderName = source.split("/")[4]
    folderName = source.split("/")[4] # 2for IP Cameras
    cam_directory = os.path.join(RESULTS_PATH, str(folderName))
    try:
        os.makedirs(cam_directory)
    except OSError as e:
        if e.errno != 17:
            raise
        pass
    try:
        c=1
        vc = cv2.VideoCapture(source)
        if not vc.isOpened():
            return

        start = time.time()
        while ((time.time() - start) < duration):
            capture_time = time.time()
            # Get the image
            rval, frame = vc.read()
            if save != 0:
            # Save the image.
                file_name = '{}/{}.jpg'.format(cam_directory,str(c))
                cv2.imwrite(file_name, frame)
            c = c + 1

            # Sleep until the interval between frames ends.
            time_to_sleep = interval - (time.time() - capture_time)
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)

        #print ("Frame rate per second: " + str(c-1))
        return (source,c-1)

    except Exception:
        return (source, c - 1)
    vc.release()


def main(args):
    # Stores FPS for each stream
    f = open("FPS.txt", "a")
    ns = parse_args(args[1:])
    duration = ns.duration
    interval = ns.interval
    save = ns.save

    if (duration is None):
        duration = 1
    if (interval is None):
        interval = 0
    if (save is None):
        save = 0
    input = ns.filename
    # read the list of addresses - urls
    fptr = open(input, 'r')

    for oneline in fptr:
        oneline = oneline.rstrip('\n')
        result = checkCamera(oneline,duration,interval,save)
        f.write(str(result)+"\n")

    f.close()
    fptr.close()


if __name__ == '__main__':
    startTime = datetime.now()
    main(sys.argv)
    endTime = datetime.now()
    print("Program took: ")
    print(endTime-startTime)
