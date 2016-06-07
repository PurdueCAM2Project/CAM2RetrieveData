"""
Descriptive Name 	 : addCamera.py
Written by		 : Youngsol Koh									      
Contact Info		 : 
Description		 : This program will automatically add cameras in the database. 
Command to run script	 : python addCamera.py <text file to put in database> <ip / non_ip>
Input file format 	 : Country,City,latitude,longitude,snapshot_url must exist in the file
				you do not have to follow the sequence of fields.
				You must list the field in the first line.
				Country(2 letter) and City must exist in the file.
				Please use field name in the info_source table

				input file examples :
			
				snapshot_url#lat#long#country#state#city#description
				http://....jpg#43.852169#-79.022083#CA#ON#Greater Toronto Area#Highway 401 near Harwood Avenue

				example 2)
				description#snapshot_url#direction#country#state#city
				Tupper Hwy 2, 2 km west of BC/Alberta border#http://....jpg#east#CA#BC#Dawson Creek
				this python program and a file should be in the same folder.
 
 Other files required by : N/A
 this script and where 
 located

--------------------------------------------------------------------------------
Package requirements : pip, chardet, MySQLdb
--------------------------------------------------------------------------------
pip     : sudo apt-get install python-pip
MySQLdb : sudo apt-get install python-dev libmysqlclient-dev
          sudo pip install MySQL-python
chardet : pip install chardet
--------------------------------------------------------------------------------
"""

import sys
import os
import codecs
import MySQLdb
import chardet
import getpass
import os
import time
import datetime
import re
import warnings
import subprocess


def detect_extra_field(fileName):
	"""Count number of #"""
	numFields = len(list_field(fileName))
	f = open(fileName,'rb')
	numLine = 1
	isSuccess= True
	print "Checking extra/missing fields"
	for line in f:
		if(len(line.split('#')) != numFields):
			print "Extra/missing field line Number : "+str(numLine)
			print line.replace('\n','')
			isSuccess = False
		numLine=numLine+1
	
	if (isSuccess==False):
		print "Try to fix extra fields/missing in printed line number"
	else:
		print "Passed"
	f.close()
	return isSuccess

def check_basic_rules(fileName,camType):
	print 'Checking basic rules ..'
	print 'i.e) country code must be 2 letter except for USA, state for USA must be 2 letter'
	print "In description, special characters like ' and "'" must be escaped by user manually'
	print 'snapshot_url,latitude,longitude,country,city information must exist'
	fields = list_field(fileName)
	index_checker= []
	if camType == 'non_ip':
		index_snapshot_url = get_field_index('snapshot_url',fields)
		index_checker.append(index_snapshot_url)
	else:
		index_ip = get_field_index('ip',fields)
		index_checker.append(index_ip)
	index_country = get_field_index('country',fields)
	index_checker.append(index_country)
	index_latitude = get_field_index('latitude',fields)
	index_checker.append(index_latitude)
	index_longitude=get_field_index('longitude',fields)
	index_checker.append(index_longitude)
	index_city = get_field_index('city',fields)
	index_checker.append(index_city)
	#find out state exist in the file
	if ('state' in fields):
		index_state = get_field_index('state',fields)
	else:
		index_state = -1
	#find out state description exist in the file
	if ('description' in fields):
		index_description = get_field_index('description',fields)
	else:
		index_description = -1

	#validate field required by program exist
	if(-1 in index_checker):
		return False

	f = open(fileName,'rb')
	isSuccess = True
	numLine = 1
	for line in f:
		#skip first line
		if numLine ==1:
			numLine +=1
			continue
		#check url
		if line.split('#')[index_snapshot_url].startswith('http'):
			pass
		else:
			print "Line %s : incorrect url format %s" %(str(numLine),line.split('#')[index_snapshot_url])
			isSuccess =False
		#check countrty code	
		if len(line.split('#')[index_country])==2:
			pass
		#added exception for USA
		elif exact_match('usa',line.split('#')[index_country].lower()):
			pass
		else:
			print "Line %s : incorrect country format %s" %(str(numLine),line.split('#')[index_country])
			isSuccess = False
		#check state length only for USA
		if((index_state == -1 and (exact_match('usa',line.split('#')[index_country].lower()) is False)) or (index_state != -1 and exact_match('usa',line.split('#')[index_country].lower()) and len(line.split('#')[index_state])==2)):
			pass
		else:
			print "Line %s : incorrect state format %s" %(str(numLine),line.split('#')[index_state])
			isSuccess = False
		#check if there are ' or " in description
		if(index_description!=-1):
			if '"' in line.split('#')[index_description] or "'" in line.split('#')[index_description]:
				print line
				print numLine
				print index_description
				print ("Line %s : description contains \' or \" : %s", str(numLine),line.split('#')[index_description])
				print "Please open file and escape manually i.e) it's example -> it"+'"'+"'"+'"'+'s example, it"s example -> it'+"'"+'"'+"'"+"s example"
				isSuccess = False
		numLine+=1
	f.close()
	return isSuccess


