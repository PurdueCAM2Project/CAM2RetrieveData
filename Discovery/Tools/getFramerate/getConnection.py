import MySQLdb
import getpass
import re


def getConnection(DB_PASSWORD):
	connection = None
	while connection == None:
		connection = connect(DB_PASSWORD)
		if connection == None and connection != -1:
			print("Connection info not correct...\n\tTry again:")
		elif connection == -1:
			return	None

	return connection

def connect(DB_PASSWORD):
	# Try to access database:
	connection = None
	try:
		databaseRead = open("database.config", "r")
		databaseInfo = list(databaseRead)
		for info in databaseInfo:
			if info.find("DB_SERVER") != -1:
				DB_SERVER = re.search(r"DB_SERVER = (?P<SERVER>[\S]*)", databaseInfo[1]).group("SERVER")
			elif info.find("DB_USER_NAME") != -1:
				DB_USER_NAME = re.search(r"DB_USER_NAME = (?P<USER>[\S]*)", databaseInfo[2]).group("USER")
			# elif info.find("DB_PASSWORD") != -1:  
			#     DB_PASSWORD = re.search(r"DB_PASSWORD = (?P<PSWD>[\S]*)", databaseInfo[3]).group("PSWD")
			elif info.find("DB_NAME") != -1:
				DB_NAME = re.search(r"DB_NAME = (?P<NAME>[\S]*)", databaseInfo[3]).group("NAME")
		print("database.config found.\nUsing:\n\tDB_SERVER = {}\n\tDB_USER_NAME = {}\n\tDB_NAME = {}".format(DB_SERVER, DB_USER_NAME, DB_NAME))

	except Exception as e:
		print("database.config missing!!")
		print("Creating database.config")
		databaseRead = open("database.config", "w")
		databaseRead.write("# The server database credentials.")
		DB_SERVER = raw_input("DB_SERVER = ")
		DB_USER_NAME = raw_input("DB_USER_NAME = ")
		DB_NAME = raw_input("DB_NAME = ")
		databaseRead.write("# The server database credentials.\nDB_SERVER = {}\nDB_USER_NAME = {}\nDB_NAME = {}".format(DB_SERVER, DB_USER_NAME, DB_NAME))

	try:
		if DB_PASSWORD == None:
			print("Input Database Password or /c to change info:")
			DB_PASSWORD = getpass.getpass("\nDB_PASSWORD = ")

		if DB_PASSWORD == "/c":
			databaseRead = open("database.config", "w")
			databaseRead.write("# The server database credentials.")
			DB_SERVER = raw_input("DB_SERVER = ")
			DB_USER_NAME = raw_input("DB_USER_NAME = ")
			DB_NAME = raw_input("DB_NAME = ")
			databaseRead.write("# The server database credentials.\nDB_SERVER = {}\nDB_USER_NAME = {}\nDB_NAME = {}".format(DB_SERVER, DB_USER_NAME, DB_NAME))
		else:
			# Connect to the database, and get the connection cursor
			connection = MySQLdb.connect(DB_SERVER, DB_USER_NAME, DB_PASSWORD, DB_NAME)
	except KeyboardInterrupt:
		connection = -1;
	except:
		connection = None

	databaseRead.close()
	return connection