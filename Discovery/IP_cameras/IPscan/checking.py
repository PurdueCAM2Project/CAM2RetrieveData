from __future__ import print_function

import glob
import os
import sys
import re

def main(args):
    path = "/home/sara/BigData/camera/IP_cameras/IPscan/results"
    os.chdir(path)
    f = open("../IPAddress_Is_Camera.txt", "w")
    folders = os.listdir(path) #Dirs give ip addresses
    #print (folders)

    for roots, dirs, files in os.walk('.'):
        if files:
            print (roots,'has image')
            ipaddr = re.findall(r'\d+',roots)
            output = ".".join(str(x) for x in ipaddr)
            #print(output)
            f.write(output + '\n')
        else:
            print (roots, 'does not have image.')

    f.close()

if __name__ == '__main__':
    main(sys.argv)