'''
--------------------------------------------------------------------------------
Descriptive Name     : getFramerate.py
Author               : Ryan Dailey                                   
Contact Info         : dailey1@purdue.edu
Date Written         : June 20 2016
Description          : Below in Program Overview
Command to run script: python getFramerate.py
Usage                : This program must have access to the cam2 database. To change username and password info for the database see archiver.py
Input file format    : List of camera ID's that you want to assess
Output               : 3 Files. A log file for debugging. A successful output file. A report of unsuccessfully assessed cameras
Note                 : 
Other files required : This file requires several other files they should all be located in the same directory:
                        1. archiver.py (A heavily modified version of the image archiver located in retrieval)
                        2. camera.py (archiver.py asset)
                        3. stream_parser.py (archiver.py asset)




Program Overview:

This program is used to collect data about camera frame rates. It is divided into 5 major stages.
    1. The first stage is the setup stage. In this stage the program opens the import file and loads all the camera ID's in that file into a list.
        Then depending on the user's input parameters, a list called activeCameras will be made. This list contains the current ID's of the cameras that are
        being assessed. The program will only assess the cameras in activeCameras at any time. 

        Camera ID's enter and leave the active camera list when either:
            a. The camera image data cannot be accessed.
            b. The camera has been in the queue for longer then the threshold time specified by the user.
            c. The camera has been successfully assessed and a frame rate has been determined.

        Once the maximum number of cameras have been loaded into the active cameras list and removed from the list given in the input file, the next stage begins.

    2. The next stage is to get the image refereed to as the reference image. This image is the first image the program gets. This image is used to determine when
        program should begin to time the frame rate of the camera. This is an important step because we are starting our assessment at an arbitrary time. We don't
        know if the current output image of the camera was posted 10min ago or 10sec ago. The function getRefImage is called to attempt to get this first image.
        If the image is successfully gotten then the image is stored in the Pictures folder. If the image is not successfully gotten then the getRefImage function
        will call the activateCamera camera function so that the current camera can be replaced. When the inaccessible image has been removed from the active cameras
        list then getRefImage is called again. Once all the cameras in the activeCameras list have an associated reference image downloaded the next step begins. 

    3. The program now uses the getStartImage function to continuously download new images form each of the cameras in the activeCameras list. The start image is the
        first different image that is downloaded after the reference image. Once the start image has been found, the program will save the time that the start image
        was downloaded in the startTimes directory. The startTimes directory keys are the string of the camera ID and the value is the float unix start time. The
        getStartImage function is the first function called continuously by the assessFramerate function. After the getStartImage function is called in the loop the
        next function to be called is the getEndImage function.

    4. The getEndImage function attempts to find the first image that is different from the start image for that camera. When the end image is found, the difference
        in unix time is taken between the start and end times. This time is the frame rate. When the frame rate has been determined, getEndImage calls the 
        activateCamera function so the camera can be replaced in the activeCameras list. A new reference image is gotten and the analysis process begins for the next
        camera in the input file. After getEndImage is called assessFramerate calls one last function dumpCameras.

    5. The last function in the assessFramerate loop is the dumpCameras function. This function keeps track of how long an image has been in the activeCameras cameras
        list. If a camera has been in the activeCameras list longer then the user specified threshold time then the camera is removed from activeCameras and replaced
        with the next camera form the input file. This insures that if a camera is no longer active then the activeCameras queue does not get filled with cameras that
        are never updated. 

The loop in assessFramerate stops when:
 1. The program has assessed all the cameras in the input file.
 2. The maximum assessment time has been reached.
 3. The user stops the assessment with ctrl + C.

When one of these conditions has been met the cleanUp function is called. This function assess how many of the cameras in the input file have been successfully assessed.
It keeps track of the cameras that exceeded the threshold and the cameras that were inaccessible.
'''

from __future__ import print_function
import os
import re
import filecmp
import sys
import archiver
import time
import logging
import datetime
import MySQLdb

