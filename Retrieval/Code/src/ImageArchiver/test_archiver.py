'''
Example usage of archiver class to retrieve one frame per second for 100 seconds from each camera specified in db_test.csv.
'''

from ImageArchiver import ImageArchiver

archiver = ImageArchiver("localhost", "root", None, "cam2")

archiver.retrieve_csv("cameraSources/test_camera_url", "NON_IP", 10, 1, "results")
#archiver.retrieve_db("cameraSources/db_test.csv",100 ,1, "/results")