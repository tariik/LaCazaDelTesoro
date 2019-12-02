from flask import Flask
import mongoengine as me
from flask_sqlalchemy import SQLAlchemy
import os
import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo

# create the flask object
app = Flask(__name__)

# add mongo url to flask config, so that flask_pymongo can use it to make connection
app.config["MONGO_URI"] = "mongodb+srv://casaDeTesoros:Annaba@cluster0-of11h.gcp.mongodb.net/cazadetesoros?retryWrites=true&w=majority"
mongo = PyMongo(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['MONGOALCHEMY_DATABASE'] = 'mongodb+srv://casaDeTesoros:Annaba@cluster0-of11h.gcp.mongodb.net/test?retryWrites=true&w=majority'
me.connect('sample_mflix', host='mongodb+srv://casaDeTesoros:Annaba@cluster0-of11h.gcp.mongodb.net/cazadetesoros?retryWrites=true&w=majority')

db = SQLAlchemy(app)
app.secret_key = "secret key"

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

