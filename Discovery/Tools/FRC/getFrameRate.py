""" This program gets FPS for IP cameras and NON-IP cameras in cam2 database.

To run this file:
1. script FROutput.txt
2. python getFrameRate.py <is_video> <more_options> <metadata> <threads> <server>
3. exit
Note: we save the terminal output to file because writing to file during the process is slow.
<is_video> can be:
    1: Cameras that support video stream = MJPEG =6337 cameras
    0: Cameras that support image stream = JPEG -> Should have a corresponding non-ip-camera.snapshoturl
and <more_options> can be:
    'all': All cameras
    '640': Cameras with resolution 640x480
    'axis640' Axis cameras with resolution 640x480
and <metadata> can be:
    'frame_rate': update the active state, the resolutions, and the frame rates.
        In this case, non-ip cameras will be ignored.
and <threads> is the number of threads used to access the cameras.
    Each thread is responsible for one camera. Use 8 when getting the frame
    rates with multithreading.
and <server> is the hostname of the database server. It is optional. If not
    specified, the local host is used.

"""

import sys
import os
import cv2
import time
import MySQLdb
import datetime
import threading
import filecmp
from camera import IPCamera
from camera import NonIPCamera
from camera import StreamFormat
from pebble import ProcessPool
from concurrent.futures import TimeoutError

# Stores images into results
RESULTS_PATH = 'results'

# Stores FPS for each camera
#f = open('cameras.txt', 'a')
# Stores cameras that did not retrieve any image
#errorFile = open('badCams.txt', 'a')

def worker(server, cameras, is_video, check_frame_rate): #cameras is just 1 camera managed by processes

    #IP Cameras
    if is_video:
        #camera[0] is ID, camera[1] is ip, camera[2]port, camera[3]video path
        cameras = IPCamera(cameras[0], cameras[1], None, cameras[3], cameras[2]) #ID,IP,imageStreamPath,optionalParams
        try:
            cameras.open_stream(StreamFormat.MJPEG)
        except Exception:
            pass

        width = 0
        height = 0
        successes = 0
        start_timestamp = time.time()
        # Keep downloading snapshots for 10 seconds.
        while (time.time() - start_timestamp) < 10:
            try:
                image, _ = cameras.get_frame()
            except Exception:
                pass
            else:
                height, width = image.shape[:2]
                if width > 400 and height > 400:
                    successes += 1

            if not check_frame_rate:
                break

        # Calculate the frame rate.
        frame_rate = successes / (time.time() - start_timestamp)
        print (str(cameras.id) +'\t' + str(frame_rate))
        #f.write(str(cameras.id) +'\t' + str(frame_rate) + '\t' + '\n')

    #NON-IP Cameras
    else:
        #Create non-ip camera object
        try:
            frame_rate_nonip = 0
            camera = NonIPCamera(cameras[0], cameras[1]) #ID,URL of the camera image stream

        except Exception as e:
            return
        #Get reference image
        try:
            RefFrame_timestamp = time.time()
            RefFrame, _= camera.get_frame()

            width = 0
            height = 0
            height, width = RefFrame.shape[:2]

            if RefFrame is not None and (width > 400 and height > 400):
                cam_directory = os.path.join(RESULTS_PATH, str(camera.id))
                try:
                    os.makedirs(cam_directory)
                except OSError as e:
                    return
                # save Ref frame
                RefFile_name = '{}/{}_{}.png'.format(
                    cam_directory, str(camera.id),
                    datetime.datetime.fromtimestamp(
                        RefFrame_timestamp).strftime('%Y-%m-%d_%H-%M-%S-%f'))
                cv2.imwrite(RefFile_name, RefFrame)
                # Keep downloading more images for 30 secs
                # to obtain the true frame rate of non-ip cameras
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

        except Exception as e: # Probably http error exceptions
            #errorFile.write(str(camera.id))
            print(str(camera.id) + '\t' + "NO REF FRAME")
            return

        if (frame_rate_nonip == 0): # Source did not update after 30 secs, so we don't care about rate = TOO SLOW
            #f.write(str(camera.id) + '\t' + "NOT UPDATE LESS THAN 30 SEC" + '\t' + '\n')
            print(str(camera.id) + '\t' + "NOT UPDATE LESS THAN 30 SEC")

        #if is_video:
            #camera.close_stream()

def main(is_video, more_options, check_frame_rate, threads_num,
         server):

    if server is None:
        DB_SERVER = 'localhost'
        DB_USER_NAME = 'root'
        DB_PASSWORD = 'password'
        DB_NAME = 'cam2New'

    connection = MySQLdb.connect(DB_SERVER,DB_USER_NAME,DB_PASSWORD,DB_NAME)
    cursor = connection.cursor()

    #options not needed
    clause = ''
    '''
    clause = ''
    if more_options == '640':
        clause = 'and resolution_width = 640 and resolution_height = 480 '
    elif more_options == 'axis640':
        clause = ('and ip_camera_model.id = 11 '
                  'and resolution_width = 640 and resolution_height = 480 ')
    #is_Active not needed bc ALL is used
    is_active_column = 'video_is_active' if is_video else 'is_active'
    clause += 'and {} = 1 '.format(is_active_column) if is_active else ''
    '''
    # ipCamera : is_active cameras only
    if is_video:
        cursor.execute('SELECT camera.id, ip, port, video_path '
                       'FROM camera, ip_camera, ip_camera_model '
                       'WHERE camera.id = ip_camera.camera_id '
                       'and ip_camera_model_id = ip_camera_model.id '
                       'and is_active=1 '+ clause +
                       'order by rand();')
    # non-ip Camera : is_active cams only
    elif not is_video and check_frame_rate:
        cursor.execute('select camera.id, non_ip_camera.snapshot_url '
                       'FROM camera, non_ip_camera '
                       'WHERE camera.id = non_ip_camera.camera_id '
                       'and is_active=1 '+ clause +
                       'order by rand();')

    # else : UNION two queries above to combine both IPCams and NON-IP Cams.

    cameras = cursor.fetchall()

    # Close the connection.
    cursor.close()
    connection.close()

    print "Number of Cameras:", len(cameras)
    # Multithreading > slow
    '''
    threads = []
    for cameras_chunk in [cameras[i::threads_num] for i in xrange(threads_num)]:

        t = threading.Thread(target=worker,
                             args=(server, cameras_chunk, is_video,
                                   check_frame_rate))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    '''
    # Multiprocessing > Faster, but times out and kills process after 35 secs.

    with ProcessPool(max_workers=25) as pool:
       #jobs = [pool.schedule(worker, args=(server,i,is_video,is_active), timeout=30) for i in cameras]
        jobs = [pool.schedule(worker, args=(server,i,is_video,check_frame_rate), timeout=35) for i in cameras]

# Call the main function
if __name__ == '__main__':
    is_video = bool(int(sys.argv[1])) # 1 for IP Camera, 0 for non-ip Camera
    check_frame_rate = True if sys.argv[3] == 'frame_rate' else False
    threads_num = int(sys.argv[4])

    try:
        server = sys.argv[5]
    except IndexError:
        server = None

    start_time = datetime.datetime.now()
    print "Start Time:", start_time

    main(is_video, sys.argv[2], check_frame_rate, threads_num,
         server)

    #f.close()
    #errorFile.close()

    print "Start Time:", start_time
    print "End Time:", datetime.datetime.now()