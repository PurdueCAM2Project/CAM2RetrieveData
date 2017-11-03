"""
Parse different types of camera streams.

This module is used to parse different types of camera streams. The module
provides the StreamParser base class which provides a uniform way of parsing
all camera streams. The module provides different subclasses, each for a
different type of camera streams (e.g. image streams, and MJPEG streams).

Examples
--------

**Example 1**: To parse a camera image stream:

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

**Example 2**: To parse a camera MJPEG stream:

1. Initialize an object of MJPEGStreamParser using the URL of the camera
MJPEG stream.

2. Open the stream by calling the open_stream method.

3. Use the get_frame method to get the most recent frame at any point of time,
as well as the frame size.

4. At the end when no more frames are needed, close the stream by calling the
close_stream method.

parser = MJPEGStreamParser('http://128.10.29.33/axis-cgi/mjpg/video.cgi')
parser.open_stream()
t = time.time()

while time.time() - t < 5:
    frame, frame_size = parser.get_frame()
    cv2.imshow('frame', frame)
    print frame_size
    cv2.waitKey(30)
    
parser.close_stream()

**Classes and Functions** 

"""
import urllib2

import cv2
import numpy as np

import error


class StreamParser(object):
    """
    Represent the base class for camera stream parsers.

    **Parameters**
    
    url : str
        The URL of the stream.

    **Attributes**
    
    url : str
        The URL of the stream.
    """

    def __init__(self, url):
        self.url = url

    def open_stream(self):
        """Open the stream.

        **Raises**
        
        error.UnreachableCameraError
            If the camera is unreachable.
        """
        pass

    def close_stream(self):
        """
        Close the MJPEG stream.
        """
        pass

    def restart_stream(self):
        """
        Restart the stream.

        This method restarts the stream by closing then opening it. This is
        useful because some cameras closes a stream if it is open for a long
        period of time.
        """
        self.close_stream()
        self.open_stream()

    def get_frame(self):
        """
        Get the most recent frame from the camera stream.

        This method is an abstract method that must be overridden by subclasses.

        **Returns**
        
        numpy.ndarray
            The downloaded frame.
        int
            The size of the downloaded frame in bytes.

        **Raises**
        
        error.CorruptedFrameError
            If the frame is corrupted.
        error.UnreachableCameraError
            If the camera is unreachable.
        error.ClosedStreamError
            If the stream needs to be opened first.
        NotImplementedError
            If the method is not overridden in the subclass.
        """
        raise NotImplementedError('The get_frame method has to be overridden.')


