from google.appengine.ext import db


class Zone(db.Model):
    name = db.StringProperty(required=True)
    latitude = db.IntegerProperty(required=True)
    longitude = db.IntegerProperty(required=True)
    height = db.IntegerProperty()
    width = db.IntegerProperty()

