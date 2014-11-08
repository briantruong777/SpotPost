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
--------

### Getting Spotposts

* In order to obtain a spotpost a GET request must be made to `www.spotpost.me/spotpost/_get`.
* This will return a JSON file containing either all Spotposts or Spotposts based on your search parameters.
* To add search parameters add `?\<parameter name\> = \<parameter value\>` to the url for the first parameter.
  for more parameters add `&\<parameter name\> = \<parameter value\>`.
* List of possible parameters, replace `\<parameter name\>` from above with this.
	* `min_rating` : Minimum rating of Spotpost to search for.
	* `max_rating` : Maximum rating of Spotpost to search for.
	* `username`   : Author of Spotpost to search for.
	* `id`  	   : ID of Spotpost. This overrides the other search parameters.
	* Location Based parameters. All three must be included, search ignores proper subsets.
		* `latitude`  : Latitude of center point of bounding square.
		* `longitude` : Longitude of center point of bounding square. 
		* `radius`    : Radius of the circle that the square inscribes.
* JSON contains an array of Spotposts based on your search parameters.
* Each Spotpost is constructed as follows.
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