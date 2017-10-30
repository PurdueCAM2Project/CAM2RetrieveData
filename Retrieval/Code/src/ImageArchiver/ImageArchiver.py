"""
This program retrieves images from cameras through the URLs or the ID numbers of 
each camera in the database and archives the images at the requested directory. 
It then places a directory of all results at a given path. This function also 
queries database for the cameras IDs specified in the csv files. 
"""

import time
import csv
import MySQLdb
from utils import check_file_exists
from camera import NonIPCamera, IPCamera, StreamCamera
from CameraHandler import CameraHandler

"""
Created on 5 September 2017
@author: Sam Yellin
"""

class ImageArchiver:
    
    """
    Retrieves images from cameras specified through a csv file.  The csv file either contains the urls of the cameras, or the ID numbers of each camera in the database.

	**Parameters** 
	
	db_server : str 
		The server the database is running on. 
		
	db_username : str
		The username for the database.
		
	db_password : str 
		Password to access the database, if in existence. 
		
	db_name : str 
		The name of the database.  

	**Attributes**
    
	db_server : str 
		The server the database is running on. 
		
	db_username : str
		The username for the database.
		
	db_password : str 
		Password to access the database, if in existence. 
		
	db_name : str 
		The name of the database.  

    """
    def __init__(self, db_server="localhost", db_username="root", db_password=None, db_name="cam2"):
        self.db_server=db_server
        self.db_username=db_username
        self.db_password=db_password
        self.db_name=db_name


    def retrieve_csv(self, camera_url_file, duration, interval, result_path):
        """
        Reads camera urls from csv file and archives the images at the requested directory.
        """

        #verify file exists and can be read
        if not check_file_exists(camera_url_file):
            return -1

        with open(camera_url_file, 'r') as camera_file:
            camera_reader=csv.reader(camera_file)
            id=1
            cams=[]
            for camera_url in camera_reader:
                #These cameras do not come from the database and so have no ID.  Assign one to them so they can be placed in a result folder.
                camera_type = camera_url[0].split(".")[-1]
                if (camera_type == "m3u8"):
                    camera = StreamCamera(id, duration, interval, camera_url[0])
                else:
                    camera = NonIPCamera(id, duration, interval,camera_url[0])
                id+=1
                cams.append(camera)
        if len(cams):
            self.__archive_cameras(cams, result_path)

    def retrieve_db(self, camera_id_file, duration, interval, result_path):
        """
        Reads camera IDs from csv file, retrieves the associated camera objects from the database, and archives the images at the requested directory.
        """
        if not check_file_exists(camera_id_file):
            return -1

        with open(camera_id_file, 'r') as id_file:
            id_reader = csv.reader(id_file)
            cams=[]
            for line in id_reader:
                try:
                    id = int(line[0])
                except:
                    raise(Exception("Error: No camera_id exists in line {} of input file \"{}\"".format(line, id_file)))

                camera = self.__get_camera_from_db(id, duration, interval)
                if camera is not None:
                    cams.append(camera)

        if len(cams):
            self.__archive_cameras(cams, result_path)
        return 0

    def __archive_cameras(self, cams, result_path):
        """
        Archives images from array of cameras.  Places directory of all results at the given path.
        """
        camera_handlers = []
        for camera in cams:
            # Create a new thread to handle the camera.
            camera_handler = CameraHandler(camera, result_path)
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

    def __get_camera_from_db(self, camera_id, duration, interval):
        """
        Reads camera IDs from file, and queries database for those cameras.  Archives the images from those cameras in the indicated result path.
        """
        connection = MySQLdb.connect(self.db_server, self.db_username, self.db_password, self.db_name)
        cursor = connection.cursor()

        camera=None
        #
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
                camera = NonIPCamera(camera_row[0], duration, interval, camera_row[1])
            else:
                # Get the stream camera with the given ID.
                cursor.execute('select camera.id, camera.m3u8_key '
                               'FROM camera, stream_camera '
                               'WHERE camera.id = stream_camera.camera_id '
                               'and camera.id = {};'.format(camera_id))
                camera_row = cursor.fetchone()
                # Create a stream camera object.
                if camera_row:
                    camera = StreamCamera(camera_row[0], duration, interval, camera_row[1])

        cursor.close()
        connection.close()

        if not camera:
            print 'There is no camera with the ID {}.'.format(camera_id)
            return None

        return camera