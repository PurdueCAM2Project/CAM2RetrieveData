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
import getpass


class Camera:
	def __init__(self, ID, activeCameras, connection):
		self.ID = ID
		self.timeInitialized = time.time()
		self.refImage = None
		self.startImage = None
		self.startTime = 0
		self.endImage = None
		self.endTime = 0
		try:
			cameraInfo = [None, ID, 0, 'ref']
			self.refImage, frame_timestamp = archiver.archive(cameraInfo, connection)
			if self.refImage == None or frame_timestamp == None:
				raise(Exception('ConstructERR: Image could not be retrieved for ID: {}'.format(ID)))

		except Exception, e:
			logging.debug(e)

	def getStartImage(self, cameras, activeCameras, errorCameras, connection):
		if self.startTime == 0:
			try:
				cameraInfo = [None, self.ID, 0, 'start']
				self.startImage, frame_timestamp = archiver.archive(cameraInfo, connection)
				if self.startTime == None or frame_timestamp == None:
					raise(Exception("StartERROR: Image could not be retrieved."))
					logging.debug(self.ID)

				if filecmp.cmp(self.refImage, self.startImage) == False:
					self.startTime = frame_timestamp
					logging.debug("ID: {} started at: {}".format(self.ID, str(frame_timestamp)))
				
			except Exception as e:
				if str(e) == str("StartERROR: Image could not be retrieved."):
					logging.warning(e)
					logging.warning("ID:{}".format(self.ID))
					cameras, activeCameras, errorCameras = getNewCam(self.ID, cameras, activeCameras, errorCameras, connection)
				else:
					logging.debug(e)
					raise(e)

		return cameras, activeCameras, errorCameras

	# The getEndImage function gets the end image described in the overview. 
	def getEndImage(self, cameras, activeCameras, errorCameras, fSuccess, connection):
		if self.startTime != 0:
			try:
				cameraInfo = [None, self.ID, 0, 'end']
				self.endImage, frame_timestamp = archiver.archive(cameraInfo, connection)
				if self.endImage == None or frame_timestamp == None:
					raise(Exception("EndERROR: Image could not be retrieved."))

				if filecmp.cmp(self.startImage, self.endImage) == False:
					self.endTime = frame_timestamp
					framerate = round(self.endTime - self.startTime)
					if framerate < 1:
						framerate = 1
					fSuccess.write(self.ID+"\t"+str(framerate)+"\n")
					logging.debug("ID: {} ended: {}".format(self.ID, framerate))
					cameras, activeCameras, errorCameras = getNewCam(activeCameras.index(self), cameras, activeCameras, errorCameras, connection)
					# logging.debug('Camera Replaced: {}'.format(self.ID))

			except Exception as e:
				if str(e) == str("EndERROR: Image could not be retrieved."):
					logging.warning(e)
					logging.warning("ID:{}".format(self.ID))
				else:
					logging.debug(e)
					raise(e)
		return cameras, activeCameras, errorCameras

	def checkThreshold(self, cameras, activeCameras, errorCameras, threshold, fFailure, connection):
		try:
			if time.time() - self.timeInitialized > threshold:
				logging.debug("ID: {} exceeded camera threshold.".format(self.ID))
				fFailure.write(self.ID+"\n")
				camera_pos = activeCameras.index(self)
				logging.debug(camera_pos)
				logging.debug(self.ID)
				cameras, activeCameras, errorCameras = getNewCam(camera_pos, cameras, activeCameras, errorCameras, connection)
		except Exception as e:
			print(e)
			logging.debug(e)
			logging.debug(self.ID)

		return cameras, activeCameras, errorCameras

			

# activateCamera is used to take cameras from the input file and swap them out with a new camera. 
# activateCamera will then check if the first image (reference image) can be downloaded.  
def getNewCam(camera_pos, cameras, activeCameras, errorCameras, connection):
	amountToProcess = len(activeCameras)
	activeCameras.pop(camera_pos)
	while len(activeCameras) < amountToProcess and len(cameras) > 0:
		currID = cameras.pop(0).rstrip()
		camera = Camera(currID, activeCameras, connection)
		if camera.refImage != None:
			activeCameras.append(camera)
		else:
			errorCameras.append(currID)

	return cameras, activeCameras, errorCameras

