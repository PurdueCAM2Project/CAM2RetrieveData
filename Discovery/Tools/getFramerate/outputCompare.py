"""
--------------------------------------------------------------------------------
Descriptive Name     : outputCompare.py
Author               : Ryan Dailey                                   
Contact Info         : dailey1@purdue.edu
Date Written         : 10/6/16
Description          : This script takes output from the frame rate assessment program (getFramerate.py) and puts it into a .csv that
                        can be easily viewed in a spreadsheet software like Excel. It compares both the Successful OUtputs and the
                        unsuccessful outputs.
Command to run script: python outputCompare.py <Directory you wish to analyze> <-m to include source and camera url>
Usage                : For use with the -m command you must have a copy of get connection in the same directory.
Input file format    : Input formats are taken directly from the output of the getFramerate.py program. No modification is necessary.
                        Input files must be .txt files and have the "SuccessfulOutput" and/or "CameraErrorReport" strings in them.
                        Input files must also be in the same directory.
Output               : This script will output two files:
                        1) SuccessfulOutput_<Input Dir>.csv
                        2) FailureCompare_<Input Dir>.csv
Note                 : 
Other files required by : To use the "-m" tag when running it (Gets source, url info) you must have the getConnection.py script.
this script and where 
located
"""

import sys
import re
import os

def main(args):
    try:
        folder_to_load = args[1]
        if folder_to_load.find("/") != -1:
            folder_to_load = folder_to_load[0:len(folder_to_load)-1]
        try:
            if args[2] == "-m":
                import getConnection
                connection = getConnection.getConnection(None)
                cursor = connection.cursor()
            else:
                raise(Exception("Flag Not Recognized."))
        except Exception as e:
            e == Exception("Flag Not Recognized.")
            raise(Exception("Flag Not Recognized."))
        except:
            cursor = None
            
    except Exception as e:
        print("ERROR: {}".format(e))
        print("Input Folder Not Found.")
        print("Call Syntax:\n\tpython OutputCompare.py <Input Directory> <-m>\n")
        print("\tNote: to use the -m flag you must have the getConnection.py \n\tmodule in the same directory.\n\n")
        return

    successCompare(folder_to_load, cursor)
    failureCompare(folder_to_load, cursor)
    if cursor != None:
        cursor.close()
        connection.close()

def successCompare(folder_to_load, cursor):
    outputFile = "SuccessCompare_{}.csv".format(folder_to_load)

    fComp = open(outputFile, "w") # The program trys to determine frame rates less than 1 min if longer it writes them here

    files = os.listdir(folder_to_load+"/")

    output = [] # List of all cameras in all files

    fileList = None
    x = 0
    fComp.write(',{}'.format("ID"))
    for onefile in files:
        if onefile.find(".txt") != -1 and onefile.find("SuccessfulOutput") != -1:
            f = open(folder_to_load+"/"+onefile, "r") 
            fileList = list(f)
            if len(fileList) > 10:
                output.append(fileList)
                x += x
                f.close()
                fComp.write(',{}'.format(onefile[:20]))
                print(onefile)
            else:
                print("File {} less then 10 entries not importing.".format(onefile))

    if fileList == None or len(fileList) <= 1:
        print("1 or less successful input files detected. Skipping.")
        return
    
    fComp.write(",Min, Max, Average, Source, URL")

    fComp.write("\n")
    
    cameraList = set()
    framerateDict = {}
    
    for oneOutput in output:
        for camera in oneOutput:
            camera = re.search(r"(?P<ID>[\d]*)\t(?P<FR>[\d.]*)\n", camera)
            try:
                cameraList.add(camera.group("ID"))
            except:
                pass
    
    
    for camera in cameraList:
        fComp.write(',{}'.format(camera))
        framerates = []
        for onefile in output:
            written = False
            for entry in onefile:
                entry = re.search(r"(?P<ID>[\d]*)\t(?P<FR>[\d.]*)\n", entry)
                if entry != None and entry.group("ID") == camera:
                    framerates.append(float(entry.group("FR")))
                    fComp.write(',{}'.format(float(entry.group("FR"))/60))
                    written = True
            if written == False:
                fComp.write(',{}'.format(""))

        if cursor != None:
            cursor.execute('select camera_id, snapshot_url FROM non_ip_camera WHERE camera_id = {};'.format(camera))
            camera_url_row = cursor.fetchone()
            cursor.execute('select source FROM camera WHERE id = {};'.format(camera))
            camera_info_row = cursor.fetchone()
            fComp.write(',,,,{},{}\n'.format(camera_info_row[0], camera_url_row[1]))
        else:
            fComp.write("\n")


    fComp.write("\n")
    fComp.close()
    

