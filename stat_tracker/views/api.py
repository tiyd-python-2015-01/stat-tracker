import base64
import json
from datetime import datetime
from flask import Blueprint, jsonify, request, abort, url_for
from flask.ext.login import login_user
from sqlalchemy import func
from ..extensions import login_manager, db
from ..models import Activity, Timestamp, User
from ..forms import ActivityForm

api = Blueprint("api", __name__)



@api.route("/activities/")
def get_activities():
    user = require_authorization()
    activities = Activity.query.filter_by(creator=user)
    activities = [activity.to_web() for activity in activities]
    return jsonify({"activities": activities})


@api.route("/activities/", methods=['POST'])
def create_activity():
    user = require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = ActivityForm(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        new_activity = Activity(name=form.name.data,
                                description=form.description.data,
                                creator=user,
                                activity_type=form.type.data)
        db.session.add(new_activity)
        db.session.commit()
        return (json.dumps(new_activity.to_dict()), 201, {"Location": url_for("activity.details", user=user, activity_name=form.name.data)})
    else:
        return json_response(400, form.errors)


@api.route("/activities/<id>")
def get_stats(id):
    user = require_authorization()
    activity = Activity.query.filter_by(name=id, creator=user).first()
    stats = Timestamp.query.filter_by(activity_id=activity.id).all()
    stats = [stat.to_dict() for stat in stats]
    return jsonify({"activity": activity.to_dict(), "times": stats})


@api.route("/activities/<id>", methods=['PUT'])
def update_activity(id):
    user = require_authorization()
    input_check = False
    body = request.get_data(as_text=True)
    data = json.loads(body)
    activity = Activity.query.filter_by(name=id, creator=user).first()
    keys = data.keys()
    if len(keys) < 3:
        if 'name' in keys:
            activity.name = data['name']
            input_check = True
        if 'description' in keys:
            activity.description = data['description']
            input_check = True
        if 'type' in keys:
            activity.activity_type = data['type']
            input_check = True
        if input_check:
            db.session.commit()
            return (json.dumps(activity.to_dict()), 201, {"Location": url_for("activity.details", user=user, activity_name=activity.name)})
    else:
        return json_response(400, "Invalid Input")


@api.route("/activities/<id>", methods=['DELETE'])
def delete_activity(id):
    user = require_authorization()
    activity = Activity.query.filter_by(name=id, creator=user).first()
    if activity:
        db.session.delete(activity)
        remaining = Activity.query.filter_by(creator=user).all()
        remaining = [act.to_dict() for act in remaining]
        return jsonify({"activity": remaining})
    else:
        return json_response(400, "Activity Not Found")

@api.route("/activities/<id>/stats", methods=['POST', 'PUT'])
def update_stats(id):
    user = require_authorization()
    activity_id = db.session.query(Activity).filter_by(name=id, creator=user).first().id
    if not activity_id:
        return json_response(400, "Activity Not Found")
    body = request.get_data(as_text=True)
    data = json.loads(body)
    date = data['timestamp']
    timestamp = Timestamp.query.filter_by(activity_id=activity_id, actor_id=user, timestamp=date).first()
    if not timestamp:
        try:
            timestamp = Timestamp(activity_id=activity_id, actor_id=user, timestamp=date)
        except IOError:
            return json_response(400, "Timestamp Invalid")
        db.session.add(timestamp)
        db.session.commit()
        stats = Timestamp.query.filter_by(activity_id=activity_id).all()
        stats = [stat.to_dict() for stat in stats]
        return jsonify({"times": stats})
    else:
        return json_response(400, "Stat Exists")



@api.route("/activities/<id>/stats", methods=['DELETE'])
def delete_stats(id):
    user = require_authorization()
    activity_id = db.session.query(Activity).filter_by(name=id, creator=user).first().id
    latest_stat_id = db.session.query(func.max(Timestamp.id)).filter_by(activity_id=activity_id).scalar()
    if latest_stat_id:
        latest_stat = Timestamp.query.filter_by(id=latest_stat_id).first()
        db.session.delete(latest_stat)
        remaining = Timestamp.query.filter_by(activity_id=latest_stat.activity_id).all()
        remaining = [stat.to_dict() for stat in remaining]
        db.session.commit()
        return jsonify({"timestamps": remaining})
    else:
        return json_response(400, "Timestamps Not Found")


def require_authorization():
    user = authorize_user(request)
    if user:
        login_user(user)
        return user.id
    else:
        abort(401)
        return None

def json_response(code, data):
    return (json.dumps(data), code, {"Content-Type": "application/json"})


@api.app_errorhandler(401)
def unauthorized(request):
    return ("", 401, {"Content-Type": "application/json"})


@login_manager.request_loader
def authorize_user(request):
    api_key = request.headers.get('Authorization')

    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        api_key = base64.b64decode(api_key).decode("utf-8")
        email, password = api_key.split(":")

        user = User.query.filter_by(email=email).first()
        if user.check_password(password):
            return user
    return None