# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

# [START imports]
from flask import Flask, render_template, request
from pymongo import MongoClient
from flask import Flask, jsonify
from model import *
import mongoengine as me


# [END imports]

# [START create_app]
app = Flask(__name__)
# [END create_app]
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]
# [START form]

@app.route('/')
def home():
    client = MongoClient('mongodb://casaDeTesoros:<123456.>@cluster0-shard-00-00-of11h.gcp.mongodb.net:27017,cluster0-shard-00-01-of11h.gcp.mongodb.net:27017,cluster0-shard-00-02-of11h.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client.test     
    return jsonify({'tasks': tasks})

# [END form]



# [START form]
@app.route('/form')
def form():
    return render_template('form.html')
# [END form]


# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']

    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments)
    # [END render_template]



@app.route('/add', methods=['POST'])
def add_user():
	_json = request.json
	_name = _json['name']
	_email = _json['email']
	_password = _json['pwd']
	# validate the received values
	if _name and _email and _password and request.method == 'POST':
		#do not save password as a plain text
		_hashed_password = generate_password_hash(_password)
		# save details
		id = mongo.db.user.insert({'name': _name, 'email': _email, 'pwd': _hashed_password})
		resp = jsonify('User added successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
		
@app.route('/users')
def users():
    data = User.objects()
    json_data = data.to_json()
    return json_data

@app.route('/user/<id>')
def user(id):
    data = User.objects(id=id)
    json_data = data.to_json()
    return json_data
		
@app.route('/update', methods=['PUT'])
def update_user():
	_json = request.json
	_id = _json['_id']
	_name = _json['name']
	_email = _json['email']
	_password = _json['pwd']		
	# validate the received values
	if _name and _email and _password and _id and request.method == 'PUT':
		#do not save password as a plain text
		_hashed_password = generate_password_hash(_password)
		# save edits
		mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name': _name, 'email': _email, 'pwd': _hashed_password}})
		resp = jsonify('User updated successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
		
@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
	mongo.db.user.delete_one({'_id': ObjectId(id)})
	resp = jsonify('User deleted successfully!')
	resp.status_code = 200
	return resp
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
