"""Define the exceptions raised by the camera package.

"""


class Error(Exception):
    """Represent a generic error.

    """
    pass


class UnreachableCameraError(Error):
    """Represent an error when a camera is unreachable.

    """
    pass


class CorruptedFrameError(Error):
    """Represent an error when a camera stream frame is corrupted.

    """
    pass


class ClosedStreamError(Error):
    """Represent an error when a stream is closed and a frame is requested.

    """
    pass