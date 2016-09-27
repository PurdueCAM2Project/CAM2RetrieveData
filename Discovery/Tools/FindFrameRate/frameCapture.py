import os
import cv2
import sys
import time
import datetime

from camera import Camera
import MySQLdb
import logging
import re
import getpass


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

def loadCameras(camera_ids, DB_PASSWORD):
    # Setup Database Connection:
    connection = None

    while connection == None:
        connection = getConnection(DB_PASSWORD)
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
            print Exception('There is no camera with the ID {}.'.format(camera_id.rstrip()))
            pass
        else:
            cameras.append(camera)

    connection.close()
    return(cameras)

