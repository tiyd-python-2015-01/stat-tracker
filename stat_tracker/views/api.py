import base64
import json

from flask import Blueprint, jsonify, abort, request, url_for, g
from flask.ext.login import login_user, current_user
from flask.ext.httpauth import HTTPBasicAuth

from ..models import Activity, Instance, User
from .. forms import ActivityForm, InstanceForm
from ..extensions import login_manager, db

import datetime as dt

api = Blueprint("api", __name__)

def json_response(code, data):
    return json.dumps(data), code, {"Content-Type: application/json"}


@api.app_errorhandler(401)
def unauthorized(request):
    return ("", 401, {"Content-Type: application/json"})



def authorize_user(request):
    authorization = request.authorization
    if authorization:
        email = authorization['username']
        password = authorization['password']

        user = User.query.filter_by(email=email).first()
        g.user = user
        if user.check_password(password):
            return user


def require_authorization():
    user = authorize_user(request)
    if user:
        g.user = user
        login_user(user)
    else:
        abort(401)


@api.route('/api/v1.0/activities', methods = ['GET'])
def get_activities():
    require_authorization()

    activities = Activity.query.filter_by(user_id = g.user.id).all()

    activities = [activity.make_dict() for activity in activities]

    return jsonify({"activities": activities})


@api.route('/api/v1.0/activities', methods = ['POST'])
def create_activity():
     require_authorization()

     title = request.json.get('title')
     unit = request.json.get('unit')

     if title is None or unit is None:
         abort(400)

     activity = Activity(user_id = g.user.id,
                         title = title,
                         unit = unit)
     db.session.add(activity)
     db.session.commit()

     activity = activity.make_dict()

     return (jsonify({ 'activity': activity }), 201)

@api.route('/api/v1.0/activities/<int:id>', methods = ['PUT'])
def edit_activity(id):
     require_authorization()
     activity = Activity.query.filter_by(id = id).first()

     if activity.user_id == g.user.id:

         title = request.json.get('title')
         unit = request.json.get('unit')

         activity.title = title
         activity.unit = unit

         db.session.commit()

         activity = activity.make_dict()

         return (jsonify({ 'activity': activity }), 201)

     return "unauthorized"




@api.route('/api/v1.0/activities/<int:id>', methods = ['DELETE'])
def delete_activity(id):
     require_authorization()
     activity = Activity.query.filter_by(id = id).first()

     if activity.user_id == g.user.id:
         instances = Instance.query.filter_by(activity_id = id).all()
         for instance in instances:
             db.session.delete(instance)
         db.session.delete(activity)
         db.session.commit()
         activity = activity.make_dict()
         return (jsonify({ 'DELETED': activity }), 201)

     return "unauthorized"


@api.route('/api/v1.0/activities/<int:id>', methods = ['GET'])
def view_activity(id):
    require_authorization()

    instances = Instance.query.filter_by(activity_id = id).all()
    instances = [instance.make_dict() for instance in instances]

    return jsonify({"Instances": instances})


@api.route('/api/v1.0/activities/<int:id>', methods = ['POST'])
def add_instance(id):
    try:
         body = request.get_data(as_text='true')
         data = json.loads(body)
         form = APIStatForm(data=data, formdata=None, csrf_enabled=False)
    except ValueError:
         form = APIStatForm()

    activity = Activity.query.get(id)
    if form.validate():
        instance = Instance.query.filter_by(date =date.today())
        if instance == None:
            instance = Instance(user_id = current_user.id,
                                activity_id = activity.id,
                                date = date.today(),
                                freq = form.freq.value)
            db.session.add(instance)
            db.sesison.commit()
        else:
            instance.freq = form.freq.data
            db.session.commit()




@api.route('/api/v1.0/delete_instance/<int:id>', methods = ['DELETE'])
def delete_instance(id):
     require_authorization()

     instance = Instance.query.filter_by(id = id).first()
     if instance.user_id == g.user.id:
         db.session.delete(instance)
         db.session.commit()

         instance.make_dict()

         return (jsonify({ 'DELETED': instance }), 201)

     return "unauthorized"