class ImageStreamParser(StreamParser):
    """
    Represent a parser for a camera image stream.

    This class subclasses the StreamParser class and inherits its attributes
    and constructor.

    **Notes**
   
    A camera that provides an image stream is a camera that provides a URL to
    get the most recent frame (regardless of how recent it is). Hence, Parsing
    an image stream is as simple as downloading the most recent frame from the
    given URL whenever requested. There is no need to call open_stream or
    close_stream since they do nothing.
    """

    def get_frame(self):
        """
        Get the most recent frame from the camera image stream.

        **Returns**
       
        frame : numpy.ndarray
            The downloaded frame.
        frame_size : int
            The size of the downloaded frame in bytes.

        **Raises**
        
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


class MJPEGStreamParser(StreamParser):
    """
    Represent a parser for a camera MJPEG stream.

    This class subclasses the StreamParser class and inherits its attributes
    and extends its constructor.

    **Parameters**
    
    url : str
        The URL of the MJPEG stream.

    **Attributes**
   
    mjpeg_stream : file-like object
        The handle to the camera MJPEG stream.
    """

    def __init__(self, url):
        super(MJPEGStreamParser, self).__init__(url)
        self.mjpeg_stream = None

    def open_stream(self):
        """
        Open the MJPEG stream.

        **Raises**
      
        error.UnreachableCameraError
            If the camera is unreachable.
        """
        try:
            self.mjpeg_stream = urllib2.urlopen(self.url, timeout=5)
        except urllib2.URLError:
            raise error.UnreachableCameraError

    def close_stream(self):
        """
        Close the MJPEG stream.
        """
        if self.mjpeg_stream is not None:
            self.mjpeg_stream.close()
            self.mjpeg_stream = None

    def get_frame(self):
        """
        Get the most recent frame from the camera MJPEG stream.

        **Returns**
       
        frame : numpy.ndarray
            The downloaded frame.
        frame_size : int
            The size of the downloaded frame in bytes.

        **Raises**
   
        error.CorruptedFrameError
            If the frame is corrupted.
        error.ClosedStreamError
            If the MJPEG stream needs to be opened first.

        **Notes**
     
        MJPEG Stream Format:
        --myboundary
        Content-Type: image/jpeg
        Content-Length: [size of image in bytes]
        [empty line]
        ..... binary data .....
        [empty line]
        --myboundary
        Content-Type: image/jpeg
        Content-Length: [size of image in bytes]
        [empty line]
        ..... binary data .....
        [empty line]
        """
        if self.mjpeg_stream is None:
            raise error.ClosedStreamError

        # Skip the boundary line.
        if self.mjpeg_stream.readline().rstrip() != '--myboundary':
            raise error.CorruptedFrameError

        # Skip the second line that has "Content-Type: image/jpeg".
        if self.mjpeg_stream.readline().rstrip() != 'Content-Type: image/jpeg':
            raise error.CorruptedFrameError

        # Verify the format of the third line, and get the frame size.
        line = [s.strip() for s in self.mjpeg_stream.readline().split(':')]
        if len(line) == 2 and line[0] == 'Content-Length' and line[1].isdigit():
            frame_size = int(line[1])
        else:
            raise error.CorruptedFrameError

        # Skip the empty line before the binary frame data.
        if self.mjpeg_stream.readline().strip() != '':
            raise error.CorruptedFrameError

        # Read the binary frame data.
        frame = self.mjpeg_stream.read(frame_size)

        # Skip the empty line after the binary frame data.
        if self.mjpeg_stream.readline().strip() != '':
            raise error.CorruptedFrameError

        # Decode the frame data to a numpy.ndarray image.
        frame = cv2.imdecode(np.fromstring(frame, dtype=np.uint8), -1)

        # Handle the cameras whose URLs return 1x1 images. The method
        # cv2.imdecode returns None if the input buffer is too short or
        # contains invalid data.
        if frame is None:
            raise error.CorruptedFrameError

        return frame, frame_size

    def __del__(self):
        """
        Close the MJPEG stream when the object is about to be destroyed.

        This destructor is a backup plan in case the user of this class did not
        call the close_stream method. The close_stream method has to be called,
        without relying on this destructor, because __del__ is not guaranteed
        to be called in some cases and it is also better to close the stream as
        soon as possible to avoid unnecessary network workload.
        """
        self.close_stream()



class mjpgStreamParser(StreamParser):
    """
    Represent a parser for a camera MJPEG stream.
    *Does not have to be MJPEG, .m3u8 media file works as well.

    This class subclasses the StreamParser class and inherits its attributes
    and extends its constructor.

    **Parameters**
    
    url : str
        The URL of the MJPEG stream.

    **Attributes**
   
    mjpeg_stream : file-like object
        The handle to the camera MJPEG stream.
    """

    def __init__(self, url):
        super(mjpgStreamParser, self).__init__(url)
        self.mjpeg_stream = None

    def get_frame(self):
        """
        Get the most recent frame from the camera MJPEG stream.

        **Returns**
        
        frame : numpy.ndarray
            The downloaded frame.
        frame_size : int
            The size of the downloaded frame in bytes.

        **Raises**
       
        error.CorruptedFrameError
            If the frame is corrupted.
        error.ClosedStreamError
            If the MJPEG stream needs to be opened first.
        """

        vc = cv2.VideoCapture(self.url)

        if vc.isOpened():
            rval , frame = vc.read()
            return frame,1
        else:
            rval = False
            print("No frame returned")
            return None,1

        vc.release()

