import base64
import json

from flask import Blueprint, jsonify, request, abort, url_for, g
from flask.ext.login import login_user, current_user

from ..models import User, Task, Tracking
from ..forms import TaskForm, TrackingForm, DeleteTrackingForm
from ..extensions import login_manager, db

from sqlalchemy.sql import and_

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
       api_key = api_key.split(":")
       email, password = api_key[0],  api_key[1]
       user = User.query.filter_by(email=email).first()
       if user.check_password(password):
            return user
    return None


def require_authorization():
    user = authorize_user(request)
    if user:
        login_user(user)
        return(user.id)
    else:
        abort(401)
        return None


@api.route("/stats", methods=["GET"])
def get_activities():
    tasks = [task.to_dict() for task in Task.query.all()]
    return jsonify({"activities": tasks})


@api.route("/stats", methods=["POST"])
def post_activities():
    #user_id=require_authorization()
    stats_data = request.get_json()
    form = TaskForm(data=stats_data)
    if form.validate():
        task = Task(form.t_name.data,
                    form.t_units.data,
                    form.t_type.data,
                    user_id)
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict())
    else:
        resp = jsonify(form.errors)
        resp.status_code = 400
        return resp


@api.route("/stats/<int:id>", methods=["GET"])
def api_task_get(id):
    task = Task.query.get(id)
    stats = Tracking.query.filter_by(tr_task_id=id).order_by(Tracking.tr_date.desc())
    pairs = [stat.to_dict() for stat in stats]
    return jsonify({"activity": task.to_dict(),"values":pairs})


@api.route("/stats/<int:id>", methods=["PUT"])
def api_task_edit(id):
    user_id=require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = TaskForm(data=data, formdata=None, csrf_enabled=False)
    task = Task.query.get(id)
    if task:
        task.t_name = form.t_name.data
        task.t_type = form.t_type.data
        task.t_units = form.t_units.data
        task.t_user = user_id
        db.session.add(task)
        db.session.commit()
        return (json.dumps(task.to_dict()), 201, {"Location": url_for(".task", id=task.id)})
    else:
        return json_response(400, form.errors)


@api.route("/stats/<int:id>", methods=["DELETE"])
def api_task_del(id):
    user_id=require_authorization()
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'result': True})
    else:
        abort(404)


@api.route("/stats/<int:id>/data", methods=["GET"])
def api_stat_get(id):
    stats = Tracking.query.filter_by(tr_task_id=id).order_by(Tracking.tr_date.desc())
    pairs = [stat.to_dict() for stat in stats]
    return jsonify({"values":pairs})


@api.route("/stats/<int:id>/data", methods=["POST"])
def api_stat_add(id):
#user_id=require_authorization()
    try:
	    body = request.get_data(as_text='true')
	    data = json.loads(body)
	    form = TrackingForm(data=data, formdata=None, csrf_enabled=False)
    except ValueError:
        form = TrackingForm()
    date_read = form.tr_date.data
    value_read = form.tr_value.data
    stat = Tracking(user_id=current_user.id,
                    task_id=id,
                    date=date_read,
                    value= value_read)
    db.session.add(stat)
    db.session.commit()
    return jsonify({"stat":stat.to_dict()})


@api.route("/stats/<int:id>/data", methods=["PUT"])
def api_stat_edit(id):
        #user_id=require_authorization()
        body = request.get_data(as_text=True)
        data = json.loads(body)
        form = TrackingForm(data=data, formdata=None, csrf_enabled=False)
        stat = Tracking.query.filter(and_(Tracking.tr_task_id==id, Tracking.tr_date==form.tr_date.data)).first()
        if stat:
            stat.tr_date = form.tr_date.data
            stat.tr_value = form.tr_value.data
            db.session.add(stat)
            db.session.commit()
            return jsonify({"stat":stat.to_dict()})
        else:
            abort(404)


@api.route("/stats/<int:id>/data", methods=["GET", "POST", "PUT", "DELETE"])
def api_stat_del(id):
    #user_id=require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = DeleteTrackingForm(data=data, formdata=None, csrf_enabled=False)
    stat = Tracking.query.filter(and_(Tracking.tr_task_id==id, Tracking.tr_date==form.tr_date.data)).first()
    if stat:
        db.session.delete(stat)
        db.session.commit()
        return jsonify({'result': True})
    else:
        abort(404)
