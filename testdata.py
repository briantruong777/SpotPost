import sqlite3
import main

connect = sqlite3.connect('data.db')
cursor = connect.cursor()

def add_spotposts():
	content 		= "This is test data, can't you see!"
	title 			= "Sample"
	username 		= "Tester"
	longitude 		= 18.0
	latitude 		= 51.0
	reputation 		= 25523
	
	cursor.execute("INSERT INTO SpotPosts(content, title, reputation, longitude, latitude, username) VALUES (?,?,?,?,?,?)", (content, title, reputation, longitude, latitude, username))

	content 		= "I need some new ideas here."
	title 			= "Blank"
	username 		= "Tester"
	longitude 		= 42.0
	latitude 		= 52.0
	reputation 		= 244
	
	cursor.execute("INSERT INTO SpotPosts(content, title, reputation, longitude, latitude, username) VALUES (?,?,?,?,?,?)", (content, title, reputation, longitude, latitude, username))

	content 		= "Garbage Data is Best Data."
	title 			= "Title is longer than the content!"
	username 		= "Admin"
	longitude 		= 34.0
	latitude 		= 11.0
	reputation 		= 23
	
	cursor.execute("INSERT INTO SpotPosts(content, title, reputation, longitude, latitude, username) VALUES (?,?,?,?,?,?)", (content, title, reputation, longitude, latitude, username))

	content 		= "Apple is the best company on planet earth!"
	title 			= "Unpopular Opinion"
	username 		= "Admin"
	longitude 		= 3.0
	latitude 		= 42.0
	reputation 		= 0
	
	cursor.execute("INSERT INTO SpotPosts(content, title, reputation, longitude, latitude, username) VALUES (?,?,?,?,?,?)", (content, title, reputation, longitude, latitude, username))

	content 		= "Gee I hope no one finds me."
	title 			= "Hidden"
	username 		= "SomeDude"
	longitude 		= 10.0
	latitude 		= 12.0
	reputation 		= 2
	
	cursor.execute("INSERT INTO SpotPosts(content, title, reputation, longitude, latitude, username) VALUES (?,?,?,?,?,?)", (content, title, reputation, longitude, latitude, username))

	content 		= "FOUND HIM!"
	title 			= "FOUND HIM!"
	username 		= "Phillabuster"
	longitude 		= 10.01
	latitude 		= 12.01
	reputation 		= 1
	
	cursor.execute("INSERT INTO SpotPosts(content, title, reputation, longitude, latitude, username) VALUES (?,?,?,?,?,?)", (content, title, reputation, longitude, latitude, username))
	connect.commit()

def add_users():
	main.store_hash_pass("Admin", "BananaPeppers")
	main.store_hash_pass("Crud Bonemeal", "Protein")
	main.store_hash_pass("SomeDude", "Garbage")
	main.store_hash_pass("Phillabuster", "Freaks812")
	main.store_hash_pass("Tester", "Dijkstra")
	main.store_hash_pass("Lurker", "NoPost")

	connect.commit()

'''
'
'	Clears all Table's current data.
'
'	SpotPosts(id, content, photo_id, reputation, longitude, latitude, visibility, username, time)
'	SpotPostComments(id, message_id, content, user_id, time)
'	Users(username, password, profile_pic_id, reputation)
'	Follows(follower_name, followee_name)
'	Photos(id, photo)
'	Rates(username, spotpost_id)
'''
def clear_tables():
	cursor.execute("DELETE FROM SpotPosts")	
	cursor.execute("DELETE FROM SpotPostComments")
	cursor.execute("DELETE FROM Users")
	cursor.execute("DELETE FROM Follows")
	cursor.execute("DELETE FROM Photos")
	cursor.execute("DELETE FROM Rates")
	
	
''''
' Adds test data to the DB. REQUIRES THE DATABASE TO BE CONSTRUCTED ALREADY.
'
'''
def add_test_data():
	clear_tables()
	add_spotposts()
	add_users()

add_test_data()