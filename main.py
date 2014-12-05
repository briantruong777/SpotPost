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
from resource.dbmanager import DBManager

#from comments 		import add_comment
import os
import sqlite3
import math

# For decoding JSON request data. Strings come in unicode format. Possibly useless :(.
from unidecode import unidecode

# If Python2.6, simplejson is better than json, but in Python2.7, simplejson became json
try: import simplejson as json
except ImportError: import json

manager = DBManager()

app = Flask(__name__)

# For logging to a file called "spotpost_log"
import logging
from logging import FileHandler
file_handler = FileHandler("spotpost_log")
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)
# how to log manually:
#   app.logger.warning("%s", "hello!")


###
# Equation for scoring posts.
# 
# delta_lon
###

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
@app.route('/followerlist/<username>')
def get_follower_list(username):
	data = manager.get_list_of_followers(username)

	return json.dumps(data)

###
#
# Allows a user to follow another user.
# @TODO ERROR CHECKING FOR THIS. 
#
###
@app.route('/_follow/<username>')
def follow_user(username):
	curr_user = session['username']
	manager.insert_follow_relation(curr_user, username)

	#TEMP MUST REPLACE WITH REAL REDIRECT
	return redirect(url_for('index'))

###
#
# Allows a user to unfollow another user.
# @TODO ERROR CHECKING FOR THIS. 
#
###
@app.route('/_unfollow/<username>')
def unfollow_user(username):
	curr_user = session['username']
	manager.delete_follow_relation(curr_user, username)

	return redirect(url_for('index'))

###
# 
# Allows clientside to make a POST request to add data to the server database.
# SpotPosts(id, content, title, reputation, longitude, latitude, username, time)
# 
# JSON must be constructed following convention below (REQUIRED DATA IS DENOTED WITH A *):
# * "content"   		: "text of spotpost"
# * "title" 			: "title of spotpost"
# "username"  			: "username of person making spotpost"  	NOTE: MAY BE DEPRECEATED IN FUTURE VERSIONING
# * "latitude" 			: "latitude of spotpost"
# * "longitude" 		: "longitude of spotpost"
# "reputation"   		: "custom starting reputation" 				NOTE: WILL BE DEPRECEATED IN FUTURE VERSIONING. 
#
###
@app.route('/spotpost/_post', methods = ['POST'])
def post_spotpost():
	data = request.data
	decoded_data = json.loads(data)
	if 'username' in session.keys():
		username = session['username']
		error_dict = manager.insert_spotpost(decoded_data, username)
	else:
		error_dict = manager.insert_spotpost(decoded_data, None)

	return json.dumps(error_dict)

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
@app.route('/comment/_post', methods = ['POST'])
def post_comment():
	manager.insert_comment(request.form, session['username'])

###
# 
# Allows clientside to make a GET request to get spotposts around a center latitude longitude point.
# Gets best top_count amount of spotposts. 10 default.
# Uses a radius provided, 100 meters default.
# 
# URL must be constructed following convention below. Latitude and longitude are required:
# URL?/&latitude 	 = latitude of center point of bounding square.
# URL&longitude   	 = longitude of center point of bounding square.
# URL?/&radius         = "radius" of bounding square.
#
###
@app.route('/spotpost/_getlocation')
def get_spotpost_by_location():
	error_dict 	= {}
	latitude 	= request.args.get('latitude')
	longitude 	= request.args.get('longitude')
	radius 		= request.args.get('radius')
	top_count 	= request.args.get('top_count')

	if not radius:
		radius = 100
	if not top_count:
		top_count = 10

	if not latitude or not longitude:
		error_dict['error'] = {"code" : "1092", "message" : "Location not provided."}
		return json.dumps(error_dict)

	max_long, max_lat, min_long, min_lat = calc_bounding_coords(float(longitude), float(latitude), float(radius))

	data = manager.location_search_spotpost(min_lat, max_lat, min_long, max_long, top_count)
	return json.dumps(data)

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
# URL?/&id 		 	 = desired spotpost ID.
# URL?/&latitude 	 = latitude of center point of bounding square. 		NOTE: ALL 3 VARIABLES MUST BE PROVIDED TO USE BOUNDING SQUARE. OTHERWISE SEARCH IGNORES IT.
# URL&longitude   	 = longitude of center point of bounding square.
# URL?/&radius         = "radius" of bounding square.
# URL?/&lock_value   = Lock status of spotposts. (0 = All posts locked or unlocked, 1 = All locked posts, 2 = All unlocked posts).
# URL?/&unlock_posts = Unlock all returned posts for the user. 0 or nothing = do not unlock posts, everything else = unlock posts. 
#
#	SEPERATE OUT FUNCTIONALITY.
###
@app.route('/spotpost/_get')
def get_spotpost():
	min_reputation 		= request.args.get('min_reputation')
	max_reputation	 	= request.args.get('max_reputation')
	username 			= request.args.get('username')
	post_id 			= request.args.get('id')
	lock_value			= request.args.get('lock_value')
	unlock_posts	 	= request.args.get('unlock_posts')

	data = manager.select_spotpost(min_reputation, max_reputation, username, post_id, lock_value)

	if not username and 'username' in session:
		username = session['username']

	if unlock_posts and username:
		unlock_posts = int(unlock_posts)
		if unlock_posts:
			#data is an array of dictionaries. 
			for row in data:
				unlock_id = row['id']
				manager.insert_unlock_relation(username, unlock_id)

	return json.dumps(data)

