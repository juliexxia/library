from flask import Flask, jsonify, make_response, request
import datetime
import dataset
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)

db = dataset.connect('sqlite:///library.db')['requests']

# requests GET - returns all requests
# requests POST - validates the given email, marks a book as requested
#    if it is available else it shows the book as not available
@app.route('/requests', methods=['GET', 'POST'])
def requests():
	if request.method == "GET":
		return make_json_response(get_requests(), 200)
	elif request.method == "POST":
		request_timestamp = datetime.datetime.now().isoformat()

		content = request.json

		if not "email" in content:
			return make_response("Request needs an 'email' key.", 404)
		email = content["email"]

		# validate email
		try:
			valid = validate_email(email)
			email = valid.email
		except EmailNotValidError as e:
			# If email is not valid, print error
			print(str(e))
			return make_response(email + ": " + str(e), 400)

		# look up book in db
		if not "title" in content:
			return make_response("Request needs an 'title' key.", 404)
		title = content["title"]
		result = db.find_one(title = title)
		if not result:
			return make_response("Title not found in library", 404)

		to_return = {
			"id": result["id"],
			"available": result["available"],
			"title": title,
			"timestamp": request_timestamp,
		}

		# Update the availability to false now that it's been requested
		db.update(dict(id=result["id"], available=False), ['id'])

		return make_json_response(to_return, 200)

# requests/:id GET - gets a specific request based on ID
# requests/:id DELETE - cancels a specific request marking the book as available
@app.route('/requests/<id>', methods = ['GET', 'DELETE'])
def request_one(id):
	found_request = db.find_one(id = id)
	if not found_request:
		return make_response("Request ID not found", 404)

	if request.method == "GET":
		return make_json_response(found_request, 200)
	elif request.method == "DELETE":
		db.update(dict(id=id, available=True), ['id'])
		return {}

# db_populate GET populates the requests database
@app.route('/db_populate', methods=['GET'])
def db_populate():
    # If the DB isn't empty, we delete everything
    # just in case it's already been populated
    # to ensure we populate with the seeds below.
    if db.count() != 0:
        db.delete()

    books = [
        "A Little Life - Hanya Yanagihara", 
        "Name of the Wind - Patrick Rothfuss", 
        "Know My Name - Chanel Miller",
        "Into Thin Air - John Krakauer"]

    for book in books:
        db.insert({
            "title": book,
            "available": True
        })

    return make_json_response(get_requests(), 200)

def get_requests():
    requests = []
    for request in db:
        requests.append(request)
    return requests

def make_json_response(content, code):
	return make_response(jsonify(content), code)

if __name__ == '__main__':
    app.run()