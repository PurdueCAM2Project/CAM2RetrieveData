import getFramerate
import sys
import os
import re
def main(args):

    fInput = "nyctest.txt"
    duration = 60*60*10
    amountToProcess = 40
    camera_dump_threshold = 60*20  
    results_path = "result1"
    is_video = 0

    DB_PASSWORD = ''

    print("Pass: 1")

    try:
        cameras, activeCameras, startTimes, dumpedCams, end_compare_cameras, DB_PASSWORD = getFramerate.setup(fInput, duration, amountToProcess, camera_dump_threshold, results_path, is_video, DB_PASSWORD)
    except Exception, e:
        print("Error: {}".format(e))
        pass

    reviewOutput(cameras, activeCameras, startTimes, dumpedCams, end_compare_cameras, results_path)
    
    print("Pass: 2")
    results_path = "result2"
    try:
        cameras, activeCameras, startTimes, dumpedCams, end_compare_cameras, DB_PASSWORD = getFramerate.setup(fInput, duration, amountToProcess, camera_dump_threshold, results_path, is_video, DB_PASSWORD)
    except Exception, e:
        print("Error: {}".format(e))
        pass

    print("Pass: 3")
    results_path = "result3"
    try:
        cameras, activeCameras, startTimes, dumpedCams, end_compare_cameras, DB_PASSWORD = getFramerate.setup(fInput, duration, amountToProcess, camera_dump_threshold, results_path, is_video, DB_PASSWORD)
    except Exception, e:
        print("Error: {}".format(e))
        pass


if __name__ == '__main__':
    main(sys.argv)