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
from Crypto.PublicKey 	import RSA
from Crypto 			import Random

#from comments 		import add_comment
import os
import sqlite3

# For decoding JSON request data. Strings come in unicode format. Possibly useless :(.
from unidecode import unidecode

# If Python2.6, simplejson is better than json, but in Python2.7, simplejson became json
try: import simplejson as json
except ImportError: import json

manager = DBManager()

# RSA Encryption Key.
random_generator = Random.new().read
key = RSA.generate(1024, random_generator)

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

###
#
# Gets the public key required for encryption.
#
# Data is sent as a JSON with {"key" : public key}
#
###
@app.route('/_publickey')
def get_public_key():
	pub_keydict = {"key" : key.publickey()}

	return json.dumps(pub_keydict)

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
# "username"  			: "username of person making spotpost"  	NOTE: MAY BE DEPRECEATED IN FUTURE VERSIONING
# * "latitude" 			: "latitude of spotpost"
# * "longitude" 		: "longitude of spotpost"
# "reputation"   		: "custom starting reputation" 				NOTE: WILL BE DEPRECEATED IN FUTURE VERSIONING. 
#
###
@app.route('/spotpost/_post', methods = ['POST'])
def post_spotpost():
	return manager.insert_spotpost(request.form, session['username'])

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
# URL&radius         = "radius" of bounding square.
# URL?/&lock_value   = Lock status of spotposts. (0 = All posts locked or unlocked, 1 = All locked posts, 2 = All unlocked posts).
# URL?/&unlock_posts = Unlock all returned posts for the user. 0 or nothing = do not unlock posts, everything else = unlock posts. 
#
###
@app.route('/spotpost/_get')
def get_spotpost():
	min_reputation 	= request.args.get('min_reputation')
	max_reputation 	= request.args.get('max_reputation')
	username 		= request.args.get('username')
	post_id 		= request.args.get('id')
	latitude 		= request.args.get('latitude')
	longitude 		= request.args.get('longitude')
	radius 			= request.args.get('radius')
	lock_value		= int(request.args.get('lock_value'))
	unlock_posts 	= int(request.args.get('unlock_posts'))

	location_search = False
	max_longitude	= None
	min_longitude	= None
	max_latitude 	= None
	min_latitude 	= None

	if longitude and latitude and radius:
		max_longitude, max_latitude, min_longitude, min_latitude = calc_bounding_coords(longitude, latitude, radius)
		location_search = True

	if not username and 'username' in session.keys():
		username = session['username']

	data = manager.select_spotpost(min_reputation, max_reputation, username, post_id, min_latitude, max_latitude, min_longitude, max_longitude, radius, location_search, lock_value)

	if unlock_posts and username:
		#data is an array of dictionaries. 
		for row in data:
			unlock_id = row['id']
			insert_unlock_relation(username, unlock_id)

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
	if session['privilege']:
		manager.delete_post(id)
		return "SUCCESS"
	else:
		return "ERROR NOT LOGGED IN AS ADMIN"

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
	if session['privilege'] and request.form['id']:
		manager.update_post(request.form)
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
		enc_password = request.form['password']
		username = request.form['username']
		password = key.decrypt(enc_pass)

		valid_login = manager.validate_user(username, password)
		
		if valid_login:
			session['username'] = username
			session['privilege'] = manager.get_privilege(curr_user)
			redirect(url_for('index'))
		else:
			return "INVALID LOGIN DETAILS"
	elif request.method == 'POST':
		return "ERROR INVALID FORMAT"
	
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
#	Registers the user into the Database.
#
###
@app.route('/_register', methods =['GET', 'POST'])
def register():
	if request.method == 'POST':
		enc_pass = request.form['password']
		passsword = key.decrypt(enc_pass)

		manager.insert_user(request.form['username'], password)
		session['privilege'] = manager.get_privilege(curr_user)
		session['username'] = request.form['username']
		redirect(url_for('index'))

	return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
    '''

###
#
# Promotes a user to an admin.
# @param username = user to be promoted.
#
###
@app.route('/promote/<username>')
def promote_user(username):
	curr_user = session['username']
	if curr_user:
		privilege = manager.get_privilege(curr_user)
		if privilege:
			manager.set_privilege(username, 1)
	else:
		return "ERROR: Must be logged in."

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
	session['username'] = "Admin"
	return render_template('index.html')

if __name__ == '__main__':
	# Runs on port 5000 by default
	# url: "localhost:5000"
	# Secret Key for sessions.

	app.secret_key = 'Bv`L>?h^`qeQr6f7c$DK.E-gvMXZR+'
	app.run(host="0.0.0.0")
	manager.close_connection()