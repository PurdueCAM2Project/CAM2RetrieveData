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
                        1. getConnection.py (Contains the method to connnect to the MySQL database)
                        2. camera.py (Holds the camera class and camera helper functions)
                        3. stream_parser.py (Functions to help download camera images)
                        4. error.py (Contains error classes)

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
        know if the current output image of the camera was posted 10min ago or 10sec ago. The function get_ref_image is called to attempt to get this first image.
        If the image is successfully gotten then the image is stored in the Pictures folder. If the image is not successfully gotten then the getRefImage function
        will call the activateCamera camera function so that the current camera can be replaced. When the inaccessible image has been removed from the active cameras
        list then getRefImage is called again. Once all the cameras in the activeCameras list have an associated reference image downloaded the next step begins. 

    3. The program now uses the get_start_image function to continuously download new images form each of the cameras in the activeCameras list. The start image is the
        first different image that is downloaded after the reference image. Once the start image has been found, the program will save the time that the start image
        was downloaded in the startTimes directory. The startTimes directory keys are the string of the camera ID and the value is the float unix start time. The
        getStartImage function is the first function called continuously by the assessFramerate function. After the getStartImage function is called in the loop the
        next function to be called is the getEndImage function.

    4. The getEndImage function attempts to find the first image that is different from the start image for that camera. When the end image is found, the difference
        in unix time is taken between the start and end times. This time is the frame rate. When the frame rate has been determined, getEndImage calls the 
        activateCamera function so the camera can be replaced in the activeCameras list. A new reference image is gotten and the analysis process begins for the next
        camera in the input file. After get_end_image is called assessFramerate calls one last function dumpCameras.

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
import camera as importCameras
import time
import logging
import datetime
import MySQLdb
import getpass
import error
import argparse

# Cameras that exceeded threshold (Handled by checkThreshold())
# Cameras that could not be loaded.
# Cameras that were not loaded beouse of time
'''
	The cleanup function is called at the close of the assessFramerate function. It determines
	how many of the cameras have successfully been assessed and then writes the cameras with errors
	to the respective error output section. 
'''
def cleanUp(cameras, activeCameras, errorCameras, end_compare_cameras, fFailure):
	# These are cameras that were not loaded either because the program was exited
	# prematurely or because it exceeded the maximum assessment time.
	fFailure.write("\nCameras Loaded But Not Finished:\n")
	for camera in activeCameras:
		fFailure.write(str(camera.id)+"\n")
		if camera in end_compare_cameras:
			end_compare_cameras.pop(end_compare_cameras.index(camera.id))

	# This is a list of cameras that could not be reached on the url specified by the database.
	fFailure.write("\nCameras with retrieval errors:\n")
	for camera in errorCameras:
		fFailure.write("{}\t{}\n".format(camera.id, camera.url))
		if camera in end_compare_cameras:
			end_compare_cameras.pop(end_compare_cameras.index(camera.id))

	# This is a list of cameras that were not loaded either because the time limit was reached
	# or because the user exited the program prematurely. 
	if cameras != None:
		fFailure.write("\nCameras Not Loaded:\n")
		for camera in cameras:
			fFailure.write(str(camera.id)+"\n")
			if camera in end_compare_cameras:
				end_compare_cameras.pop(end_compare_cameras.index(camera))

	if end_compare_cameras != None:
		for camera in end_compare_cameras:
			fFailure.write(str(camera)+"\n")


