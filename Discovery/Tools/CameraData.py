"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for cameras in WorldCamera website
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 30 June 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: N/A
Usage                : N/A
Input file format    : N/A
Output               : N/A
Note                 : This class creates an instance that contains img_src, country, state, city, and description as instance variables variables
Other files required by : N/A
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : N/A
In database (Y/N)    : N/A
Date added to Database : N/A
--------------------------------------------------------------------------------
"""
class CameraData:
    def __init__(self, img_src, country, state, city, description):
        self.img_src        = img_src
        self.country        = country
        self.state          = state
        self.city           = city
        self.description    = description

    def get_img_src(self):
        return self.img_src

    def get_country(self):
        return self.country

    def get_state(self):
        return self.state

    def get_city(self):
        return self.city

    def get_description(self):
        return self.description
