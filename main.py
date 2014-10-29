from flask import Flask, session, request, abort, render_template, redirect, url_for
import os
import sqlite3

# For decoding JSON request data. Strings come in unicode format.
from unidecode import unidecode

# If Python2.6, simplejson is better than json, but in Python2.7, simplejson became json
try: import simplejson as json
except ImportError: import json

connect = sqlite3.connect('demo.db')
cursor = connect.cursor()

app = Flask(__name__)

# For logging to a file called "spotpost_log"
import logging
from logging import FileHandler
file_handler = FileHandler("spotpost_log")
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

'''
'	
'	Initializes the Database by creating each table. Below are the tables in relational format.
'
'	SpotPosts(id, content, photo_id, reputation, longitude, latitude, visibility, user_id, time)
'	SpotPostComments(id, message_id, content, user_id, time)
'	Users(username, password, profile_pic)
'	Follows(follower_name, followee_name)
'	
'''
def initDB():
	#SpotPosts(id, content, photo_id, reputation, longitude, latitude, visibility, user_id, time)
	cursor.execute("CREATE TABLE IF NOT EXISTS SpotPosts(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, content varchar(255), " + 
		"photo_id INTEGER, rating INTEGER DEFAULT 0, longitude REAL NOT NULL, latitude REAL NOT NULL, visibility REAL," + 
		" username TEXT, time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)")

	#SpotPostComments(id, message_id, content, user_id, time)
#	add_test_data("CREATE TABLE IF NOT EXISTS SpotPostComments(ID INTEGER PRIMARY KEY AUTO)")
	
	#Users(username, password, profile_pic)
	cursor.execute("CREATE TABLE IF NOT EXISTS Users(username TEXT PRIMARY KEY, password TEXT, profile_pic_id INTEGER)")
	
	#Follows(follower_name, followee_name)
	cursor.execute("CREATE TABLE IF NOT EXISTS Follows(follower_name TEXT, followee_name TEXT)")

	#Photos(id, photo)
	cursor.execute("CREATE TABLE IF NOT EXISTS test(num INTEGER, words TEXT, morenum INTEGER, user TEXT)")

'''
'	
'	Adds test data into the database.
'
'''
@app.route('/add_data')
def add_test_data():
	content = "This is test data, can't you see!"
	photo_id = 12
	username = "TEST"
	longitude = 18.0
	latitude = 51.0
	visibility = 13.37
	rating = 25523
	
	cursor.execute("INSERT INTO SpotPosts(content, photo_id, rating, longitude, latitude, visibility, username) VALUES (?,?,?,?,?,?,?)", (content, photo_id, rating, longitude, latitude, visibility, username))
	connect.commit()


@app.route('/post', methods = ['POST'])
def post_spotpost():
	content = unidecode(request.form['content'])
	photo_id = int(request.form['photo_id'])
	user_id = int(request.form['user_id'])
	longitude = unidecode(request.form['latitude'])
	latitude = unidecode(request.form['longitude'])
	visibility = float(request.form['visibility'])
	rating = int(request.form['rating'])
	
	cursor.execute("INSERT INTO SpotPosts(content, photo_id, rating, longitude, latitude, visibility, username) VALUES (?,?,?,?,?,?,?)", (content, photo_id, rating, longitude, latitude, visibility, username))
	connect.commit()

	return "Success"

@app.route('/_get')
def get_spotpost():
	query = "SELECT * FROM SpotPosts"
	where_query = False
	min_rating = request.form['min_rating']
	max_rating = request.form['max_rating']
	username = request.form['username']
	post_id = request.form['id']

	if post_id != '':
		query = query + "WHERE ID = " + post_id
		where_query = True
	if username != '':
		if !where_query:
			query = query + "WHERE username = " + username
			where_query = True
		else:
			query = query + "AND username = " + username
	if min_rating != '':
		if !where_query:
			query = query + "WHERE rating >= " + min_rating
			where_query = True
		else:
			query = query + "AND rating >= " + min_rating
	if max_rating != '':
		if !where_query:
			query = query + "WHERE rating <= " + max_rating
			where_query = True
		else:
			query = query + "AND rating <= " + max_rating
