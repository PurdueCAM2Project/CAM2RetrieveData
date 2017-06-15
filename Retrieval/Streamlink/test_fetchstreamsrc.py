"""
This module tests the methods of the fetchstreamsrc module.

*****************************
Command Line Usage: python -m unittest test_fetchstreamsrc

** WARNING ** This tester connects to the Internet. Tests may run slowly.

******************************
    ** THE CAM2 PROJECT **
******************************
Authors: Caleb Tung,
Created: 6/13/2017
Preferred: Python3.x
"""

from __future__ import print_function # Force the use of Python3.x print()

import unittest
import fetchstreamsrc as fsrc



class Tests(unittest.TestCase):

    def test_get_stream_from_supported_multi_resolution_site_returns_properly_formatted_url(self):
        """ Tests a stream grab from YouTube, a site specifically supported
        with multiple resolutions"""
        src_url = fsrc.get_stream_src_from_url('https://www.youtube.com/watch?v=jlD3vw0LRSI')
        self.assertTrue(src_url.startswith('http://manifest.googlevideo.com/'))
        self.assertTrue(src_url.endswith('.m3u8'))

    def test_get_stream_unsupported_site_returns_properly_formatted_url(self):
        """ Tests a stream grab from Earthcam, a site not specifically supported"""
        src_url = fsrc.get_stream_src_from_url('http://www.earthcam.com/usa/newyork/timessquare/?cam=tsrobo1')
        self.assertTrue(src_url.startswith('http://video3.earthcam.com/'))
        self.assertTrue(src_url.endswith('.m3u8'))

    def test_get_stream_from_supported_single_resolution_site_returns_properly_formatted_url(self):
        """Tests a stream grab from uLive, a specifically supported site.
        Also ensures that when no 'best' stream exists, a stream is still selected"""
        src_url = fsrc.get_stream_src_from_url('http://www.ustream.tv/channel/apl-specials')
        self.assertTrue(src_url.startswith('http://'))
        self.assertTrue('.m3u8' in src_url)
        self.assertTrue('ustream.tv' in src_url)

    def test_get_stream_from_no_livestream_site_returns_none(self):
        """Tests that None is returned when the site contains no livestream."""

        self.assertIsNone(fsrc.get_stream_src_from_url('http://calebtung.com'))

    def test_get_stream_from_malformed_url_string_returns_none(self):
        """Tests that None is returned when the provided page URL is malformed"""
        self.assertIsNone(fsrc.get_stream_src_from_url('httpbustedwebsitestring'))

