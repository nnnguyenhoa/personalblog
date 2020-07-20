
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import base64
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
import config

app = Flask(__name__)
app.config['MONGO_URI'] = config.MONGO_URI
mongo = PyMongo(app)
app.jinja_env.filters['decode'] = lambda u: u.decode()


@app.route('/')
def index():
    Posts = mongo.db.Posts.find().sort([('$natural', -1)])
    return render_template('home.html', Posts=Posts)


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
		name=request.form['name']
		email=request.form['email']
		message=request.form['message']
	return render_template('contact.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0")
