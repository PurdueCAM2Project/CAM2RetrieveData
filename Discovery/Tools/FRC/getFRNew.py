""" This program gets FPS for IP cameras and NON-IP cameras in cam2 database.
To run the program:
python getFRNew.py -r "400 x 400" -d cam2 0 (0 for non-ip)
"""

import sys
import os
import cv2
import time
import MySQLdb
import datetime
import filecmp
from camera import IPCamera
from camera import NonIPCamera
from camera import StreamFormat
from pebble import ProcessPool
from concurrent.futures import TimeoutError
import multiprocessing
import argparse
import re

lock = multiprocessing.Lock()
# Stores images into results
RESULTS_PATH = 'results'




def worker(cam, is_video, res_width, res_height, maxTime):
    #IP Cameras
    if is_video:
        #camera[0] is ID, camera[1] is ip, camera[2]port, camera[3]video path
        camera = IPCamera(cam[0], cam[1], None, cam[3], cam[2]) #ID,IP,imageStreamPath,optionalParams
        try:
            camera.open_stream(StreamFormat.MJPEG)
        except Exception:
            pass

        width = 0
        height = 0
        successes = 0
        start_timestamp = time.time()
        # Keep downloading snapshots for 10 seconds.
        while (time.time() - start_timestamp) < 10:
            try:
                image, _ = camera.get_frame()
            except Exception:
                pass
            else:
                height, width = image.shape[:2]
                if width >= res_width and height >= res_height:
                    successes += 1

        # Calculate the frame rate.
        frame_rate = successes / (time.time() - start_timestamp)
        return camera.id,frame_rate

    #NON-IP Cameras
    else:
        #Create non-ip camera object
        try:
            frame_rate_nonip = -1
            camera = NonIPCamera(cam[0], cam[1]) #ID,URL of the camera image stream

        except Exception as e:
            return
        #Get reference image
        try:
            frame_timestamp = time.time()
            RefFrame, _= camera.get_frame()

            width = 0
            height = 0
            height, width = RefFrame.shape[:2]

            if (RefFrame is not None and width >= res_width\
                and height >= res_height):
                cam_directory = os.path.join(RESULTS_PATH, str(camera.id))
                # save Ref frame
                RefFile_name = '{}/REF.png'.format(cam_directory)
                cv2.imwrite(RefFile_name, RefFrame)
                StartFile_name = '{}/START.png'.format(cam_directory)
                # Keep downloading more images for maxTime
                # to obtain the true frame rate of non-ip cameras
                if (get_next_frame(camera, None, RefFile_name, StartFile_name, maxTime) > -1):
                    EndFile_name = '{}/END.png'.format(cam_directory)
                    frame_rate_nonip = get_next_frame(camera, RefFile_name, StartFile_name, EndFile_name, maxTime)
                '''
                start_time = time.time()
                while (time.time() - start_time) < 30: # 30 secs minute currently
                    try:
                        frame_timestamp = time.time()
                        frame, _ = camera.get_frame()

                        if frame is not None:
                            #save frame
                            file_name = '{}/{}_{}.png'.format(
                                cam_directory, str(camera.id),
                                datetime.datetime.fromtimestamp(
                                    frame_timestamp).strftime('%Y-%m-%d_%H-%M-%S-%f'))
                            cv2.imwrite(file_name, frame)
                            # Compare each frame with ref frame
                            # Once different, obtain frame rate and exit.
                            if not filecmp.cmp(file_name, RefFile_name,shallow=True):
                                frame_rate_nonip = frame_timestamp - RefFrame_timestamp
                                #f.write(str(camera.id) + '\t' + str(frame_rate_nonip) + '\t' + '\n')
                                print(str(camera.id) + '\t' + str(frame_rate_nonip))
                                break;

                    except Exception: # Probably http error exceptions
                        #errorFile.write(str(camera.id))
                        print(str(camera.id) + '\t' + "NO FRAME")
                        return
                '''
        # We need to fix the exceptions
        except Exception as e: # Probably http error exceptions
            #print(str(camera.id) + '\t' + "NO REF FRAME")
            return camera.id,frame_rate_nonip

        #if (frame_rate_nonip == 0): 
            #print(str(camera.id) + '\t' + "NOT UPDATE LESS THAN 30 SEC")

        return camera.id,frame_rate_nonip

def get_next_frame(camera, file1, file2, file3, maxTime):
    start_time = time.time()
    while ((time.time() - start_time) < maxTime):
        frame, _ = camera.get_frame()
        cv2.imwrite(file3, frame)
        if (not filecmp.cmp(file2, file3, shallow=True)):
            if (file1 is not None):
                if (not filecmp.cmp(file1, file2, shallow=True)):
                    return (time.time() - start_time)
            else:
                return (time.time() - start_time)
    return -1

def parse_args(args):
    desc = 'Get the framerate of cameras in the database.'
    prog = 'getFRNew.py'
    parser = argparse.ArgumentParser(prog=prog, description=desc)
    parser.add_argument('is_video', nargs='+', help='whether the cameras are'\
                        ' videos or not.', type=int)
    parser.add_argument('-r', '--resolution', help='the minimum resolution'\
                        ' to evaluate. Pass as a string, for example, '\
                        ' \'400 x 400\'', type=str)
    parser.add_argument('-t', '--timeout', help='the maximum time to evaluate'\
                        ' a camera.', type=int)
    parser.add_argument('-p', '--processes', help='the number of processes'\
                        ' that will run concurrently.', type=int)
    parser.add_argument('-d', '--database', help='the name of the SQL database.'\
                        , type=str)
    return parser.parse_args(args)

