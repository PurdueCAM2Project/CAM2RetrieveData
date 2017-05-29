About the program: 
  
This program takes a CSV file as input with necessary fields filled in and extracts images from the given link to Youtube video and saves it in a new folder. The program has three flags which can be used to pass in command line arguments.

___________________________________________________________________________________________________________________________________

Input CSV File:

FOLDER NAME	DURATION(S)	OUTPUT FORMAT	OUTPUT NAME	LINK

1. FOLDER NAME:   Name of the folder to which the user wants to save the images to. If the folder does not exist, the program would 		      create a new folder.

2. DURATION:	  The interval of the video in seconds.

3. OUTPUT FORMAT: The output format of the images to download (jpeg/bmp/etc)

4. OUTPUT NAME:   Image names
		  If the output name is "scene" and the output format is "bmp"
		  The the stored images would be: "scene01.bmp", "scene02.bmp", ...
		  
5. LINK:	  URL of the Youtube video to download.
	
Flags: (Command line arguments)
  
  -f = "Name of CSV file containing info with .csv extension (should be in same directory as program)"
  -n = "Takes a string to create new csv file (must have .csv extension)"
  -c = "Yes to create new file is file with filename does not exist"
  
  
