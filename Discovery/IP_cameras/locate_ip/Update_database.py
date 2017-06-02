import MySQLdb
import urllib2
import json
import re
import sys

def Update_inf():
        # open db connection
        db = MySQLdb.connect("ee220cpc2.ecn.purdue.edu", "root", "Cam$!D1r2L@u", "yangtest")
        cursor = db.cursor()
        ip = " SELECT camera_id, ip FROM ip_camera "
        result = cursor.execute(ip)
        cams = cursor.fetchall()
        print cams[1]
        #for ip in cams[1]:
                
        '''url = "http://www.geobytes.com/IpLocator.htm?GetLocation&IpAddress=" + str(cams[api_cycle][2])
                            soup = BeautifulSoup(urllib2.urlopen(url).read())
                            print soup
                            for ls1 in soup.find_all('input',{'name':'ro-no_bots_pls13'}):
                                                 country = ls1.get('value')
                                                 update="UPDATE camera set country ='" + country 
                            for ls2 in soup.find_all('input',{'name':'ro-no_bots_pls15'}):
                                                 state = ls2.get('value')
                                                 update="UPDATE camera set state ='" + state 
                            for ls3 in soup.find_all('input',{'name':'ro-no_bots_pls17'}):
                                                 city = ls3.get('value')
                                                 update="UPDATE camera set city ='" + city 
                            for ls4 in soup.find_all('input',{'name':'ro-no_bots_pls10'}):
                                                 latitude = ls4.get('value')
                                                 update="UPDATE camera set latitude ='" + latitude 
                            for ls5 in soup.find_all('input',{'name':'ro-no_bots_pls19'}):
                                                 longitude = ls5.get('value')
                                                 update="UPDATE camera set longitude ='" + longitude '''
        
Update_inf()
                    


