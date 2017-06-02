# need to have HTML parser , called BeautifulSoup


from bs4 import BeautifulSoup
import fetchHTML
import re
import sys
import time
import urllib2

def Opentopia():
	BASE_URL_TOTAL_NUM = "http://www.opentopia.com/hiddencam.php"
	BASE_URL = "http://www.opentopia.com/webcam/"
	EXTENSION_1 = "?viewmode=livestill"
	EXTENSION_2 = "?viewmode=livevideo"
	

	""" removed since it counts duplicates
	#Parse total number
	html = fetchHTML.fetchHTML(BASE_URL_TOTAL_NUM)
	source = BeautifulSoup(html)
	numbers = source.find_all('option')
	total = 0
	for number in numbers:
		try:
			temp = int(number.string[number.string.index("(") + 1:number.string.rindex(")")])
			if temp>1000:
				us = temp
		except:
			temp = 0;
		finally:
			total+=temp

	
	print str(total) +' will be searched'

	"""
	
	total = 2186
	n =1  #index
	fptr = open(sys.argv[1],'w')
	url = BASE_URL+str(n)+EXTENSION_1
	#Parse camera data
	while(n <20000):
		try:
			html = fetchHTML.fetchHTML(url)
			if html is None:
				n = n+1;
				url = BASE_URL+str(n)+EXTENSION_1
				continue
			source = BeautifulSoup(html)
			addr = source.find('div', attrs={'class':'big'}).img.get('src')
			invalid = source.find('div',style='color:#f00')
			#if there is no invalid message and no "not available" screen on  img addr
			
			if (invalid is None) and not('nosnapshot' in addr)and not('opentopia'in addr):
				fptr.write(addr+'#')
				caminfos = source.find('div',attrs={'class':'caminfo'})
				hasGeoinfo = False
				for caminfo in caminfos:
					if('Facility' in str(caminfo)):
						fptr.write(str(caminfo.find('label',attrs={'class':'right'}).contents[0].encode('utf-8'))+'#')
						print str(caminfo.find('label',attrs={'class':'right'}).contents[0])
					elif('State/Region' in str(caminfo)):
						fptr.write(str(caminfo.find('label',attrs={'class':'right region'}).contents[0].encode('utf-8'))+'#')
						print str(caminfo.find('label',attrs={'class':'right region'}).contents[0])
					elif('City:' in str(caminfo)):
						fptr.write(str(caminfo.find('label',attrs={'class':'right locality'}).contents[0].encode('utf-8'))+'#')
						print str(caminfo.find('label',attrs={'class':'right locality'}).contents[0])
					elif('Country:' in str(caminfo)):
						fptr.write(str(caminfo.find('label',attrs={'class':'right country-name'}).contents[0].encode('utf-8'))+'#')
						print str(caminfo.find('label',attrs={'class':'right country-name'}).contents[0])
					elif('Brand:' in str(caminfo)):
						fptr.write(str(caminfo.find('label',attrs={'class':'right'}).contents[0].encode('utf-8'))+'#') 
						print str(caminfo.find('label',attrs={'class':'right'}).contents[0])
					if('Coordinates' in str(caminfo)):
						hasGeoinfo = True
						latitude = str(caminfo.find('span',attrs={'class':'latitude'}).contents[0])
						print str(caminfo.find('span',attrs={'class':'latitude'}).contents[0])
						longitude = str(caminfo.find('span',attrs={'class':'longitude'}).contents[0])
						print str(caminfo.find('span',attrs={'class':'longitude'}).contents[0])

				if hasGeoinfo:
					fptr.write(latitude+'#')
					fptr.write(longitude)
				else:
					fptr.write('none#none')
				fptr.write('\n')
				total -=1
				print "camid : "+str(n)+"  Found @ "+addr
			#if it there is not invalid message and contains opentopia.com in img addr
			#try other route
			elif(invalid is None) and ('opentopia' in addr):
				url = BASE_URL+str(n)+EXTENSION_2
				continue
			elif(invalid is not None):
				print str(n)+' : invalid'	
			
		except Exception as e:
			print e
			addr = 'None'
			if(source.find('div', attrs={'class':'big'}).img is None):
				n-=1;
		n +=1
		url = BASE_URL+str(n)+EXTENSION_1
		print "remaining : "+str(total)+'  '+url	
		#
		
	fptr.close()
Opentopia();