from __future__ import print_function
import os
import re
import filecmp
import sys
import frameCapture
import time
import logging
import datetime
import MySQLdb
import getpass


# Cameras that exceeded threshold (Handled by checkThreshold())
# Cameras that could not be loaded.
# Cameras that were not loaded beouse of time

def cleanUp(cameras, activeCameras, errorCameras, end_compare_cameras, fFailure):
	fFailure.write("\nCameras Loaded But Not Finished:\n")
	for camera in activeCameras:
		fFailure.write(str(camera.id)+"\n")
		if camera in end_compare_cameras:
			end_compare_cameras.pop(end_compare_cameras.index(camera.id))

	fFailure.write("\nCameras with retrieval errors:\n")
	for camera in errorCameras:
		fFailure.write("{}\t{}\n".format(camera.id, camera.url))
		if camera in end_compare_cameras:
			end_compare_cameras.pop(end_compare_cameras.index(camera.id))

	if cameras != None:
		fFailure.write("\nCameras Not Loaded:\n")
		for camera in cameras:
			fFailure.write(str(camera.id))
			if camera in end_compare_cameras:
				end_compare_cameras.pop(end_compare_cameras.index(camera))

	if end_compare_cameras != None:
		for camera in end_compare_cameras:
			fFailure.write(camera)

#     if end_compare_cameras != None:
#         fFailure.write("Cameras that could not be accessed:\n")
#         for camera in end_compare_cameras:
#             fFailure.write("{}\n".format(camera))


def assessFramerate(cameras, activeCameras, errorCameras, threshold, duration, totalCams, fSuccess, fFailure):
	start_timestamp = time.time()
	print("\rAssessment Runtime: {}sec Max Runtime: {}sec. Processing {}of{}          ".format(round(time.time()-start_timestamp), duration, totalCams - len(cameras), totalCams), end = '\r')
	sys.stdout.flush()
	try:
		while ((duration > 0 and (time.time() - start_timestamp) < duration) or duration <= 0) and len(activeCameras) > 0 :
			for camera in activeCameras:				
				cycle_start = time.time()
				num_passes = 0
				cycle_times = 0
				try:
					cameras, activeCameras, errorCameras = camera.get_start_image(cameras, activeCameras, errorCameras)
					print("\rAssessment Runtime: {}sec Max Runtime: {}sec. Processing {}of{}          ".format(round(time.time()-start_timestamp), duration, totalCams - len(cameras), totalCams), end = '\r')
					sys.stdout.flush()
				except Exception as e:
					print("\n\nError! get_start_image Failed")
					logging.error(e)
					raise e
				try:
					cameras, activeCameras, errorCameras = camera.get_end_image(cameras, activeCameras, errorCameras, fSuccess)
					print("\rAssessment Runtime: {}sec Max Runtime: {}sec. Processing {}of{}          ".format(round(time.time()-start_timestamp), duration, totalCams - len(cameras), totalCams), end = '\r')
					sys.stdout.flush()
				except Exception as e:
					print("\n\nError! get_end_image Failed")
					logging.error(e)
					raise e
				try:
					cameras, activeCameras, errorCameras = camera.checkThreshold(cameras, activeCameras, errorCameras, threshold, fFailure)
					print("\rAssessment Runtime: {}sec Max Runtime: {}sec. Processing {}of{}          ".format(round(time.time()-start_timestamp), duration, totalCams - len(cameras), totalCams), end = '\r')
					sys.stdout.flush()
				except Exception as e:
					print("Error! checkThreshold Failed")
					logging.error(e)
					raise e
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
	fSuccess = open(results_path+"/SuccessfulOutput.txt", "w") # Output file contains list of cameras with frame rates. Format ID frame_rate
	fFailure = open(results_path+"/CameraErrorReport.txt", "w") # The program trys to determine frame rates less than 1 min if longer it writes them here
	fFailure.write("Assment Info:\n**\nInput: {}\nMax Runtime: {}\nSize of Queue: {}\nThreshold: {}\n**\n".format(inputFile, duration, amountToProcess, threshold))
	fFailure.write("Cameras that exceeded threshold:\n")


	if fSuccess == None or fFailure == None:
		return

	# Opening Input Files and Loading Cameras:
	logging.info("Loading cameras...")

	try:
		fInput = open(inputFile)
	except:
		logging.Error("File Not Loaded")
		return

	camera_ids = list(fInput)
	end_compare_cameras = list(fInput)
	cameras = frameCapture.loadCameras(camera_ids, None)
	fInput.close()

	if cameras == None or len(cameras) == 0:
		logging.info("Problem loading cameras...")
		return

	logging.info("Cameras loaded successfully")
	logging.info("Setting up reference images...")

	totalCams = len(cameras)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


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
	cameras, activeCameras, errorCameras = assessFramerate(cameras, activeCameras, errorCameras, threshold, duration, totalCams, fSuccess, fFailure)
	

	cleanUp(cameras, activeCameras, errorCameras, end_compare_cameras, fFailure)
	logging.info("Done. Exit...")

	fFailure.close()
	fSuccess.close()
	# return cameras, activeCameras, errorCameras, startTimes, dumpedCams, end_compare_cameras, DB_PASSWORD



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
				fInput.close()

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
			duration = -1
			print("\tNo duration entered using default: {}sec".format(duration))

		amountToProcess = raw_input('Number of feeds to process at once: ')
		if amountToProcess != '':
			amountToProcess = int(amountToProcess)
		else:
			amountToProcess = 30
			print("\tNo number entered using default: {}".format(amountToProcess))

		threshold = raw_input('Longest possible time to assess camera before dumped (seconds): ')
		if threshold != '':
			threshold = int(threshold)
		else:
			threshold = 600
			print("\tNo number entered using default: {}sec".format(threshold))

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

	setup(inputFile, duration, amountToProcess, threshold, results_path, is_video, None)

if __name__ == '__main__':
	main(sys.argv)