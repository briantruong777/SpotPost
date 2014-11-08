'''
'	
'	Spotpost serverside. Provides all functionality for the website and application.
'	Allows for location based notes to be viewed and made by users.
'
'	@author Jakub Wlodarczyk
'	@author Brian Truong
'	@author Nate Norgaard
'	@author Adam Davis
' 
'''

from flask 				import Flask, session, request, abort, render_template, redirect, url_for, escape
from passlib.hash 		import sha256_crypt
import resource.dbmanager

#from comments 		import add_comment
import os
import sqlite3

# For decoding JSON request data. Strings come in unicode format. Possibly useless :(.
from unidecode import unidecode

# If Python2.6, simplejson is better than json, but in Python2.7, simplejson became json
try: import simplejson as json
except ImportError: import json

connect = sqlite3.connect('data.db')
cursor = connect.cursor()
data_manager = DBManager()

app = Flask(__name__)

# For logging to a file called "spotpost_log"
import logging
from logging import FileHandler
file_handler = FileHandler("spotpost_log")
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

###
#
# Calculates bounding latitude and longitude.
# Bounds by approximation using a square.
#
# @param lon = longitude of center point.
# @param lat = latitude of center point.
# @param radius = radius in meters of circle contained within square.
#
# @return maximum longitude in bounding square.
# @return maximum latitude in bounding square.
# @return minimum longitude in bounding square.
# @return minimum latitude in bounding square.
#
###
def calc_bounding_coords(lon, lat, radius):
	km_radius = radius / 1000

	km_per_long_deg = 111.320 * math.cos(lat / 180.0 * math.pi)

	deltaLat  = km_radius / 111.1
	deltaLong = km_radius / km_per_long_deg

	min_lat  = lat - deltaLat
	max_lat  = lat + deltaLat
	min_long = lon - deltaLong
	max_long = lon + deltaLong


	return max_long, max_lat, min_long, min_lat

def build_comments_JSON(curr_id):
	comments = []
	cursor.execute("SELECT * FROM SpotPostComments WHERE message_id = ?", (curr_id,))
	data = cursor.fetchall

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
	userinfo = []
	cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
	rawdata = cursor.fetchall

	for row in rawdata:
		user_dict = {}
		user_dict['username'] 		= unidecode(row[0])
		user_dict['profile_pic_id'] = row[2]
		user_dict['reputation']		= row[3]

		userinfo.append(user_dict)

	return userinfo

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
def initDB():
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
@app.route('/spotpost/_post', methods = ['POST'])
def post_spotpost():
	content = unidecode(request.form['content'])
	title = unidecode(request.form['title'])
	username = unidecode(request.form['username'])
	longitude = float(unidecode(request.form['latitude']))
	latitude = float(unidecode(request.form['longitude']))
	reputation = int(request.form['reputation'])
	cursor.execute("INSERT INTO SpotPosts(content, title, reputation, longitude, latitude, username) VALUES (?,?,?,?,?)", (content, reputation, longitude, latitude, username))
	connect.commit()

	return "Success"

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
#
###
@app.route('/spotpost/_get')
def get_spotpost():
	query 			= "SELECT * FROM SpotPosts"
	query_data 		= ()
	where_query 	= False
	min_reputation 	= request.args.get('min_reputation')
	max_reputation 	= request.args.get('max_reputation')
	username 		= request.args.get('username')
	post_id 		= request.args.get('id')
	latitude 		= request.args.get('latitude')
	longitude 		= request.args.get('longitude')
	radius 			= request.args.get('radius')

	if post_id:
		query = query + "WHERE id = ?"
		query_data = query_data + (post_id,)
		where_query = True
	if longitude and latitude and radius:
		max_longitude, max_latitude, min_longitude, min_latitude = calc_bounding_coords(longitude, latitude, radius)
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

	return json.dumps(data)

###
#
#
#
###
@app.route('/comment/_post', methods = ['POST'])
def post_comment():
	content = unidecode(request.form['content'])
	title = unidecode(request.form['title'])
	username = unidecode(request.form['username'])
	longitude = float(unidecode(request.form['latitude']))
	latitude = float(unidecode(request.form['longitude']))
	reputation = int(request.form['reputation'])
	cursor.execute("INSERT INTO SpotPosts(content, title, reputation, longitude, latitude, username) VALUES (?,?,?,?,?)", (content, reputation, longitude, latitude, username))
	connect.commit()

	return "Success"

