from bs4 import BeautifulSoup
import urllib2
import time
import re
def getCameras():
	URL="http://camelive.info/index/index/offset/"
	offset = 0
	limit = 8072 #total number of  camera shown in the pages.
	out = open("camlive.list",'a')
	while offset <limit:
		link_count =0
		req = urllib2.Request(URL+str(offset))
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36')
		source = urllib2.urlopen(req)
		bs = BeautifulSoup(source.read())
		links = bs.find_all('span',{'style':'color: darkgreen; font-weight: bold;'}) #Extract green link on the pages
		information = bs.find_all('div',{'style':'font-size: 11px;'}) #collect all info (View count,location,brand,geolocation)
		offset = offset+len(links)
		for link_count in range(0,len(links)):
			#if it is not ip camera
			if "jpeg" in information[link_count].get_text().encode("utf-8").split("\n")[4].split('/')[0].lower():
				continue
			out.write(links[link_count].get_text().encode('utf-8')+'#')
			out.write(information[link_count].get_text().encode("utf-8").split("\n")[3]+'#') #location
			out.write(information[link_count].get_text().encode("utf-8").split("\n")[4].split('/')[0]+'#')	#brand
			out.write(information[link_count].get_text().encode("utf-8").split("\n")[5].split("/")[0].split(" ")[1]+'#') #lat
			out.write(information[link_count].get_text().encode("utf-8").split("\n")[5].split("/")[1].split(" ")[2]+'\n') #long
		
		time.sleep(10)
	out.close()
getCameras()




