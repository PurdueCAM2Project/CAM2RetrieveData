"""Provide classes to deal with different types of cameras.

This module is used to deal with different types of cameras. The module
provides the Camera base class which provides a uniform way of dealing with
all types of cameras. The module provides different subclasses, each for a
different type of cameras (e.g. IP cameras, and non-IP cameras). The module
also provides the StreamFormat Enum for the different camera stream formats.

Examples
--------
Example 1: To get frames from a non-IP camera image stream:
1. Initialize a NonIPCamera object using the ID and the URL of the camera
image stream.
2. Use the get_frame method to get the most recent frame at any point of time,
as well as the frame size. There is no need to call open_stream or close_stream.

camera = NonIPCamera(1, 'http://images.webcams.travel/preview/1169307993.jpg')
frame, frame_size = camera.get_frame()
cv2.imshow('frame', frame)
print frame_size
cv2.waitKey()

Example 2: To get frames from an IP camera image stream:
1. Initialize an IPCamera object using the ID, IP, image stream path, and
other optional parameters.
2. Use the get_frame method to get the most recent frame at any point of time,
as well as the frame size. While dealing with image streams of IP cameras,
there is no need to call open_stream or close_stream.

camera = IPCamera(1, '128.10.29.33', '/axis-cgi/jpg/image.cgi')
frame, frame_size = camera.get_frame()
cv2.imshow('frame', frame)
print frame_size
cv2.waitKey()

Example 3: To get frames from an IP camera MJPEG stream:
1. Initialize an IPCamera object using the ID, IP, image stream path, MJPEG
stream path, and other optional parameters.
2. Open the camera MJPEG stream by calling the open_stream method with the
StreamFormat.MJPEG parameter.
3. Use the get_frame method to get the most recent frame at any point of time,
as well as the frame size.
4. At the end when no more frames are needed, Close the camera MJPEG stream by
calling the close_stream method.

camera = IPCamera(1, '128.10.29.33', '/axis-cgi/jpg/image.cgi',
                  '/axis-cgi/mjpg/video.cgi')
camera.open_stream(StreamFormat.MJPEG)
t = time.time()
while time.time() - t < 5:
    frame, frame_size = camera.get_frame()
    cv2.imshow('frame', frame)
    print frame_size
    cv2.waitKey(30)
camera.close_stream()

"""
import error
import stream_parser


class StreamFormat(object):
    """Represent an Enum for the different camera stream formats.

    Attributes
    ----------
    IMAGE : int
        The constant class variable representing image streams.
    MJPEG : int
        The constant class variable representing MJPEG streams.

    """

    IMAGE = 1
    MJPEG = 2


class Camera(object):
    """Represent the base class for all types of cameras.

    Parameters
    ----------
    id : int
        The unique camera ID.

    Attributes
    ----------
    id : int
        The unique camera ID.
    parser : StreamParser
        The parser of the camera stream.

    Notes
    -----
    A camera handles a single stream at a time. Use the open_stream method to
    open the stream of the desired format (e.g. MJPEG). Then, use the method
    get_frame to get frames from the currently open stream. Then, use the
    method close_stream to close the currently open stream. This class does
    not allow dealing with multiple streams from the same camera object at
    the same time.

    """

    def __init__(self, id):
        self.id = id
        self.parser = None

    def open_stream(self, stream_format):
        """Open the camera stream of the given format.

        Parameters
        ----------
        stream_format : int
            The stream format of the camera. This can be any of the StreamFormat
            class variables (e.g. StreamFormat.IMAGE or StreamFormat.MJPEG)

        Raises
        ------
        error.UnreachableCameraError
            If the camera is unreachable.

        """
        pass

    def close_stream(self):
        """Close the currently open camera stream.

        """
        pass

    def restart_stream(self):
        """Restart the currently open camera stream.

        This method restarts the stream by closing then opening it. This is
        useful because some cameras closes a stream if it is open for a long
        period of time.

        """
        self.parser.restart_stream()

    def get_frame(self):
        """Get the most recent frame from the currently open camera stream.

        Returns
        -------
        numpy.ndarray
            The downloaded frame.
        int
            The size of the downloaded frame in bytes.

        Raises
        ------
        error.CorruptedFrameError
            If the frame is corrupted.
        error.UnreachableCameraError
            If the camera is unreachable.
        error.ClosedStreamError
            If the stream needs to be opened first.

        """
        if self.parser is None:
            raise error.ClosedStreamError
        return self.parser.get_frame()