"""
Check if there is a certain field, returns index 
when it returns -1, it does not exist
i.e) get_field_index('snapshot_url',field_list)
"""
def get_field_index(fieldName,field_list):
	index = -1
	if(fieldName in field_list) ==False:
		print 'Error : There is no fields name called '+fieldName+' in your file'
	else:
		index = field_list.index(fieldName)
	return(index)




"""This function will remove special characters in the file
	Create a temp file and overwrite to original filename  """
def check_special_chars(fileName):
	"""Copy characters one by one without special chars write file in UTF-8"""
	isSuccess = True
	isPrinted = False
	print "Checking special characters"
	try:
		f = open(fileName,'rb')
		o = open(fileName+'.temp','wb')
		"""check if there any hidden chars like \r \t except for \n"""
		for line in f:
			for char in line:
				if ord(char)==13:  #13 us \r
					if isPrinted ==False:
						print "Carriage return detected : removed"
						isPrinted = True
				else:
					o.write(char)
		o.close()
		f.close()
		"""overwrite"""
		reNameFile = 'mv '+fileName+'.temp'+' '+fileName
		os.system(reNameFile)

	except IOError:
		isSuccess = False
		print "IOError : open/write failed"
	except OSError:
		isSuccess = False
		print "OSError : invalid file name"
	if(isSuccess == True):
		print "Passed"
	return isSuccess

"""Check File Encoding, return True/False
   ascii is subset of UTF-8"""

def check_file_encoding(fileName):
	print "Cheking file encoding"
	stream = open(fileName,'r').read()
	result = chardet.detect(stream)
	encoding = result['encoding']
	confidence = result['confidence']
	print "Encoding   : "+encoding
	print "Confidence : "+str(confidence)+' out of 1'
	if (encoding =='utf-8' or encoding=='ascii')and confidence >0.80:
		isSuccess = True
	elif((encoding =='utf-8' or encoding=='ascii')and confidence <=0.80):
		print "Your file encoding confidence indicates is too low"
		print "Are you sure it is utf-8?(y/n)"
		print "If you continue, you are responsible for data integrity in database"
		yn = raw_input()
		if yn=='y' or 'Y':
			isSuccess = True
		else:
			isSuccess =False
	else:
		isSuccess = False
		print "Please encode your data to UTF-8"
	return isSuccess

"""
First line should be fields name i.e) imgurl#description#latitude#longitude
Returns fields as list
"""
def list_field(filename):	 
	f = open(filename,'r')
	first_line = f.readline().replace('\n','')
	fields = first_line.split('#')
	f.close()
	return fields
"""
Ask user name and password for database
"""
def authenticate():
	print "Enter user name for MySQL :"
	userName = raw_input()
	passwd = getpass.getpass()
	return userName,passwd
