import json
import base64
from functools import wraps
from flask.ext.login import login_user, current_user
from flask import Blueprint, request, jsonify, g, Response, url_for, abort

# from ..api_helpers import returns_json, APIView, api_form
from ..models import Activity, Stats, User
from ..forms import ActivityForm, RegistrationForm, EditForm
from ..extensions import db, login_manager
from datetime import datetime


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
        return user.id
    else:
        abort(401)

@api.route("/activity/", methods=['POST'])
def post_activity():
    user_id = require_authorization()
    body = request.get_data(as_text='True')
    data = json.loads(body)
    form = ActivityForm(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        check = Activity.query.filter_by(title=form.title.data).first()
        if not check:
            activity = Activity(title = form.title.data,
                                description = form.description.data,
                                user_id= user_id)
            db.session.add(activity)
            db.session.commit()
            return jsonify(activity.to_dict())
        else:
            return jsonify({"Error: Activity Exists": 400})
    return jsonify({"Test":400})



@api.route("/activity/<int:id>", methods=['GET'])
def get_activity(id):
    activity = Activity.query.filter_by(id=id).first()
    return jsonify(activity.to_dict())