'''
	The assessFramerate function contains the main loop of the frame rate assessment.
	It calls 3 functions in the camera class for each camera that is in the activeCameras
	list.  
'''
def assessFramerate(cameras, activeCameras, errorCameras, threshold, duration, totalCams, fSuccess, fFailure):
	start_timestamp = time.time()
        progress(start_timestamp, duration, totalCams-len(cameras), totalCams)
	try:
		while ((duration > 0 and (time.time() - start_timestamp) < duration) or duration <= 0) and len(activeCameras) > 0 :
			for camera in activeCameras:				
				cycle_start = time.time()
				num_passes = 0
				cycle_times = 0
				try:
					cameras, activeCameras, errorCameras = camera.get_start_image(cameras, activeCameras, errorCameras)
                                        progress(start_timestamp, duration,
                                                 totalCams-len(cameras),
                                                 totalCams)
				except Exception as e:
					logging.exception(e)
					print("\n\nError! get_start_image Failed")
				try:
					cameras, activeCameras, errorCameras = camera.get_end_image(cameras, activeCameras, errorCameras, fSuccess)
                                        progress(start_timestamp, duration,
                                                 totalCams-len(cameras),
                                                 totalCams)
				except Exception as e:
					logging.exception(e)
					print("\n\nError! get_end_image Failed")
				try:
					cameras, activeCameras, errorCameras = camera.checkThreshold(cameras, activeCameras, errorCameras, threshold, fFailure)
                                        progress(start_timestamp, duration,
                                                 totalCams-len(cameras),
                                                 totalCams)
				except Exception as e:
					logging.exception(e)
					print("Error! checkThreshold Failed")

				cycle_times += (time.time() - cycle_start)
				num_passes += 1
	except:
		logging.info("Stopped, Cleaning Up...")

	if time.time() - start_timestamp > duration:
		logging.info("Assessment Limit Time Reached, Cleaning Up....")
	
	# logging.debug("Average Cycle Time: {}".format(float(cycle_times/num_passes)))

	return cameras, activeCameras, errorCameras
	

def setup(inputFile, duration, amountToProcess, threshold, results_path, is_video, DB_PASSWORD):
	# Create the results directory.
	try:
		os.makedirs(results_path)
	except OSError:
		pass
	# Create the Pictures directory to store the pictures for comparison.
	try:
		os.makedirs('Pictures')
	except OSError:
		pass

	# Setup Logging Information: 
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

	# Record Input Parm:
	logging.debug("Input File: {}".format(inputFile))
	logging.debug("Input Duration: {}".format(duration))
	logging.debug("Number of feeds processed at a time: {}".format(amountToProcess))
	logging.debug("Camera Dump Threshold: {}".format(threshold))
	logging.debug("Results Path: {}".format(results_path))
	logging.debug("Is Video: {}".format(is_video))

	# Create Results Files:
	fSuccess = open("{}/{}_SuccessfulOutput.txt".format(results_path, results_path), "w") # Output file contains list of cameras with frame rates. Format ID frame_rate
	fFailure = open("{}/{}_CameraErrorReport.txt".format(results_path, results_path), "w") # The program trys to determine frame rates less than 1 min if longer it writes them here
	fFailure.write("Assment Info:\n**\nInput: {}\nMax Runtime: {}\nSize of Queue: {}\nThreshold: {}\n**\n".format(inputFile, duration, amountToProcess, threshold))
	fFailure.write("Cameras that exceeded threshold:\n")
	print(results_path)

	# Check that the files were opened correctly.
	if fSuccess == None or fFailure == None:
		return
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	# Opening Input Files and Loading Cameras:
	logging.info("Loading cameras...")

	try:
		fInput = open(inputFile)
	except:
		logging.error("File: \"{}\" Not Loaded".format(inputFile))
		return

	camera_ids = list(fInput)
	end_compare_cameras = list(fInput)
	cameras = importCameras.loadCameras(camera_ids, DB_PASSWORD)
	fInput.close()

	if cameras == None or len(cameras) == 0:
		logging.info("Problem loading cameras...")
		return

	logging.info("Cameras loaded successfully")
	logging.info("Setting up reference images...")

	totalCams = len(cameras)

	# List of camera objects
	activeCameras = []
	errorCameras = []

	refTime = time.time() # Keeps track of how long it takes to fetch refImages
	numAttempts = 0 # Keeps track of how many refrence gets were attempted
	numSuccess = 0 # Keeps track of the number of gets successful

	if amountToProcess > len(cameras):
		amountToProcess = len(cameras)

	while len(activeCameras) < amountToProcess and len(cameras) > 0:
		camera = cameras.pop(0)
		cameras, activeCameras, errorCameras = camera.get_ref_image(cameras, activeCameras, errorCameras)
		numAttempts += 1
		if camera.refImage != None:
			activeCameras.append(camera)
			numSuccess += 1
		else:
			errorCameras.append(camera)

	logging.info("Reference Files Downloaded: {}sec".format(time.time()-refTime))
	logging.info("# gets: {}Attempted. {}Successful. {}Unsuccessful".format(numAttempts, numSuccess, numAttempts - numSuccess))

