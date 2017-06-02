#!/usr/bin/python

def out(fptr, tag, data):
   fptr.write("   <" + tag + ">\n")
   fptr.write("      " + data + "\n")
   fptr.write("   </" + tag + ">\n")
