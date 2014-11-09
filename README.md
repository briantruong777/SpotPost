SpotPost
========

Post SpotPosts at cool spots.

How To Launch Development Site
--------

### First time setup
1. Install python2.7 (might work with python3) and virtualenv
2. Make a directory for the project and go into it
3. Run `git clone` with the git url
4. Make a directory called `venv` inside here
5. Run `virtualenv venv`
6. Run `. venv/bin/activate`
7. Run `pip install flask`
8. If you are done, run `deactivate` to exit the virtual environment

### Daily Development
1. Go to project directory
2. Run `. venv/bin/activate`
3. Enter the git repo directory
4. Run `python main.py`

You will now have a server running on `localhost:5000` that you can access in
your web browser. Feel free to do development and make commits inside the
virtual environment.

5. Run `deactivate` to exit the virtual environment

Notes for Deployment Server
--------

###  Important Files/Directories

* `/var/www/spotpost/` (main directory for spotpost)
  * `README.md` (Readme that has instructions for updating deployment server)
  * `spotpost.wsgi` (Python script that is run by apache to connect to Flask
                     using WSGI)
  * `venv/` (virtualenv folder, see `git/README.md`)
* `/var/www/spotpost/git/` (git repo for SpotPost)
  * `spotpost_log` (a log file for Flask used in deployment)
  * `README.md` (Another readme file)
* `/etc/httpd/conf.d/spotpost.conf` (The apache config for WSGI virtual host)
* `/var/log/httpd/error_log` (apache error log, will need to be root)

### Random Notes

* Any errors should be written to a `spotpost_log` file in the `git` directory
* Be careful when letting sqlite create the database from scratch. The
  permissions may not be correct for the deployment server (needs to be group
  writable). Also the directory the database is in needs to be group writable

Server API
========

### Generating Test Data
1. Simply run `python testdata.py`
2. This will empty the tables and add in test data.

### Admin Info
1. Admin in test data's password is `BananaPeppers`

### Registering a User
1. Send a `POST` request to `/_register` containing the user's info.
2. User's info is expected as a JSON following this format:
	* `username` : Username to register.
	* `password` : Password of new user.
3. Server will store the password encrypted using SHA256-encrypt.
4. This will log the person in once they have registered. 
5. It is also important to note this does not handle duplicates yet.

### Logging in as a User
1. Send a `POST` request to `/_login` containing the user's info.
2. User's info is expected as a JSON following this format:
	* `username` : Username of user.
	* `password` : User's password.
3. Server will check the encrypted password and will log the user in.
4. User will be pushed onto session object.

### Logging Out
1. Simply navigate to `/_logout`.
2. This will pop the user from the session.

### Getting Spotposts

1. In order to obtain a spotpost a GET request must be made to `www.spotpost.me/spotpost/_get`.
2. This will return a JSON file containing either all Spotposts, or Spotposts based on your search parameters.
3. To add search parameters add `?<parameter name> = <parameter value>` to the url for the first parameter.
  for more parameters add `&<parameter name> = <parameter value>`.
4. Jquery can do this for you using `.getJSON()` if possible find an alternative using whatever JS you use.
5. List of possible parameters, replace `<parameter name>` from above with this.
	* `min_rating` : Minimum rating of Spotpost to search for.
	* `max_rating` : Maximum rating of Spotpost to search for.
	* `username`   : Author of Spotpost to search for.
	* `id`  	   : ID of Spotpost. This overrides the other search parameters.
	* Location Based parameters. All three must be included, search ignores proper subsets.
		* `latitude`  : Latitude of center point of bounding square.
		* `longitude` : Longitude of center point of bounding square. 
		* `radius`    : Radius of the circle that the square inscribes in meters.
