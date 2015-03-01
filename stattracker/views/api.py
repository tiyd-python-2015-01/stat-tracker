import base64
import json

from flask import Blueprint, jsonify, request, abort, url_for, Response, g
from flask.ext.login import login_user

from ..models import Enterprise, User, Stat
from ..forms import EnterpriseForm, StatForm
from ..extensions import login_manager, db

from functools import wraps


def returns_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        retval = f(*args, **kwargs)
        if type(retval) is Response:
            return retval
        elif type(retval) is tuple:
            response = jsonify(retval[0])
            if len(retval) > 1:
                response.status_code = retval[1]
            if len(retval) > 2:
                for key, value in retval[2].items():
                    response.headers[key] = value
            return response
        else:
            return jsonify(retval)
    return decorated_function

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


def require_authorization():
    user = authorize_user(request)
    if user:
        login_user(user)
    else:
        abort(401)


@api.route("/activities", methods=["GET", "POST"])
def activities():
    if request.method == "POST":
        return create_activity()

    enterprises = Enterprise.query.all()
    enterprises = [enterprise.to_dict() for enterprise in enterprises]
    return jsonify({"activities": enterprises})


def create_bookmark():
    """Creates a new enterprise from a JSON request."""
    require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = EnterpriseForm(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        enterprise = Enterprise.query.filter_by(url=form.ent_name.data).first()
        if enterprise:
            return json_response(400, {"ent_value": "This activity has already been created."})
        else:
            enterprise = Enterprise(**form.data)
            db.session.add(enterprise)
            db.session.commit()
            return (json.dumps(enterprise.to_dict()), 201, {"Location": url_for(".create_enterprise", id=enterprise.id)})
    else:
        return json_response(400, form.errors)


@api.route("/activities/<int:id>")
def enterprise(id):
    enterprise = Enterprise.query.get_or_404(id)
    return jsonify(enterprise.to_dict())
