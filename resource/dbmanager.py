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
from passlib.hash import sha256_crypt
from unidecode import unidecode

connect = sqlite3.connect('data.db')
cursor = connect.cursor()

def build_comments_JSON(curr_id):
	comments = []
	cursor.execute("SELECT * FROM SpotPostComments WHERE message_id = ?", (curr_id,))
	data = cursor.fetchall()

	for row in data:
		comment_dict 				= {}
		comment_dict['id'] 		 	= row[0]
		comment_dict['message_id']	= row[1]
		comment_dict['content'] 	= unidecode(row[2])
		comment_dict['username'] 	= unidecode(row[3])
		comment_dict['time'] 		= unidecode(row[4])

		comments.append(comment_dict)

###
#
#	Builds dictionary to add to the JSON sent back on a get.
#	Returned dictionary contains user info.
#	
#	@return A dictionary, see below.
#
#	Returned dictionary will follow this format:
#	'username' : username of user.
#	'profile_pic_id' : profile picture id of user.
#	'reputation' : reputation of user.
#
###	
def build_username_JSON(username):
	userinfo = []
	cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
	rawdata = cursor.fetchall()

	for row in rawdata:
		user_dict = {}
		user_dict['username'] 		= unidecode(row[0])
		user_dict['profile_pic_id'] = row[2]
		user_dict['reputation']		= row[3]

		userinfo.append(user_dict)

	return userinfo
	
	return comments

###
#
#	Securely stores the password in the database
#
#	@param username = username of user.
#	@param password = password of user.
#
###
def store_hash_pass(username, password):
	pass_hash = sha256_crypt.encrypt(password)
	cursor.execute("INSERT INTO Users(username, password) VALUES(?, ?)", (username, pass_hash))
	connect.commit()

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

	###
	# 
	# Allows clientside to make a POST request to add data to the server database.
	# 
	# JSON must be constructed following convention below (ALL DATA IS REQUIRED):
	# "content"   		: "text of spotpost"
	# "username"  		: "username of person making spotpost"  	NOTE: MAY BE DEPRECEATED IN FUTURE VERSIONING
	# "latitude" 		: "latitude of spotpost"
	# "longitude" 		: "longitude of spotpost"
	# "reputation"   	: "custom starting reputation" 				NOTE: WILL BE DEPRECEATED IN FUTURE VERSIONING. 
	#
	###
	def insert_spotpost(self, form):
		content 	= form['content']
		title 		= form['title']
		username	= form['username']
		longitude 	= form['latitude']
		latitude 	= form['longitude']
		reputation 	= form['reputation']
		
		cursor.execute("INSERT INTO SpotPosts(content, title, reputation, longitude, latitude, username) VALUES (?,?,?,?,?)", (content, reputation, longitude, latitude, username))
		connect.commit()

	def insert_user(self, form):
		client_username = form['username']
		client_password = form['password']

		store_hash_pass(client_username, client_password)

		#@TODO REPLACE WITH REGISTRATION FORM
		return '''
	        <form action="" method="post">
	            <p><input type=text name=username>
	            <p><input type=text name=password>
	            <p><input type=submit value=Login>
	        </form>
	    '''

	def insert_comment(self):
		connect.commit()


	def select_spotpost(self, min_reputation, max_reputation, username, post_id, min_latitude, max_latitude, min_longitude, max_longitude, radius, is_area_search):
		query = "SELECT * FROM SpotPosts"
		query_data = ()
		where_query = False

		if post_id:
			query = query + " WHERE id = ?"
			query_data = query_data + (post_id,)
			where_query = True
		if is_area_search:
			if not where_query:
				query 		= query + " WHERE latitude <= ? AND latitude >= ? AND longitude <= ? AND longitude >= ?"
				query_data 	= query_data + (max_latitude, min_latitude, max_longitude, min_longitude)
				where_query = True
			else:
				query 		= query + " AND latitude <= ? AND latitude >= ? AND longitude <= ? AND longitude >= ?"
				query_data 	= query_data + (max_latitude, min_latitude, max_longitude, min_longitude)
		if username:
			if not where_query:
				query 		= query + " WHERE username = ?"
				query_data 	= query_data + (username,)
				where_query = True
			else:
				query 		= query + " AND username = ?"
				query_data 	= query_data + (username,)
		if min_reputation:
			if not where_query:
				query 		= query + " WHERE reputation >= ?"
				query_data 	= query_data + (min_reputation,)
				where_query = True
			else:
				query 		= query + " AND reputation >= ?"
				query_data 	= query_data + (min_reputation,)
		if max_reputation:
			if not where_query:
				query 		= query + " WHERE reputation <= ?"
				query_data 	= query_data + (max_reputation,)
				where_query = True
			else:
				query_data 	= query_data + (max_reputation,)
				query 		= query + " AND reputation <= ?"

		cursor.execute(query, query_data)	
		rawdata = cursor.fetchall()
		data = []
		for row in rawdata:
		#SpotPosts(id, content, reputation, longitude, latitude, user_id, time)
			data_dict 				= {}
			data_dict['id'] 		= row[0]
			data_dict['content'] 	= unidecode(row[1])
			data_dict['title']		= unidecode(row[2])
			data_dict['reputation'] = row[3]
			data_dict['longitude']	= row[4]
			data_dict['latitude'] 	= row[5]
			data_dict['username'] 	= build_username_JSON(unidecode(row[6]))
			data_dict['time'] 		= unidecode(row[7])
			data_dict['comments'] 	= build_comments_JSON(row[0])

			data.append(data_dict)

		return data

	###
	#
	#	Helper function for rating. Changes reputation of SpotPost by change_in_reputation
	#
	#	@param change_in_reputation = number to be added to reputation.
	#	@param id = id of SpotPost.
	#
	###
	def rate_post(self, change_in_reputation, id, username):
		cursor.execute("SELECT * FROM Rates WHERE username = ? AND spotpost_id = ?", (username, id))
		curr_user_data = cursor.fetchone()

		cursor.execute("SELECT * FROM SpotPosts WHERE id = ?", (id,))
		spotpost_data = cursor.fetchone()
		spotpost_creator = spotpost_data[6]

		if not curr_user_data and spotpost_data:		#If the user HASN'T upvoted, and the SpotPost exists.
			cursor.execute("UPDATE SpotPosts SET reputation = reputation + ? WHERE id = ?", (change_in_reputation, id))					# Increase rep of SpotPost
			cursor.execute("INSERT INTO Rates (username, spotpost_id) VALUES (?, ?)", (username, id))	# Insert relation into Rates
			cursor.execute("UPDATE Users SET reputation = reputation + ? WHERE username = ?", (change_in_reputation, spotpost_creator))	# Increase rep of Creator
			connect.commit()
			return "SUCCESS"
		else:
			return "ERROR USER ALREADY VOTED OR SPOTPOST DOESN'T EXIST"

	###
	#
	#	Deletes a spotpost with id provided.
	#
	#	@param id = id of spotpost to delete.
	#
	###
	def delete_post(self, id):
		cursor.execute("DELETE FROM SpotPosts WHERE id = ?", (id,))
