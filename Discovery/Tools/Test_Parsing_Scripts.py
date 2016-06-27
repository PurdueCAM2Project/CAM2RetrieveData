""" 
--------------------------------------------------------------------------------
Descriptive Name     : Test_Parsing_Scripts.py
Author               : Thomas Norling								      
Contact Info         : tnorling@purdue.edu
Date Written         : June 21, 2016
Description          : Test parsing scripts to ensure they run without error and 
                       the text file outputted is formatted correctly and cameras
                       were successfully parsed.
Command to run script: python Test_Parsing_Scripts.py (Followed by any number of 
                       scripts you would like to test separated by spaces)
Usage                : N/A
Input file format    : .py file or .txt file with names of .py files on separate lines
Output               : TestOutput.txt
Note                 : Check the usage of the scripts you are trying to test. If the
                       scripts won't run on their own on certain machines, they 
                       will fail when run through this script as well.
                       Also the output text file name for all parsing scripts should
                       be list_(Name of parsing script without '.py').txt
                       For example if your parsing script is NY.py the output text
                       file should be list_NY.txt
Other files required by : N/A
this script and where 
located

--------------------------------------------------------------------------------
"""

import sys
import time
import subprocess
import re
import os
import signal

class Testing:
    def __init__(self):
        self.scriptsToTest = sys.argv
        self.testOutput = open('testOutput.txt', 'w')
        self.scriptSuccess = []
        self.scriptFailure = []

    def testRunWithoutError(self):
        DEVNULL = open(os.devnull, 'w')
        self.testOutput.write("Output results for: " + str(self.scriptsToTest[1:]) + "\n")
        count = 0
        for item in self.scriptsToTest:
            if (count == 0) or (item == "Test_Parsing_Scripts.py") or (re.search(r".txt", item)):
                if re.search(r".txt", item):
                    argFile = open(item, 'r')
                    for line in argFile.readlines():
                        line = line.replace("\n", "")
                        self.scriptsToTest.append(line)
                    argFile.close()
            else:
                print "Testing: " + item
                errorFile = open('errorFile.txt', 'w')
                self.testOutput.write("\nScript: " + item + "\n")
                p = subprocess.Popen('python ' + item, stdout=DEVNULL, stderr=errorFile, preexec_fn=os.setsid, shell=True)
                p.wait()
                try:
                    os.killpg(p.pid, signal.SIGTERM)
                except:
                    pass
                errorFile.close()
                errorFile = open('errorFile.txt', 'r')
                err = errorFile.readlines()
                errorFile.close()
                time.sleep(1)
                
                if p.returncode == 0:
                    self.testOutput.write(item + " ran without error\n")                  
                    self.testOutputFile(item)
                    if item not in self.scriptFailure:
                        self.scriptSuccess.append(item)
                else:
                    self.testOutput.write(item + " failed to run. Please try debugging this script and try again. Error message is located below:\n\n")
                    self.testOutput.write(''.join(err))
                    self.scriptFailure.append(item)
            count += 1
        DEVNULL.close()
        os.remove('errorFile.txt')
        
    def testOutputFile(self, inputfile):
        print "Testing output file of: " + inputfile
        filename = "list_" + inputfile.split('.')[0] + ".txt"
        self.testOutput.write("\nOutput file: " + filename + "\n")
        try:
            with open(filename) as outFile:
                lines = list(outFile)
        except:
            self.testOutput.write("No output file found. Please ensure the parsing script outputs a file with the correct filename\n")
            self.testOutput.write(inputfile + " should output a file with the name: " + filename + "\n")
        else:
            numLines = len(lines)
            if numLines <= 1:
                error = 1
                self.testOutput.write(inputfile + " did not parse any cameras. Please fix your parsing script and try again.\n")
            else:
                error = 0
                self.testOutput.write(inputfile + " parsed " + str((numLines - 1)) + " cameras\n")

            if error == 0:
                header = lines[0]
                header = header.strip()
                header = header.split('#')
                numHeadFields = len(header)

                if "country" in header:
                    pass
                else:
                    error = 1
                    self.testOutput.write(filename + " does not contain required elements. Please ensure header contains 'country' and that fields are separated by '#'\n")
                if "city" in header:
                    pass
                else:
                    error = 1
                    self.testOutput.write(filename + " does not contain required elements. Please ensure header contains 'city' and that fields are separated by '#'\n")
                if "snapshot_url" in header:
                    pass
                else:
                    error = 1
                    self.testOutput.write(filename + " does not contain required elements. Please ensure header contains 'snapshot_url' and that fields are separated by '#'\n")
                if "latitude" in header:
                    pass
                else:
                    error = 1
                    self.testOutput.write(filename + " does not contain required elements. Please ensure header contains 'latitude' and that fields are separated by '#'\n")
                if "longitude" in header:
                    pass
                else:
                    error = 1
                    self.testOutput.write(filename + " does not contain required elements. Please ensure header contains 'longitude' and that fields are separated by '#'\n")

                first_line = lines[1]
                first_line = first_line.split('#')
                if "USA" in first_line:
                    if "state" in header:
                        pass
                    else:
                        error = 1
                        self.testOutput.write(filename + " does not contain required elements. Please ensure header contains 'state' if country is USA\n")

                if error == 0:
                    lineNum = 0
                    for camera in lines:
                        camera = camera.split('#')
                        numFields = len(camera)
                        if numFields == numHeadFields:
                            pass
                        else:
                            error = 1
                            self.testOutput.write("Line " + str(lineNum) + " does not have the same number of fields as the header. Please ensure camera data matches the header.\n")
                        lineNum += 1
                
                if error == 0:
                    self.testOutput.write(filename + " contains all required elements and the header is formatted correctly.\n")
                else:
                    self.scriptFailure.append(inputfile)

    def askDelete(self):
        delete = raw_input("\nWould you like to delete output text files from the parsing scripts? (y/n): ")
        if delete == "y" or delete == "Y":
            for file in self.scriptsToTest[1:]:
                file = file.split('.')[0]
                filename = "list_" + file + ".txt"
                try:
                    os.remove(filename)
                except:
                    print "Could not remove: " + filename

        print "Done. Please check testOutput.txt for more detailed information."

    def SuccessFailure(self):
        print "\nThe following files parsed successfully: " + ', '.join(self.scriptSuccess)
        print "The following files had one or more errors: " + ', '.join(self.scriptFailure)
        print "Check testOutput.txt for more details"

        self.testOutput.write("\nThe following files parsed successfully: " + ', '.join(self.scriptSuccess))
        self.testOutput.write("\nThe following files had one or more errors: " + ', '.join(self.scriptFailure))          

if __name__ == '__main__':
    test = Testing()
    test.testRunWithoutError()
    test.SuccessFailure()
    test.askDelete()
