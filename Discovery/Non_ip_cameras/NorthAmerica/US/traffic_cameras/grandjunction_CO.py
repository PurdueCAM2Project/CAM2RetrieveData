from bs4 import BeautifulSoup
import urllib2
import sys
import saveImage
def grandjunction():
	if len(sys.argv) ==1:
		print 'xml to make list file'
		print 'download to download image based on list file'
		print 'xml first and run download'
		return
	if(sys.argv[1]=='xml'):
		FIRSTPAGE = 'http://publicweb-fs.ci.grandjct.co.us/e-net/PublicWorks/TrafficCam/I70BAnd25Road.asp'
		BASE_URL  ='http://publicweb-fs.ci.grandjct.co.us/e-net/PublicWorks/TrafficCam/'
		IMG_URL = 'http://publicweb-fs.ci.grandjct.co.us'
		f = open('grandjct.list','w')
		req = urllib2.Request(FIRSTPAGE)
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36')
		source = urllib2.urlopen(req)
		bs = BeautifulSoup(source.read())
		links = bs.find_all('td',{'height':'25'})
		#above is pre-process for extract camera pages
		#below is to extract all the image path

		for link in links:
			#check if it has "a href" component
			if link.a is not None:
				url2cam= BASE_URL+link.a['href'] #extract all the possible link and visit all page since each page has 4 cameras 
				req = urllib2.Request(url2cam)
				req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36')
				source = urllib2.urlopen(req)
				bs = BeautifulSoup(source.read())
				img_links = bs.find_all('img',{'border':'2'})
				for img_link in img_links:
					f.write(IMG_URL+img_link['src']+'\n')

	elif(sys.argv[1] =='download'):
		f = open('grandjct.list','r')
		for line in f:
			file_name = line.split('/')[6].split('\n')[0]
			imgurl =line.split('\n')[0]
			saveImage.saveImage(imgurl,file_name)


			


grandjunction()