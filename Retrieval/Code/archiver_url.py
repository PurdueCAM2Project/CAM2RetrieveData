"""This program archives images from a set of cameras.

To use this program:
python archiver.py <input_file> <duration> <interval>

where:
<input_file> is the path to the two-column space-separated input file. The
first column is the integer camera ID, and the second column is the camera URL.
<duration> is the archiving duration in seconds.
<interval> is the interval between two frames in seconds (or 0 for the maximum
frame rate possible).

For example, this command downloads a snapshot from every camera every one
second for 60 seconds.
python archiver.py cams.txt 60 1

Sample input file:
31837 http://207.251.86.238/cctv290.jpg
31838 http://207.251.86.238/cctv294.jpg
31839 http://207.251.86.238/cctv296.jpg
31840 http://207.251.86.238/cctv297.jpg
31843 http://207.251.86.238/cctv302.jpg
31844 http://207.251.86.238/cctv303.jpg
31918 http://207.251.86.238/cctv428.jpg
31919 http://207.251.86.238/cctv429.jpg
31921 http://207.251.86.238/cctv431.jpg
31950 http://207.251.86.238/cctv467.jpg
31954 http://207.251.86.238/cctv470.jpg
31963 http://207.251.86.238/cctv482.jpg

Notes
-----
This program has a single third-party dependency: the PIL library. It can be
installed using the following command:
sudo apt-get install python-imaging

"""

import os
import sys
import time
import datetime
import threading
from urllib2 import urlopen
from StringIO import StringIO

from PIL import Image


# The path of the results directory.
RESULTS_PATH = 'results'


def read_file(path):
    """Read the input two-column file into a dictionary.

    Parameters
    ----------
    path : str
        The path of the input file.

    Returns
    -------
    cams : dict
        The dictionary withe camera IDs and URLs as the keys and values.

    """
    with open(path) as f:
        lines = f.read().strip().splitlines()

    cams = {}
    for line in lines:
        parts = line.split()
        cams[parts[0]] = parts[1]

    return cams


def download_image(image_url):
    """Download an online image given its URL.

    Parameters
    ----------
    image_url : str
        The full URL of the image to be downloaded.

    Returns
    -------
    image : PIL.Image.Image
        The downloaded image in RGB format.

    Raises
    ------
    Exception
        If there is any error downloading the image.

    """
    try:
        # Download the image.
        image = Image.open(StringIO(urlopen(image_url, timeout=5).read()))

        # Convert the image format to RGB if it is not.
        if image.mode != "RGB":
            image = image.convert("RGB")
    except Exception, e:
        raise Exception('Error downloading the image.')
    else:
        return image


class CameraHandler(threading.Thread):
    """The thread to download snapshots from a single camera.

    Parameters
    ----------
    id : int
        The ID of the the camera.
    url : str
        The URL of the camera image stream.
    duration : int
        The duration of downloading the images in seconds.
    interval : int
        The interval between each two successive snapshots.

    Attributes
    ----------
    id : int
        The ID of the the camera.
    url : str
        The URL of the camera image stream.
    duration : int
        The duration of downloading the images in seconds.
    interval : int
        The interval between each two successive snapshots.

    """
    def __init__(self, id, url, duration, interval):
        threading.Thread.__init__(self)
        self.id = id
        self.url = url
        self.duration = duration
        self.interval = interval

    def run(self):
        """Download snapshots from the camera, and save locally."""

        # Create the camera results directory.
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
                image = download_image(self.url)
            except Exception:
                pass
            else:
                # Save the image.
                file_name = '{}/{}_{}.png'.format(
                    cam_directory, self.id,
                    datetime.datetime.fromtimestamp(
                        frame_timestamp).strftime('%Y-%m-%d_%H-%M-%S-%f'))
                image.save(file_name)

            # Sleep until the interval between frames ends.
            time_to_sleep = self.interval - (time.time() - frame_timestamp)
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)


def main(args):
    # Read the input arguments.
    try:
        assert len(args) == 4
        input_file_path = args[1]
        duration = int(args[2])
        interval = int(args[3])
    except:
        import archiver
        print archiver.__doc__
        return

    # Read the input file.
    cams = read_file(input_file_path)

    camera_handlers = []
    for id, url in cams.iteritems():
        # Create a new thread to handle the camera.
        camera_handler = CameraHandler(id, url, duration, interval)
        # Run the thread.
        camera_handler.start()
        # Add the thread to the array of threads.
        camera_handlers.append(camera_handler)

        # Sleep to shift the starting time of all the threads.
        time.sleep(interval / len(cams))

    # Wait for all the threads to finish execution.
    for camera_handler in camera_handlers:
        camera_handler.join()


if __name__ == '__main__':
    main(sys.argv)
