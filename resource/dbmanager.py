'''
'	
'	Spotpost serverside. 
'	--------------------
'	Manager for the database, all SQL interaction is done by
' 	the manager.
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

	return comments

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
	cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
	rawdata = cursor.fetchall()

	for row in rawdata:
		user_dict = {}
		user_dict['username'] 		= unidecode(row[0])
		user_dict['profile_pic_id'] = row[2]
		user_dict['reputation']		= row[3]

	return user_dict

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

		#SpotPostComments(id, message_id, content, username, reputation, time)
		cursor.execute("CREATE TABLE IF NOT EXISTS SpotPostComments(id INTEGER PRIMARY KEY AUTOINCREMENT, message_id INTEGER, content TEXT,"
						+ "username TEXT, reputation INTEGER DEFAULT 0, time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)")
		
		#Users(username, password, profile_pic, reputation)
		cursor.execute("CREATE TABLE IF NOT EXISTS Users(username varchar(24) PRIMARY KEY, password TEXT, profile_pic_id INTEGER DEFAULT -1, reputation INTEGER DEFAULT 0)")
		
		#Follows(follower_name, followee_name)
		cursor.execute("CREATE TABLE IF NOT EXISTS Follows(follower_name TEXT, followee_name TEXT)")

		#Photos(id, photo)
		cursor.execute("CREATE TABLE IF NOT EXISTS Photos(id INTEGER PRIMARY KEY AUTOINCREMENT, photo_url TEXT)")

		#Rates(username, spotpost_id, comment_id)
		cursor.execute("CREATE TABLE IF NOT EXISTS Rates(username TEXT, spotpost_id INTEGER DEFAULT -1 NOT NULL, comment_id INTEGER DEFAULT -1 NOT NULL)")

		testdata.add_test_data()

	###
	#
	# Inserts follower relation into the database.
	# Prevents duplicates.
	#
	# @param follower_name = username of follower.
	# @param followee_name = username of followee.
	#
	###
	def insert_follow_relation(self, follower_name, followee_name):
		cursor.execute("SELECT * FROM Follows WHERE follower_name = ? AND followee_name = ?", (follower_name, followee_name))
		data = cursor.fetchone()
		if data:
			return "ERROR"
		else:
			cursor.execute("INSERT INTO Follows(follower_name, followee_name) VALUES (?,?)", (follower_name, followee_name))
			connect.commit()
			return "SUCCESS"

	###
	#
	# Deletes follower relation from the database.
	#
	# @param follower_name = username of follower.
	# @param followee_name = username of followee.
	#
	###
	def delete_follow_relation(self, follower_name, followee_name):
		cursor.execute("SELECT * FROM Follows WHERE follower_name = ? AND followee_name = ?", (follower_name, followee_name))
		data = cursor.fetchone()

		if data:
			cursor.execute("DELETE FROM Follows WHERE follower_name = ? AND followee_name = ?", (follower_name, followee_name))
			connect.commit()
		else:
			return "ERROR"

	###
	# 
	# Allows clientside to make a POST request to add data to the server database.
	# SpotPosts(id, content, title, reputation, longitude, latitude, username, time)
	# 
	# JSON must be constructed following convention below (REQUIRED DATA IS DENOTED WITH A *):
	# * "content"   		: "text of spotpost"
	# "username"  			: "username of person making spotpost"  	NOTE: MAY BE DEPRECEATED IN FUTURE VERSIONING
	# * "latitude" 			: "latitude of spotpost"
	# * "longitude" 		: "longitude of spotpost"
	# "reputation"   		: "custom starting reputation" 				NOTE: WILL BE DEPRECEATED IN FUTURE VERSIONING. 
	#
	###
	def insert_spotpost(self, form, client_username):
		content 	= form['content']
		title 		= form['title']
		longitude 	= form['latitude']
		latitude 	= form['longitude']
		reputation 	= form['reputation']
		
		if form['username']:
			client_username = form['username']

		if reputation:
			cursor.execute("INSERT INTO SpotPosts(content, title, reputation, longitude, latitude, username) VALUES (?,?,?,?,?)", (content, reputation, longitude, latitude, client_username))
		else:
			cursor.execute("INSERT INTO SpotPosts(content, title, longitude, latitude, username) VALUES (?,?,?,?)", (content, longitude, latitude, client_username))

		connect.commit()

	###
	#
	# Inserts a user into the Database. Encrypts the password provided using sha256_crypt. 
	# 
	# Provided JSON must follow this form (ALL DATA IS REQUIRED)
	# "username"	: "username of user"
	# "password"	: "password of user"
	#
	##
	def insert_user(self, form):
		client_username = form['username']
		client_password = form['password']

		store_hash_pass(client_username, client_password)

		return "SUCCESS"		

	#SpotPostComments(id, message_id, content, username, reputation, time)
	###
	#
	# Adds a comment to the database.
	#
	# Provided JSON must follow this format (REQUIRED DATA IS DENOTED WITH A *)
	# * "message_id"	: "id of spotpost this comment is from"
	# * "content"		: "content of comment"
	# "username"		: "username of user who posted comment, Optional will normally be current user."	NOTE: WILL BE DEPREACTED ONCE EVERYTHING IS CONFIRMED FUNCTIONING.
	# "reputation"		: "custom starting reputation" 				NOTE: WILL BE DEPRECEATED IN FUTURE VERSIONING.
	#
	###
	def insert_comment(self, form, client_username):
		spotpost_id = form['message_id']
		content 	= form['content']
		reputation 	= form['reputation']

		if form['username']:
			client_username = form['username']

		if reputation: 
			cursor.execute("INSERT INTO SpotPostComments(message_id, content, username, reputation) VALUES (?,?,?,?)", (spotpost_id, content, client_username, reputation))
		else:
			cursor.execute("INSERT INTO SpotPostComments(message_id, content, username) VALUES (?,?,?)", (spotpost_id, content, client_username))

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
	#	Checks if the login information is correct.
	#
	#	@param username = username to be checked.
	#	@param password = password to be checked.
	#	@return true if information is correct, false otherwise.
	#
	###
	def validate_user(self, username, password):
		cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
		data = cursor.fetchone()

		if data:
			db_hash = data[1]
			if(sha256_crypt.verify(client_password, db_hash)):
				return True
			else:
				return False
		else:
			return False


	###
	#
	#	Function for rating. Changes reputation of SpotPost by change_in_reputation
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

		if not curr_user_data and spotpost_data:		#If the user HASN'T upvoted, and the SpotPost exists.
			spotpost_creator = spotpost_data[6]
			cursor.execute("UPDATE SpotPosts SET reputation = reputation + ? WHERE id = ?", (change_in_reputation, id))					# Increase rep of SpotPost
			cursor.execute("INSERT INTO Rates (username, spotpost_id) VALUES (?, ?)", (username, id))	# Insert relation into Rates
			cursor.execute("UPDATE Users SET reputation = reputation + ? WHERE username = ?", (change_in_reputation, spotpost_creator))	# Increase rep of Creator
			connect.commit()
			return "SUCCESS"
		else:
			return "ERROR USER ALREADY VOTED OR SPOTPOST DOESN'T EXIST"

	###
	#
	#	Function for rating. Changes reputation of Comment by change_in_reputation
	#
	#	@param change_in_reputation = number to be added to reputation.
	#	@param id = id of Comment.
	#	
	#	@TODO ERROR CHECKING.
	###
	def rate_comment(self, change_in_reputation, id, username):
		cursor.execute("SELECT * FROM Rates WHERE username = ? AND comment_id = ?", (username, id))
		curr_user_data = cursor.fetchone()

		cursor.execute("SELECT * FROM SpotPostComments WHERE id = ?", (id,))
		spotpost_data = cursor.fetchone()

		if not curr_user_data and spotpost_data:		#If the user HASN'T upvoted, and the comment exists.
			comment_creator = spotpost_data[6]
			cursor.execute("UPDATE SpotPostComments SET reputation = reputation + ? WHERE id = ?", (change_in_reputation, id))					# Increase rep of comment
			cursor.execute("INSERT INTO Rates (username, spotpost_id) VALUES (?, ?)", (username, id))	# Insert relation into Rates
			cursor.execute("UPDATE Users SET reputation = reputation + ? WHERE username = ?", (change_in_reputation, comment_creator))	# Increase rep of Creator
			connect.commit()
			return "SUCCESS"
		else:
			return "ERROR USER ALREADY VOTED OR SPOTPOST DOESN'T EXIST"

	###
	#
	#	Updates a given spotpost with new values. Must be logged in as Admin.
	#
	#	JSON must be constructed following convention below (REQUIRES AT LEAST ONE TO BE ENTERED):
	#	"id"				: "id of spotpost"
	#	"content"   		: "text of spotpost"
	#	"username"  		: "username of person making spotpost"  	NOTE: MAY BE DEPRECEATED IN FUTURE VERSIONING
	#	"latitude" 			: "latitude of spotpost"
	#	"longitude" 		: "longitude of spotpost"
	#	"reputation"   		: "custom starting reputation" 				NOTE: WILL BE DEPRECEATED IN FUTURE VERSIONING. 
	#
	###
	def update_post(self, form):
		query = "UPDATE SpotPosts SET "
		query_data = ()

		first_data  = True
		post_id 	= form['id']
		content 	= form['content']
		username 	= form['username']
		latitude 	= form['latitude']
		longitude 	= form['longitude']
		reputation 	= form['reputation']
		
		where_query = "WHERE id = ?"

		if content:
			query = query + "content = ?"
			query_data = query_data + (content,)
			first_data = False
		if username:
			if first_data:
				query = query + "username = ?"
				first_data = False
			else:
				query = query + ", username = ?"
			query_data = query_data + (username,)
		if latitude:
			if first_data:
				query = query + "latitude = ?"
				first_data = False
			else:
				query = query + ", latitude = ?"
			query_data = query_data + (latitude,)
		if longitude:
			if first_data:
				query = query + "longitude = ?"
				first_data = False
			else:
				query = query + ", longitude = ?"
			query_data = query_data + (longitude,)
		if reputation:
			if first_data:
				query = query + "reputation = ?"
				first_data = False
			else:
				query = query + ", reputation = ?"
			query_data = query_data + (reputation,)

		if first_data:
			return "ERROR MUST ENTER IN ONE VALUE."
		
		query = query + where_query
		query_data = query_data + (id,)

		cursor.execute(query, query_data)
		connect.commit()


	###
	#
	#	Deletes a spotpost with id provided.
	#
	#	@param id = id of spotpost to delete.
	#
	###
	def delete_post(self, id):
		cursor.execute("DELETE FROM SpotPosts WHERE id = ?", (id,))
		connect.commit()

	###
	#
	#	Deletes a comment with id provided.
	#
	#	@param id = id of comment to delete.
	#
	###
	def delete_comment(self, id):
		cursor.execute("DELETE FROM SpotPostComments WHERE id = ?", (id,))
		connect.commit()