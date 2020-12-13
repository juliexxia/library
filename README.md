# LIBRARY REQUESTS

## SET UP

This is a python/flask based service. 

### install necessary tooling
0. Install python3 (preferably using [pyenv](https://github.com/pyenv/pyenv) for easy version management)
1. Install [flask](https://flask.palletsprojects.com/en/1.1.x/installation/#)
2. Install [dataset](https://dataset.readthedocs.io/en/latest/index.html) - `pip install dataset` 
3. Install [email-validator]((https://pypi.org/project/email-validator/) - `pip install email-validator` 

### set up the sqlite3 database

cd to this directory where db.py is and:

	python3 db.py # run the script that sets up library.db
	sqlite3 library.db # open sqlite
	sqlite> .tables # check to ensure the library table was created

### run the server

cd to this directory where app.py is and run `python3 hello.py`

### using the service

In a new terminal, use classic curl commands or a helper like [HTTPie](https://httpie.io/)
to interact with the app e.g.:

	$ curl --header "Content-Type: application/json" \
		--data '{"title": "Know My Name - Chanel Miller", "email": "user@gd.com"}' \
		--request POST http://127.0.0.1:5000/requests

## Next steps for this project

### Adding tests:
- missing email in request POST: 
	curl --header "Content-Type: application/json" \
	--data '{"title": "Know My Name - Chanel Miller"}' \
	--request POST http://127.0.0.1:5000/requests
- missing title in request POST:
	curl --header "Content-Type: application/json" \
	--data '{"email": "j@g.com"}' \
	--request POST http://127.0.0.1:5000/requests
- malformed email:
	curl --header "Content-Type: application/json" \
	--data '{"title": "Know My Name - Chanel Miller", "email": "bad"}' \
	--request POST http://127.0.0.1:5000/requests
- seed db
- request an availble book
- request an unavailabel book
- request a request id that exists
- request a request id that does not exist
- delete a request on boook, freeing it up


