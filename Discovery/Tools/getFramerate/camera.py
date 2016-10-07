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
        # super(NonIPCamera, self).__init__(id)
        self.id = id
        self.url = url

        self.timeInitialized = time.time()
        self.refImage = None
        self.startImage = None
        self.startTime = 0
        self.endImage = None
        self.endTime = 0

        self.parser = None
        self.parser = stream_parser.ImageStreamParser(url)

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

# activateCamera is used to take cameras from the input file and swap them out with a new camera. 
# activateCamera will then check if the first image (reference image) can be downloaded.  
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


def loadCameras(camera_ids, DB_PASSWORD):
    # Setup Database Connection:
    connection = None

    while connection == None:
        connection = getConnection.getConnection(DB_PASSWORD)
        if connection == None and connection != -1:
            print("Connection info not correct...\n\tTry again:")
        elif connection == -1:
            return

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