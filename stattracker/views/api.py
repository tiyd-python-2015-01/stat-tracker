import base64
import json

from flask import Blueprint, jsonify, request, abort, url_for, Response, g
from flask.ext.login import login_user, current_user

from ..models import Enterprise, User, Stat
from ..forms import EnterpriseForm, StatForm, RegistrationForm
from ..extensions import login_manager, db

from functools import wraps
from datetime import datetime

api = Blueprint('api', __name__)


def json_response(code, data):
    return (json.dumps(data), code, {"Content-Type": "application/json"})


@api.app_errorhandler(401)
def unauthorized(request):
    return ("", 401, {"Content-Type": "application/json"})


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
    else:
        abort(401)

@api.route("/users", methods=["GET"])
def users():
    users = User.query.all()
    users = [user.to_dict() for user in users]
    return jsonify({"users": users})


@api.route("/users", methods=["POST"])
def add_user():
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = RegistrationForm(data=data, formdata=None, csrf_enabled=False)
    return json.dumps(form.data)
    # if form.validate():
    #     user = User(**form.data)
    #     db.session.add(user)
    #     db.session.commit()
    #     user = user.to_dict()
    #     return(json.dumps(user), 201)
    # else:
    #     return json_response(400, form.errors)


@api.route("/activities", methods=["GET", "POST"])
def user_activities():
    if request.method == "POST":
        return add_activity()
    else:
        enterprises = Enterprise.query.filter_by(user_id=current_user.id)
        enterprises = [enterprise.to_dict() for enterprise in enterprises]
        # for enterprise in enterprises:
        #     enterprise["location"] = request.url_root + url_for(".enterprise",
        #                                 enterprise_id=enterprise["id"])
        return jsonify({"activities": enterprises})

def add_activity():
    require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = EnterpriseForm(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        enterprise = Enterprise(**form.data)
        enterprise.user_id = current_user.id
        db.session.add(enterprise)
        db.session.commit()
        enterprise = enterprise.to_dict()
        return (json.dumps(enterprise), 201)
    else:
        return json_response(400, form.errors)

@api.route("/activities/<int:id>", methods=["GET"])
def enterprise(id):
    require_authorization()
    enterprise = Enterprise.query.get_or_404(id)
    stats = Stat.query.filter_by(enterprise_id=enterprise.id).all()
    enterprise = enterprise.to_dict()
    enterprise["stats"] = [stat.to_dict() for stat in stats]
    return jsonify(enterprise), 201

@api.route("/activities/<int:id>", methods=["POST"])
def edit_enterprise(id):
    require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    enterprise = Enterprise.query.get_or_404(id)
    form = EnterpriseForm(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        enterprise.ent_name = form.ent_name.data
        enterprise.ent_unit = form.ent_unit.data
        db.session.commit()
        return(json.dumps(enterprise.to_dict()), 201)
    else:
        return json_response(400, form.errors)

@api.route("/activities/<int:id>", methods=["DELETE"])
def delete_enterprise(id):
    require_authorization()
    enterprise = Enterprise.query.get_or_404(id)
    stats = Stat.query.filter_by(enterprise_id=id)
    for stat in stats:
        db.session.delete(stat)
    db.session.commit()
    db.session.delete(enterprise)
    db.session.commit()
    return json_response(201, "Deleted Activity")



@api.route("/activities/<int:id>/data", methods=["POST",
                                                                 "PUT",
                                                                 "DELETE"])
def modify_stat(id):
    require_authorization()
    if request.method == "POST":
        return add_stat(id)
    elif request.method == "PUT":
        return update_stat(id)
    elif request.method == "DELETE":
        return delete_stat(id)


def add_stat(id):
    body = request.get_data(as_text=True)
    data = json.loads(body)
    if "recorded_at" in data.keys():
        try:
            date = datetime.strptime(data["recorded_at"], "%Y-%m-%d")
            stat = Stat.query.filter_by(enterprise_id=id).filter_by(
                recorded_at=date).first()
            if stat:
                stat.value = data["value"]
                db.session.commit()
            else:
                stat = Stat(enterprise_id=id,
                            recorded_at=date,
                            value=data["value"])
                db.session.add(stat)
                db.session.commit()
            return json_response(201, "Stat added")
        except ValueError:
            return json_response(400, "Invalid date format.")
    else:
        stat = Stat.query.filter_by(enterprise_id=id).filter_by(
            recorded_at=datetime.today().date()).first()
        if stat:
            stat.value = data["value"]
            db.session.commit()
            return json_response(201, stat.to_dict())
        else:
            stat = Stat(enterprise_id=id,
                        recorded_at=date,
                        value=data["value"])
            db.session.add(stat)
            db.session.commit()
            return json_response(201, stat.to_dict())


def update_stat(id):
    body = request.get_data(as_text=True)
    data = json.loads(body)
    if "recorded_at" not in data.keys():
        return json_response(400, "Date required.")
    else:
        try:
            date = datetime.strptime(data["recorded_at"], "%Y-%m-%d")
            stat = Stat.query.filter_by(enterprise_id=id).filter_by(
                recorded_at=date).first()
            if not stat:
                return json_response(400, "Stat not found.")
            else:
                stat.value = data["value"]
                db.session.commit()
                return json_response(201, "Stat Updated")
        except ValueError:
            return json_response(400, "Invalid date format.")


def delete_stat(id):
    body = request.get_data(as_text=True)
    data = json.loads(body)
    if "recorded_at" not in data.keys():
        return json_response(400, "Date required.")
    else:
        try:
            date = datetime.strptime(data["recorded_at"], "%Y-%m-%d")
            stat = Stat.query.filter_by(enterprise_id=id).filter_by(
                recorded_at=date).first()
            if not stat:
                return json_response(400, "Stat not found.")
            else:
                db.session.delete(stat)
                db.session.commit()
                return json_response(201, "Activity stat deleted.")
        except ValueError:
            return json_response(400, "Invalid date format.")