# Anylize Framerate:
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	logging.info("Determining frame rates... This may take a while...")
	try:
			cameras, activeCameras, errorCameras = assessFramerate(cameras, activeCameras, errorCameras, threshold, duration, totalCams, fSuccess, fFailure)
	except KeyboardInterrupt:
		print("\n")
		cleanUp(cameras, activeCameras, errorCameras, end_compare_cameras, fFailure)
		logging.info("Done. Exit...")

		fFailure.close()
		fSuccess.close()
		raise(KeyboardInterrupt)
	

	cleanUp(cameras, activeCameras, errorCameras, end_compare_cameras, fFailure)
	logging.info("Done. Exit...")

	fFailure.close()
	fSuccess.close()
	# return cameras, activeCameras, errorCameras, startTimes, dumpedCams, end_compare_cameras, DB_PASSWORD


'''
progress() prints to stdout the progress of getFramerate.py
'''
def progress(start, dur, left, tot):
        sys.stdout.write("\rAssessment Runtime: {0:0.1f}sec Max Runtime: {1:d}"
                         "sec. Processing {2:d}of{3:d}"
                         .format(time.time() - start, dur, left, tot))
        sys.stdout.flush()
        return

'''
parse_cmd_args gets a list of the command line arguments and returns a
namespace with the necessary values for the script to run.
'''
def parse_cmd_args(args):
        desc = 'Get the framerate of cameras in the databse based on a '\
               '.txt file of camera IDs, one per line.'
        parser = argparse.ArgumentParser(prog='getFrameratey.py',
                                         description=desc)
        parser.add_argument('-t', '--threshold', help='the maximum threshold '
                            '(in seconds) to check a camera.')
        parser.add_argument('-r', '--runtime', help='the maximum runtime (in '
                            'seconds) for the program.')
        parser.add_argument('-d', '--directory', help='the name of the '
                            'directory in which the output files will be '
                            'saved.')
        parser.add_argument('-p', '--password', help='the password for mysql.')
        parser.add_argument('-f', '--filename', help='the .txt file from which '
                            'the ids will be taken.')
        parser.add_argument('-n', '--number', help='the number of cameras to '
                            'process at once.')
        return parser.parse_args(args)
'''
	main contains the functions to get the initial assessment parameters if getFramerate.py is run without the manageGetFramerate program.
	If manageGetFramerate.py is called this function is skipped.
'''
def main(args):
	relatedFiles = ["archiver.py", "Pictures", "archiver.pyc", "camera.pyc", "error.py", "stream_parser.pyc", "results", "getFramerate.py", "error.pyc", "camera.py", "stream_parser.py"]

        inputFile = None
        duration = None
        amountToProcess = None
        threshold = None
        results_path = None
        password = None
        if (len(args) > 1):
                ns = parse_cmd_args(args[1:])
                inputFile = ns.filename
                duration = ns.runtime
                amountToProcess = ns.number
                threshold = ns.threshold
                results_path = ns.directory
                password = ns.password
	try:
                if (inputFile is None):
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
				        fInput.close()

				        break
			        except Exception as e:
				        print("Input file couldn't be opened... Try again.")
				        pass
	except KeyboardInterrupt:
		print("\n")
		raise(KeyboardInterrupt)

	try:
                if (duration is None):
		        duration = raw_input('Assessment Duration (seconds): ')
		        if duration != '':
			        duration = int(duration)
		        else:
			        duration = -1
			        print("\tNo duration entered using default: {}sec".format(duration))
                if (amountToProcess is None):
		        amountToProcess = raw_input('Number of feeds to process at once: ')
		        if amountToProcess != '':
			        amountToProcess = int(amountToProcess)
		        else:
			        amountToProcess = 30
			        print("\tNo number entered using default: {}".format(amountToProcess))
                if (threshold is None):
		        threshold = raw_input('Longest possible time to assess camera before dumped (seconds): ')
		        if threshold != '':
			        threshold = int(threshold)
		        else:
			        threshold = 600
			        print("\tNo number entered using default: {}sec".format(threshold))
                if (results_path is None):
		        results_path = raw_input('Path to save reports: ')
		        if results_path != '':
			        results_path = results_path
		        else:
			        results_path = "results"
			        print("\tNo path entered using default: {}/".format(results_path))

	except KeyboardInterrupt:
		print("\n")
		return


	is_video = 0

	setup(inputFile, int(duration), int(amountToProcess), int(threshold), results_path, is_video, password)

if __name__ == '__main__':
	main(sys.argv)
