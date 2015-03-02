import base64
import json

from datetime import datetime
from flask import Blueprint, jsonify, request, abort, url_for
from flask.ext.login import login_user, current_user
from ..models import Activity, Stat, User
from ..forms import ActivityForm
from ..extensions import login_manager, db

api = Blueprint("api", __name__)


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


def require_authorization():
    user = authorize_user(request)
    if user:
        login_user(user)
    else:
        abort(401)


@api.route("/api/v1/activities", methods=["GET", "POST"])
def user_activities():
    require_authorization()
    if request.method == "POST":
        return add_activity(request)
    else:
        activities = Activity.query.filter_by(owner=current_user.id)
        activities = [activity.to_dict() for activity in activities]
        for activity in activities:
            activity["location"] = request.url_root + url_for(".activity",
                                           activity_id=activity["id"])[1:]
        return jsonify({"activities": activities})


def add_activity(request):
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = ActivityForm(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        activity = Activity(**form.data)
        activity.owner = current_user.id
        activity.date = datetime.today().date()
        db.session.add(activity)
        db.session.commit()
        activity = activity.to_dict()
        activity["location"] = url_for(".activity", activity_id=activity["id"])
        return (json.dumps(activity), 201)
    else:
        return json_response(400, form.errors)


@api.route("/api/v1/activities/<int:activity_id>", methods=["GET", "PUT",
                                                            "DELETE"])
def activity(activity_id):
    require_authorization()
    if request.method == "PUT":
        return edit_activity(request, activity_id)
    elif request.method == "DELETE":
        return delete_activity(activity_id)
    else:
        activity = Activity.query.get_or_404(activity_id)
        stats = Stat.query.filter_by(activity=activity.id).all()
        activity = activity.to_dict()
        activity["stats"] = [stat.to_dict() for stat in stats]
        return jsonify(activity), 201


def edit_activity(request, activity_id):
    body = request.get_data(as_text=True)
    data = json.loads(body)
    activity = Activity.query.get_or_404(activity_id)
    form = ActivityForm(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        activity.title = form.title.data
        db.session.commit()
        return(json.dumps(activity.to_dict()), 201)
    else:
        return json_response(400, form.errors)


def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    stats = Stat.query.filter_by(activity=activity_id)
    for stat in stats:
        db.session.delete(stat)
    db.session.commit()
    db.session.delete(activity)
    db.session.commit()
    return json_response(201, "Deleted Activity")


@api.route("/api/v1/activities/<int:activity_id>/data", methods=["POST",
                                                                 "PUT",
                                                                 "DELETE"])
def modify_stat(activity_id):
    require_authorization()
    if request.method == "POST":
        return add_stat(request, activity_id)
    elif request.method == "PUT":
        return update_stat(request, activity_id)
    elif request.method == "DELETE":
        return delete_stat(request, activity_id)


def add_stat(request, activity_id):
    body = request.get_data(as_text=True)
    data = json.loads(body)
    if "date" in data.keys():
        try:
            date = datetime.strptime(data["date"], "%Y-%m-%d")
            stat = Stat.query.filter_by(activity=activity_id).filter_by(
                date=date).first()
            if stat:
                stat.value = data["value"]
                db.session.commit()
            else:
                stat = Stat(activity=activity_id,
                            date=date,
                            value=data["value"])
                db.session.add(stat)
                db.session.commit()
            return json_response(201, stat.to_dict())
        except ValueError:
            return json_response(400, "Invalid date format.")
    else:
        stat = Stat.query.filter_by(activity=activity_id).filter_by(
            date=datetime.today().date()).first()
        if stat:
            stat.value = data["value"]
            db.session.commit()
            return json_response(201, stat.to_dict())
        else:
            stat = Stat(activity=activity_id,
                        date=datetime.today().date(),
                        value=data["value"])
            db.session.add(stat)
            db.session.commit()
            return json_response(201, stat.to_dict())


def update_stat(request, activity_id):
    body = request.get_data(as_text=True)
    data = json.loads(body)
    if "date" not in data.keys():
        return json_response(400, "Date required.")
    else:
        try:
            date = datetime.strptime(data["date"], "%Y-%m-%d")
            stat = Stat.query.filter_by(activity=activity_id).filter_by(
                date=date).first()
            if not stat:
                return json_response(400, "Stat not found.")
            else:
                stat.value = data["value"]
                db.session.commit()
                return json_response(201, stat.to_dict())
        except ValueError:
            return json_response(400, "Invalid date format.")


def delete_stat(request, activity_id):
    body = request.get_data(as_text=True)
    data = json.loads(body)
    if "date" not in data.keys():
        return json_response(400, "Date required.")
    else:
        try:
            date = datetime.strptime(data["date"], "%Y-%m-%d")
            stat = Stat.query.filter_by(activity=activity_id).filter_by(
                date=date).first()
            if not stat:
                return json_response(400, "Stat not found.")
            else:
                db.session.delete(stat)
                db.session.commit()
                return json_response(201, "Activity stat deleted.")
        except ValueError:
            return json_response(400, "Invalid date format.")