def failureCompare(folder_to_load, cursor):
    outputFile = "FailureCompare_{}.csv".format(folder_to_load)

    fComp = open(outputFile, "w") # The program trys to determine frame rates less than 1 min if longer it writes them here

    files = os.listdir(folder_to_load+"/")

    output = [] # List of all cameras in all files

    fileList = None
    x = 0
    for onefile in files:
        if onefile.find(".txt") != -1 and onefile.find("CameraErrorReport") != -1:
            f = open(folder_to_load+"/"+onefile, "r") 
            fileList = list(f)
            if len(fileList) > 10:
                output.append(fileList)
                x += x
                f.close()
                # fComp.write(',{}'.format(onefile[:20]))
                print(onefile)
            else:
                print("File {} less then 10 entries not importing.".format(onefile))

    if fileList == None or len(fileList) <= 1:
        print("1 or less successful input files detected. Skipping.")
        return

    fComp.write('\n')
    fComp.write('ID,Cameras that exceeded threshold,Cameras Loaded But Not Finished,Cameras with retrieval errors,Other Cameras, Source, URL\n')
    
    cameraList = set()
    framerateDict = {}
    
    # list_to_add_to gives a constant # that determines which list we are adding to.

    threshold = [] # 1
    unfinished = [] # 2
    retrevalErrors = [] # 3
    others = [] # others shouldn't hold any cameras. It only holds cameras if 1,2, or 3 isn't specified.

    for oneOutput in output:
        list_to_add_to = 0
        for oneLine in oneOutput:
            ID = re.search(r'[0-9]*', oneLine)

            if oneLine.find("Cameras that exceeded threshold") != -1:
                list_to_add_to = 1
            if oneLine.find("Cameras Loaded But Not Finished") != -1:
                list_to_add_to = 2
            if oneLine.find("Cameras with retrieval errors") != -1:
                list_to_add_to = 3
            if oneLine.find("Cameras Not Loaded") != -1:
                break

            if list_to_add_to == 1 and str(ID.group(0)) != '':
                threshold.append(ID.group(0))
            elif list_to_add_to == 2 and str(ID.group(0)) != '':
                unfinished.append(ID.group(0))
            elif list_to_add_to == 3 and str(ID.group(0)) != '':
                retrevalErrors.append(ID.group(0))
            elif str(ID.group(0)) != '':
                others.append(ID.group(0))
               
            try:
                if str(ID.group(0)) != '':
                    cameraList.add(ID.group(0))
                    
            except:
                pass
    
    for camera in cameraList:
        if cursor != None:
            cursor.execute('select camera_id, snapshot_url FROM non_ip_camera WHERE camera_id = {};'.format(camera))
            camera_url_row = cursor.fetchone()
            cursor.execute('select source FROM camera WHERE id = {};'.format(camera))
            camera_info_row = cursor.fetchone()
            fComp.write('{},{},{},{},{},{},{}\n'.format(camera, threshold.count(camera), unfinished.count(camera), retrevalErrors.count(camera), others.count(camera), camera_info_row[0], camera_url_row[1]))
        else:
            fComp.write('{},{},{},{},{}\n'.format(camera, threshold.count(camera), unfinished.count(camera), retrevalErrors.count(camera), others.count(camera)))


    fComp.close()

if __name__ == '__main__':
    main(sys.argv)