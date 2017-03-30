from subprocess import Popen,PIPE,STDOUT
import os
import csv

if(os.path.isfile("rtmpstreams.csv")): #check if files exists

        csv_handle = open('rtmpstreams.csv', 'rb')
        myreader = csv.reader(csv_handle,delimiter=",")
	rtmps=[]
        urls=[]
        swfs=[]
	outputfiles=[]
	durations=[]
	flvnames=[]
	k = 0;
        #get required info
        for row in myreader:
	    rtmps.append(row[0])
	    urls.append(row[1])
	    swfs.append(row[2])
	    flvnames.append(row[3])
            outputfiles.append(row[4])
	    durations.append(row[5])
        del urls[0]
	del outputfiles[0]
	del swfs[0]
	del durations[0]
	del flvnames[0]
	del rtmps[0]
	#run commands in bash 1 by 1
	for i in range(len(urls)):
		print "start"

		shell_command='rtmpdump -r '+rtmps[i]+' -p "'+ urls[i] + '" -s "' + swfs[i] + '" -v -y '+ flvnames[i]+'.flv -R -o - | ffmpeg -i pipe:0 -t '+durations[i]+' '+ outputfiles[i]+'.avi'
		print shell_command
		event=Popen(shell_command,shell=True)
		(output,err)=event.communicate()

		print "end"


else:#if file does not exist
    try:
       option = raw_input("File rtmpstreams.csv does not exist. Would you like to create it?(Yes/No) ")
       if option == 'Yes' or option =="yes":
      
            # open a file
            csv_handle = open('rtmpstreams.csv', 'wb')

            mywriter = csv.writer(csv_handle)
            mywriter.writerow(["RTMP STREAMS","URLS","SWF streams","FLV names","Output filename (no extension)","Duration"])

            #close file
            csv_handle.close()
       else:
            print "Closing program"
    except():
        print "Unable to create file"
        csv_handle.close()





