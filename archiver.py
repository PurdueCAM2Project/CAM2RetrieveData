"""This program archives images from a single camera.
To use this program:
python archiver.py <camera_id> <is_video> <duration> <interval>
where:
<camera_id> is the camera ID in the database.
<is_video> is 1 for a MJPEG stream, 0 for a JPEG stream.
<duration> is the archiving duration in seconds.
<interval> is the interval between two frames in seconds (or 0 for the maximum
frame rate possible).
"""

import os
import cv2
import sys
import time
import datetime
from camera import IPCamera
from camera import NonIPCamera
from camera import StreamFormat
import MySQLdb


# The path of the results directory.
RESULTS_PATH = 'results'

# The server database credentials.
DB_SERVER = 'localhost'
DB_USER_NAME = 'root'
DB_PASSWORD = '1234'
DB_NAME = 'cam2'


def get_camera(camera_id):
    """ Get a camera from the database. """

    camera = None

    # Connect to the database, and get the connection cursor
    connection = MySQLdb.connect(DB_SERVER, DB_USER_NAME, DB_PASSWORD, DB_NAME)
    cursor = connection.cursor()

    # Get the IP camera with the given ID.
    cursor.execute('SELECT camera.id, ip_camera.ip, ip_camera.port, '
                   'ip_camera_model.image_path, ip_camera_model.video_path '
                   'FROM camera, ip_camera, ip_camera_model '
                   'WHERE camera.id = ip_camera.camera_id '
                   'and ip_camera.ip_camera_model_id = ip_camera_model.id '
                   'and camera.id = {};'.format(camera_id))
    camera_row = cursor.fetchone()

    # Create an IPCamera object.
    if camera_row:
        camera = IPCamera(camera_row[0], camera_row[1], camera_row[3],
                          camera_row[4], camera_row[2])
    else:
        # Get the non-IP camera with the given ID.
        cursor.execute('select camera.id, non_ip_camera.snapshot_url '
                       'FROM camera, non_ip_camera '
                       'WHERE camera.id = non_ip_camera.camera_id '
                       'and camera.id = {};'.format(camera_id))
        camera_row = cursor.fetchone()

        # Create a NonIPCamera object.
        if camera_row:
            camera = NonIPCamera(camera_row[0], camera_row[1])

    cursor.close()
    connection.close()

    if not camera:
        print 'There is no camera with the ID {}.'.format(camera_id)
        return None

    return camera


def archiver(args):
    # Read the input arguments.
    try:
        assert len(args) == 4
        camera_id = int(args[0])
        is_video = int(args[1])
        duration = int(args[2])
        interval = float(args[3])
    except:
        import archiver
        print archiver.__doc__
        return

    # Get the camera information from the database.
    camera = get_camera(camera_id)

    if camera == None:
    	return

    # If a video stream is requested, check the type of the camera.
    if is_video and not isinstance(camera, IPCamera):
        print 'The camera with the ID {} does not support video streaming.'.format(camera_id)
        return

    # Open the video stream.
    if is_video:
        camera.open_stream(StreamFormat.MJPEG)

    # Create the results directory.
    try:
        os.makedirs(RESULTS_PATH)
    except OSError:
        pass

    # Set the starting timestamp, and process until the end of the duration.
    start_timestamp = time.time()
    while (time.time() - start_timestamp) < duration:

        # Set the timestamp of the snapshot that will be downloaded.
        frame_timestamp = time.time()

        try:
            # Download the image.
            frame, _ = camera.get_frame()

            # Save the image.
            file_name = '{}/{}_{}.png'.format(
                RESULTS_PATH, camera_id,
                datetime.datetime.fromtimestamp(
                    frame_timestamp).strftime('%Y-%m-%d_%H-%M-%S-%f'))
            cv2.imwrite(file_name, frame)
        except Exception, e:
            pass

        # Sleep until the interval between frames ends.
        time_to_sleep = interval - (time.time() - frame_timestamp)
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

    # Close the video stream.
    if is_video:
        camera.close_stream()


if __name__ == '__main__':
    archiver(sys.argv)
