import sqlite3
from resource.dbmanager import DBManager

manager = DBManager()

def add_spotposts():
	test_form = {}

	test_form['content']	= "This is test data, can't you see!"
	test_form['title'] 		= "Sample"
	test_form['username']	= "Tester"
	test_form['longitude'] 	= 18.0
	test_form['latitude'] 	= 51.0
	test_form['reputation'] = 40
	
	manager.insert_spotpost(test_form, "Tester")

	test_form['content']	= "Well Well Well, ain't this a surprise!"
	test_form['title'] 		= "Sample2"
	test_form['username']	= "Tester"
	test_form['longitude'] 	= 19.0
	test_form['latitude'] 	= 51.0
	test_form['reputation'] = 4
	
	manager.insert_spotpost(test_form, "Tester")

	test_form['content']	= "I am the admin, fear me!"
	test_form['title'] 		= "GodMode"
	test_form['username']	= "Admin"
	test_form['longitude'] 	= 30.0
	test_form['latitude'] 	= 32.0
	
	manager.insert_spotpost(test_form, "Admin")

	test_form['content']	= "There are gorrilas everywhere."
	test_form['title'] 		= "Gorrilas"
	test_form['username']	= "Admin"
	test_form['longitude'] 	= 30.01
	test_form['latitude'] 	= 32.01
	test_form['reputation'] = 6
	
	manager.insert_spotpost(test_form, "Admin")

def add_users():
	manager.insert_user("Admin", "BananaPeppers")
	manager.insert_user("Crud Bonemeal", "Protein")
	manager.insert_user("SomeDude", "Garbage")
	manager.insert_user("Phillabuster", "Freaks812")
	manager.insert_user("Tester", "Dijkstra")
	manager.insert_user("Lurker", "NoPost")	
	
''''
' Adds test data to the DB.
'
'''
def add_test_data():
	add_spotposts()
	add_users()

add_test_data()
manager.close_connection()