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


# The path of the results directory.
RESULTS_PATH = 'results'


def get_camera_db(camera_id, duration, interval):
    """ Get a camera from the database. """
    try:
        import MySQLdb
    except Exception as e:
        raise(e)

    # The server database credentials.
    DB_SERVER = 'localhost'
    DB_USER_NAME = 'root'
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
        camera = IPCamera(camera_row[0], duration, interval, camera_row[1], camera_row[3],
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
            camera = NonIPCamera(camera_row[0], duration, interval, camera_row[1])

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
    duration : int
        The duration of downloading the images in seconds.
    interval : int
        The interval between each two successive snapshots.

    """
    def __init__(self, camera):
        threading.Thread.__init__(self)
        self.camera = camera
        self.id = camera.id
        self.duration = camera.duration
        self.interval = camera.interval

    def run(self):
        """Download snapshots from the camera, and save locally."""
        # Create the camera results directory.
        print("Starting Download from camera with id: {}".format(self.id))
        cam_directory = os.path.join(RESULTS_PATH, str(self.id))
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
                    cam_directory, self.id,
                    datetime.datetime.fromtimestamp(
                        frame_timestamp).strftime('%Y-%m-%d_%H-%M-%S-%f'))
                cv2.imwrite(file_name, frame)

            # Sleep until the interval between frames ends.
            time_to_sleep = self.interval - (time.time() - frame_timestamp)
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)


def parse_input(args):
    # List of camera objects to archive
    cams = []
    # Read the input arguments.
    parser = argparse.ArgumentParser(description="This program downloads image snapshots from 2 sources\
        (1) A given URL address (2) A camera ID in the MySQL database * MySQL database must be available on host computer.")
    parser.add_argument('-f','--filename',help="Name of CSV file containing camera info with .csv extension(should\
         be in same directory as program)",type = str)
    parser.add_argument('-l','--list',help="List of camera ID's to be archived separated by spaces. \
        * This requires a version of the MYSQL database on your local machine.", type = int, nargs='+')
    parser.add_argument('-d','--duration',help="Duration of time to archive snapshots from the cameras. Required\
         for -l argument.",type = int)
    parser.add_argument('-i','--interval',help="Interval between snapshots from each camera. Required\
         for -l argument.",type = int)
    args = parser.parse_args()

    if args.filename != None:
        if(os.path.isfile(args.filename) != True):
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
                    raise(Exception("Error: No camera_id exists in line {} of input file \"{}\"".format(line, args.filename)))
                try:
                    duration = int(line[2])
                    interval = int(line[3])
                except:
                    raise(Exception("Error: No duration or interval exists in line {} of input file \"{}\"".format(line, args.filename)))
                if line[5] != '':
                    url = line[5]
                    cam = NonIPCamera(camera_id, duration, interval, url)
                    if cam != None:
                        cams.append(cam)
                else:
                    cam = get_camera_db(camera_id, duration, interval)
                    if cam != None:
                        cams.append(cam)


            # Do file parsing Stuff
    if args.list != None: 
        if args.duration != None and args.interval != None:
            for ID in args.list:
                cam = get_camera_db(ID, args.duration, args.interval)
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

        # Sleep to shift the starting time of all the threads.
        # time.sleep(interval / len(cams)) # Old
        time.sleep(0.5)

    # Wait for all the threads to finish execution.
    for camera_handler in camera_handlers:
        camera_handler.join()


if __name__ == '__main__':
    archiver(sys.argv)
