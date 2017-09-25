import unittest
from mock import patch
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from camera import Camera, IPCamera, NonIPCamera, StreamFormat
from error import ClosedStreamError

class TestCamera(unittest.TestCase):
    def setUp(self):

        #Instantiate camera test fixtures
        self.cam = Camera(1, 1, 1)
        self.ip_cam = IPCamera(1, 1, 1, "127.1.1.1", "Image_Path")

    def test_get_frame_no_parser(self):
        #Assert camera raises error when no parser is present
        self.assertRaises(ClosedStreamError, self.cam.get_frame)

    def test_open_stream_invalid_enum(self):
        self.assertRaises(ValueError, self.ip_cam.open_stream, "INVALID_ENUM_VAL")

    def test_open_stream_valid_enum(self):
        with patch.object(self.ip_cam.parser, 'open_stream') as mock:
            self.ip_cam.open_stream(StreamFormat.MJPEG)

        mock.assert_called_once()

if __name__ == '__main__':
    unittest.main()