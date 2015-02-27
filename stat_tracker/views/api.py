from flask import Blueprint, jsonify, request, abort, url_for
from ..models import Links, User
from ..extensions import login_manager
from flask.ext.login import login_user

api = Blueprint('api', __name__)

@api.app_errorhandler(401)
def unauthorized(request):
    return ("", 401, {'Content-Type': "application/json"})

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


@api.route('/links')
def links():
    #require_authorization()
    links = Links.query.all()
    links = [link.to_dict() for link in links]
    return jsonify({'links': links})


@api.route('/links/<int:id>')
def link(id):
    link = Links.query.get_or_404(id)
    return jsonify
