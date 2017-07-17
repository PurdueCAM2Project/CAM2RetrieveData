
# The program takes a file that contains sources to capture frames.

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
    desc = 'Check sources for MJPEG Stream Parser.'
    prog = 'checkSource.py'
    parser = argparse.ArgumentParser(prog=prog, description=desc)
    parser.add_argument('-f','--filename',help="Name of file containing sources(file is mandatory and\
         should be in same directory as program)",type = str)
    parser.add_argument('-t', '--timeout', help='the maximum time to evaluate'\
                        ' a source.', type=int)
    parser.add_argument('-p', '--processes', help='the number of processes'\
                        ' that will run concurrently.', type=int)
    parser.add_argument('-d', '--duration', help='Duration of time to capture frames from cameras', type=int)

    parser.add_argument('-i', '--interval', help='Interval between snapshots from each camera.', type=int)

    return parser.parse_args(args)

def task_done(future):
    # Stores FPS for each stream
    f = open("FPS.txt", "a")
    try:
        result = future.result() # blocks until results are ready
    except TimeoutError as e:
        print("Function took longer than %d seconds" % e.args[1])
    except Exception as e:
        print("Function raised %s" % e)
        print(e.traceback) # traceback of the function
    else:
        lock.acquire()
        f.write(str(result)+"\n")
        lock.release()
    f.close()

def checkCamera(source,duration,interval):
    folderName = source.split("/")[4]
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
    ns = parse_args(args[1:])
    processes_num = ns.processes
    timeout = ns.timeout
    duration = ns.duration
    interval = ns.interval

    if (processes_num is None):
        #default number of processes correspond to 8 CPU cores
        processes_num = 8
    if (timeout is None):
        timeout = 30
    if (duration is None):
        duration = 1
    if (interval is None):
        interval = 1
    input = ns.filename
    # read the list of addresses - urls
    fptr = open(input, 'r')

    with ProcessPool(max_workers=processes_num) as pool:
        for oneline in fptr:
            oneline = oneline.rstrip('\n')
            future = pool.schedule(checkCamera, args=(oneline,duration,interval), timeout=timeout)
            future.add_done_callback(task_done)

    fptr.close()


if __name__ == '__main__':
    startTime = datetime.now()
    main(sys.argv)
    endTime = datetime.now()
    print("Program took: ")
    print(endTime-startTime)