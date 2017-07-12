
# The program takes one command-line argument as the name of the file

import sys
import argparse
import cv2
import readKnownCameras
import multiprocessing
from concurrent.futures import TimeoutError
from datetime import datetime
from pebble import ProcessPool

lock = multiprocessing.Lock()
f = open("sources.txt","a")

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
    return parser.parse_args(args)

def task_done(future):
    # Stores FPS for each camera
    f = open("sources.txt", "a")
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

def checkCamera(address, port, cameras):

    for path in sorted(cameras.keys()):

       try:
           source = "http://" + address + ":" + port + path
           vc = cv2.VideoCapture(source)

           if vc.isOpened():
               return source
           #else:
               #rval = False


       except Exception as e:
          return "Not Found"

    return "Not Found"

def checkCapture(src,cameraPaths):
    src = src.rstrip('\n')
    address, colon, port = src.partition(':')

    if(port == ""):
        port = "80"

    source = checkCamera(address,port,cameraPaths)

    if (source != "Not Found"):
            #print source
            return source
    else:
            #print source
            return (address + ":" + port)

def main(args):

    ns = parse_args(args[1:])
    processes_num = ns.processes
    timeout = ns.timeout
    if (processes_num is None):
        processes_num = 8
    if (timeout is None):
        timeout = 30

    input = ns.filename
    # read the paths of cameras
    # create a dictionary
    cameras = {}
    #knowncameras has a list of paths that are known for IP cameras
    readKnownCameras.readPaths("knownCameras", cameras)

    # read the list of IP addresses - IP file
    fptr = open(input, 'r')

    with ProcessPool(max_workers=processes_num) as pool:
        for oneline in fptr:
           future = pool.schedule(checkCapture, args=(oneline, cameras), timeout=timeout)
           future.add_done_callback(task_done)

    fptr.close()


if __name__ == '__main__':
    startTime = datetime.now()
    main(sys.argv)
    endTime = datetime.now()
    print("Program took: ")
    print(endTime-startTime)
