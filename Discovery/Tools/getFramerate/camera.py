'''
--------------------------------------------------------------------------------
Descriptive Name     : camera.py
Author               : Ryan Dailey                                   
Contact Info         : dailey1@purdue.edu
Date Written         : June 20 2016
Description          : This file contains the Camera class which is used by the frame rate assessment program. 
Command to run script: This script is only to be run within getFramerate.py
Usage                : This script is only for use by getFramerate.py
Input file format    : N/A
Output               : N/A
Note                 : 
Other files required : This file requires several other files they should all be located in the same directory:
'''
import os
import cv2
import sys
import time
import datetime
import MySQLdb
import filecmp
import getpass
import logging
import re

import error
import stream_parser
import getConnection


class Camera():

    def __init__(self, id, url):
        self.id = id
        self.url = url

        self.timeInitialized = time.time()  # Holds the time that the class was initialized
        self.refImage = None                # Holds the string name of the reference image
        self.startImage = None              # Holds the string name of the start image
        self.endImage = None                # Holds the string name of the end image
        self.startTime = 0                  # Holds the unix start time that the start image was captured
        self.endTime = 0                    # Holds the unix start time that the end image was captured
                                            # The frame rate is the difference between these two times. 

        self.parser = None                  # This is the image stream parser object it will always be for static images. 
        self.parser = stream_parser.ImageStreamParser(url)
    '''
    The get_ref_image function gets the reference image. The reference image is used to compare to the start image and see when
    a new image is posted to the server. The get_ref_image function is only called once per camera class instance. If the refImage
    is successfully obtained the program will begin to try and get a startImage. If the image cannot be obtained (either because
    of a connection issue or because the image is no longer available at that url) then this is recorded and the camera is dumped
    from the activeCameras list. 
    '''
    def get_ref_image(self, cameras, activeCameras, errorCameras):
        # Set the timestamp of the snapshot that will be downloaded.
        frame_timestamp = time.time()
        file_name = None # Set file name to none to determine success
        try:
            # Download the image.
            frame, _ = self.parser.get_frame()
            self.refImage = 'Pictures/ref_{}_{}.png'.format(self.id, datetime.datetime.fromtimestamp(frame_timestamp).strftime('%Y-%m-%d_%H-%M-%S-%f'))

            cv2.imwrite(self.refImage, frame)

        except error.UnreachableCameraError:
            logging.info('get_ref_image_ERROR: Image could not be retrieved for ID: {}'.format(self.id))
            # cameras, activeCameras, errorCameras = getNewCam(self.id, cameras, activeCameras, errorCameras)

        except Exception, e:
            logging.exception(e)

        return cameras, activeCameras, errorCameras
        '''
        The get_start_image function will get an image from the url and compare it to the referenceImage.
        If the image is successfully captured the string name of the image is stored in the startImage
        class variable. If the new image is the same as the refImage no other action is taken. If the
        new startImage is different then the image stored in the refImage variable then the startTime is
        stored and the program will no longer attempt to get a startImage for this camera. The startImage
        is used to compare to the endImage and the difference between the startTime and the endTime is the
        frame rate. 
        '''
    def get_start_image(self, cameras, activeCameras, errorCameras):
        if self.startTime == 0 and self.refImage != None:
            # Set the timestamp of the snapshot that will be downloaded.
            frame_timestamp = time.time()
            self.startImage = None # Set file name to none to determine success
            try:
                # Download the image.
                frame, _ = self.parser.get_frame()
                self.startImage = 'Pictures/start_{}.png'.format(self.id)
                cv2.imwrite(self.startImage, frame)

                if self.startImage == None or frame_timestamp == None:
                    raise(Exception("get_start_image_ERROR: Image could not be retrieved."))
                    # logging.debug(self.ID)

                if filecmp.cmp(self.refImage, self.startImage) == False:
                    self.startTime = frame_timestamp
                    # logging.debug("ID: {} started at: {}".format(self.ID, str(frame_timestamp)))

            except Exception("get_start_image_ERROR: Image could not be retrieved."), e:
                cameras, activeCameras, errorCameras = getNewCam(self.ID, cameras, activeCameras, errorCameras)
            except Exception, e:
                logging.exception(e)

        return cameras, activeCameras, errorCameras
        '''
        get_end_image only downloads an image if the start image has been captured. If the startImage exists
        it will attempt to download another image from the url provided in the class. Then, it will compare this
        new image to the startImage. If the images are the same then it will do nothing. If the images are different
        then that means that the image on the server has changed since the startImage was downloaded. If the image has 
        changed then the frame rate for this camera has been determined and the frame rate is recorded by taking the
        difference between the startTime and the endTime. The successfully assessed frame rate is written to the 
        SuccessfulOutput.txt file. Then the camera is removed from the active cameras list and replaced by another 
        camera so the frame rate can be determined.
        '''
    def get_end_image(self, cameras, activeCameras, errorCameras, fSuccess):
        if self.startTime != 0:
            # Set the timestamp of the snapshot that will be downloaded.
            frame_timestamp = time.time()
            self.endImage = None # Set file name to none to determine success
            try:
                # Download the image.
                frame, _ = self.parser.get_frame()
                self.endImage = 'Pictures/end_{}.png'.format(self.id)
                cv2.imwrite(self.endImage, frame)

                if self.endImage == None or frame_timestamp == None:
                    print(frame)
                    raise(Exception("EndERROR: Image could not be retrieved."))
                    
                if filecmp.cmp(self.startImage, self.endImage) == False:
                    self.endTime = frame_timestamp
                    framerate = round(self.endTime - self.startTime)
                    if framerate < 1:
                        framerate = 1
                    fSuccess.write("{}\t{}\n".format(self.id, framerate))
                    cameras, activeCameras, errorCameras = getNewCam(activeCameras.index(self), cameras, activeCameras, errorCameras)

            except Exception, e:
                logging.exception(e)
                raise(e)

        return cameras, activeCameras, errorCameras
        # raw_input("PICK ME")
        '''
        checkThreshold checks to see if the camera has been in the activeCameras list longer then the
        threshold time. If the camera has exceeded the maximum threshold time then the camera is dumped
        and written to the errorCameras file. A new camera is then added to the activeCameras list to 
        fill out the list if one is available.
        '''
    def checkThreshold(self, cameras, activeCameras, errorCameras, threshold, fFailure):
        try:
            if time.time() - self.timeInitialized > threshold:
                if self in activeCameras:
                    fFailure.write("{}\t{}\n".format(self.id, self.url))
                    camPos = activeCameras.index(self)
                    cameras, activeCameras, errorCameras = getNewCam(camPos, cameras, activeCameras, errorCameras)
                    
        except Exception as e:
            logging.exception(e)

        return cameras, activeCameras, errorCameras
    '''
    getNewCam is used to take cameras from the input file and swap them out with a new camera. 
    getNewCam will then check if the first image (reference image) can be downloaded.  
    '''
