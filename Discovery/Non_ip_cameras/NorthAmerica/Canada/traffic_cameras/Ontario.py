""" 
--------------------------------------------------------------------------------
Descriptive Name     : Ontario.py
Author               : Subhav Ramachandran								      
Contact Info         : subhav@purdue.edu
Date                 : May 28, 2014 11:36:16 AM
Description          : Parse cameras on the Ontario Ministry of Transportation traffic camera website
Command to run script: python Ontario.py <outputfile_name>
Output               : output urls, country, city and latitude, longitude to a 
                       textfile <outputfile_name>
Other files required by : N/A
this script and where 
located
----For Parsing Scripts---------------------------------------------------------
Website 	     : http://www.mto.gov.on.ca/english/traveller/trip/traffic_cameras_list.shtml
URL Parsed	     : http://www.mto.gov.on.ca/english/traveller/compass/camera/camData.xml
In database (Y/N)    : Y
--------------------------------------------------------------------------------

The name of the traffic reporting system they use is COMPASS.

Data is taken from the following document:
    http://www.mto.gov.on.ca/english/traveller/compass/camera/camData.xml
which is expected to be of the following form::

    <mapInfo>
        <!-- Existing Camera Locations in Toronto -->
        <mapArea   areaDesc="GTA" lat="43.741169984847446" lng="-79.42590809499603" zoomLevel="11">
            <marker
                    lat="43.852169"
                    lng="-79.022083"
                    fullDesc="Highway 401 near Harwood Avenue"
                    shortDesc="401 near Harwood Ave"
                    icon="http://www.cdn.mto.gov.on.ca/english/traveller/compass/camera/CCTV_Active.gif"
                    imgURL="http://www.cdn.mto.gov.on.ca/english/traveller/compass/camera/pictures/loc103.jpg"
                    topImg="http://www.cdn.mto.gov.on.ca/english/traveller/compass/camera/pictures/ReferencePictures/TopPictures/loc103.jpg"
                    topTxt="Looking East"
                    bottomImg="http://www.cdn.mto.gov.on.ca/english/traveller/compass/camera/pictures/ReferencePictures/BottomPictures/loc103.jpg"
                    bottomTxt="Looking West"
                    provideImg="http://www.cdn.mto.gov.on.ca/english/traveller/compass/camera/pictures/ReferencePictures/logo-compass-66x20.gif"
                    provideTxt="Images provided by:"
            />
            ...
        </mapArea>
        ...
    </mapInfo>

This document is used to populate data on the Google Map located here:
    http://www.mto.gov.on.ca/english/traveller/compass/camera/camhome1.shtml

A simple list of available cameras can be found at:
    http://www.mto.gov.on.ca/english/traveller/trip/traffic_cameras_list.shtml

"""
import sys
from xml.dom import minidom
import urllib2

def getON(outfile):
	"""Gets traffic camera information from Ontario.

	There are also static images available pointing in opposite directions
	which can be used to determine which direction the camera is facing.
	We are NOT currently collecting this information, though it can be done
	easily if ever necessary.

	It gathers information from an XML file (`url`) which is used to send
	camera data to the browser, to be displayed in a map. (More information
	about this in the module documentation.)

	Camera information is output to the file `outfile` in the format::
		<imageURL>#<latitude>#<longitude>#Canada#Ontario#<city or area>#<street or intersection>
	with one line representing each camera.
	"""

	url = 'http://www.mto.gov.on.ca/english/traveller/compass/camera/camData.xml'

	# A string containing the entire XML document.
	xml_string = urllib2.urlopen(url).read()

	# Object model of the XML document (of type Document).
	document = minidom.parseString(xml_string)

	outfile_handle = open(outfile, 'w')

	# Each area (or city) is represented by a `mapArea` element.
	for area_element in document.getElementsByTagName("mapArea"):

		area = area_element.getAttribute("areaDesc")

		# Expand the area abbreviations
		if area == "GTA":
			area = "Greater Toronto Area"
		if area == "1000Islands":
			area = "Thousand Islands"

		# Each camera is represented by a (self-closing) `marker` element.
		for camera_element in area_element.getElementsByTagName("marker"):
			latitude = camera_element.getAttribute("lat")
			longitude = camera_element.getAttribute("lng")
			description = camera_element.getAttribute("fullDesc")

			image_url = camera_element.getAttribute("imgURL")

			outfile_handle.write("%s#%s#%s#Canada#Ontario#%s#%s\n" %
					(image_url, latitude, longitude, area, description))

	outfile_handle.close()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "usage: getON.py <output file>"
		sys.exit(1)
	else:
		getON(sys.argv[1])
