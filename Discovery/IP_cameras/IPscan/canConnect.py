#!/usr/bin/python
# 
# check whether connection is allowed to an IP address and a port
#
import httplib
import re

def isOn(address, port):
    # print "address=" + address + "port=" + port + "*"
    try: 
        conn = httplib.HTTPConnection(address, port, timeout = 5)
        conn.request("GET", "/")
    except Exception:
        # print "exception HTTPConnect"
        return 0
    try: 
        resp = conn.getresponse()
    except Exception:
        # print "exception getresponse"
        return 0
    if (resp.status != 200): # not HTTP OK
        # print "status not 200: " + str(resp.status)
        return 0
    return 1

    # check whether the response contains the word "camera"
    # this does not work because we cannot handle javascript
    """
    data = resp.read()
    data = data.lower()
    print data
    mch = re.search("camera", data)
    if mch: 
       return 1
    return 0
    """
