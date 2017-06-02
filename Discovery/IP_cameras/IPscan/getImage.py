import os
import cv2
import sys
import time
import datetime
import threading
import argparse
import csv
from camera import IPCamera
from camera import StreamFormat

# The path of the results directory.
RESULTS_PATH = 'results'

class CameraHandler(threading.Thread):
    """The thread to download snapshots from a single camera.

    Parameters
    ----------
    camera : camera object
        The camera from which snapshots will be taken.

    Attributes
    ----------
    camera : camera object
        The camera from which snapshots will be taken.
    ip : int
        The IP addr of the the camera.
    url : str
        The URL of the camera image stream.
    duration : int
        The duration of downloading the images in seconds.
        Currently, set to 1 in order to retrieve just 1 image.
    interval : int
        The interval between each two successive snapshots.
        Currently, set to 1 in order to retrieve just 1 image.

    """

    def __init__(self, camera):
        threading.Thread.__init__(self)
        self.camera = camera
        self.ip = camera.ip
        self.duration = camera.duration = 1
        self.interval = camera.interval = 1

    def run(self):
        """Download snapshots from the camera, and save locally."""
        # Create the camera results directory.
        print("Starting Download from camera with ip: {}".format(self.ip))
        cam_directory = os.path.join(RESULTS_PATH, str(self.ip))
        try:
            os.makedirs(cam_directory)
        except OSError:
            pass

        # Set the starting timestamp, and process until the end of the duration.
        start_timestamp = time.time()
        while (time.time() - start_timestamp) < self.duration:

            # Set the timestamp of the snapshot that will be downloaded.
            frame_timestamp = time.time()

            try:
                # Download the image.
                frame, _ = self.camera.get_frame()
            except Exception as e:
                pass
            else:
                # Save the image.
                file_name = '{}/{}_{}.png'.format(
                    cam_directory, self.ip,
                    datetime.datetime.fromtimestamp(
                        frame_timestamp).strftime('%Y-%m-%d_%H-%M-%S-%f'))
                cv2.imwrite(file_name, frame)

            # Sleep until the interval between frames ends.
            time_to_sleep = self.interval - (time.time() - frame_timestamp)
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)

def archiver(camera): #pass IP camera
    # Create a new thread to handle the camera.
    camera_handler = CameraHandler(camera)
    # Run the thread.
    camera_handler.start()
    time.sleep(0.5)


