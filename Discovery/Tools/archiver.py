import os
import cv2
import sys
import time
import datetime
from camera import IPCamera
from camera import NonIPCamera
from camera import StreamFormat
import MySQLdb
import logging
import re

def get_camera(camera_id, connection):
    """ Get a camera from the database. """

    camera = None

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

    if not camera:
        return None

    return camera


def archive(args, connection):
    # Read the input arguments.
    try:
        camera_id = int(args[1])
        is_video = int(args[2])
        imgGetType = args[3] # Holds the type of image we are getting: ref/start/end 
    except:
        import archiver
        return

    file_name = None # Set file name to none to determine success
    camera = None

    # Get the camera information from the database.
    camera = get_camera(camera_id, connection)

    # Check if camera returned
    if camera == None:
        raise Exception('There is no camera with the given ID.')
        pass

    # If a video stream is requested, check the type of the camera.
    if is_video and not isinstance(camera, IPCamera):
        logging.info('This camera does not support video streaming.')
        exit()

    # Open the video stream.
    if is_video:
        camera.open_stream(StreamFormat.MJPEG)

    # Set the timestamp of the snapshot that will be downloaded.
    frame_timestamp = time.time()

    try:
        # Download the image.
        frame, _ = camera.get_frame()

        # Save the image.
        if imgGetType == 'ref':
            file_name = 'Pictures/ref_{}_{}.png'.format(camera_id,
                datetime.datetime.fromtimestamp(
                    frame_timestamp).strftime('%Y-%m-%d_%H-%M-%S-%f'))
        elif imgGetType == 'start':
            file_name = 'Pictures/start_{}.png'.format(camera_id)
        elif imgGetType == 'end':
            file_name = 'Pictures/end_{}.png'.format(camera_id)
        else:
            raise(Exception('imgGetType error'))

        cv2.imwrite(file_name, frame)
    except Exception, e:
        logging.info(e)
        pass

    # Close the video stream.
    if is_video:
        camera.close_stream()

    return file_name, frame_timestamp


if __name__ == '__main__':
    archive(sys.argv)