import unittest
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from camera import Camera, IPCamera, NonIPCamera, StreamFormat
from error import ClosedStreamError

class TestCamera(unittest.TestCase):
    def setUp(self):

        #Instantiate camera test fixtures
        self.cam = Camera(1, 1, 1)
        self.ip_cam = IPCamera(1, 1, 1, "127.1.1.1", "/test_image_path", "/test_mjpeg_path", "3000")

    def test_get_frame_no_parser(self):
        #Assert camera raises error when no parser is present
        self.assertRaises(ClosedStreamError, self.cam.get_frame)

    def test_open_stream_invalid_enum(self):
        #Assert exception raised with invalid enum
        self.assertRaises(ValueError, self.ip_cam.open_stream, "INVALID_ENUM_VAL")

    def test_get_url_invalid_enum(self):
        #Assert exception raised with invalid enum
        self.assertRaises(ValueError, self.ip_cam.get_url, "INVALID_ENUM_VAL")

    def test_get_url_mjpeg(self):
        #Assert url correctly created for mjpeg case
        result = self.ip_cam.get_url(StreamFormat.MJPEG)
        self.assertEquals(result, "http://127.1.1.1:3000/test_mjpeg_path")

    def test_get_url_image(self):
        #Assert url correctly created for image case
        result = self.ip_cam.get_url(StreamFormat.IMAGE)
        self.assertEquals(result, "http://127.1.1.1:3000/test_image_path")



if __name__ == '__main__':
    unittest.main()