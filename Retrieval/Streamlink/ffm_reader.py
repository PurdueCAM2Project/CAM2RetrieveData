import subprocess
#import ffmpy
import sys, os
import time

fileName = "TW-FFMPEG.txt"
time_start = time.time();
i = 0
with open(fileName,"r") as fp:
    for line in fp:
        i = i + 1
        line = fp.readline()
        print(line)
        print("ffmpeg -i " + line.rstrip() + " -t 5 taiwan_images.png")
        subprocess.call("ffmpeg -i " + line.rstrip() + " -vf fps=1 -framerate 1 -t 5 taiwan_images" + str(i) + "%d.png", shell=True)

time_cur = time.time()

print(time_cur - time_start)
