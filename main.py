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

# For decoding JSON request data. Strings come in unicode format. Possibly useless :(.
from unidecode import unidecode

# If Python2.6, simplejson is better than json, but in Python2.7, simplejson became json
try: import simplejson as json
except ImportError: import json

connect = sqlite3.connect('data.db')
cursor = connect.cursor()
manager = DBManager()

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
#	Initializes the Database Manager
#
#	SpotPosts(id, content, title, reputation, longitude, latitude, username, time)
#	SpotPostComments(id, message_id, content, user_id, time)
#	Users(username, password, profile_pic_id, reputation)
#	Follows(follower_name, followee_name)
#	Photos(id, photo)
#	Rates(username, spotpost_id)
#
###
#def initDB():
#	manager = DBManager()

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
	return manager.insert_spotpost(request.form)

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
	location_search = False
	min_reputation 	= request.args.get('min_reputation')
	max_reputation 	= request.args.get('max_reputation')
	username 		= request.args.get('username')
	post_id 		= request.args.get('id')
	latitude 		= request.args.get('latitude')
	longitude 		= request.args.get('longitude')
	radius 			= request.args.get('radius')
	max_longitude	= None
	min_longitude	= None
	max_latitude 	= None
	min_latitude 	= None

	if longitude and latitude and radius:
		max_longitude, max_latitude, min_longitude, min_latitude = calc_bounding_coords(longitude, latitude, radius)
		location_search = True

	data = manager.select_spotpost(min_reputation, max_reputation, username, post_id, min_latitude, max_latitude, min_longitude, max_longitude, radius, location_search)

	return json.dumps(data)

###
#
#
#
###
@app.route('/comment/_post', methods = ['POST'])
def post_comment():
	manager.insert_comment(request.form)

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
	if session['username'] is "Admin":
		manager.delete_post(id)
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
		client_username = request.form['username']

		valid_login = manager.validate_user(client_username, client_password)
		
		if valid_login:
			session['username'] = client_username
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
		manager.insert_user(request.form)
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
#	Logs the user out.
#
###
@app.route('/_logout')
def logout():
	session.pop('username', None)
	return "LOGGED OUT."

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
	connect.close()