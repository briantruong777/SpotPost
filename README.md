SpotPost
========

Post SpotPosts at cool spots.

How To Launch Development Site
--------

### First time setup
1. Install python2.7 and virtualenv
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
