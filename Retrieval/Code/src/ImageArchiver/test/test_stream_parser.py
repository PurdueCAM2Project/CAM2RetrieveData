import unittest
from mock import patch
import sys
import urllib2
from os import path
import json
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from StreamParser import StreamParser, MJPEGStreamParser, ImageStreamParser
from error import UnreachableCameraError, CorruptedFrameError, ClosedStreamError

class DummyUrlObject:

    def __init__(self, read_retval, readline_retval):
        self.read_retval = read_retval
        self.readline_retvals = readline_retval
        self.readline_count = 0

    def read(self, param=None):
        return self.read_retval

    def readline(self):
        retval = self.readline_retvals[self.readline_count]
        self.readline_count += 1
        return retval

    def close(self):
        pass

class TestStreamParser(unittest.TestCase):
    test_url = "http://testurl.com/camera"

    def setUp(self):
        self.stream_parser = StreamParser(self.test_url)
        self.image_stream_parser = ImageStreamParser(self.test_url)
        self.mjpeg_stream_parser = MJPEGStreamParser(self.test_url)
    # StreamParser Tests
    def test_get_frame_not_overwritten(self):
        self.assertRaises(NotImplementedError, self.stream_parser.get_frame)

    # ImageStreamParser Tests
    @patch('StreamParser.urllib2.urlopen', side_effect=urllib2.URLError("test"))
    def test_image_get_frame_unreachable_camera(self, mocked_urllib):
        self.assertRaises(UnreachableCameraError, self.image_stream_parser.get_frame)

    @patch('StreamParser.urllib2.urlopen', return_value=DummyUrlObject('', None))
    def test_image_no_frame(self, mocked_urllib):
        self.assertRaises(CorruptedFrameError, self.image_stream_parser.get_frame)

    @patch('StreamParser.cv2.imdecode', return_value=None)
    @patch('StreamParser.np.fromstring', return_value=None)
    @patch('StreamParser.urllib2.urlopen', return_value=DummyUrlObject('Test', None))
    def test_image_failed_decode(self, mocked_cv2, mocked_np, mocked_urllib):
        self.assertRaises(CorruptedFrameError, self.image_stream_parser.get_frame)

    # MJPEGStreamParser Tests
    def test_mjpeg_no_stream(self):
        self.assertRaises(ClosedStreamError, self.mjpeg_stream_parser.get_frame)

    @patch('StreamParser.urllib2.urlopen', side_effect=urllib2.URLError("test"))
    def test_mjpeg_url_open_failure(self, mocked_urllib):
        self.assertRaises(UnreachableCameraError, self.mjpeg_stream_parser.open_stream)

    @patch('StreamParser.urllib2.urlopen', return_value=DummyUrlObject(None, ['test']))
    def test_mjpeg_url_wrong_boundary(self, mocked_urllib):
        self.mjpeg_stream_parser.open_stream()
        self.assertRaises(CorruptedFrameError, self.mjpeg_stream_parser.get_frame)
        self.assertEqual(self.mjpeg_stream_parser.mjpeg_stream.readline_count, 1)

    @patch('StreamParser.urllib2.urlopen', return_value=DummyUrlObject(None, ['--myboundary', 'test']))
    def test_mjpeg_url_wrong_content_type(self, mocked_urllib):
        self.mjpeg_stream_parser.open_stream()
        self.assertRaises(CorruptedFrameError, self.mjpeg_stream_parser.get_frame)
        self.assertEqual(self.mjpeg_stream_parser.mjpeg_stream.readline_count, 2)

    @patch('StreamParser.urllib2.urlopen', return_value=DummyUrlObject(None, ['--myboundary', 'Content-Type: image/jpeg', 'first:second:third']))
    def test_mjpeg_frame_line_three_too_long(self, mocked_urllib):
        self.mjpeg_stream_parser.open_stream()
        self.assertRaises(CorruptedFrameError, self.mjpeg_stream_parser.get_frame)
        self.assertEqual(self.mjpeg_stream_parser.mjpeg_stream.readline_count, 3)

    @patch('StreamParser.urllib2.urlopen', return_value=DummyUrlObject(None, ['--myboundary', 'Content-Type: image/jpeg', 'Content-Length:not_a_digit']))
    def test_mjpeg_frame_line_three_invalid_content_length(self, mocked_urllib):
        self.mjpeg_stream_parser.open_stream()
        self.assertRaises(CorruptedFrameError, self.mjpeg_stream_parser.get_frame)
        self.assertEqual(self.mjpeg_stream_parser.mjpeg_stream.readline_count, 3)

    @patch('StreamParser.urllib2.urlopen', return_value=DummyUrlObject(None, ['--myboundary', 'Content-Type: image/jpeg', 'wrong:10']))
    def test_mjpeg_frame_line_three_invalid_content_length(self, mocked_urllib):
        self.mjpeg_stream_parser.open_stream()
        self.assertRaises(CorruptedFrameError, self.mjpeg_stream_parser.get_frame)
        self.assertEqual(self.mjpeg_stream_parser.mjpeg_stream.readline_count, 3)

    @patch('StreamParser.urllib2.urlopen', return_value=DummyUrlObject(None, ['--myboundary', 'Content-Type: image/jpeg', 'Content-Length:10', 'not-empty']))
    def test_mjpeg_frame_no_empty_line_before_binary(self, mocked_urllib):
        self.mjpeg_stream_parser.open_stream()
        self.assertRaises(CorruptedFrameError, self.mjpeg_stream_parser.get_frame)
        self.assertEqual(self.mjpeg_stream_parser.mjpeg_stream.readline_count, 4)

    @patch('StreamParser.urllib2.urlopen', return_value=DummyUrlObject(None, ['--myboundary', 'Content-Type: image/jpeg', 'Content-Length:10', '', 'not-empty']))
    def test_mjpeg_frame_no_empty_line_after_binary(self, mocked_urllib):
        self.mjpeg_stream_parser.open_stream()
        self.assertRaises(CorruptedFrameError, self.mjpeg_stream_parser.get_frame)
        self.assertEqual(self.mjpeg_stream_parser.mjpeg_stream.readline_count, 5)

    @patch('StreamParser.urllib2.urlopen', return_value=DummyUrlObject(None, ['--myboundary', 'Content-Type: image/jpeg', 'Content-Length:10', '', '']))
    @patch('StreamParser.cv2.imdecode', return_value=None)
    @patch('StreamParser.np.fromstring', return_value=None)
    def test_mjpeg_frame_is_none(self, mocked_urllib, mocked_cv2, mocked_np):
        self.mjpeg_stream_parser.open_stream()
        self.assertRaises(CorruptedFrameError, self.mjpeg_stream_parser.get_frame)
        self.assertEqual(self.mjpeg_stream_parser.mjpeg_stream.readline_count, 5)
        self.assertTrue(mocked_np.called)
        self.assertTrue(mocked_cv2.called)

    @patch('StreamParser.urllib2.urlopen', return_value=DummyUrlObject(None, ['--myboundary', 'Content-Type: image/jpeg', 'Content-Length:10', '', '']))
    @patch('StreamParser.cv2.imdecode', return_value="Test")
    @patch('StreamParser.np.fromstring', return_value=None)
    def test_mjpeg_frame_is_none(self, mocked_urllib, mocked_cv2, mocked_np):
        self.mjpeg_stream_parser.open_stream()
        self.assertEqual(self.mjpeg_stream_parser.get_frame(), ("Test", 10))
        self.assertEqual(self.mjpeg_stream_parser.mjpeg_stream.readline_count, 5)
        self.assertTrue(mocked_np.called)
        self.assertTrue(mocked_cv2.called)

if __name__ == '__main__':
    unittest.main()