# activateCamera is used to take cameras from the input file and swap them out with a new camera. 
# activateCamera will then check if the first image (reference image) can be downloaded.  
def activateCamera(camera, cameras, activeCameras, refFiles, connection):
    try:
        if len(cameras) > 0:
            newCam = cameras.pop(0).rstrip() # Get a new camera from the cameras list
            logging.debug("Replacing camera ID {} with camera ID {}".format(camera, newCam))
            activeCameras[activeCameras.index(str(camera))] = newCam
            camera = newCam
            camera, cameras, activeCameras, refFiles = getRefImage(camera, cameras, activeCameras, refFiles, connection)
        else:
            activeCameras.remove(str(camera))
            camera = None
            

        return camera, cameras, activeCameras, refFiles
        
    except Exception as e:
        logging.error(e)
        raise e

# getRefImage function attempts to download the reference image from website.
# if it can't get the reference image it replaces the camera with activateCamera.
def getRefImage(camera, cameras, activeCameras, refFiles, connection):
    file_name = None
    try:
        cameraInfo = [None, camera, 0, 'ref']
        file_name, frame_timestamp = archiver.archive(cameraInfo, connection)
        if file_name == None or frame_timestamp == None:
            raise(Exception('RefERROR: Image could not be retrieved for ID: {}'.format(camera)))

        refFiles[str(camera)] = file_name

    except Exception, e:
        logging.error(e)
        camera, cameras, activeCameras, refFiles = activateCamera(camera, cameras, activeCameras, refFiles, connection)
    
    return camera, cameras, activeCameras, refFiles

# getStartImage gets the starting image described in the overview.
def getStartImage(cameras, activeCameras, refFiles, startTimes, connection):
    logging.debug(activeCameras)
    for camera in activeCameras:
        logging.debug(camera)
        if startTimes.get(str(camera)) == 0:
            try:
                cameraInfo = [None, camera, 0, 'start']
                file_name, frame_timestamp = archiver.archive(cameraInfo, connection)
                if file_name == None or frame_timestamp == None:
                    raise(Exception("StartERROR: Image could not be retrieved."))
                    logging.error(camera)

                if filecmp.cmp(str(refFiles.get(str(camera))), file_name) == False:
                    startTimes[str(camera)] = frame_timestamp
                    logging.debug("ID: {} started at: {}".format(camera, str(frame_timestamp)))
                
            except Exception as e:
                if str(e) == str("StartERROR: Image could not be retrieved."):
                    logging.warning(e)
                    logging.warning("ID:{}".format(camera))
                    camera, cameras, activeCameras, refFiles = activateCamera(camera, cameras, activeCameras, refFiles, connection)

                else:
                    logging.error(e)
                    raise(e)

    return startTimes

# The getEndImage function gets the end image described in the overview. 
def getEndImage(camera, cameras, activeCameras, refFiles, startTimes, f, connection):
    for camera in activeCameras:
        if startTimes.get(str(camera)) != None and startTimes.get(str(camera)) != 0:
            try:
                cameraInfo = [None, camera, 0, 'end']
                file_name, frame_timestamp = archiver.archive(cameraInfo, connection)
                if file_name == None or frame_timestamp == None:
                    raise(Exception("EndERROR: Image could not be retrieved."))

                if filecmp.cmp(('Pictures/start_{}.png'.format(camera)), file_name) == False:
                    framerate = round(frame_timestamp - startTimes.get(str(camera)))
                    f.write(camera+"\t"+str(framerate)+"\n")
                    logging.debug("ID: {} ended: {}".format(camera, framerate))
                    startTimes.pop(str(camera))
                    camera, cameras, activeCameras, refFiles = activateCamera(camera, cameras, activeCameras, refFiles, connection)
                    logging.debug('Camera Replaced: {}'.format(camera))
                    if camera != None:
                        startTimes[str(camera)] = 0

            except Exception as e:
                if str(e) == str("EndERROR: Image could not be retrieved."):
                    logging.warning(e)
                    logging.warning("ID:{}".format(camera))
                else:
                    logging.error(e)
                    raise(e)

    return camera, activeCameras, refFiles, startTimes, cameras