"""
Backup database
Success -> return True
Fail -> return False
"""
def backup_database(userName,passwd):
	timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
	p = subprocess.Popen(['mysqldump','-h','localhost','--routines','-u',userName,'-p'+passwd,'cam2'],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	dump = p.communicate()[0]
	if p.returncode != 0:
		print dump.replace('\n\n','\n')
		print "Backup database failed"
		return False
	f = open(timeStamp+'-cam2Backup.sql','wb')
	f.write(dump)
	f.close()
	print 'Backup database completed!'
	return True

"""
Connect to database
return  db object exit program
"""
def connect_database(userName,passwd):
	try:
		print "Connecting to database.."
		db = MySQLdb.connect("localhost",userName,passwd,"cam2")
	except MySQLdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		return False
	else:
		return db
"""
disconnect from database
"""
def disconnect_database(db):
	print "Disconnecting database."
	db.close()

	
def show_desc(db,tableName):
	cursor = db.cursor()
	cursor.execute("desc "+tableName)
	desc = cursor.fetchall()
	print '-----------------------------------------------------------------------------------'
	print 'FIELD'.ljust(25)+'TYPE'.ljust(25)+'NULL'.ljust(25)+'EXTRA'.ljust(25)
	for line in desc:
		print line[0].ljust(25)+line[1].ljust(25)+line[2].ljust(25)+line[3].ljust(25)
	print '-----------------------------------------------------------------------------------'
"""
Request desc [table_name]
return as tuple [[fieldName,type,is_null,extra],...]
"""
def desc_table(db,tableName):
	cursor = db.cursor()
	cursor.execute("desc "+tableName)
	desc = cursor.fetchall()
	
	return desc

def compare_info_source_with_file(fileName,db):
	fields_in_file = list_field(fileName)
	fields_in_table = desc_table(db,'info_source')
	fields = [(i[0]) for i in fields_in_table]
	print_desc = False
	for member in fields_in_file:
		if member in fields:
			pass
		else:
			print_desc = True
			print "ERROR : there is no fields called %s in info_source table" %member
	
	if print_desc ==True:
		print '-----------------------------------------------------------------------------------'
		print 'FIELD'.ljust(25)+'TYPE'.ljust(25)+'NULL'.ljust(25)+'EXTRA'.ljust(25)
		for line in fields_in_table:
			print line[0].ljust(25)+line[1].ljust(25)+line[2].ljust(25)+line[3].ljust(25)
		print '-----------------------------------------------------------------------------------'
	return (not print_desc)
"""
Creating temp table based on user input file
return true /falase
"""
def create_temp_table(fileName,db):
	isSuccess = True
	cursor = db.cursor()
	fields = list_field(fileName)
	desc = desc_table(db,'info_source')
	print '---------------------------------------------------------------------------------'
	print "STEP 1. Creating temp table, below are the current list of the table."
	print "Avoid the same naming convention below, DO NOT USE SPACE IN THE NAME"
	print "Waiting 4 seconds to read"
	time.sleep(4)
	table_list = show_tables(db)
	print_tables(table_list)
	print "Enter temp table name :"
	temp_tableName = raw_input().replace(' ','')
	while temp_tableName in table_list:
		print "ERROR : same table name found"
		print "Enter temp table name : "
		temp_tableName = raw_input().replace(' ','')
	print '---------------------------------------------------------------------------------'
	print "Your file %s has following fields"%fileName
	print fields
	print '---------------------------------------------------------------------------------'
	print "temp table %s will be created by using following command:"%temp_tableName
	sql = 'CREATE TABLE '+temp_tableName+' ('
	print sql
	cmd =[]
	#Creating sql command
	for field in fields:
		if field =='snapshot_url' and exact_match('snapshot_url',field):
			cmd.append([item[0]+' '+item[1] for item in desc if field in item[0] and exact_match(field,item[0])][0] +' not null unique')
		else:
			cmd.append([item[0]+' '+item[1] for item in desc if field in item[0] and exact_match(field,item[0])][0])
	i=0
	for member in cmd:
		if i == len(cmd)-1:
			sql = sql+member+')'
			print member+')'
		else:
			sql = sql+member+','
			print member+','
		i=i+1
	print '---------------------------------------------------------------------------------'
	print 'Is this correct? (y/n) if this seems not correct, please contact Youngsol/double check file'
	yn = raw_input()
	if yn =='y' or 'Y':
		try:
			print "Creating table : %s"%temp_tableName
			cursor.execute(sql)
			print "%s created, below is description of %s"%(temp_tableName,temp_tableName)
			show_desc(db,temp_tableName)			
		except MySQLdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			isSuccess = False
	else:
		isSuccess = False
	
	return isSuccess,temp_tableName
def insert_into_info_source(temp_tableName,db):
	print '---------------------------------------------------------------------------------'
	print "STEP 3 : Load temp table into info_source"
	print 'field "source" must be exist and unique'
	print 'avoid below source waiting 4 seconds to read'
	time.sleep(4)
	source_list = distinct_source(db)
	print_tables(source_list)
	print '---------------------------------------------------------------------------------'
	print "Enter your source name, if it is from Department of transportation, STATE_dot i.e) in_dot"
	print "If it is from webcams.trave : webcams_travel"
	print "bbc in uk: bbc_uk"
	print "Something that can differentiate related to your  source url (domain name)"
	print "MAXIMUM LENGTH 20 char"
	source_name = raw_input().replace(' ','')
	while source_name in source_list:
		print "ERROR : same source name found"
		print "Enter source name : "
		source_name = raw_input().replace(' ','')
	print '---------------------------------------------------------------------------------'
	isSuccess = True
	cursor = db.cursor()
	#set warning to error
	warnings.simplefilter("error",MySQLdb.Warning)
	fields_in_file = list_field(fileName)
	#Build SQL
	sql = 'INSERT INTO info_source ('
	print sql
	i = 0
	for field in fields_in_file:
		if i == len(fields_in_file)-1:
			sql = sql+field+', source) SELECT '
			print field+', source) SELECT '
		else:
			sql = sql+field+','
			print field +','
		i=i+1
	
	i = 0
	for field in fields_in_file:
		if i == len(fields_in_file)-1:
			sql = sql+field+",'"+source_name+"' from "+temp_tableName
			print field+",'"+source_name+"' from "+temp_tableName
		else:
			sql = sql+field+','
			print field+','
		i=i+1
	print '---------------------------------------------------------------------------------'
	print sql
	print '---------------------------------------------------------------------------------'
	print 'Is this correct? (y/n) if this seems not correct, please contact Youngsol/double check file'
	yn = raw_input()
	if yn =='y' or 'Y':
		try:
			print "Inerting into info_source from %s"%temp_tableName
			cursor.execute(sql)
			cursor.execute("select * from info_source where source = "+"'"+source_name+"'")
			num_record=cursor.rowcount
			cursor.execute("select * from "+temp_tableName)
			num_table = cursor.rowcount
			print "%d recorded in info_source out of %d from %s"%(int(num_record),int(num_table),temp_tableName)
		except MySQLdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			isSuccess = False
		except MySQLdb.Warning,e:
			print "MYSQL Warning : %s"%e
			#print "MySQL Warning[%d]: %s"% (e.args[0], e.args[1])
			isSuccess = False
	else:
		isSuccess =False

	return isSuccess,source_name
def delete_from_table(tableName,sourceName,db):
	cursor = db.cursor()
	print "Deleting source = '%s' from %s due to errors/warnings"%(sourceName,tableName)
	cursor.execute("Delete from "+tableName+" where source = '"+sourceName+"'")
	after = cursor.rowcount
	print str(after) +' row are affected'


def distinct_source(db):
	cursor = db.cursor()
	cursor.execute('select distinct source from info_source')
	source_list = [(i[0]) for i in cursor.fetchall()]
	return source_list

def load_file_to_temp_table(fileName,tableName,db):
	print "STEP 2 : Load your file into temp table you created"
	print "ALL warning will be raised as error except for duplicates in the file "
	print "table will be dropped if loading failed"
	print '---------------------------------------------------------------------------------'
	print "Loading your file to %s"%tableName
	print '---------------------------------------------------------------------------------'
	isSuccess = True
	cursor = db.cursor()
	#set warning to error
	warnings.simplefilter("error",MySQLdb.Warning)
	fields_in_table = desc_table(db,tableName)
	fields_in_file = list_field(fileName)
	sql = 'insert ignore into '+tableName+'('
	i =0
	field_type=[]
	for member in fields_in_file:
		if i == len(fields_in_file)-1:
			sql = sql+member+') VALUES ('
		else:
			sql = sql+member+','
		i = i+1
		field_type.append([item[1] for item in fields_in_table if member in item[0] and exact_match(member,item[0])][0])
		


	f = open(fileName,'rb')
	
	skipfirstLine = True
	for line in f:
		if(skipfirstLine):
			skipfirstLine =False
			continue
		members = line.replace('\n','').split('#')
		i=0
		cmd = sql
		for member in members:
			types = field_type[i]
			if 'char' in types:
				if i == len(members)-1:
					cmd = cmd +"'"+member+"'"+')'
				else:
					cmd = cmd +"'"+member+"'"+','
			else:
				if i == len(members)-1:
					cmd = cmd +member+')'
				else:
					cmd = cmd +member+','
			i = i+1
		try:
			cursor.execute(cmd)
		except MySQLdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			isSuccess = False
		except MySQLdb.Warning,e:
			print "MYSQL Warning : %s"%e
			isSuccess = False

	f.close()
	return isSuccess
def drop_table(talbName,db):
	cursor = db.cursor()
	cursor.execute('drop table '+tableName)
def exact_match(phrase, word):
    b = r'(\s|^|$)' 
    res = re.match(b + word + b, phrase, flags=re.IGNORECASE)
    return bool(res)
	
"""
result of show tables before user create temp table
return as list of tables

"""
def print_temp_res(fileName,tableName,db):
	f = open(fileName,'rb')
	numLine = 0
	for line in f:
		numLine +=1
	f.close()
	numLine -=1 #exclude fields line
	cursor = db.cursor()
	desc = desc_table(db,tableName)
	field = [(i[0]) for i in desc]
	print field
	cursor.execute("select * from "+tableName)
	for l in cursor.fetchall():
		print l
	print str(cursor.rowcount) +' recorded (%d duplicate)'% (int(numLine)-int(cursor.rowcount))

def show_tables(db):
	cursor = db.cursor()
	cursor.execute("show tables")
	tables = [(i[0]) for i in cursor.fetchall()]
	return tables
def print_tables(tables):
	print "-------------------------------"
	for table_name in tables:
		print "|"+table_name.ljust(30)+"|"
	print "-------------------------------"
def insert_into_camera(sourceName,cameraType,db):
	print '---------------------------------------------------------------------------------'
	print "STEP 4 : Load camera table from info_source where source = '%s'"%sourceName
	print "Is this camera traffic camera? (y/n) if it is traffic camera, is_safe will be 1"
	print "otherwise, 0"
	print '---------------------------------------------------------------------------------'
	isSuccess = True
	cursor = db.cursor()
	yn = raw_input()
	if yn == 'y' or 'Y':
		sql = "INSERT IGNORE INTO camera (camera_key, encrypted_camera_key, type, source, latitude, longitude, country, state, city, resolution_width, resolution_height, frame_rate, is_video, is_active, is_safe, is_high_load, is_analysis_restricted, utc_offset, timezone_id, timezone_name, reference_logo, reference_url,multiple_cameras,is_located,weather_wind_speed,weather_temperature_faren,weather_humidity,weather_code) SELECT snapshot_url, null, %s, source, latitude, longitude, country, state, city, null, null, null, 0, 1, 1, 0, 0, null, null, null, null, null, null, 1, null, null, null, null FROM info_source WHERE source=%s"%(("'"+cameraType+"'","'"+sourceName+"'"))
	else:
		sql = "INSERT IGNORE INTO camera (camera_key, encrypted_camera_key, type, source, latitude, longitude, country, state, city, resolution_width, resolution_height, frame_rate, is_video, is_active, is_safe, is_high_load, is_analysis_restricted, utc_offset, timezone_id, timezone_name, reference_logo, reference_url,multiple_cameras,is_located,weather_wind_speed,weather_temperature_faren,weather_humidity,weather_code) SELECT snapshot_url, null, %s, source, latitude, longitude, country, state, city, null, null, null, 0, 1, 0, 0, 0, null, null, null, null, null, null, 1, null, null, null, null FROM info_source WHERE source=%s"%(("'"+cameraType+"'","'"+sourceName+"'"))
	try:
		print "Inserting into camera table from info_source"
		cursor.execute(sql)
		cursor.execute("select * from info_source where source = "+"'"+sourceName+"'")
		num_record=cursor.rowcount
		cursor.execute("select * from camera where source = "+"'"+sourceName+"'")
		num_table = cursor.rowcount
		print "%d recorded in camera out of %d from info_source"%(int(num_table),int(num_record))
	except MySQLdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		isSuccess = False
	except MySQLdb.Warning,e:
		print "MYSQL Warning : %s"%e
		isSuccess = False

	return isSuccess
def insert_into_non_ip(sourceName,db):
	cursor = db.cursor()
	print '---------------------------------------------------------------------------------'
	print "STEP 5 : insert into non_ip_camera table"
	sql = "INSERT IGNORE INTO non_ip_camera (camera_id, snapshot_url) SELECT id, camera_key FROM camera WHERE source ="+"'"+sourceName+"'"
	print sql
	print '---------------------------------------------------------------------------------'
	isSuccess =True
	try:
		print "inserting into non_ip_camera table"
		cursor.execute(sql)
		num_record = cursor.rowcount
		print "%d row affected"%(int(num_record))
	except MySQLdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		isSuccess = False
	except MySQLdb.Warning,e:
		print "MYSQL Warning : %s"%e
		#print "MySQL Warning[%d]: %s"% (e.args[0], e.args[1])
		isSuccess = False
	return isSuccess
def update_camera_id(db):
	print '---------------------------------------------------------------------------------'
	print "STEP 6 : update camera IDs in info_source, camera table"
	cursor= db.cursor()
	sql = "UPDATE info_source, camera SET camera_id = id WHERE camera_key = snapshot_url"
	print sql
	print '---------------------------------------------------------------------------------'
	isSuccess =True
	try:
		print "Updating IDs.."
		cursor.execute(sql)
		num_record = cursor.rowcount
		print "%d row affected"%(int(num_record))
	except MySQLdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		isSuccess = False
	except MySQLdb.Warning,e:
		print "MYSQL Warning : %s"%e
		isSuccess = False

	return isSuccess
if __name__ == '__main__':
	if len(sys.argv)<3:
		print "python addCamera.py <text file to put in database> <type>"
		print "type : ip / non_ip"
	else:

		fileName = sys.argv[1]
		camType = sys.argv[2]


		if exact_match(camType,'non_ip') or exact_match(camType,'ip'):
			pass
		else:
			print "Wrong camType entered"
			sys.exit(1)


		"""File verification"""

		if(detect_extra_field(fileName)==False):
			sys.exit(1)
		if(check_file_encoding(fileName)==False):
			sys.exit(1)	
		if(check_special_chars(fileName)==False):
			sys.exit(1)
		if(check_basic_rules(fileName,camType)==False):
			sys.exit(1)
	
		"""Database manage"""
		#id and password for db
		userName,passwd = authenticate()

		#backup db	
		if(backup_database(userName,passwd)==False):
			sys.exit(1)

		
		#connect to db
		db = connect_database(userName,passwd)
		if(compare_info_source_with_file(fileName,db)==False):
			sys.exit(1)
		try:
			res, tableName = create_temp_table(fileName,db)
			if res ==False:
				raise
			if(load_file_to_temp_table(fileName,tableName,db)==False):
				raise
			print_temp_res(fileName,tableName,db)
			
			res,sourceName = insert_into_info_source(tableName,db)
			if(res==False):
				delete_from_table('info_source',sourceName,db)
				raise
			if(insert_into_camera(sourceName,camType,db)==False):
				print"Please go to fix errors manually in camera table in MySQL"
				print"your input in info_source will reamin with source = '"+sourceName+"'"
				raise
			if(camType =='non_ip'):
				if(insert_into_non_ip(sourceName,db)==False):
					print"Please go to fix errors manually in camera table, non_ip_camera talbe in MySQL"
					print"your input in info_source will reamin with source = '"+sourceName+"'"
					raise
			else:
				#ip camera
				pass
			if(update_camera_id(db)==False):
				print "Please go update camera id manually"
				raise
			drop_table(tableName,db)
			print "Please go to website and check camera added recently shows on the map"
			print "http://ee220cpc2.ecn.purdue.edu:5555"
		except Exception as e:
			print e
			print "dropping temp table %s"%tableName
			drop_table(tableName,db)
		finally:
			disconnect_database(db)
		

			

		


