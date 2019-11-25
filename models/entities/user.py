
class User(db.Model):
    mail = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    role = db.StringProperty(required=True)
    isOnline = db.BooleanProperty(required=True)
    createdAt = db.StringProperty(required=True)
    lastLogin = db.StringProperty(required=True)
    