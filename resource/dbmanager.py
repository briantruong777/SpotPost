'''
'	
'	Spotpost serverside. 
'	--------------------
'	Deals with comments to SpotPosts.
'
'	@author Jakub Wlodarczyk
'	@author Brian Truong
'	@author Nate Norgaard
'	@author Adam Davis
' 
'''
import sqlite3
import testdata

connect = sqlite3.connect('data.db')
cursor = connect.cursor()

class DBManager:
	###
	#	
	#	Initializes the Database by creating each table. Below are the tables in relational format.
	#
	#	SpotPosts(id, content, title, reputation, longitude, latitude, username, time)
	#	SpotPostComments(id, message_id, content, user_id, time)
	#	Users(username, password, profile_pic_id, reputation)
	#	Follows(follower_name, followee_name)
	#	Photos(id, photo)
	#	Rates(username, spotpost_id)
	#
	###
	def __init__(self):
		cursor.execute("DROP TABLE IF EXISTS SpotPosts")
		cursor.execute("DROP TABLE IF EXISTS SpotPostComments")
		cursor.execute("DROP TABLE IF EXISTS Users")
		cursor.execute("DROP TABLE IF EXISTS Follows")
		cursor.execute("DROP TABLE IF EXISTS Photos")
		cursor.execute("DROP TABLE IF EXISTS Rates")

		#SpotPosts(id, content, photo_id, reputation, longitude, latitude, visibility, user_id, time)
		cursor.execute("CREATE TABLE IF NOT EXISTS SpotPosts(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, content TEXT, title TEXT," + 
			"reputation INTEGER DEFAULT 0, longitude REAL NOT NULL, latitude REAL NOT NULL," + 
			" username TEXT, time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)")

		#SpotPostComments(id, message_id, content, username, time)
		cursor.execute("CREATE TABLE IF NOT EXISTS SpotPostComments(id INTEGER PRIMARY KEY AUTOINCREMENT, message_id INTEGER, content TEXT,"
						+ "username TEXT, reputation INTEGER DEFAULT 0, time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)")
		
		#Users(username, password, profile_pic, reputation)
		cursor.execute("CREATE TABLE IF NOT EXISTS Users(username varchar(24) PRIMARY KEY, password TEXT, profile_pic_id INTEGER DEFAULT -1, reputation INTEGER DEFAULT 0)")
		
		#Follows(follower_name, followee_name)
		cursor.execute("CREATE TABLE IF NOT EXISTS Follows(follower_name TEXT, followee_name TEXT)")

		#Photos(id, photo)
		cursor.execute("CREATE TABLE IF NOT EXISTS Photos(id INTEGER PRIMARY KEY AUTOINCREMENT, photo_url TEXT)")

		#Rates(username, spotpost_id)
		cursor.execute("CREATE TABLE IF NOT EXISTS Rates(username TEXT, spotpost_id INTEGER NOT NULL)")

		testdata.add_test_data()

	def insert_spotpost(self):
		connect.commit()

	def insert_spotpost(self):
		connect.commit()