""" 
--------------------------------------------------------------------------------
Descriptive Name     : Clean.py
Author               : Thomas Norling								      
Contact Info         : thomas.l.norling@gmail.com
Date Written         : June 9, 2016
Description          : Cleans up location data. Can either call functions on their
                       own or call the suite which will clean the location information
                       with every function contained in this class.
                       1. Import Class: from Clean import Clean

                       2. Instatiate an instance of the class: variable = Clean(loc)
                       where loc is the string you would like to clean
  
                       3. Call the function you would like to use:
                       e.g. variable.suite()

Command to run script: N/A
Usage                : Must be imported into another script
Input file format    : N/A
Output               : N/A
Note                 : 
Other files required by : N/A
this script and where 
located
--------------------------------------------------------------------------------
"""

import re

class Clean:
    def __init__(self, textString):
        self.textString = textString

    def remove_Whitespace(self):
        self.textString = self.textString.replace('\n', '')
        self.textString = re.sub(r"\s+", " ", self.textString)
        self.textString = self.textString.strip()
    
    def remove_direction(self):
        self.textString = self.textString.replace("North of", "")
        self.textString = self.textString.replace("South of", "")
        self.textString = self.textString.replace("East of", "")
        self.textString = self.textString.replace("West of", "")
        self.textString = self.textString.replace("north of", "")
        self.textString = self.textString.replace("south of", "")
        self.textString = self.textString.replace("east of", "")
        self.textString = self.textString.replace("west of", "")
        self.textString = self.textString.replace("N of", "")
        self.textString = self.textString.replace("S of", "")
        self.textString = self.textString.replace("E of", "")
        self.textString = self.textString.replace("W of", "")
        self.textString = self.textString.replace("North Bound", "")
        self.textString = self.textString.replace("South Bound", "")
        self.textString = self.textString.replace("West Bound", "")
        self.textString = self.textString.replace("East Bound", "")
        self.textString = self.textString.replace("NB", "")
        self.textString = self.textString.replace("SB", "")
        self.textString = self.textString.replace("WB", "")
        self.textString = self.textString.replace("EB", "")
        self.textString = self.textString.replace("Inbound", "")
        self.textString = self.textString.replace("IB", "")
        self.textString = self.textString.replace("Outbound", "")
        self.textString = self.textString.replace("OB", "")
        self.textString = self.textString.replace("Onramp", "")
        self.textString = self.textString.replace("onramp", "")
        self.textString = self.textString.replace("on Ramp", "")
        self.textString = self.textString.replace("on-ramp", "")
        self.textString = self.textString.replace("On-ramp", "")
        self.textString = self.textString.replace("On-Ramp", "")
        self.textString = self.textString.replace("Offramp", "")
        self.textString = self.textString.replace("offramp", "")
        self.textString = self.textString.replace("off Ramp", "")
        self.textString = self.textString.replace("off-ramp", "")
        self.textString = self.textString.replace("Off-ramp", "")
        self.textString = self.textString.replace("Off-Ramp", "")
        self.textString = self.textString.replace("Before", "")
        self.textString = self.textString.replace("before", "")
        self.textString = self.textString.replace("After", "")
        self.textString = self.textString.replace("after", "")
        self.textString = self.textString.replace("Around", "")
        self.textString = self.textString.replace("around", "")
        self.textString = self.textString.replace("Behind", "")
        self.textString = self.textString.replace("behind", "")
        self.textString = self.textString.replace("Near", "")
        self.textString = self.textString.replace("near", "")
        self.textString = re.sub(r"(^|\s)in\s", "", self.textString)
        self.textString = re.sub(r"(^|\s)In\s", "", self.textString)
        self.textString = self.textString.replace("Opposite", "")
        self.textString = self.textString.replace("opposite", "")
        self.textString = self.textString.replace("Interchange", "")
        self.textString = self.textString.replace("interchange", "")
        self.textString = self.textString.replace("Intersection", "")
        self.textString = self.textString.replace("intersection", "")
        self.textString = self.textString.replace("Ramps", "")
        self.textString = self.textString.replace("ramps", "")
        self.textString = self.textString.replace("Ramp", "")
        self.textString = self.textString.replace("ramp", "")
        self.textString = self.textString.replace("Jct", "")
        self.textString = self.textString.replace("JCT", "")

    def remove_repeating(self):
        self.textString = re.sub(r"\.{2,}", ".", self.textString)
        self.textString = re.sub(r"\,{2,}", ",", self.textString)
        self.textString = re.sub(r"\#{2,}", "#", self.textString)

    def remove_bad_char(self):
        self.textString = self.textString.replace('(', '')
        self.textString = self.textString.replace(')', '')
        self.textString = self.textString.replace('[', '')
        self.textString = self.textString.replace(']', '')
        self.textString = self.textString.replace('{', '')
        self.textString = self.textString.replace('}', '')
        self.textString = self.textString.replace('<', '')
        self.textString = self.textString.replace('>', '')
        self.textString = self.textString.replace('^', '')
        self.textString = self.textString.replace(':', '')

    def replace_at_with_and(self):
        self.textString = self.textString.replace('@', 'and')
        self.textString = re.sub(r"\sat\s", " and ", self.textString)

    def remove_mileposts(self):
        self.textString = re.sub(r"MP\s[0-9]+\.[0-9]+", "", self.textString)
        self.textString = re.sub(r"MP\:\s[0-9]+\.[0-9]+", "", self.textString)
        self.textString = re.sub(r"Milepost\s[0-9]+\.[0-9]+", "", self.textString)
        self.textString = re.sub(r"MP\s[0-9]+", "", self.textString)
        self.textString = re.sub(r"MP\:\s[0-9]+", "", self.textString)
        self.textString = re.sub(r"Milepost\s[0-9]+", "", self.textString)
        self.textString = re.sub(r"MP[0-9]+\.[0-9]+", "", self.textString)
        self.textString = re.sub(r"MP\:[0-9]+\.[0-9]+", "", self.textString)
        self.textString = re.sub(r"MP[0-9]+", "", self.textString)
        self.textString = re.sub(r"MP\:[0-9]+", "", self.textString)
        self.textString = re.sub(r"[0-9]+\smiles{0,1}", "", self.textString)
        self.textString = re.sub(r"[0-9]+\sMiles{0,1}", "", self.textString)

    def remove_exits(self):
        self.textString = re.sub(r"Exit\s[0-9]+", "", self.textString)
        self.textString = re.sub(r"Exit[0-9]+", "", self.textString)
        self.textString = re.sub(r"exit\s[0-9]+", "", self.textString)
        self.textString = re.sub(r"exit[0-9]+", "", self.textString)
        self.textString = re.sub(r"\sexit\s", "", self.textString)
        self.textString = re.sub(r"\sExit\s", "", self.textString)

    def remove_begin_end_words(self):
        self.textString = re.sub(r"\sand$", "", self.textString)
        self.textString = re.sub(r"^and\s", "", self.textString)
        self.textString = re.sub(r"\sat$", "", self.textString)
        self.textString = re.sub(r"^at\s", "", self.textString)

    def suite(self):
        self.remove_direction()
        self.remove_mileposts()
        self.remove_exits()
        self.remove_bad_char()
        self.replace_at_with_and()
        self.remove_repeating()
        self.remove_Whitespace()
        self.remove_begin_end_words()

