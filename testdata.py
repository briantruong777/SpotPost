import sqlite3

connect = sqlite3.connect('data.db')
cursor = connect.cursor()

''''
' Adds test data to the DB. REQUIRES THE DATABASE TO BE CONSTRUCTED ALREADY.
'
'''
def add_test_data():
	content 	= "This is test data, can't you see!"
	username 	= "TEST"
	longitude 	= 18.0
	latitude 	= 51.0
	reputation 		= 25523
	
	cursor.execute("INSERT INTO SpotPosts(content, reputation, longitude, latitude, username) VALUES (?,?,?,?,?)", (content, reputation, longitude, latitude, username))
	connect.commit()

	content 	= "SSSSSSSSSSSSSSSSSSS"
	username 	= "TEST"
	longitude 	= 42
	latitude 	= 52
	reputation 		= 244
	
	cursor.execute("INSERT INTO SpotPosts(content, reputation, longitude, latitude, username) VALUES (?,?,?,?,?)", (content, reputation, longitude, latitude, username))
	connect.commit()

	content 	= "Garbage Data is Best Data."
	username 	= "Admin"
	longitude 	= 34
	latitude 	= 11
	reputation 		= 23
	
	cursor.execute("INSERT INTO SpotPosts(content, reputation, longitude, latitude, username) VALUES (?,?,?,?,?)", (content, reputation, longitude, latitude, username))
	connect.commit()

	content 	= "Unpopular Opinion"
	username 	= "Admin"
	longitude 	= 3
	latitude 	= 42
	reputation 		= 0
	
	cursor.execute("INSERT INTO SpotPosts(content, reputation, longitude, latitude, username) VALUES (?,?,?,?,?)", (content, reputation, longitude, latitude, username))
	connect.commit()

add_test_data()