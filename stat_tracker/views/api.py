from flask import Blueprint, jsonify, request, abort, url_for
from ..models import Activities, User, Stat
from ..extensions import login_manager
from flask.ext.login import login_user


api = Blueprint('api', __name__)


def json_response(code, data):
    return (json.dumps(data), code, {"Content-Type": "application/json"})

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


@api.route('/activities')
def activities():
    #require_authorization()
    activities = Activities.query.all()
    activities = [a.to_dict() for a in activities]
    return jsonify({'activities': activities})


@api.route('/activities/<int:id>')
def activity(id):
    activities = Activities.query.get_or_404(id)
    stats = Stat.query.filter_by(activity_id=id).all()
    stats = [stat.stat_to_dict() for stat in stats]
    activities = activities.to_dict()
    return jsonify({'activities': activities, 'stats': stats})
