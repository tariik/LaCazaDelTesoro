from flask import Flask, render_template, redirect, request
from google.appengine.ext import db
from models.facade import *
from models.entities.user import User
from models.entities.zone import Zone

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


""" 
CRUD User routes       
"""


# user list
@app.route('/user_all')
def user_all():
    data = get_all_user()
    return render_template('user/user_all.html', data=data)


#  get user info
@app.route('/user_one/<id>')
def user_one(id):
    user = user_get_one(id)
    return render_template('user/user_one.html', user=user)


#  new user
@app.route('/user_new', methods=['GET', 'POST'])
def user_new():
    if request.method == 'POST':
        user = User(
            user_name=request.form.get('username'),
            email=request.form.get('email'),
            first_name=request.form.get('firstname'),
            last_name=request.form.get('lastname'),
            gender=request.form.get('gender'),
            role='user'  # por defecto
        )
        user.put()
        return redirect('user_all')
    else:
        return render_template('user/user_new.html')


#  update user info
@app.route('/user_edit/<id>', methods=['GET', 'POST'])
def user_edit(id):
    if request.method == 'POST':
        user_id = int(id)
        user = db.get(db.Key.from_path('User', user_id))
        user.user_name = str(request.form.get('username'))
        user.email = str(request.form.get('email'))
        user.first_name = str(request.form.get('firstname'))
        user.last_name = str(request.form.get('lastname'))
        user.gender = str(request.form.get('gender'))
        user.role = 'user'
        user.put()
        return redirect('/user_all')

    else:
        user_id = int(id)
        user = db.get(db.Key.from_path('User', user_id))
        return render_template('user/user_edit.html', user=user)


#  delete user
@app.route('/user_delete/<id>')
def user_delete(id):
    user_id = int(id)
    user = db.get(db.Key.from_path('User', user_id))
    db.delete(user)
    return redirect('/user_all')


""" 
CRUD Zona routes       
"""


# zone list
@app.route('/zone_all')
def zone_all():
    data = get_all_zone()
    return render_template('zone/zone_all.html', data=data)


#  get zone info
@app.route('/zone_one/<id>')
def zone_one(id):
    zone = zone_get_one(id)
    return render_template('zone/zone_one.html', zone=zone)


#  new zone
@app.route('/zone_new', methods=['GET', 'POST'])
def zone_new():
    if request.method == 'POST':
        zone = Zone(
            name=request.form.get('name'),
            latitude=int(request.form.get('latitude')),
            longitude=int(request.form.get('longitude')),
            height=int(request.form.get('height')),
            width=int(request.form.get('width')),
        )
        zone.put()
        return redirect('zone_all')
    else:
        return render_template('zone/zone_new.html')


#  update zone info
@app.route('/zone_edit/<id>', methods=['GET', 'POST'])
def zone_edit(id):
    if request.method == 'POST':
        zone_id = int(id)
        zone = db.get(db.Key.from_path('Zone', zone_id))
        zone.name = str(request.form.get('name'))
        zone.latitude = int(request.form.get('latitude'))
        zone.longitude = int(request.form.get('longitude'))
        zone.height = int(request.form.get('height'))
        zone.width = int(request.form.get('width'))
        zone.put()
        return redirect('/zone_all')

    else:
        zone_id = int(id)
        zone = db.get(db.Key.from_path('Zone', zone_id))
        return render_template('zone/zone_edit.html', zone=zone)

#  delete zone
@app.route('/zone_delete/<id>')
def zone_delete(id):
    if id:
        zone_id = int(id)
        zone = db.get(db.Key.from_path('Zone', zone_id))
        db.delete(zone)
        return redirect('/zone_all')

""" 
SEARCH FOR GAME       
"""
@app.route('/game_search/<keyword>')
def game_search(keyword):
    if keyword:
        keyword = str(keyword)
        q = Game.all()
        result = q.filter("game_name =", keyword)
        return render_template('game_search.html', data=result)


if __name__ == '__main__':
    app.run()
