# import json
#
# from flask import Blueprint, jsonify, request, abort, url_for
# from flask.ext.login import login_user
#
# from ..models import User
# from ..extensions import login_manager, db
#
# api = Blueprint('api', __name__)
#
# def json_response(code, data):
#     return (json.dumps(data), code, {"Content-Type": 'application/json'})
#
# @api.app_errorhandler(401)
# def unauthorized(request):
#     return ("", 401, {"Content-Type": 'application/json'})
#
#
# @login_manager.request_loader
# def authorize_user(request):
#     api_key = request.headers.get('Authorization')
#     if api_key:
#         api_key = api_key.replace('Basic ', '', 1)
#         api_key = api_key.split(':')
#         email, password = api_key[0], api_key[1]
#         user = User.query.filter_by(email=email).first()
#         if user.check_password(password):
#             return user
#
#     return None
#
#
# def require_authorization():
#     user = authorize_user(request)
#     if user:
#         login_user(user)
#     else:
#         abort(401)