###
#
#	Upvotes a given spotpost.
#	
#	@param id = id of SpotPost.
#
###
@app.route('/spotpost/_upvote/<id>')
def upvote_spotpost(id):
	session['username'] = "Admin"
	return rate_post(1, id)

###
#
#	Downvotes a given spotpost.
#	
#	@param id = id of SpotPost.
#
###
@app.route('/spotpost/_downvote/<id>')
def downvote_spotpost(id):
	session['username'] = "Admin"
	return rate_post(-1, id)

###
#
#	Helper function for rating. Changes reputation of SpotPost by change_in_reputation
#
#	@param change_in_reputation = number to be added to reputation.
#	@param id = id of SpotPost.
#
###
def rate_post(change_in_reputation, id):
	if 'username' in session:
		cursor.execute("SELECT * FROM Rates WHERE username = ? AND spotpost_id = ?", (session['username'], id))
		curr_user_data = cursor.fetchone()

		cursor.execute("SELECT * FROM SpotPosts WHERE id = ?", (id,))
		spotpost_data = cursor.fetchone()
		spotpost_creator = spotpost_data[6]

		if not curr_user_data and spotpost_data:		#If the user HASN'T upvoted, and the SpotPost exists.
			cursor.execute("UPDATE SpotPosts SET reputation = reputation + ? WHERE id = ?", (change_in_reputation, id))					# Increase rep of SpotPost
			cursor.execute("INSERT INTO Rates (username, spotpost_id) VALUES (?, ?)", (session['username'], id))	# Insert relation into Rates
			cursor.execute("UPDATE Users SET reputation = reputation + ? WHERE username = ?", (change_in_reputation, spotpost_creator))	# Increase rep of Creator
			connect.commit()
			return "SUCCESS"
		else:
			return "ERROR USER ALREADY VOTED OR SPOTPOST DOESN'T EXIST"
	else:
		return "ERROR USER NOT LOGGED IN"
###
#
#	Deletes a given spotpost. Must be logged in as Admin
#	
#	@param id = id of SpotPost.
#
###
@app.route('/spotpost/_delete/<id>')
def delete_spotpost(id):
	if session['username'] is "Admin":
		cursor.execute("DELETE FROM SpotPosts WHERE id = ?", (id,))
		return "SUCCESS"
	else:
		return "ERROR NOT LOGGED IN AS ADMIN"

###
#
#	Logs the user in if the user exists and the password is correct.
#
###
@app.route('/_login', methods =['GET', 'POST'])
def login():
	if request.method == 'POST' and 'username' in request.form.keys():
		client_password = request.form['password']

		cursor.execute("SELECT * FROM Users WHERE username = ?", (client_username,))
		data = cursor.fetchone()

		if data:
			db_hash = data[1]
			if(sha256_crypt.verify(client_password, db_hash)):
				session['username'] = request.form['username']
				return redirect(url_for('index'))
			else:
				return "INVALID PASSWORD"
		else:
			return "INVALID USERNAME"
	else:
		return "ERROR"
	
	#@TODO REPLACE WITH LOGIN FORM
	return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
    '''

###
#
#	Logs the user out.
#
###
@app.route('/_logout')
def logout():
	session.pop('username', None)
	return "LOGGED OUT."

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

###
#
#	Registers the user into the Database.
#
###
@app.route('/_register', methods =['GET', 'POST'])
def register():
	if request.method == 'POST':
		client_username = request.form['username']
		client_password = request.form['password']

		store_hash_pass(client_username, client_password)

	#@TODO REPLACE WITH REGISTRATION FORM
	return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
    '''

###
#
#	Shows homepage, simply serves as a way to get to other pages.
#
###
@app.route('/')
def index():
	#if 'username' in session:
	#	return 'Logged in as %s' % escape(session['username'])
	#return 'You are not logged in'
	session['username'] = "Admin"
	return render_template('index.html')

initDB()

if __name__ == '__main__':
	# Runs on port 5000 by default
	# url: "localhost:5000"
	# Secret Key for sessions.
	app.secret_key = 'Bv`L>?h^`qeQr6f7c$DK.E-gvMXZR+'
	app.run(host="0.0.0.0")
	connect.close()