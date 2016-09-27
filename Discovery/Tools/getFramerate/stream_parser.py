"""Parse different types of camera streams.

This module is used to parse different types of camera streams. The module
provides the StreamParser base class which provides a uniform way of parsing
all camera streams. The module provides different subclasses, each for a
different type of camera streams (e.g. image streams, and MJPEG streams).

Examples
--------
Example 1: To parse a camera image stream:
1. Initialize an object of ImageStreamParser using the URL of the camera
image stream.
2. Use the get_frame method to get the most recent frame at any point of
time, as well as the frame size. There is no need to call open_stream or
close_stream.

parser = ImageStreamParser('http://128.10.29.33/axis-cgi/jpg/image.cgi')
frame, frame_size = parser.get_frame()
cv2.imshow('frame', frame)
print frame_size
cv2.waitKey()

"""
import urllib2

import cv2
import numpy as np

import error


class StreamParser(object):
    """Represent the base class for camera stream parsers.

    Parameters
    ----------
    url : str
        The URL of the stream.

    Attributes
    ----------
    url : str
        The URL of the stream.

    """

    def __init__(self, url):
        self.url = url


class ImageStreamParser(StreamParser):
    """Represent a parser for a camera image stream.

    This class subclasses the StreamParser class and inherits its attributes
    and constructor.

    Notes
    -----
    A camera that provides an image stream is a camera that provides a URL to
    get the most recent frame (regardless of how recent it is). Hence, Parsing
    an image stream is as simple as downloading the most recent frame from the
    given URL whenever requested. There is no need to call open_stream or
    close_stream since they do nothing.

    """

    def get_frame(self):
        """Get the most recent frame from the camera image stream.

        Returns
        -------
        frame : numpy.ndarray
            The downloaded frame.
        frame_size : int
            The size of the downloaded frame in bytes.

        Raises
        ------
        error.CorruptedFrameError
            If the frame is corrupted.
        error.UnreachableCameraError
            If the camera is unreachable.

        """
        try:
            # Download the frame data.
            frame = urllib2.urlopen(self.url, timeout=5).read()
        except urllib2.URLError:
            raise error.UnreachableCameraError

        # Handle the cameras that return empty content.
        if frame == '':
            raise error.CorruptedFrameError

        # Get the size of the downloaded frame in bytes.
        frame_size = len(frame)

        # Decode the frame data to a numpy.ndarray image.
        frame = cv2.imdecode(np.fromstring(frame, dtype=np.uint8), -1)

        # Handle the cameras whose URLs return 1x1 images. The method
        # cv2.imdecode returns None if the input buffer is too short
        # or contains invalid data.
        if frame is None:
            raise error.CorruptedFrameError

        return frame, frame_size
