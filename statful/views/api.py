import json
import base64
from flask import Blueprint, jsonify, request, abort, url_for
from flask.ext.login import login_user
from ..forms import ActivityForm, UpdateForm
from ..models import User, Activity, Stat
from ..extensions import login_manager, db
from datetime import datetime


api = Blueprint('api', __name__)


def json_response(code, data):
    return (json.dumps(data), code, {"Content-Type": 'application/json'})


@api.app_errorhandler(401)
def unauthorized(request):
    return ("", 401, {"Content-Type": 'application/json'})


@login_manager.request_loader
def authorize_user(request):
    authorization = request.authorization
    if authorization:
        email = authorization['username']
        password = authorization['password']

        user = User.query.filter_by(email=email).first()
        if user.check_password(password):
            return user

    return None



def require_authorization():
    user = authorize_user(request)
    if user:
        login_user(user)
        return user.id
    else:
        abort(401)
        return None


@api.route('/activities', methods=["GET", "POST"])
def activites():
    if request.method == "POST":
        return create_activity()

    activities = Activity.query.all()
    activities = [activity.to_dict() for activity in activities]
    return jsonify({"activities": activities})


def create_activity():
    """Creates a new link from a JSON request."""
    id = require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = ActivityForm(data=data, formdata=None, csrf_enabled=False)
    accepted_types = ['clicker', 'yes_no', 'scale']
    if form.validate():
        activity = Activity.query.filter_by(name=form.name.data).first()
        if activity:
            return json_response(400, {"url": "You have already submitted this activity."})
        else:
            if form.type.data not in accepted_types:
                return json_response(400, {"url": "You did not submit an accepted activity type."})
        activity = Activity(name=form.name.data,
                            type=form.type.data,
                            unit=form.unit.data,
                            user_id=id)
        db.session.add(activity)
        db.session.commit()
        return (json.dumps(activity.to_dict()), 201, {"Location": url_for(".activity", id=activity.id)})
    else:
        return json_response(400, form.errors)


@api.route("/activities/<int:id>", methods=["GET", "PUT", "DELETE"])
def activity(id):
    if request.method == 'PUT':
        return change_activity(id)

    if request.method == "DELETE":
        return delete_activity(id)

    activity = Activity.query.get_or_404(id)
    stats = activity.stat_id
    stats = [stat.to_dict() for stat in stats]
    activity = activity.to_dict()
    return jsonify({"activity": activity, "stats": stats})


def delete_activity(id):
    require_authorization()
    activity = Activity.query.filter(Activity.id == id).first()
    db.session.delete(activity)
    db.session.commit()
    return ("Yay")


def change_activity(id):
    require_authorization()
    activity = Activity.query.filter(Activity.id == id).first()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = ActivityForm(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        activity.name = form.name.data
        activity.type = form.type.data
        activity.unit = form.unit.data
        db.session.commit()
        return (json.dumps(activity.to_dict()), 201, {"Location": url_for(".activity", id=activity.id)})
    else:
        return json_response(400, form.errors)


@api.route('/activities/<int:id>/stats', methods=["POST", "PUT", "DELETE"])
def stats(id):
    # require_authorization()
    activity = Activity.query.filter(Activity.id == id).first()
    if request.method == "POST" or request.method == "PUT":
        return change_make_stat(request, activity)

    if request.method == "DELETE":
        return delete_stat(activity)

    return


def change_make_stat(request, activity):
    try:
        body = request.get_data(as_text='true')
        data = json.loads(body)
        form = UpdateForm(data=data, formdata=None, crsf_enabled=False)
    except ValueError:
        form = UpdateForm()
    stat = Stat.query.filter(Stat.when == form.date.data).filter(Stat.activity_id == activity.id).first()
    if stat:
        stat.occurrences = form.occurrences.data
        stat.scale = form.scale.data
        stat.yes_no = form.yes_no.data
        db.session.commit()
        return json_response(200, "yay")
    else:
        stat = Stat(occurrences=form.occurrences.data,
                    scale=form.scale.data,
                    yes_no=form.yes_no.data,
                    when=form.date.data,
                    activity_id=activity.id
                    )
        db.session.add(stat)
        db.session.commit()
        return json_response(200, "yay")
    return json_response(400, form.errors)


def delete_stat(activity):
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = UpdateForm(data=data, formdata=None, csrf_enabled=False)
    stat = Stat.query.filter(Stat.when == form.date.data).filter(Stat.activity_id == activity.id).first()
    if stat:
        db.session.commit()
        return ("Deleted")
    else:
        abort(401)