# The dumpCameras function determines if the camera has been assessed longer then the threshold permits.
# If the camera exceeds the threshold time then it is replaced.
def dumpCameras(cameras, dumpedCams, activeCameras, camera_dump_threshold, timeInQueue, startTimes, refFiles, connection):
    for camera in activeCameras:
        if timeInQueue.get(str(camera)) != None and (time.time() - timeInQueue.get(str(camera))) > camera_dump_threshold:
            try:
                logging.debug("ID: {} exceeded camera threshold.                                                         ".format(camera))
                startTimes.pop(str(camera))
                timeInQueue.pop(str(camera))
                dumpedCams.append(camera)
                camera, cameras, activeCameras, refFiles = activateCamera(camera, cameras, activeCameras, refFiles, connection)
                if camera != None:
                    logging.debug('Camera Replaced: {}'.format(camera))
                    startTimes[str(camera)] = 0
                    timeInQueue[str(camera)] = time.time()
                
            except Exception, e:
                logging.error(e)
            
        # timeInQueue[str(camera)] = time.time() 
        return dumpedCams, timeInQueue, activeCameras, refFiles, startTimes, cameras

# This function is called after the execution of the while loop. It assesses how many of the cameras
# have been successfully assessed and outputs a report.
def cleanUp(cameras, activeCameras, startTimes, fLong, dumpedCams, end_compare_cameras):
    tmpList = []
    print("Cleaning Up.")
    if activeCameras != None:
        fLong.write("Cameras Loaded But Not Finished:\n")
        fLong.write("ID \t\t Time Assessed\n")
        for camera in activeCameras:
            if startTimes.get(str(camera)) != None and startTimes.get(str(camera)) != 0:
                logging.debug(startTimes.get(str(camera)))
                fLong.write("{}\t\t{}\n".format(camera,str(time.time()-float(startTimes.get(str(camera))))))
                if camera in end_compare_cameras:
                    end_compare_cameras.pop(end_compare_cameras.index(camera))
            else:
                tmpList.append(camera)

    if dumpCameras != None:
        fLong.write("Cameras that exceeded threshold:\n")
        for camera in dumpedCams:
            fLong.write(camera+"\n")
            if camera in end_compare_cameras:
                end_compare_cameras.pop(end_compare_cameras.index(camera))

    if tmpList != None:
        fLong.write("Cameras Not Loaded:\n")
        fLong.write("ID\n")
        for camera in tmpList:
            fLong.write("{}\n".format(camera))
            if camera in end_compare_cameras:
                end_compare_cameras.pop(end_compare_cameras.index(camera))

    if cameras != None:
        for camera in cameras:
            fLong.write("{}".format(camera))
            if camera in end_compare_cameras:
                end_compare_cameras.pop(end_compare_cameras.index(camera))

    if end_compare_cameras != None:
        fLong.write("Cameras that could not be accessed:\n")
        for camera in end_compare_cameras:
            fLong.write("{}\n".format(camera))

def getConnection():

    # Try to access database:
    connection = None
    try:
        databaseRead = open("databaseConfig.config", "r")
        databaseInfo = list(databaseRead)
        for info in databaseInfo:
            if info.find("DB_SERVER") != -1:
                DB_SERVER = re.search(r"DB_SERVER = (?P<SERVER>[\S]*)", databaseInfo[1]).group("SERVER")
            elif info.find("DB_USER_NAME") != -1:
                DB_USER_NAME = re.search(r"DB_USER_NAME = (?P<USER>[\S]*)", databaseInfo[2]).group("USER")
            elif info.find("DB_PASSWORD") != -1:  
                DB_PASSWORD = re.search(r"DB_PASSWORD = (?P<PSWD>[\S]*)", databaseInfo[3]).group("PSWD")
            elif info.find("DB_NAME") != -1:
                DB_NAME = re.search(r"DB_NAME = (?P<NAME>[\S]*)", databaseInfo[4]).group("NAME")

        # Connect to the database, and get the connection cursor
        connection = MySQLdb.connect(DB_SERVER, DB_USER_NAME, DB_PASSWORD, DB_NAME)

    except Exception as e:
        logging.debug(e)
        print("databaseConfig.config missing!!")
        print("Creating databaseConfig.config")
        databaseRead = open("databaseConfig.config", "w")
        databaseRead.write("# The server database credentials.")
        DB_SERVER = raw_input("DB_SERVER = ")
        DB_USER_NAME = raw_input("DB_USER_NAME = ")
        DB_PASSWORD = raw_input("DB_PASSWORD = ")
        DB_NAME = raw_input("DB_NAME = ")
        databaseRead.write("# The server database credentials.\nDB_SERVER = {}\nDB_USER_NAME = {}\nDB_PASSWORD = {}\nDB_NAME = {}".format(DB_SERVER, DB_USER_NAME, DB_PASSWORD, DB_NAME))


    databaseRead.close()
    return connection
        

