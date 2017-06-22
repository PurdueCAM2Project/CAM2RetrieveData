Streamlink
===================

[Streamlink](https://streamlink.github.io/) is a command line utility and Python API that uses a plugin-based system to download source URLs for livestreams on various websites.


Setup
-------------
1. Install the Streamlink command line utility as described [here](https://streamlink.github.io/install.html).
2. Test access to the utility:
```
$ streamlink --version
```
3. Test access to the Python module:
```
$ python
>>> import streamlink
```
> **Note:**
> Streamlink may not install for Python correctly. If the import fails, run the following (prepend ```sudo``` if necessary)
>```
> $ pip2 install streamlink # For Python2.x
> $ pip3 install streamlink # For Python3.x
>```

----------

Tutorial on using Streamlink in Python
-------------
> API Guide for Streamlink is at [https://streamlink.github.io/api_guide.html](https://streamlink.github.io/api_guide.html)

Open [fetchstreamsrc.py](https://github.com/PurdueCAM2Project/CAM2RetrieveData/blob/master/Retrieval/Streamlink/fetchstreamsrc.py).

Pass a webpage with a live stream to ```streamlink.streams()```
For example, see line 38 (```page_url``` might store something like "[https://www.youtube.com/watch?v=jlD3vw0LRSI](https://www.youtube.com/watch?v=jlD3vw0LRSI)"):
```
38: page_streams = streamlink.streams(page_url)
```

```page_streams``` is a Python dictionary.  The keys are the names of the streams (in the case of the YouTube page, they are named by resolution: ```'144p'```, ```'240p'```, ```'720p'```, etc.).  The corresponding values are ```Stream``` objects that store information about that stream.

We want to retrieve the source URL of the stream.  For sites like YouTube, Dailymotion, and Twitch, where multiple resolutions of the same stream is available, Streamlink automatically tags in extra entries to the library: ```'best'``` and ```'worst'```.  You can quickly fetch the ```.url``` property of ```Stream``` as seen in line 48:
```
48: src_url = page_streams['best'].url
```
You now have the source for the livestream, and you can pass it to a program like FFmpeg to collect frames.

### Exception Handling
> API reference on Streamlink exceptions is at [https://streamlink.github.io/api.html#exceptions](https://streamlink.github.io/api.html#exceptions)

Streamlink is a plugin-based tool. When it encounters sites it has no plugins for (or if the plugin fails), it may throw an exception.  When run on a Times Square [Earthcam](http://www.earthcam.com), Streamlink 0.6.0 throws a ```PluginError```.

The error's message looks something like this:
```
error: Unable to open URL: //video3.earthcam.com/fecnetwork/hdtimes10.flv/playlist.m3u8
(Invalid URL '//video3.earthcam.com/fecnetwork/hdtimes10.flv/playlist.m3u8': No schema supplied.
Perhaps you meant http:////video3.earthcam.com/fecnetwork/hdtimes10.flv/playlist.m3u8?)

```

Using simple regular expression parsing (lines 57-59), fetchstreamsrc.py can still retrieve a functional source URL.


More details
-------------------
* [Official Streamlink documentation](https://streamlink.github.io/)
* [Streamlink Github repo](https://github.com/streamlink/streamlink)
* [BSD 2-clause open-source license (Streamlink is licensed under this)](https://github.com/streamlink/streamlink/blob/master/LICENSE)
* [Livestreamer documentation (dead tool from which Streamlink was forked)](http://docs.livestreamer.io/)
