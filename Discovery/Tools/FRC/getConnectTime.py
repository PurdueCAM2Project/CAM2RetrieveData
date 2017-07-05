# This program is similar to archiver
# Instead of downloading images from cameras in cam2 database
# it "pings" the cameras and returns the connection time for each camera.

import os
import cv2
import sys
import time
import datetime
import threading
import argparse
import csv
from camera import IPCamera
from camera import NonIPCamera
from camera import StreamFormat

lock = threading.Lock()
log = open('connectionErrors.csv', 'a')
log.write('ID' + ',' + 'HTTPResponse' + '\n')
f = open('connectionTime.csv', 'a')

def get_camera_db(camera_id):
    """ Get a camera from the database. """
    try:
        import MySQLdb
    except Exception as e:
        raise (e)

    # The server database credentials.
    DB_SERVER = 'localhost'
    DB_USER_NAME = 'cam2'
    DB_PASSWORD = ''
    DB_NAME = 'cam2'

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
                          camera_row[4], camera_row[2])  # 1 is ip and 3 is image path

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
    id : int
        The ID of the the camera.
    url : str
        The URL of the camera image stream.

    """
    def __init__(self, camera):
        threading.Thread.__init__(self)
        self.camera = camera
        self.id = camera.id

    def run(self):
        """Test connection to the camera."""
        #print("Starting to request camera with id: {}".format(self.id))
        try:
            start = time.clock()
            result = self.camera.connect()
	    
        except Exception as e:
            pass
        else:
            end = time.clock()
            lock.acquire()
	    log.write(", ".join(str(r) for r in result.values()))
	    log.write("\n")
            f.write(str(self.camera.id) + "," + str(end - start) + "\n")
            lock.release()

def parse_input(args):
    # List of camera objects to archive
    cams = []
    # Read the input arguments.
    parser = argparse.ArgumentParser(description="This program downloads image snapshots from 2 sources\
        (1) A given URL address (2) A camera ID in the MySQL database * MySQL database must be available on host computer.")
    parser.add_argument('-f', '--filename', help="Name of CSV file containing camera info with .csv extension(should\
         be in same directory as program)", type=str)
    parser.add_argument('-l', '--list', help="List of camera ID's to be archived separated by spaces. \
        * This requires a version of the MYSQL database on your local machine.", type=int, nargs='+')
    parser.add_argument('-d', '--duration', help="Duration of time to archive snapshots from the cameras. Required\
         for -l argument.", type=int)
    parser.add_argument('-i', '--interval', help="Interval between snapshots from each camera. Required\
         for -l argument.", type=int)
    args = parser.parse_args()

    if args.filename != None:
        if (os.path.isfile(args.filename) != True):
            print("Input File \"{}\" could not be found.".format(args.filename))
        else:
            f = open(args.filename)
            f_csv = csv.reader(f, delimiter=",")
            # Skip row labels
            f_csv.next()
            for line in f_csv:
                try:
                    camera_id = int(line[0])
                except:
                    raise (
                    Exception("Error: No camera_id exists in line {} of input file \"{}\"".format(line, args.filename)))

                cam = get_camera_db(camera_id)
                if cam != None:
                    cams.append(cam)


                        # Do file parsing Stuff
    if args.list != None:
        for ID in args.list:
            cam = get_camera_db(ID)
            if cam != None:
                cams.append(cam)
    else:
        parser.print_help()

    if len(cams) == 0:
        parser.print_help()

    return cams


def archiver(args):
    cams = parse_input(args)

    camera_handlers = []
    for camera in cams:
        # Create a new thread to handle the camera.
        camera_handler = CameraHandler(camera)
        # Run the thread.
        camera_handler.start()
        # Add the thread to the array of threads.
        camera_handlers.append(camera_handler)

    # Wait for all the threads to finish execution.
    for camera_handler in camera_handlers:
        camera_handler.join()

    log.close()
    f.close()


if __name__ == '__main__':
    archiver(sys.argv)
