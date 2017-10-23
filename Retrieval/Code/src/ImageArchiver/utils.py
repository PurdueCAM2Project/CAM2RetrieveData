"""
Description:  Checks that the given file exists. 
"""

import os

def check_file_exists(file_name):
    if (os.path.isfile(file_name) != True):
        print("Input File \"{}\" could not be found.".format(file_name))
        return 0
    return 1