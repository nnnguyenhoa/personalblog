from __future__ import print_function
from flask import Flask, render_template, jsonify, request, make_response
from flask_pymongo import PyMongo
import base64
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
import os
import time
import quickstart
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import config

app = Flask(__name__)
#app.config['MONGO_URI'] = os.environ.get('MONGODB_URI')
app.config['MONGO_URI'] = config.MONGO_URI
mongo = PyMongo(app)
app.jinja_env.filters['decode'] = lambda u: u.decode()
Posts = mongo.db.Posts.find().sort([('$natural', -1)])
Posts = list(Posts)
db_len = len(Posts)
global curr_post
curr_post = 1

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
creds = None

if os.path.exists('token.pickle'):
	with open('token.pickle', 'rb') as token:
		creds = pickle.load(token)

if not creds or not creds.valid:
	if creds and creds.expired and creds.refresh_token:
		creds.refresh(Request())
	else:
		flow = InstalledAppFlow.from_client_secrets_file(
			'credentials.json', SCOPES)
		creds = flow.run_local_server(port=0)

	with open('token.pickle', 'wb') as token:
		pickle.dump(creds, token)

service = build('gmail', 'v1', credentials=creds)


@app.route('/')
def index():
    return render_template('home.html', Posts=Posts[:curr_post])


@app.route('/readmore/<post_id>')
def readmore(post_id):
	post = mongo.db.Posts.find_one({"_id": ObjectId(post_id)})
	return render_template('expanded_post.html', post=post)

@app.route('/home')
def home():
	return index()

@app.route('/resume')
def resume():
	return render_template('resume.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	if request.method == 'POST':
		to = "nnnguyenhoa@yahoo.com"
		name=request.form['name']
		email =request.form['email']
		sender = "nnnguyennnhoa@gmail.com"
		subject = name + "@" + email + " sends email from blog"
		message=request.form['message']
		sendee = "nnnguyenhoa@yahoo.com"
		email = MIMEText(message)
		email['to'] = sendee
		email['from'] = sender
		email['subject'] = subject
		raw_email = base64.urlsafe_b64encode(email.as_string().encode("utf-8"))
		email = {'raw': raw_message.decode("utf-8")}
		try:
			send = service.users().messages().send(userId="me", body=email).execute()
		except Exception as e:
			print('An error occured: %s' %e)
	
	return render_template('contact.html')

@app.route('/load')
def load():
	time.sleep(0.2)
	global curr_post
	if curr_post == db_len:
		res = make_response(jsonify({}), 200)
	elif curr_post + 3 < db_len:
		new_posts = dumps(Posts[curr_post:curr_post+3])
		res = make_response(new_posts,200)
		curr_post += 3
	else:
		new_posts = dumps(Posts[curr_post:])
		res = make_response(new_posts,200)
		curr_post = db_len
	return res

if __name__ == "__main__":
	app.run()