# getFRNew Usage and Algorithm

Program usage: python getFRNew.py --help or -h

usage: getFRNew.py [-h] [-r RESOLUTION] [-t TIMEOUT] [-p PROCESSES]
                   [-d DATABASE]
                   is_video [is_video ...]

Get the framerate of cameras in the database.

positional arguments:
  is_video              whether the cameras are videos or not.

optional arguments:
*  -h, --help            show this help message and exit
*  -r RESOLUTION, --resolution RESOLUTION
                        the minimum resolution to evaluate. Pass as a string,
                        for example, '400 x 400'
*  -t TIMEOUT, --timeout TIMEOUT
                        the maximum time to evaluate a camera.
*  -p PROCESSES, --processes PROCESSES
                        the number of processes that will run concurrently.
*  -d DATABASE, --database DATABASE
                        the name of the SQL database.

Ex. Python getFRNew.py -r “400 x 400” -p 8 -d cam2 0


The program getFRNew.py relies on the following algorithm to determine
framerate:

* Pull an image from the camera. This will be referred to as the Reference
Image.
* Continue to pull images from the camera until an image is returned that is
different from the Reference Image. This will be referred to as the Start
Image. Get the time that this image was retrieved.
* Continue to pull images from the camera until an image is returned that is
different from both the Start Image and the Reference Image. This will be
referred to as the End Image. Get the time that this image was retrieved.
* Find the difference between the time that the Start and End images were
retrieved. This is the elapsed time (in seconds) it takes for the frame to
update. Note that this is seconds per frame, while framerate is normally
expressed in frames per second, or FPS.
