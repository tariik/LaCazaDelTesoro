from flask import Flask, request, jsonify
from flask_mongoalchemy import MongoAlchemy
from flask_sqlalchemy import SQLAlchemy
import mongoengine as me
from marshmallow_mongoengine import ModelSchema
import mongoengine as me
from mongoengine import *

from datetime import datetime


import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['MONGOALCHEMY_DATABASE'] = 'mongodb+srv://casaDeTesoros:Annaba@cluster0-of11h.gcp.mongodb.net/test?retryWrites=true&w=majority'
me.connect('sample_mflix', host='mongodb+srv://casaDeTesoros:Annaba@cluster0-of11h.gcp.mongodb.net/cazadetesoros?retryWrites=true&w=majority')

db = SQLAlchemy(app)

class User(me.Document):
    id = me.IntField(primary_key=True, default=1)
    name = me.StringField()
    email = me.StringField()
    password = me.StringField()
    role = me.StringField(default='0')
    score = me.StringField(default='0')
    createdAt = me.DateTimeField(default=datetime.now())

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)

class Juego(me.Document):
    id = me.IntField(primary_key=True, default=1)
    name = me.StringField()
    description = StringField(max_length=500)
    is_approved = BooleanField(default=False)
    createdAt = me.DateTimeField(default=datetime.now())
    createdBy = me.StringField()
    ganador = me.StringField(default=0)
    user_id = me.ListField(me.ReferenceField('User'))


class Tesoro(me.Document):
    id = me.IntField(primary_key=True, default=1)
    name = me.StringField()
    score = me.StringField()
    juego_id = me.ListField(me.ReferenceField('Juego'))
    zona_id = me.ListField(me.ReferenceField('Zona'))



class Zona(me.Document):
    id = me.IntField(primary_key=True, default=1)
    name = me.StringField()
    lat = me.StringField()
    lon = me.StringField()

class UserSchema(ModelSchema):
    class Meta:
        model = User

class JuegoSchema(ModelSchema):
    class Meta:
        model = Juego

class TesoroSchema(ModelSchema):
    class Meta:
        model = Tesoro

class ZonaSchema(ModelSchema):
    class Meta:
        model = Zona


user_schema = UserSchema()
juego_schema = JuegoSchema()
Tesoro_schema = TesoroSchema()
zona_schema = ZonaSchema()


user = User(
    name='Tarek Khalfaoui',
    email = 'tariik21@gmail.com',
    password = '123456'
    ).save()

#dump_data = user_schema.dump(user).data

for user in User.objects:
    print user.name

if __name__ == '__main__':
    app.run(debug=True)