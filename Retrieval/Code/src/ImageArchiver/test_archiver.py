'''
Example usage of archiver class to retrieve one frame per second for 100 seconds from each camera specified in db_test.csv.
'''
import os

from ImageArchiver import ImageArchiver

archiver = ImageArchiver("localhost", "root", os.environ['DB_PASS'], "cam2")

#archiver.retrieve_csv("cameraSources/test_camera_url", 10, 1, "results/")
archiver.retrieve_db("cameraSources/db_test.csv", 10, 1, "results/")