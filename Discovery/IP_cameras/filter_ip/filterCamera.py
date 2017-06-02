"""
You must install selenium package to run this code
To be able to run pip  you must install python-pip
--------List of API requirement----------------
selenium
(sudo) pip install
		or
(sudo) easy_install 
--------------------------------------------------
To run in background, install python virtual display (not yet needed)
---------------------------------------------------
(sudo) apt-get install xvfb,xserver-xephyr,tightvncserver (dependencies)
(sudo) pip install pyvirtualdisplay
---------------------------------------------------
Selenium keeps waiting on page to be completely downloaded before locate element of the page
it will cause timeout problem. Install Pymouse to automatically stop page by clicking stop button on the
firefox using macro triggered by pymouse
---------------------------------------------------
(sudo) pip install pymouse
(sudo) apt-get install python-xlib(requirement)
---------------------------------------------------
(sudo) pip install python-uinput  (keyboard emulator)

---------End of API requirement--------------------

---------------------Usage-------------------------
sudo python filterCamera.py <list of possible Cams> <camera to be saved> <socket time out list>
ADMIN PERMISSION  since it send a key to system
log file (save last search line) must EXIST BEFORE EXCUTION
log file name should be "log"
place mouse cursor to stop button on firefox to properly function
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from pymouse import PyMouse
import uinput
#import xaut
#from pyvirtualdisplay import Display
import datetime
import sys
import random
import time
import socket
import httplib
import os
"""
Search terms
"""
def SearchTitle(title,browser,cameralist,candidate):
	
	if('camera' in title.lower()):
		cameralist.write(candidate+'\n')
		browser.save_screenshot(candidate+'.png')
		print "-------------------------Found @ " + candidate
		
	elif('MASTER' in title):
		cameralist.write(candidate+'\n')
		browser.save_screenshot(candidate+'.png')
		print "-------------------------Found @ " + candidate
		
	elif('image' in title.lower()):
		cameralist.write(candidate+'\n')
		browser.save_screenshot(candidate+'.png')
		print "-------------------------Found @ " + candidate
		
	elif(title.startswith('Starts')):
		cameralist.write(candidate+'\n')
		browser.save_screenshot(candidate+'.png')
		print "-------------------------Found @ " + candidate

"""
Main program
"""
candidates = open(sys.argv[1],'r')
cameralist = open(sys.argv[2],'a')
timeoutlist= open(sys.argv[3],'a')
outputlog = open(str(datetime.datetime.now()),'w') # file to store all the output from program
sys.stdout = outputlog #redirect output of python
log = open('log','r+') #load logfile
device = uinput.Device([uinput.KEY_ESC]) #Escape Key
size = PyMouse()
[xcoord,ycoord]=size.screen_size() #obtain screen size of the computer
browser = webdriver.Firefox() #get local session of Firefox
browser.maximize_window()#Maximize browser
browser.set_page_load_timeout(40) # set page load timeout as of 200 response
socket.setdefaulttimeout(30) # request time out set since selenium uses socket
count = 1
timeoutcounter = 0
lastsearch = int(log.readline())#last searched Line on file
print 'Last Search stopped @ '+str(lastsearch)+' line in '+sys.argv[1]
print 'Skipping lines to '+str(lastsearch)

for candidate in candidates:
	#go to the line to be continued
	if(count<lastsearch):
		count+=1
		continue
	else: #save last search to log
		log.seek(0)
		log.truncate()
		log.write(str(count)+'\n')
	#test if page requires HTTP Athentication
	candidate=candidate.rstrip('\n')
	addr = 'http://'+candidate
	print datetime.datetime.now()
	print str(count) +' : '+addr
	print str(count)+" : Httplib status pre-check"

	#Pre- response check to prevent popup from system such as Authentication required popup

	try:
		conn = httplib.HTTPConnection(candidate)
		conn.request('HEAD','/') #just send a HTTP Head
		res = conn.getresponse().status
		print str(count)+" : Httplib Pre check result:			"+ str(res)
	except Exception as e:
		print e
		res = 401 # if exception raised go to next candidate
	finally:
		conn.close()
	if(int(res)==401): #add 400 if you want to fast scanning
		print str(count)+" : Authentication Required or Bad request Continue to next candidate"
		count+=1
		continue	
	
	#Load page to analyze
	try:
		count +=1
		browser.get(addr) #navigate web
		final_url = browser.current_url
	except Exception as e: #unexcpected exception handle such as popups,dialouge
		print e
		final_url = 'None'
		if 'timed' in str(e):
			timeoutcounter+=1
			timeoutlist.write(candidate+'\n')
			size.click(xcoord/2,ycoord/2,1)  #click middle of the screen (where athentication dialog appears)
			device.emit_click(uinput.KEY_ESC) # send ESC key
			time.sleep(1) #wait


	finally:
###############################################################################Close JavaScript Level Alert box

		try:#Try to handle alert box if exists(javascript level)
			alert=browser.switch_to_alert()
			alert.dismiss()
		except Exception as e:
			print str(count-1)+" : No JavaScript Alert Box"

###############################################################################Try to search camera through title
		try:#Try to analyze the title even though page load exception is set
			#it will search title outside of <head></head><title></title>
			print str(count-1)+' : Try to catch title'
			wait = WebDriverWait(browser,2) #wait only 2 seconds to find title
			wait.until(lambda browser: browser.title)
			title = str(browser.title)
			SearchTitle(title,browser,cameralist,candidate)
		except Exception as e: #timeout exception handle
			print str(count-1)+" : No result from outer title"
			#try to search title between the <head><title></title><head>  
			try:
				title = str(browser.find_element_by_xpath("//head/title").get_attribute("textContent").encode('utf-8','ignore'))
				SearchTitle(title,browser,cameralist,candidate)
				
			except Exception as e:
				print e
				print str(count-1)+" : No result from inner title"
			#search for D-link Camera
			if('top.htm' in final_url):
				browser.save_screenshot(candidate+'.png')
				cameralist.write(candidate+'\n')
				print "-------------------------Found @ " + candidate
		finally:

#############################################################################close and re open files
			cameralist.close()
			timeoutlist.close()
			cameralist = open(sys.argv[2],'a')
			timeoutlist= open(sys.argv[3],'a')
############################################################################# Wait time setting between page
			wait =6
################################################################################ Pop-up check

			try:	
				pop_up_number = len(browser.window_handles) #check how many
				print str(count-1)+" : # of Pop ups :			  "+str(pop_up_number)
				while(pop_up_number>1): #close all the popups
					browser.switch_to_window(browser.window_handles[pop_up_number-1])#switch to pop ups
					time.sleep(1)
					try:
						alert=browser.switch_to_alert()
						alert.dismiss()
					except Exception as e:
						print str(count-1)+" : No Alert box in pop up"
					finally:
						try:
							browser.close() #close
							pop_up_number-=1 #move index
						except Exception as e:
							print e
							#print 'Switchong failed'
							browser.switch_to_window(browser.window_handles[pop_up_number-1])
				browser.switch_to_window(browser.window_handles[0])
			except Exception as e:
				print e
				browser.switch_to_window(browser.window_handles[0])

############################################################################ Reset webdriver to release resource or solve timeout problem

			if(count%1000==0 or timeoutcounter>3): #close and reopen to reduce timeout
				timeoutcounter=0
				try:
					browser.close()
					browser = webdriver.Firefox() #get local session of Firefox
					browser.maximize_window()
					browser.set_page_load_timeout(40) # set page load timeout as of 200 response
				except Exception as e: #if fail, force to close
					print "Reset Browser failed - Force Syetem to Kill"
					print e
					size.click(xcoord/2,ycoord/2,1)  #try to click athentication box and send ESC to remove
					device.emit_click(uinput.KEY_ESC)
					os.system("killall -9 firefox")
					print "Settle down for 5 seconds"
					time.sleep(5)
					browser = webdriver.Firefox() #get local session of Firefox
					browser.maximize_window()
					browser.set_page_load_timeout(40)
			print 'Wait for '+str(wait)+' seconds'
			time.sleep(wait) # wait for next candidates


log.close()
outputlog.close()
timeoutlist.close()
cameralist.close()
candidates.close()
browser.close()



		

		