6. JSON contains an array of Spotposts based on your search parameters.
7. Each Spotpost is constructed as follows.
	* `id` 		  	: ID of Spotpost.
	* `content`  	: Content of Spotpost.
	* `rating`   	: Rating of Spotpost.
	* `longitude`	: Longitude of Spotpost.
	* `latitude`  	: Latitude of Spotpost.
	* `username`  	: A dictionary containing the following.
		* `username`   : Name of user who posted the Spotpost.
		* `reputation` : Reputation of users who posted the Spotpost.
	* `comments`  	: Array of comments, where each comment contains the following.
		* `id`		   : ID of comment.
		* `message_id` : Spotpost ID of the spotpost the comment is from.
		* `content`    : Content of the comment.
		* `username`   : Username of person who posted comment.
		* `time`       : Date and Time comment was posted.
	* `time`		: Date and Time Spotpost was posted. 

### Posting Spotposts
1. In order to post a SpotPost you must make a `POST` request to `/spotpost/_post`.
2. You must send a JSON file containing the data associated with the SpotPost.
3. Format the JSON using the following form.
4. Please note that required parameters are marked with a *.
	* \* `content`	: content of SpotPost.
	* \* `latitude` : latitude position of SpotPost.
	* \* `longitude`: longitude position of SpotPost.
	* `username`	: Username of user who posted the SpotPost. Default is the current logged in user.
	* `reputation`	: Custom starting reputation of SpotPost. Default is 0.

### Updating Spotposts
1. In order to update you must make a `POST` request to `/spotpost/_update`.
2. You must also send a JSON file containing the data associated with the SpotPost. 
3. Format the JSON in the following way.
4. The ID field is REQUIRED, however all the others are optional, but you must include one at least.
	* `id`			: id of SpotPost. 
	* `content`		: content of SpotPost.
	* `latitude` 	: latitude position of SpotPost.
	* `longitude`	: longitude position of SpotPost.
	* `username`	: Username of user who posted the SpotPost. Default is the current logged in user.
	* `reputation`	: Custom starting reputation of SpotPost. Default is 0.


### Upvoting Spotposts
1. You must be logged in as a valid user to do this.
2. Go to `/spotpost/_upvote/<id>`. Replace `<id>` with the ID of the Spotpost you are upvoting.
3. `<id>` must be a valid ID. Users can only vote on any given Spotpost once.
4. There is minimal error checking, it won't crash the server though.

### Downvoting Spotposts
1. Same procedure and rules as Upvoting.
2. However, you must go to `/spotpost/_downvote/<id>` instead. Replace `<id>` with the ID of the Spotpost.

### Posting Comments
1. In order to post a comment you must make a `POST` request to `/comment/_post`.
2. You must send a JSON file containing the data associated with the comment.
3. Please note that required parameters are marked with a *.
	* \* `message_id` 	: ID of the spotpost the comment is from.
	* \* `content`		: Content of the comment.
	* `username`		: Username of user who posted the comment. Default is the current logged in user.
	* `reputation`		: Custom starting reputation of comment. Default is 0.

### Upvoting Comments
1. You must be logged in as a valid user to do this.
2. Go to `/comment/_upvote/<id>`. Replace `<id>` with the ID of the comment you are upvoting.
3. `<id>` must be a valid ID. Users can only vote on any given comment once.
4. There is minimal error checking, it won't crash the server though.

### Downvoting Comments
1. Same procedure and rules as Upvoting.
2. However, you must go to `/comment/_downvote/<id>` instead. Replace `<id>` with the ID of the comment.

### Deleting Spotposts
1. Must be logged in as Admin to do this.
2. Go to `/spotpost/_delete/<id>`.
3. Replace `<id>` with the ID of the spotpost you want to delete

### Following A User
1. Go to `/_follow/<username>` where `<username>` is the username of the person being followed.
2. This will make the current logged in user follow `<username>`.
3. Accounts for duplicates and will prevent users from double following.

### Unfollowing A User
1. Go to `/_unfollow/<username>` where `<username>` is the username of the person being followed.
2. This will make the current logged in user unfollow `<username>`.

### ERRORS
Section under construction will be available once frontend gets further along.