def getNewCam(camera_pos, cameras, activeCameras, errorCameras):
    amountToProcess = len(activeCameras)
    activeCameras.pop(camera_pos)
    while len(activeCameras) < amountToProcess and len(cameras) > 0:
        camera = cameras.pop(0)
        camera.get_ref_image(cameras, activeCameras, errorCameras)
        
        if camera.refImage != None:
            activeCameras.append(camera)
        else:
            errorCameras.append(camera)

    return cameras, activeCameras, errorCameras

    '''
    get_camera is used by the loadCameras function to get camera information from the database. 
    At the start of the getFramerate function, all of this information is accessed in the 
    database and recorded in the corresponding camera Class. 
    '''
def get_camera(camera_id, connection):
    """ Get a camera from the database. """

    camera = None

    cursor = connection.cursor()

    # Get the non-IP camera with the given ID.
    cursor.execute('select camera.id, non_ip_camera.snapshot_url '
                   'FROM camera, non_ip_camera '
                   'WHERE camera.id = non_ip_camera.camera_id '
                   'and camera.id = {};'.format(camera_id))
    camera_row = cursor.fetchone()

    # Create a NonIPCamera object.
    if camera_row:
        camera = Camera(camera_row[0], camera_row[1])

    cursor.close()

    if not camera:
        return None

    return camera

    '''
    loadCameras creates all the camera class objects at the beginning of the execution
    of the getFramerate program from the input file. 
    '''
def loadCameras(camera_ids, DB_PASSWORD):
    # Setup Database Connection:
    connection = None
    connection = getConnection.getConnection(DB_PASSWORD)

    logging.info("Database Successfully Opened")

    cameras = []
    for camera_id in camera_ids:
        camera = None
        # Get the camera information from the database.
        camera = get_camera(camera_id, connection)
        # Check if camera returned
        if camera == None:
            logging.error(Exception('There is no camera in the database with the ID {}.'.format(camera_id.rstrip())))
            
        else:
            cameras.append(camera)

    connection.close()
    return(cameras)