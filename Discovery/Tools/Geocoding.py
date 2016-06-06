###############################################################################
# Descriptive Name for File: Get Coordinates from Location
#
# Written by: Thomas Norling									      
# Contact Info: thomas.l.norling@gmail.com
#
# Command to Run Script: Should not be run from Command Line
# Other files required by this script and where located: None
#
# Description:
#   1. Import Class: from Geocoding import Geocoding
#   
#   2. Insantiate an instance of the class: 
#   variable = Geocoding(source, key)
#   source is either "Google" or "Nominatim" depending on which geocoder
#   you wish to use 
#   key is your Google API key or "None" if you don't have one
#
#   3. Call the function:
#   variable.locateCoords(locat, city, state, country)
#   locat is the street address, intersection, county, etc.
#   city is the city, if you don't have a city name: city = "" (the API will
#   fill it in for you) 
#   state is the 2 digit state code, if the country is not USA: state = ""
#   country is the 2 digit country code
#
#   4. To do the reverse (find city, state, country from coordinates):
#   Call the function: variable.reverse(latitude, longitude)
#
#   5. The info you need will be stored in the variables:
#   variable.city, variable.state, variable.country, variable.latitude,
#   variable.longitude
#   
#
#
# DO NOT PUT USERNAMES/PASSWORDS IN CODE
###############################################################################

import sys
import time
from geopy.geocoders import GoogleV3
from geopy.geocoders import Nominatim

class Geocoding:
    def __init__(self, source, key):
        if source == 'Google':
            self.geolocator = GoogleV3(api_key = key)
        if source == 'Nominatim':
            self.geolocator = Nominatim()
        self.latitude = ""
        self.longitude = ""
        self.city = ""
        self.state = ""
        self.country = ""

    def locateCoords(self, locat, city, state, country): 
        time.sleep(0.2)
        self.locat = locat
        self.city = city 
        self.state = state
        self.country = country
        self.latitude = ""
        self.longitude = ""

        try:
            searchTerm = str(self.locat + ',' + self.city + ',' + self.state + ',' + self.country) #Search for location, city, state (if there is one), and country
            searchTerm = searchTerm.replace(',,', ',')
            searchTerm = searchTerm.replace(',,', ',')
            location = self.geolocator.geocode(searchTerm)
        except:
            searchTerm = str(self.city + ',' + self.state + ',' + self.country) #Search for only city, state (if there is one) and country
            searchTerm = searchTerm.replace(',,', ',')
            searchTerm = searchTerm.replace(',,', ',')
            location = self.geolocator.geocode(searchTerm)

        self.latitude = str(location.latitude)
        self.longitude = str(location.longitude)

        if self.city == "":
            extractCity = location.raw['address_components'] #Get the raw JSON information so that the city name can be extracted
            for item in extractCity:
                types = item['types']
                if types[0] == "locality":
                    self.city = item['long_name']
        if self.city == "":
            raise Exception('City is a required field and City is currently empty!')

    def reverse(self, latitude, longitude):
        time.sleep(0.2)
        self.city = ""
        self.state = ""
        self.country = ""
        self.latitude = latitude
        self.longitude = longitude  
        
        searchTerm = str(latitude + ',' + longitude)
        location = self.geolocator.reverse(searchTerm)

        extractInfo = location.raw['address_components'] #Get the raw JSON information so that the city name can be extracted
        for item in extractInfo:
            types = item['types']
            if types[0] == "locality":
                self.city = item['long_name']
            if types[0] == "country":
                self.country = item['short_name']
        self.country = self.country.replace("US", "USA")

        if self.country == "USA":
            for item in extractInfo:
                types = item['types']
                if types[0] == "administrative_area_level_1":
                    self.state = item['short_name']