# Cameras that exceeded threshold (Handled by checkThreshold())
# Cameras that could not be loaded.
# Cameras that were not loaded beouse of time

def cleanUp(cameras, activeCameras, errorCameras, end_compare_cameras, fFailure):
	fFailure.write("\nCameras Loaded But Not Finished:\n")
	for camera in activeCameras:
		fFailure.write(camera.ID+"\n")
		if camera in end_compare_cameras:
			end_compare_cameras.pop(end_compare_cameras.index(camera.ID))

	fFailure.write("\nCameras with retrieval errors:\n")
	for camera in errorCameras:
		fFailure.write(camera+"\n")
		if camera in end_compare_cameras:
			end_compare_cameras.pop(end_compare_cameras.index(camera.ID))

	if cameras != None:
		fFailure.write("\nCameras Not Loaded:\n")
		for camera in cameras:
			fFailure.write(camera)
			if camera in end_compare_cameras:
				end_compare_cameras.pop(end_compare_cameras.index(camera))

	if end_compare_cameras != None:
		for camera in end_compare_cameras:
			fFailure.write(camera)

#     if end_compare_cameras != None:
#         fFailure.write("Cameras that could not be accessed:\n")
#         for camera in end_compare_cameras:
#             fFailure.write("{}\n".format(camera))


def getConnection(DB_PASSWORD):
	# Try to access database:
	connection = None
	try:
		databaseRead = open("database.config", "r")
		databaseInfo = list(databaseRead)
		for info in databaseInfo:
			if info.find("DB_SERVER") != -1:
				DB_SERVER = re.search(r"DB_SERVER = (?P<SERVER>[\S]*)", databaseInfo[1]).group("SERVER")
			elif info.find("DB_USER_NAME") != -1:
				DB_USER_NAME = re.search(r"DB_USER_NAME = (?P<USER>[\S]*)", databaseInfo[2]).group("USER")
			# elif info.find("DB_PASSWORD") != -1:  
			#     DB_PASSWORD = re.search(r"DB_PASSWORD = (?P<PSWD>[\S]*)", databaseInfo[3]).group("PSWD")
			elif info.find("DB_NAME") != -1:
				DB_NAME = re.search(r"DB_NAME = (?P<NAME>[\S]*)", databaseInfo[3]).group("NAME")
		print("database.config found.\nUsing:\n\tDB_SERVER = {}\n\tDB_USER_NAME = {}\n\tDB_NAME = {}".format(DB_SERVER, DB_USER_NAME, DB_NAME))

	except Exception as e:
		logging.debug(e)
		print("database.config missing!!")
		print("Creating database.config")
		databaseRead = open("database.config", "w")
		databaseRead.write("# The server database credentials.")
		DB_SERVER = raw_input("DB_SERVER = ")
		DB_USER_NAME = raw_input("DB_USER_NAME = ")
		DB_NAME = raw_input("DB_NAME = ")
		databaseRead.write("# The server database credentials.\nDB_SERVER = {}\nDB_USER_NAME = {}\nDB_NAME = {}".format(DB_SERVER, DB_USER_NAME, DB_NAME))

	try:
		if DB_PASSWORD == None:
			print("Input Database Password or /c to change info:")
			DB_PASSWORD = getpass.getpass("\nDB_PASSWORD = ")

		if DB_PASSWORD == "/c":
			databaseRead = open("database.config", "w")
			databaseRead.write("# The server database credentials.")
			DB_SERVER = raw_input("DB_SERVER = ")
			DB_USER_NAME = raw_input("DB_USER_NAME = ")
			DB_NAME = raw_input("DB_NAME = ")
			databaseRead.write("# The server database credentials.\nDB_SERVER = {}\nDB_USER_NAME = {}\nDB_NAME = {}".format(DB_SERVER, DB_USER_NAME, DB_NAME))
		else:
			# Connect to the database, and get the connection cursor
			connection = MySQLdb.connect(DB_SERVER, DB_USER_NAME, DB_PASSWORD, DB_NAME)
	except KeyboardInterrupt:
		connection = -1;
	except:
		connection = None

	databaseRead.close()
	return connection

