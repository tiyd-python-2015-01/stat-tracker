import json

from flask import Blueprint, jsonify, request, abort, url_for
from flask.ext.login import login_user

from ..models import User, Item, Action
from ..forms import LoginForm, AddActivity, LogActivity
from ..extensions import login_manager, db
from .items import pick_activity


api = Blueprint("api", __name__)

def json_response(code, data):
    return (json.dumps(data), code, {"Content-Type": "application/json"})


@api.app_errorhandler(401)
def unauthorized(request):
    return ("", 401, {"Content-Type": "application/json"})


@login_manager.request_loader
def authorize_user(request):
    # Authorization: Basic username:password
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        email, password = api_key.split(":")

        user = User.query.filter_by(email=email).first()
        if user.check_password(password):
            return user
    return None


def require_authorization():
    user = authorize_user(request)
    if user:
        login_user(user)
        return user
    else:
        abort(401)


@api.route("/activities")
def activities():
    user = require_authorization()
    activities = Item.query.filter_by(user_id=user.id).all()
    activities = [activity.to_dict() for activity in activities]
    return jsonify({"activity": activities})

@api.route("/activities/<int:id>")
def activity(id):
    require_authorization()
    activity = Item.query.get_or_404(id)
    return jsonify(activity.to_dict())


@api.route("/activities/add", methods=['POST'])
def create_activities():
    user = require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = AddActivity(data=data, formdata=None, csrf_enabled=False)

    if form.validate():
        activity = Item(**form.data)
        activity.user_id = user.id
        db.session.add(activity)
        db.session.commit()
        return (json.dumps(activity.to_dict()), 201,
                {"Location": url_for(".activity", id=activity.id)})
    else:
        return json_response(400, form.errors)


@api.route("/activities/update/<int:id>", methods=['PUT'])
def update_activities(id):
    user = require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    activity = Item.query.get_or_404(id)

    activity.name = data.get('name')
    activity.goal = data.get('goal')
    activity.description = data.get('description')
    db.session.commit()
    return (json.dumps(activity.to_dict()), 201,
            {"Location": url_for(".activity", id=activity.id)})

@api.route("/activities/delete/<int:id>", methods=['DELETE'])
def delete_activities(id):
    require_authorization()
    activity = Item.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    return (json.dumps('deleted item: {}'.format(id)), 200,
            {"Content-Type": "application/json"})

@api.route("/logs")
def logs():
    user = require_authorization()
    logs = Action.query.filter(Action.item.has(user_id=user.id))
    logs = [log.to_dict() for log in logs]
    return jsonify({"logs": logs})

@api.route("/logs/<int:id>")
def log(id):
    require_authorization()
    log = Action.query.get_or_404(id)
    return jsonify(log.to_dict())

@api.route("/logs/add", methods=['POST'])
def create_logs():
    user = require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = LogActivity(data=data, formdata=None, csrf_enabled=False)
    form.item_id.choices = pick_activity()

    if form.validate():
        log = Action(**form.data)
        db.session.add(log)
        db.session.commit()
        return (json.dumps(log.to_dict()), 201,
                {"Location": url_for(".log", id=log.id)})
    else:
        return json_response(400, form.errors)

@api.route("/logs/update/<int:id>", methods=['PUT'])
def update_logs(id):
    user = require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    log = Action.query.get_or_404(id)

    log.value = data.get('value')
    log.logged_at = data.get('logged_at')
    db.session.commit()
    return (json.dumps(log.to_dict()), 201,
            {"Location": url_for(".log", id=log.id)})

@api.route("/logs/delete/<int:id>", methods=['DELETE'])
def delete_logs(id):
    require_authorization()
    log = Action.query.get_or_404(id)
    db.session.delete(log)
    db.session.commit()
    return (json.dumps('deleted item: {}'.format(id)), 200,
            {"Content-Type": "application/json"})
