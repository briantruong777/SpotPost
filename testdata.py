import sqlite3
from resource.dbmanager import DBManager

manager = DBManager()

###
#
# Adds sample spotposts to the Database.
#
###
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

	test_form['content']	= "Im here as well!"
	test_form['title'] 		= "Location Testing"
	test_form['username']	= "Tester"
	test_form['longitude'] 	= 30.3212
	test_form['latitude'] 	= 32.1020
	test_form['reputation'] = 0
	
	manager.insert_spotpost(test_form, "Tester")

	test_form['content']	= "Coming in live off the coast of Egypt!"
	test_form['title'] 		= "Location Testing"
	test_form['username']	= "Crud Bonemeal"
	test_form['longitude'] 	= 30.3214
	test_form['latitude'] 	= 32.1022
	test_form['reputation'] = 3
	
	manager.insert_spotpost(test_form, "Crud Bonemeal")

	test_form['content']	= "I can't swim. This is probably not the best medium for my rescue."
	test_form['title'] 		= "Location Testing"
	test_form['username']	= "SomeDude"
	test_form['longitude'] 	= 30.3214
	test_form['latitude'] 	= 32.1021
	test_form['reputation'] = 203
	
	manager.insert_spotpost(test_form, "SomeDude")

	test_form['content']	= "Wow its crowded here."
	test_form['title'] 		= "Location Testing"
	test_form['username']	= "Tester"
	test_form['longitude'] 	= 30.3211
	test_form['latitude'] 	= 32.1021
	test_form['reputation'] = 12
	
	manager.insert_spotpost(test_form, "Tester")

	test_form['content']	= "Calling all dollars, your admin needs help."
	test_form['title'] 		= "Location Testing"
	test_form['username']	= "Admin"
	test_form['longitude'] 	= 30.3211
	test_form['latitude'] 	= 32.1021
	test_form['reputation'] = 394
	
	manager.insert_spotpost(test_form, "Admin")

	test_form['content']	= "No comment."
	test_form['title'] 		= "Location Testing"
	test_form['username']	= "Phillabuster"
	test_form['longitude'] 	= 30.321143
	test_form['latitude'] 	= 32.1021214
	test_form['reputation'] = 3
	
	manager.insert_spotpost(test_form, "Phillabuster")

	test_form['content']	= "Swimming is so good for the core brah."
	test_form['title'] 		= "Location Testing"
	test_form['username']	= "Crud Bonemeal"
	test_form['longitude'] 	= 30.32131948
	test_form['latitude'] 	= 32.10243481
	test_form['reputation'] = 7
	
	manager.insert_spotpost(test_form, "Crud Bonemeal")

###
#
# Adds sample users to the database.
#
###
def add_users():
	manager.insert_user("Admin", "BananaPeppers")
	manager.update_privilege("Admin", 1)

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

manager.drop_tables()
manager.create_tables()
add_test_data()
manager.close_connection()