class IPCamera(Camera):
    """Represent an IP camera.

    This class subclasses the Camera class and inherits its attributes and
    extends its constructor.

    Parameters
    ----------
    id : int
        The unique camera id.
    ip : str
        The IP address of the camera.
    image_path : str
        The path to the camera image stream.
    mjpeg_path : str, optional
        The path to the camera MJPEG stream.
    port : int, optional
        The port of the camera.

    Attributes
    ----------
    ip : str
        The IP address of the camera.
    image_path : str
        The path to the camera image stream.
    mjpeg_path : str
        The path to the camera MJPEG stream.
    port : int
        The port of the camera.

    Notes
    -----
    By default, the constructor of this class initializes an ImageStreamParser
    so that frames can be retrieved from the image stream without the need to
    call the open_stream method.

    """

    def __init__(self, id, ip, image_path, mjpeg_path=None, port=None):
        super(IPCamera, self).__init__(id)
        self.ip = ip
        self.image_path = image_path
        self.mjpeg_path = mjpeg_path
        self.port = port

        # Initializes an ImageStreamParser so that frames can be retrieved from
        # the image stream without the need to call the open_stream method.
        self.parser = stream_parser.ImageStreamParser(self.get_url())

    def open_stream(self, stream_format):
        """Open the camera stream of the given format.

        Parameters
        ----------
        stream_format : int
            The stream format of the camera. This can be any of the StreamFormat
            class variables (e.g. StreamFormat.IMAGE or StreamFormat.MJPEG)

        Raises
        ------
        ValueError
            If the value of stream_format is invalid.
        error.UnreachableCameraError
            If the camera is unreachable.

        """
        # Get the URL of the stream of the given format.
        url = self.get_url(stream_format)

        # Initialize and open the parser according to the stream format.
        if stream_format == StreamFormat.MJPEG:
            self.parser = stream_parser.MJPEGStreamParser(url)
            self.parser.open_stream()
        elif stream_format == StreamFormat.IMAGE:
            # The image stream parser is always initialized, and the stream
            # does not need to be opened.
            pass
        else:
            raise ValueError('Invalid Argument: stream_format')

    def close_stream(self):
        """Close the currently open camera stream.

        Notes
        -----
        After closing the currently open camera stream, this method initializes
        an ImageStreamParser so that frames can be retrieved from the image
        stream without the need to call the open_stream method.

        """
        if self.parser is not None:
            self.parser.close_stream()
            self.parser = stream_parser.ImageStreamParser(self.get_url())

    def get_url(self, stream_format=StreamFormat.IMAGE):
        """Get the URL to the camera stream of the given format.

        Parameters
        ----------
        stream_format : int, optional
            The stream format of the camera. This can be any of the StreamFormat
            class variables (e.g. StreamFormat.IMAGE or StreamFormat.MJPEG)

        Returns
        -------
        url : str
            The URL to the camera stream of the given format.

        Raises
        ------
        ValueError
            If the value of stream_format is invalid.

        """
        # Set the path according to the stream format.
        if stream_format == StreamFormat.IMAGE:
            path = self.image_path
        elif stream_format == StreamFormat.MJPEG:
            path = self.mjpeg_path
        else:
            raise ValueError('Invalid Argument: stream_format')

        # Construct the URL using the IP, port, and path.
        if self.port is None:
            url = 'http://{}{}'.format(self.ip, path)
        else:
            url = 'http://{}:{}{}'.format(
                self.ip, self.port, path)

        return url

    def __del__(self):
        """Close the currently open camera stream before destroying the object.

        This destructor is a backup plan in case the user of this class did not
        call the close_stream method. The close_stream method has to be called,
        without relying on this destructor, because __del__ is not guaranteed
        to be called in some cases and it is also better to close the stream as
        soon as possible to avoid unnecessary network workload.

        """
        self.close_stream()


class NonIPCamera(Camera):
    """Represent a non-IP camera.

    This class represents a camera whose IP is not known. A web server hides
    the information about the camera, and provides only a URL to get the most
    recent frame from the camera. This class subclasses the Camera class and
    inherits its attributes and extends its constructor.

    Parameters
    ----------
    id : int
        The unique camera ID.
    url : str
        The URL that is used to get the most recent frame from the camera.

    Attributes
    ----------
    url : str
        The URL that is used to get the most recent frame from the camera.

    Notes
    -----
    By default, the constructor of this class initializes an ImageStreamParser
    so that frames can be retrieved from the image stream without the need to
    call the open_stream method.

    """

    def __init__(self, id, url):
        super(NonIPCamera, self).__init__(id)
        self.url = url

        self.parser = stream_parser.ImageStreamParser(url)