def assessFramerate(cameras, activeCameras, errorCameras, threshold, duration, totalCams, fSuccess, fFailure, connection):
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
					cameras, activeCameras, errorCameras = camera.getStartImage(cameras, activeCameras, errorCameras, connection)
					print("\rAssessment Runtime: {}sec Max Runtime: {}sec. Processing {}of{}          ".format(round(time.time()-start_timestamp), duration, totalCams - len(cameras), totalCams), end = '\r')
					sys.stdout.flush()
				except Exception as e:
					print("\n\nError! getStartImage Failed")
					logging.error(e)
					raise e
				try:
					cameras, activeCameras, errorCameras = camera.getEndImage(cameras, activeCameras, errorCameras, fSuccess, connection)
					print("\rAssessment Runtime: {}sec Max Runtime: {}sec. Processing {}of{}          ".format(round(time.time()-start_timestamp), duration, totalCams - len(cameras), totalCams), end = '\r')
					sys.stdout.flush()
				except Exception as e:
					print("\n\nError! getEndImage Failed")
					raise e
				try:
					cameras, activeCameras, errorCameras = camera.checkThreshold(cameras, activeCameras, errorCameras, threshold, fFailure, connection)
					print("\rAssessment Runtime: {}sec Max Runtime: {}sec. Processing {}of{}          ".format(round(time.time()-start_timestamp), duration, totalCams - len(cameras), totalCams), end = '\r')
					sys.stdout.flush()
				except Exception as e:
					print("Error! checkThreshold Failed")
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

	# Setup Database Connection:
	connection = None

	while connection == None:
		connection = getConnection(DB_PASSWORD)
		if connection == None and connection != -1:
			print("Connection info not correct...\n\tTry again:")
		elif connection == -1:
			return

	logging.info("Database Successfully Opened")

	# Create Results Files:
	fSuccess = open(results_path+"/SuccessfulOutput.txt", "w") # Output file contains list of cameras with frame rates. Format ID frame_rate
	fFailure = open(results_path+"/CameraErrorReport.txt", "w") # The program trys to determine frame rates less than 1 min if longer it writes them here

	fFailure.write("Assment Info:\n**\nInput: {}\nMax Runtime: {}\nSize of Queue: {}\nThreshold: {}\n**\n".format(inputFile, duration, amountToProcess, threshold))

	if fSuccess == None or fFailure == None:
		return


	# Opening Input Files and Loading Cameras:
	logging.info("Loading cameras...")

	try:
		fInput = open(inputFile)
	except:
		logging.Error("File Not Loaded")
		return

	cameras = list(fInput)
	end_compare_cameras = list(fInput)
	fInput.close()

	if cameras == None or len(cameras) == 0:
		logging.info("Problem loading cameras...")
		return

	logging.info("Cameras loaded successfully")
	logging.info("Setting up reference images...")

	totalCams = len(cameras)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	fFailure.write("Cameras that exceeded threshold:\n")

	# List of camera objects
	activeCameras = []
	errorCameras = []

	refTime = time.time() # Keeps track of how long it takes to fetch refImages
	numAttempts = 0 # Keeps track of how many refrence gets were attempted
	numSuccess = 0 # Keeps track of the number of gets successful

	if amountToProcess > len(cameras):
		amountToProcess = len(cameras)

	while len(activeCameras) < amountToProcess and len(cameras) > 0:
		currID = cameras.pop(0).rstrip()
		camera = Camera(currID, activeCameras, connection)
		numAttempts += 1
		if camera.refImage != None:
			activeCameras.append(camera)
			numSuccess += 1
		else:
			errorCameras.append(currID)
		

	logging.info("Reference Files Downloaded: {}sec".format(time.time()-refTime))
	logging.info("# gets: {}Attempted. {}Successful. {}Unsuccessful".format(numAttempts, numSuccess, numAttempts - numSuccess))

# Anylize Framerate:
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	cameras, activeCameras, errorCameras = assessFramerate(cameras, activeCameras, errorCameras, threshold, duration, totalCams, fSuccess, fFailure, connection)

	logging.info("Determining frame rates... This may take a while...")
	

	cleanUp(cameras, activeCameras, errorCameras, end_compare_cameras, fFailure)
	logging.info("Done. Exit...")

	connection.close()
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
			duration = 7200
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
			results_path = int(results_path)
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