def assessFramerate(camera_dump_threshold, camera, cameras, activeCameras, refFiles, f, duration, totalCams, fLong, connection):
    assessTime_start = time.time()
    print("\rAssessment Runtime: {}sec Max Runtime: {}sec. Processing {}of{}          ".format(round(time.time()-assessTime_start), duration, totalCams - len(cameras), totalCams), end = '\r')
    sys.stdout.flush()
    # Set the starting timestamps, and process until the end of the duration.
    start_timestamp = time.time()

    startTimes = {}
    timeInQueue = {} # Holds total time that cameras have been processed
    dumpedCams = [] # Holds cameras that exceed the the threshold 
    for camera in activeCameras:
        startTimes[str(camera)] = 0
        timeInQueue[str(camera)] = time.time()

    try:
        while (time.time() - start_timestamp) < duration and len(activeCameras) > 0 :
            try:
                startTimes = getStartImage(cameras, activeCameras, refFiles, startTimes, connection)
                print("\rAssessment Runtime: {}sec Max Runtime: {}sec. Processing {}of{}          ".format(round(time.time()-assessTime_start), duration, totalCams - len(cameras), totalCams), end = '\r')
                sys.stdout.flush()
            except Exception as e:
                print("\n\nError! getStartImage Failed")
                raise e
            try:
                camera, activeCameras, refFiles, startTimes, cameras = getEndImage(camera, cameras, activeCameras, refFiles, startTimes, f, connection)
                print("\rAssessment Runtime: {}sec Max Runtime: {}sec. Processing {}of{}          ".format(round(time.time()-assessTime_start), duration, totalCams - len(cameras), totalCams), end = '\r')
                sys.stdout.flush()
            except Exception as e:
                print("\n\nError! getEndImage Failed")
                raise e
            try:
                dumpedCams, timeInQueue, activeCameras, refFiles, startTimes, cameras = dumpCameras(cameras, dumpedCams, activeCameras, camera_dump_threshold, timeInQueue, startTimes, refFiles, connection)
                print("\rAssessment Runtime: {}sec Max Runtime: {}sec. Processing {}of{}          ".format(round(time.time()-assessTime_start), duration, totalCams - len(cameras), totalCams), end = '\r')
                sys.stdout.flush()
            except Exception as e:
                print("Error! dumpCameras Failed")
                raise e
    except:
        logging.info("Stopped, Cleaning Up...")
        pass

    if time.time() - start_timestamp > duration:
        logging.info("Assessment Limit Time Reached, Cleaning Up....")

    return cameras, activeCameras, startTimes, fLong, dumpedCams
    # cleanUp(cameras, activeCameras, startTimes, fLong, dumpedCams)
    # logging.info("Done. Exit...")
    # print("Done. Exit...")


