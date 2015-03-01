import base64
import json

from flask import Blueprint, jsonify, request, abort, url_for
from flask.ext.login import login_user

from ..models import User, Task, Tracking
from ..forms import TaskForm, TrackingForm
from ..extensions import login_manager, db


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
       #api_key = base64.b64decode(api_key).decode("utf-8")
       #email, password = api_key.split(":")
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


@api.route("/activities", methods=["GET", "POST"])
def activities():
    if request.method == "POST":
        return create_task()
    tasks = Task.query.all()
    tasks = [task.to_dict() for task in tasks]
    return jsonify({"activities": tasks})


def create_task():
    """Creates a new task from a JSON request."""
    user_id=require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = TaskForm(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        task = Task(form.name.data,
                    form.units.data,
                    form.t_type.data,
                    user_id)
        db.session.add(task)
        db.session.commit()
        return (json.dumps(task.to_dict()), 201, {"Location": url_for(".task", id=task.id)})
    else:
        return json_response(400, form.errors)


def update_task(id):
    user_id=require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    task = Task.query.get(id)
    form = TaskForm(obj=task, formdata=None, csrf_enabled=False)
    if form.validate_on_submit():
        form.populate_obj(task)
        db.session.commit()
        return (json.dumps(task.to_dict()), 201, {"Location": url_for(".task", id=task.id)})
    else:
        return json_response(400, form.errors)


def delete_task(id):
    user_id=require_authorization()
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'result': True})
    else:
        abort(404)
        

@api.route("/activities/<int:id>", methods=["GET", "PUT", "DELETE"])
def task(id):
    if request.method == "PUT":
        return update_task(id)
    elif request.method == "DELETE":
        return delete_task(id)
    stats = Tracking.query.filter_by(tr_task_id=id).order_by(Tracking.tr_date.desc())
    pairs = [stat.to_dict() for stat in stats]
    return jsonify({"activity": task.to_dict(),"values":pairs})