###
#
#	Upvotes a given comment.
#	
#	@param id = id of comment.
#
###
@app.route('/comment/_upvote/<id>')
def upvote_comment(id):
	if 'username' in session:
		return manager.rate_comment(1, id, session['username'])
	else:
		return "MUST BE LOGGED IN TO UPVOTE."

###
#
#	Downvotes a given comment.
#	
#	@param id = id of comment.
#
###
@app.route('/comment/_downvote/<id>')
def downvote_comment(id):
	if 'username' in session:
		return manager.rate_comment(-1, id, session['username'])
	else:
		return "MUST BE LOGGED IN TO DOWNVOTE."

###
#
#	Upvotes a given spotpost.
#	
#	@param id = id of SpotPost.
#
###
@app.route('/spotpost/_upvote/<id>')
def upvote_spotpost(id):
	return manager.rate_post(1, id, session['username'])

###
#
#	Downvotes a given spotpost.
#	
#	@param id = id of SpotPost.
#
###
@app.route('/spotpost/_downvote/<id>')
def downvote_spotpost(id):
	return manager.rate_post(-1, id, session['username'])

###
#
#	Deletes a given spotpost. Must be logged in as Admin
#	
#	@param id = id of SpotPost.
#
###
@app.route('/spotpost/_delete/<id>')
def delete_spotpost(id):
	error_dict = {}
	if 'privilege' in session:
		manager.delete_post(id)
		error_dict['error'] = {"code" : "1000", "message" : "Success."}
		return json.dumps(error_dict);
	else:
		error_dict['error'] = {"code" : "1032", "message" : "Admin privileges required."}
		return json.dumps(error_dict);

###
#
#	Updates a given spotpost with new values. Must be logged in as Admin.
#
#	JSON must be constructed following convention below (REQUIRES AT LEAST ONE TO BE ENTERED):
#	id field is REQUIRED.
# 
# 	"id"				: "id of spotpost"
#	"content"   		: "text of spotpost"
#	"username"  		: "username of person making spotpost"  	NOTE: MAY BE DEPRECEATED IN FUTURE VERSIONING
#	"latitude" 			: "latitude of spotpost"
#	"longitude" 		: "longitude of spotpost"
#	"reputation"   		: "custom starting reputation" 				NOTE: WILL BE DEPRECEATED IN FUTURE VERSIONING. 
#
###
@app.route('/spotpost/_update', methods = ['POST'])
def update_spotpost():
	error_dict = {}
	if session['privilege'] and request.form['id']:
		manager.update_post(request.form)
		error_dict['error'] = {"code" : "1000", "message" : "Success."}
		return json.dumps(error_dict);
	else:
		error_dict['error'] = {"code" : "1032", "message" : "Admin privileges required."}
		return json.dumps(error_dict);

###
#
#	Logs the user in if the user exists and the password is correct.
#
###
@app.route('/login', methods =['GET', 'POST'])
def login():
	if request.method == 'POST':
		data = request.data
		decoded_data = json.loads(data)
		username = decoded_data['username']
		password = decoded_data['password']

		valid_login = manager.validate_user(username, password)
		
		if valid_login:
			session['username'] = username
			session['privilege'] = manager.get_privilege(username)

			error_dict = {"code" : "1000", "message" : "Success."}
			return json.dumps(error_dict)
		else:
			error_dict = {"code" : "1050", "message" : "Invalid login information."}
			return json.dumps(error_dict)
	
	return render_template('login.html')

###
#
#	Registers the user into the Database.
#
###
@app.route('/_register', methods =['POST'])
def register():
	data = request.data
	decoded_data = json.loads(data)
	username = decoded_data['username']
	password = decoded_data['password']

	retval = manager.insert_user(username, password)

	#Log user in. 
	session['privilege'] = manager.get_privilege(username)
	session['username'] = username

	return json.dumps(retval)

###
#
# Promotes a user to an admin.
# @param username = user to be promoted.
#
###
@app.route('/promote/<username>')
def promote_user(username):
	error_dict = {}

	if 'username' in session:
		curr_user = session['username']
	else:
		error_dict['error'] = {"code" : "1087", "message" : "Not logged in."}

	if curr_user:
		privilege = manager.get_privilege(curr_user)
		if privilege:
			manager.update_privilege(username, 1)
		else:
			error_dict['error'] = {"code" : "1032", "message" : "Admin privileges required."}
			return json.dumps(error_dict)

###
#
# Quick debugging fix to check if there is a user or not.
#
###
@app.route('/_userstatus')
def is_logged_in():
	data = {}
	if 'username' in session:
		data = manager.get_user(session['username'])
		data['error'] = {"code" : "1000", "message" : "Success."}
	else:
		data['error'] = {"code" : "1087", "message" : "Not logged in."}

	return json.dumps(data)

###
#
#	Logs the user out.
#
###
@app.route('/_logout')
def logout():
	session.pop('username', None)
	session.pop('privilege', None)
	return redirect(url_for('index'))

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
	if 'username' in session:
		return render_template('index.html')
	else:
		return redirect(url_for('login'))

if __name__ == '__main__':
	# Runs on port 5000 by default
	# url: "localhost:5000"
	# Secret Key for sessions.
	# @TODO Change to random key.
	app.secret_key = 'Bv`L>?h^`qeQr6f7c$DK.E-gvMXZR+'
	app.run(host="0.0.0.0")
	manager.close_connection()
