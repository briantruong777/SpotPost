from flask import Flask, session, request, abort, render_template, redirect, url_for
import os
import sqlite3

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
'	Initializes the Database by creating each table.
'
'''
def initDB():
	cursor.execute("CREATE TABLE IF NOT EXISTS test(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, title varchar(15), name varchar(15), content varchar(255), time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)")

'''
'	
'	Processes input for getting a spotpost.
'
'''
@app.route('/spotpost/get', methods = ['GET', 'POST'])
def get_spotpost_input():
	if request.method == 'GET':
		return render_template('get_spotpost.html')
	curr_id = request.form['id']
	return redirect(url_for('get_spotpost', id = curr_id))

'''
'
'	Gets the spotpost associated with the ID.	
'	@param id = ID of spotpost to get
'
'''
@app.route('/spotpost/get/<id>')
def get_spotpost(id):
	cursor.execute('SELECT * FROM test WHERE id = ?', (id,))
	data = cursor.fetchone()
	return render_template('get_spotpost_byid.html', item = data)

'''
'
'	Gets and displays ALL spotposts.	
'
'''
@app.route('/spotpost/get/all')
def get_all_spotposts():
	cursor.execute('SELECT * FROM test')
	data = cursor.fetchall()
	
	return render_template('get_all_spotposts.html', data_query = data)

'''
'
'	Allows user to post spotposts, by manually inputting what to enter
'	Into the database.
'
'''
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


'''
'
'	Deletes a given spotpost.
'	@input id = id of spotpost to delete.
'
'''
@app.route('/spotpost/delete/<id>')
def delete_spotpost(id):
	cursor.execute("DELETE FROM test WHERE id = ?", (id,))
	connect.commit()
	return render_template('delete_spotpost.html')

'''
'
'	Prompts the user to enter an ID for which spotpost to delete.
'
'''
@app.route('/spotpost/delete', methods = ['GET', 'POST'])
def delete_spotpost_input():
	if request.method == 'GET':
		return render_template('delete_byid.html')

	curr_id = request.form['id']
	return redirect(url_for('delete_spotpost', id = curr_id))

'''
'
'	Updates a spotpost with given id. Prompts user to enter in new data for
'	the spotpost, and will show the old data in the text fields.
'	@param id = ID of spotpost to update	
'
'''
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

'''
'
'	Asks user for which spotpost they would like to Update.
'
'''
@app.route('/spotpost/update', methods = ['GET', 'POST'])
def update_spotpost_input():
	if request.method == 'GET':
		return render_template('update_byid.html')

	curr_id = request.form['id']
	return redirect(url_for('update_spotpost', id = curr_id))

'''
'
'	Shows homepage, simply serves as a way to get to other pages.
'
'''
@app.route('/')
def index():
	return render_template('layout.html')

initDB()

if __name__ == '__main__':
	# Runs on port 5000 by default
	# url: "localhost:5000"
	app.run(host="0.0.0.0")
	connect.close()