'''
'	
'	Processes input for getting a spotpost by ID.
'
'
@app.route('/spotpost/getid', methods = ['GET', 'POST'])
def get_spotpost_input_id():
	if request.method == 'GET':
		return render_template('get_spotpost_byid.html')
	curr_id = request.form['id']
	return redirect(url_for('get_spotpost', id = curr_id))

'
'	
'	Prompts the user to input a username to search spotposts for.
'
'
@app.route('/spotpost/getuser', methods = ['GET', 'POST'])
def get_spotpost_input_user():
	if request.method == 'GET':
		return render_template('get_spotpost_byuser.html')
	user = request.form['user']
	return redirect(url_for('get_spotpost_user', user = user))

'
'
'	Gets the spotpost associated with the ID.	
'	@param id = ID of spotpost to get
'
'
@app.route('/_get/<id>')
def get_spotpost(id):
	cursor.execute('SELECT * FROM test WHERE id = ?', (id,))
	data = cursor.fetchall()
	return render_template('get_spotpost.html', data_query = data)

'
'
'	Gets and displays ALL spotposts.	
'
'
@app.route('/spotpost/get/all')
def get_all_spotposts():
	cursor.execute('SELECT * FROM test')
	data = cursor.fetchall()
	
	return render_template('get_spotpost.html', data_query = data)

'
'
'	Gets the spotposts associated with the User.	
'	@param user = User of spotpost to get.
'
'
@app.route('/spotpost/get/user/<user>')
def get_spotpost_user(user):
	cursor.execute('SELECT * FROM test WHERE name = ?', (user,))
	data = cursor.fetchall()
	
	return render_template('get_spotpost.html', data_query = data)

'
'
'	Allows user to post spotposts, by manually inputting what to enter
'	Into the database.
'
'
@app.route('/spotpost/post', methods=['GET', 'POST'])
def post_spotpost():
	if request.method == 'POST':
		title = request.form['title']
		user = request.form['user']
		content = request.form['content']
		cursor.execute("INSERT INTO test(title, name, content) VALUES (?,?,?)", (title, user, content))
		cursor.execute("SELECT MAX(ID) FROM test")
		curr_id = cursor.fetchone()[0]
		connect.commit()

		return redirect(url_for('get_spotpost', id = curr_id))

	return render_template('add_spotpost.html')


'
'
'	Deletes a given spotpost.
'	@input id = id of spotpost to delete.
'
'
@app.route('/spotpost/delete/<id>')
def delete_spotpost(id):
	cursor.execute("DELETE FROM test WHERE id = ?", (id,))
	connect.commit()
	return render_template('delete_spotpost.html')

'
'
'	Prompts the user to enter an ID for which spotpost to delete.
'
'
@app.route('/spotpost/delete', methods = ['GET', 'POST'])
def delete_spotpost_input():
	if request.method == 'GET':
		return render_template('delete_byid.html')

	curr_id = request.form['id']
	return redirect(url_for('delete_spotpost', id = curr_id))

'
'
'	Updates a spotpost with given id. Prompts user to enter in new data for
'	the spotpost, and will show the old data in the text fields.
'	@param id = ID of spotpost to update	
'
'
@app.route('/spotpost/update/<id>', methods = ['GET', 'POST'])
def update_spotpost(id):
	if request.method == 'GET':
		cursor.execute('SELECT * FROM test WHERE id = ?', (id,))
		data = cursor.fetchone()
		return render_template('update_input.html', item = data)
	else:
		title = request.form['title']
		user = request.form['user']
		content = request.form['content']
		cursor.execute("UPDATE test SET title = ?, name = ?, content = ? WHERE ID = ?", (title, user, content, id))
		connect.commit()
		return redirect(url_for('get_spotpost', id = id))

'
'
'	Asks user for which spotpost they would like to Update.
'
'
@app.route('/spotpost/update', methods = ['GET', 'POST'])
def update_spotpost_input():
	if request.method == 'GET':
		return render_template('update_byid.html')

	curr_id = request.form['id']
	return redirect(url_for('update_spotpost', id = curr_id))
'''

'''
'
'	Shows homepage, simply serves as a way to get to other pages.
'
'''
@app.route('/')
def index():
	return render_template('index.html')

initDB()

if __name__ == '__main__':
	# Runs on port 5000 by default
	# url: "localhost:5000"
	app.run(host="0.0.0.0")
	connect.close()
