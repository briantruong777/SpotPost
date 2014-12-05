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
#Need to use log10.
import math
from passlib.hash 	import sha256_crypt
from unidecode 		import unidecode

connect = sqlite3.connect('data.db')
cursor = connect.cursor()

###
#
# Gets the sign of the rating for scoring purposes.
# 
# @param rating = rating whose sign is to be determined.
# @return 1 if positive, -1 if negative, 0 if neither.
#
###
def score_sign(rating):
	return 1 if rating > 0 else -1 if rating < 0 else 0

###
#
# Returns the log10 of a score in the database.
# Added as a function in the database. Minimum rating being 1.
# 
# @param rating = rating to be used for score generation.
# @return log10 of either 1 or rating, whichever is higher.
###
def log_score(rating):
	return math.log10(max(rating , 1))

###
#
# Builds the JSON data for comments to be transmitted to the client
# along with spotpost information. Comments are an array of dictionaries.
# JSON is built as follows
#--------------------------
# 'id' 			: id of comment.
# 'message_id' 	: id of spotpost linked to comment.
# 'content'		: content of comment.
# 'username' 	: username of creator.
# 'time' 		: date and time comment was posted.
#
###
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
		comment_dict['reputation'] = row[4]
		comment_dict['time'] 		= unidecode(row[5])

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
	user_dict = {}
		
	for row in rawdata:
		user_dict['username'] 		= unidecode(row[0])
		user_dict['profile_pic_id'] = row[2]
		user_dict['reputation']		= row[3]
		user_dict['privilege'] 		= row[4]

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
	# Drops all tables.
	#
	###
	def drop_tables(self):
		cursor.execute("DROP TABLE SpotPosts")
		cursor.execute("DROP TABLE SpotPostComments")
		cursor.execute("DROP TABLE Users")
		cursor.execute("DROP TABLE Follows")
		cursor.execute("DROP TABLE Photos")
		cursor.execute("DROP TABLE Rates")
		cursor.execute("DROP TABLE Unlocks")

		connect.commit()

	###
	#
	# Closes the connection, used when closing the server.
	#
	###
	def close_connection(self):
		connect.close()

	def create_tables(self):
		#SpotPosts(id, content, photo_id, reputation, longitude, latitude, visibility, user_id, time)
		cursor.execute("CREATE TABLE IF NOT EXISTS SpotPosts(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, content TEXT, title TEXT," + 
			"reputation INTEGER DEFAULT 0, longitude REAL NOT NULL, latitude REAL NOT NULL," + 
			" username TEXT, time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)")

		#SpotPostComments(id, message_id, content, username, reputation, time)
		cursor.execute("CREATE TABLE IF NOT EXISTS SpotPostComments(id INTEGER PRIMARY KEY AUTOINCREMENT, message_id INTEGER, content TEXT,"
						+ "username TEXT, reputation INTEGER DEFAULT 0, time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)")
		
		#Users(username, password, profile_pic, reputation)
		#Privilege: 0 = USER, 1 = ADMIN
		cursor.execute("CREATE TABLE IF NOT EXISTS Users(username varchar(24) PRIMARY KEY, password TEXT, profile_pic_id INTEGER DEFAULT -1,"
		 				+ " reputation INTEGER DEFAULT 0, privilege INTEGER DEFAULT 0)")
		
		#Follows(follower_name, followee_name)
		cursor.execute("CREATE TABLE IF NOT EXISTS Follows(follower_name TEXT, followee_name TEXT)")

		#Photos(id, photo)
		cursor.execute("CREATE TABLE IF NOT EXISTS Photos(id INTEGER PRIMARY KEY AUTOINCREMENT, photo_url TEXT)")

		#Rates(username, spotpost_id, comment_id)
		cursor.execute("CREATE TABLE IF NOT EXISTS Rates(username TEXT, spotpost_id INTEGER DEFAULT -1 NOT NULL, comment_id INTEGER DEFAULT -1 NOT NULL)")

		#Unlocks(username, spotpost_id)
		cursor.execute("CREATE TABLE IF NOT EXISTS Unlocks(username TEXT, spotpost_id INTEGER)")

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
	#	Unlocks(username, spotpost_id)
	#
	###
	def __init__(self):
		self.create_tables()

		#Creates the functions we need for the scoring algorithm
		connect.create_function("log", 1, log_score)
		connect.create_function("sign", 1, score_sign)

	###
	#
	# Inserts in an unlock relationship. Once unlocked that spotpost is completely viewable by the user.
	# @param username = username of user who unlocked the spotpost.
	# @param id = id of unlocked spotpost.
	#
	###
	def insert_unlock_relation(self, username, id):
		cursor.execute("SELECT * FROM Unlocks WHERE username = ? AND spotpost_id = ?", (username, id))
		exists = cursor.fetchone()
		if not exists:
			cursor.execute("INSERT INTO Unlocks(username, spotpost_id) VALUES (?,?)", (username, id))
			connect.commit()
		else:
			return "ERROR RELATION ALREADY EXISTS"

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
	# * "title"				: "title of spotpost"
	# "username"  			: "username of person making spotpost"  	NOTE: MAY BE DEPRECEATED IN FUTURE VERSIONING
	# * "latitude" 			: "latitude of spotpost"
	# * "longitude" 		: "longitude of spotpost"
	# "reputation"   		: "custom starting reputation" 				NOTE: WILL BE DEPRECEATED IN FUTURE VERSIONING. 
	#
	###
	def insert_spotpost(self, form, client_username):
		content 	= form['content']
		title 		= form['title']
		latitude 	= form['latitude']
		longitude 	= form['longitude']
		if 'reputation' in form.keys():
			reputation 	= form['reputation']
		else:
			reputation = None

		if 'username' in form.keys():
			client_username = form['username']

		if reputation:
			cursor.execute("INSERT INTO SpotPosts(content, title, reputation, longitude, latitude, username) VALUES (?,?,?,?,?,?)", (content, title, reputation, longitude, latitude, client_username))
		else:
			cursor.execute("INSERT INTO SpotPosts(content, title, longitude, latitude, username) VALUES (?,?,?,?,?)", (content, title, longitude, latitude, client_username))

		connect.commit()
		return {"error": {"code": "1000", "message" : "Success."}}

	###
	#
	# Inserts a user into the Database. Encrypts the password provided using sha256_crypt. 
	# 
	# Provided JSON must follow this form (ALL DATA IS REQUIRED)
	# "username"	: "username of user"
	# "password"	: "password of user"
	#
	##
	def insert_user(self, username, password):
		cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
		exists = cursor.fetchone()

		if not exists:
			store_hash_pass(username, password)
		else:
			error_dict = {"code" : "1055", "message" : "Username already in use."}
			return error_dict

		error_dict = {"code" : "1000" , "message" : "Success."}
		return error_dict		

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

		if 'reputation' in form.keys():
			reputation = form['reputation']
		else:
			reputation = None

		if 'username' in form.keys():
			client_username = form['username']

		if reputation: 
			cursor.execute("INSERT INTO SpotPostComments(message_id, content, username, reputation) VALUES (?,?,?,?)", (spotpost_id, content, client_username, reputation))
		else:
			cursor.execute("INSERT INTO SpotPostComments(message_id, content, username) VALUES (?,?,?)", (spotpost_id, content, client_username))

		connect.commit()

		error_dict = {"code" : "1000", "message" : "Success"}
		return error_dict


	###
	#
	# Returns a JSON containing an array of users who are following 
	# the user with username. 
	#
	# @TODO CURRENTLY ONLY RETURNS LIST OF USERNAMES MODIFY TO RETURN LIST OF USER ARRAYS.
	#
	# @param username = username of followee
	#
	###
	def get_list_of_followers(self, username):
		cursor.execute("SELECT * FROM Follows WHERE followee_name = ?", (username,))
		rawdata = cursor.fetchall()
		data = []

		for row in rawdata:
			data.append(rawdata[0])

		return data

	###
	#
	# Gets the top `top_count` posts in an area surrounded by the 4 location variables.
	#
	# @param min_latitude = minimum latitude to search inside.
	# @param max_latitude = maximum latitude to search inside.
	# @param min_longitude = minimum longitude to search inside.
	# @param max_longitude = maximum longitude to search inside.
	# @param top_count = number of posts to return.
	#####
	## Taken from http://amix.dk/blog/post/19588. Reddit's algorithm for determining scores.
	#### 
	#	Equation: 
	#	s = score(ups, downs)
    #	order = log(max(abs(s), 1), 10)
    #	sign = 1 if s > 0 else -1 if s < 0 else 0
    #	seconds = epoch_seconds(date) - 1134028003
    #	return round(order + sign * seconds / 45000, 7)
	###
	def location_search_spotpost(self, min_latitude, max_latitude, min_longitude, max_longitude, top_count):
		#Time in seconds since 1/1/1970 to be used as a starting time, This is December 8 2005. Its what reddit uses so, when in rome.
		start_time = 1134028003

		equation = "(round(log(reputation) + sign(reputation) * (strftime('%s',time) - ?)/45000.0, 7))"
		query = "SELECT *, " + equation + " AS score FROM SpotPosts WHERE latitude <= ? AND latitude >= ? AND longitude >= ? AND longitude <= ? ORDER BY score DESC LIMIT ?"
		query_data = (start_time, max_latitude, min_latitude, min_longitude, max_longitude, top_count)

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
			data_dict['user'] 		= build_username_JSON(unidecode(row[6]))
			data_dict['time'] 		= unidecode(row[7])
			data_dict['comments'] 	= build_comments_JSON(row[0])

			data.append(data_dict)

		return data

	###
	#  
	# Allows clientside to make a GET request to get spotposts from the server database.
	# 
	# NOTE: TO ADD MORE ARGUMENTS THE CONVENTION ?min_reputation=10&max_reputation=100 MUST BE FOLLOWED.
	# NOTE: TO FURTHER THE POINT ABOVE I HAVE WRITTEN ?/& TO SHOW THAT ITS ONE OR THE OTHER DEPENDING ON PREVIOUS DATA.
	#
	# URL must be constructed following convention below (NOT ALL DATA IS REQUIRED):
	# URL?min_reputation 	= minimum reputation to search for. 
	# URL?/&max_reputation 	= maximum reputation to search for. 	
	# URL?/&id 		 	= desired spotpost ID.
	# URL?/&latitude 	= latitude of center point of bounding square. 		NOTE: ALL 3 VARIABLES MUST BE PROVIDED TO USE BOUNDING SQUARE. OTHERWISE SEARCH IGNORES IT.
	# URL&longitude   	= longitude of center point of bounding square.
	# URL&radius        = "radius" of bounding square.
	# URL?/&lock_value  = Lock status of spotposts. (0 = All posts locked or unlocked, 1 = All locked posts, 2 = All unlocked posts).
	#
	###
	def select_spotpost(self, min_reputation, max_reputation, username, post_id, lock_value):
		query = "SELECT * FROM SpotPosts"
		query_data = ()
		where_query = False

		if lock_value:
			lock_value = int(lock_value)
			if lock_value == 1:
				query = query + " INNER JOIN Unlocks ON SpotPosts.id <> Unlocks.spotpost_id "
			else:
				query = query + " INNER JOIN Unlocks ON SpotPosts.id = Unlocks.spotpost_id "

		if post_id:
			query = query + " WHERE id = ?"
			query_data = query_data + (post_id,)
			where_query = True
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
			data_dict['user'] 		= build_username_JSON(unidecode(row[6]))
			data_dict['time'] 		= unidecode(row[7])
			data_dict['comments'] 	= build_comments_JSON(row[0])

			data.append(data_dict)

		return data

	###
	#
	# Returns information about a given user. Returns it in dictionary format according
	# to the following schema.
	#---------------------------------------
	# "username" 	: username of user.
	# "reputation"	: reputation of user.
	# "privilege" 	: privilege level of user.
	#
	###
	def get_user(self, username):
		data = build_username_JSON(username)
		return data

	###
	#
	# Gets the privileges of the user.
	# @param username = username of user whos priviliges are to be returned.
	# @return 0 if regular user, 1 if admin.
	#
	###
	def get_privilege(self, username):
		cursor.execute("SELECT privilege FROM Users WHERE username = ?", (username,))
		privilege = cursor.fetchone()

		return int(privilege[0])

	###
	#
	# Updates the privileges of the user.
	# @param username = username of user whos priviliges are to be changed.
	# @param newpriv = new privilege level of user.
	# @return 0 if regular user, 1 if admin.
	#
	###
	def update_privilege(self, username, newpriv):
		error_dict = {}
		cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
		data = cursor.fetchall()
		if data:
			cursor.execute("UPDATE Users SET privilege = ? WHERE username = ?", (newpriv, username))
			error_dict['error'] = {"code": "1000", "message" : "Success."}
		else:
			error_dict['error'] = {"code" : "9110", "message" : "User does not exist."}

		connect.commit()

		return error_dict

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
		cursor.execute("SELECT password FROM Users WHERE username = ?", (username,))
		data = cursor.fetchone()

		if data:
			db_hash = data[0]
			if(sha256_crypt.verify(password, db_hash)):
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

		cursor.execute("SELECT username, message_id FROM SpotPostComments WHERE id = ?", (id,))
		spotpost_data = cursor.fetchone()

		if not curr_user_data and spotpost_data:		#If the user HASN'T upvoted, and the comment exists.
			comment_creator = spotpost_data[0]
			spotpost_id = spotpost_data[1]

			cursor.execute("UPDATE SpotPostComments SET reputation = reputation + ? WHERE id = ?", (change_in_reputation, id))					# Increase rep of comment
			cursor.execute("INSERT INTO Rates (username, spotpost_id, comment_id) VALUES (?, ?, ?)", (username, spotpost_id, id))	# Insert relation into Rates
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
		if 'content' in form.keys():
			content	= form['content']
		else:
			content = None

		if 'username' in form.keys():
			username = form['username']
		else:
			username = None

		if 'latitude' in form.keys():
			latitude = form['latitude']
		else:
			latitude = None

		if 'longitude' in form.keys():
			longitude = form['longitude']
		else:
			longitude = None

		if 'reputation' in form.keys():
			reputation 	= form['reputation']
		else:
			reputation = None

		if 'title' in form.keys():
			title = form['title']
		else:
			title = None

		where_query = " WHERE id = ?"

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

		if title:
			if first_data:
				query = query + "title = ?"
				first_data = False
			else:
				query = query + ", title = ?"
			query_data = query_data + (title,)

		if first_data:
			return "ERROR MUST ENTER IN ONE VALUE."
		
		query 		= query + where_query
		query_data 	= query_data + (post_id,)

		cursor.execute(query, query_data)
		connect.commit()

	###
	#
	# Deletes all comments contained inside the Spotpost with id = id.
	#
	# id = id of spotpost whose comments will be deleted.
	#
	###
	def delete_comments_by_spotpost(self, id):
		cursor.execute("DELETE FROM SpotPostComments WHERE message_id = ?", (id,))
		connect.commit()

	###
	#
	# Deletes all rates relations associated with the deleted spotpost.
	#
	# id = id of spotpost whose rates will be deleted.
	#
	###
	def delete_spotpost_rates(self, id):
		cursor.execute("DELETE FROM Rates WHERE spotpost_id = ?", (id,))
		connect.commit()

	###
	#
	# Deletes all unlocks relations associated with the deleted spotpost.
	#
	# id = id of spotpost whose unlocks will be deleted.
	#
	###
	def delete_spotpost_unlocks(self, id):
		cursor.execute("DELETE FROM Unlocks WHERE spotpost_id = ?", (id,))
		connect.commit()

	###
	#
	#	Deletes a spotpost with id provided.
	#
	#	@param id = id of spotpost to delete.
	#
	#	@TODO Make sure it deletes dependent data from DB.
	###
	def delete_post(self, id):
		cursor.execute("DELETE FROM SpotPosts WHERE id = ?", (id,))
		self.delete_comments_by_spotpost(id)
		self.delete_spotpost_rates(id)
		self.delete_spotpost_unlocks(id)

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