def task_done(future):
    # Stores FPS for each camera
    f = open('FRs.txt', 'a')
    try:
        result = future.result() # blocks until results are ready
    except TimeoutError as e:
        lock.acquire()
        f.write(str(result)+"\n")
        lock.release()
        print("Function took longer than %d seconds" % e.args[1])
    except Exception as e:
        print("Function raised %s" % e)
        print(e.traceback) # traceback of the function
    else:
        lock.acquire()
        f.write(str(result)+"\n")
        lock.release()
    f.close()

def main(args):

    ns = parse_args(args[1:])
    is_video = ns.is_video[0]
    if is_video:
        is_video = True
    else:
        is_video = False
    processes_num = ns.processes
    database = ns.database
    timeout = ns.timeout
    if (ns.resolution is not None):
        m = re.match(r"(\d{3,})\s*[Xx]\s*(\d{3,})", ns.resolution)
        if m:
            res_height = int(m.group(1))
            res_width = int(m.group(2))
        else:
            print("Unable to understand resolution: using default value.")
            res_height = 400
            res_width = 400
    else:
        res_height = 400
        res_width = 400
    if (processes_num is None):
        processes_num = 25
    if (database is None):
        database = 'cam2New'
    if (timeout is None):
        timeout = 30

    DB_SERVER = 'localhost'
    DB_USER_NAME = 'cam2'
    DB_PASSWORD = ''
    DB_NAME = database

    connection = MySQLdb.connect(DB_SERVER,DB_USER_NAME,DB_PASSWORD,DB_NAME)
    cursor = connection.cursor()

    # ipCamera : is_active cameras only
    if is_video:
        cursor.execute('SELECT camera.id, ip, port, video_path '
                       'FROM camera, ip_camera, ip_camera_model '
                       'WHERE camera.id = ip_camera.camera_id '
                       'and ip_camera_model_id = ip_camera_model.id '
                       'and is_active=1 order by rand();')
    # non-ip Camera : is_active cams only
    elif not is_video:
        cursor.execute('select camera.id, non_ip_camera.snapshot_url '
                       'FROM camera, non_ip_camera '
                       'WHERE camera.id = non_ip_camera.camera_id '
                       'and is_active=1 and camera.id between 105000 and '
                       '106000 order by rand();')
    # 157868 157532
    # else : UNION two queries above to combine both IPCams and NON-IP Cams.

    # add functionality for ffmpeg retreival

    cameras = cursor.fetchall()

    # Close the connection.
    cursor.close()
    connection.close()

    # Empty the FRs.txt file (if one exists). Create one if it doesn't.
    f = open('FRs.txt', 'w')

    print "Number of Cameras:", len(cameras)
    init_len = len(cameras)
    cameras = tuple(get_active_cams(f, cameras, timeout))
    print("Eliminated {0:d} cameras".format(init_len - len(cameras)))

    f.close()
    
    print("Starting camera analysis")
    with ProcessPool(max_workers=processes_num) as pool:
       for camera in cameras:
            future = pool.schedule(worker, args=(camera, is_video, res_width,\
                    res_height, timeout), timeout=timeout*2 + 5)
            future.add_done_callback(task_done)

def get_active_cams(f, cameras, maxTime):
    cameras = list(cameras)
    print("Performing camera check")
    start_time = time.time()
    i = 0
    while i < len(cameras):
        print_progress(i, len(cameras))
        cam = cameras[i]
        camera = NonIPCamera(cam[0], cam[1])
        cam_directory = os.path.join(RESULTS_PATH, str(camera.id))
        try:
            frame, _ = camera.get_frame()
        except:
            del cameras[i]
            f.write("({0:d}L, -1)\n".format(camera.id))
            continue
        try:
            os.makedirs(cam_directory)
        except OSError as e:
            pass
        RefFile_name = '{}/REF.png'.format(cam_directory)
        cv2.imwrite(RefFile_name, frame)
        i += 1
    
    print_progress(1, 1)
    print('\nFirst Loop Done')
    time.sleep(max(0, maxTime - (time.time() - start_time)))

    i = 0
    while i < len(cameras):
        print_progress(i, len(cameras))
        cam = cameras[i]
        camera = NonIPCamera(cam[0], cam[1])
        cam_directory = os.path.join(RESULTS_PATH, str(camera.id))
        try:
            frame, _ = camera.get_frame()
        except:
            del cameras[i]
            i -= 1
            continue
        RefFile_name = '{}/REF.png'.format(cam_directory)
        StartFile_name = '{}/START.png'.format(cam_directory)
        cv2.imwrite(StartFile_name, frame)
        if (filecmp.cmp(RefFile_name, StartFile_name)):
            del cameras[i]
            f.write("({0:d}L, -1)\n".format(camera.id))
            i -= 1
        i += 1

    print_progress(1, 1)
    print('')

    return cameras

def print_progress(num_done, num_tot):
    sys.stdout.write('\r{0:0.2f}% completed'.format(float(num_done * 100)/num_tot))
    sys.stdout.flush()

# Call the main function
if __name__ == '__main__':
    start_time = datetime.datetime.now()
    print "Start Time:", start_time
    main(sys.argv)
    print "Start Time:", start_time
    print "End Time:", datetime.datetime.now()