def setup(fInput, duration, amountToProcess, camera_dump_threshold, results_path, is_video):
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S',
                    filename=results_path+'/assessFramerate.log',
                    filemode='w')

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    logging.debug("Input File: {}".format(fInput))
    logging.debug("Input Duration: {}".format(duration))
    logging.debug("Number of feeds processed at a time: {}".format(amountToProcess))
    logging.debug("Camera Dump Threshold: {}".format(camera_dump_threshold))
    logging.debug("Results Path: {}".format(results_path))
    logging.debug("Is Video: {}".format(is_video))

    # Create the results directory.
    try:
        os.makedirs(results_path)
    except OSError:
        pass
    try:
        os.makedirs('Pictures')
    except OSError:
        pass

    connection = None

    while connection == None:
        connection = getConnection()

    print("Database Successfully Opened")


    f = open(results_path+"/SuccessfulOutput.txt", "w") # Output file contains list of cameras with frame rates. Format ID frame_rate
    fLong = open(results_path+"/CameraErrorReport.txt", "w") # The program trys to determine frame rates less than 1 min if longer it writes them here


    logging.info("Loading cameras...")

    # program_start_time = datetime.datetime()
    # logging.info("Program Start Time: {}".format(program_start_time))

    cameras = list(fInput)
    end_compare_cameras = list(fInput)
    fInput.close()
    if cameras == None or len(cameras) == 0:
        logging.info("Problem loading cameras...")
        return
        pass
    logging.info("Cameras loaded successfully")
    logging.info("Setting up reference images...")

    totalCams = len(cameras)

    # List to store cameras actively being processed
    activeCameras = []
    # List to store names of reference files
    refFiles = {}

    if amountToProcess > len(cameras):
        amountToProcess = len(cameras)

    for camera in range(0, amountToProcess):
        activeCameras.append(cameras.pop(0).rstrip())

    refTime = time.time()
    for camera in activeCameras:
        camera, cameras, activeCameras, refFiles = getRefImage(camera, cameras, activeCameras, refFiles, connection)


    logging.info("Reference Files Downloaded: {}sec".format(time.time()-refTime))
    logging.info("Determining frame rates... This may take a while...")
    cameras, activeCameras, startTimes, fLong, dumpedCams = assessFramerate(camera_dump_threshold, camera, cameras, activeCameras, refFiles, f, duration, totalCams, fLong, connection)
    # logging.info("Total Runtime: {}".format(datetime.timedelta(program_start_time, datetime.datetime())))

    cleanUp(cameras, activeCameras, startTimes, fLong, dumpedCams, end_compare_cameras)
    logging.info("Done. Exit...")

    connection.close()
    fLong.close()
    f.close()


def main(args):
    relatedFiles = ["archiver.py", "Pictures", "archiver.pyc", "camera.pyc", "error.py", "stream_parser.pyc", "results", "getFramerate.py", "error.pyc", "camera.py", "stream_parser.py"]

    try:
        while 1:
            try:
                print("\nFiles in current directory:")
                files = os.listdir(os.curdir)
                diffFiles = []
                file_detected = False; 
                for onefile in files:
                    if onefile not in relatedFiles and onefile.find(".txt") != -1:
                        diffFiles.append(onefile)

                for onefile in range(0,(len(diffFiles))):
                    print("\t[{}] {}".format(onefile, diffFiles[onefile]))
                    file_detected = True;

                if file_detected == False:
                    print("\n\tNo input files detected!!\n\tMake sure that the desired input file is in the same directory and is a .txt file!\n")
                    return
                    
                print("\n")
                inputFile = str(raw_input('Enter input file or number: '))
                try:
                    inputFile = int(inputFile)
                    inputFile = diffFiles[inputFile]
                    print(inputFile)
                except:
                    pass
                fInput = open(inputFile, "r")

                break
            except Exception as e:
                print("Input file couldn't be opened... Try again.")
                pass
    except KeyboardInterrupt:
        print("\n")
        return

    try:
        duration = raw_input('Assessment Duration (seconds): ')
        if duration != '':
            duration = int(duration)
        else:
            print("No duration entered using default.")
            duration = 10*60

        amountToProcess = raw_input('Number of feeds to process at once: ')
        if amountToProcess != '':
            amountToProcess = int(amountToProcess)
        else:
            print("No number entered using default.")
            amountToProcess = 50

        camera_dump_threshold = raw_input('Longest possible time to assess camera before dumped (seconds): ')
        if camera_dump_threshold != '':
            camera_dump_threshold = int(camera_dump_threshold)
        else:
            print("No number entered using default.")
            camera_dump_threshold = 20*60

        results_path = raw_input('Path to save reports: ')
        if results_path != '':
            results_path = int(results_path)
        else:
            print("No path entered using default.")
            results_path = "results"

    except KeyboardInterrupt:
        print("\n")
        return


    is_video = 0

    setup(fInput, duration, amountToProcess, camera_dump_threshold, results_path, is_video)

if __name__ == '__main__':
    main(sys.argv)
