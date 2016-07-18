"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for cameras in WorldCamera website
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 30 June 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python WorldCameras.py
Usage                : N/A
Input file format    : N/A
Output               : list_WorldCamera_Other.txt list_WorldCamera_US.txt
Note                 : This website contains a lot of cameras all over the world.
                        For this reason, it has two output files, one for US and the other for non-US countries.
Other files required by : It requires Selenium and BeautifulSoup4 to be installed.
                            It also requires to install pycountry
this script and where
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://www.meteosurfcanarias.com/en/webcams
In database (Y/N)    : Y
Date added to Database : 30 June 2016
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
