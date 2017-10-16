import threading
import time
import cv2
import datetime
import os

class CameraHandler(threading.Thread):
    """
    The thread to download snapshots from a single camera.

    Parameters
    ----------
    camera : camera object
        The camera from which snapshots will be taken.

    Attributes
    ----------
    camera : camera object
        The camera from which snapshots will be taken.
    id : int
        The ID of the the camera.
    url : str
        The URL of the camera image stream.
    duration : int
        The duration of downloading the images in seconds.
    interval : int
        The interval between each two successive snapshots.

    """

    # The path of the results directory.

    def __init__(self, camera, result_path):
        threading.Thread.__init__(self)
        self.camera = camera
        self.id = camera.id
        self.duration = camera.duration
        self.interval = camera.interval
        self.result_path = result_path

    def run(self):
        """
        Download snapshots from the camera, and save locally.
        """
        # Create the camera results directory.
        print("Starting Download from camera with id: {}".format(self.id))
        # Set the starting timestamp, and process until the end of the duration.
        cam_directory = os.path.join(self.result_path, str(self.id))
        try:
            os.makedirs(cam_directory)
        except OSError as e:
            pass

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
                    cam_directory, self.id,
                    datetime.datetime.fromtimestamp(
                        frame_timestamp).strftime('%Y-%m-%d_%H-%M-%S-%f'))
                cv2.imwrite(file_name, frame)


            # Sleep until the interval between frames ends.
            time_to_sleep = self.interval - (time.time() - frame_timestamp)
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
