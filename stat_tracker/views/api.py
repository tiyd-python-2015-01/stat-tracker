import json
import base64
from functools import wraps
from flask.ext.login import login_user, current_user
from flask import Blueprint, request, jsonify, g, Response, url_for, abort
from ..models import Activity, Stat, User
from ..forms import ActivityForm, StatForm, APIStatForm
from ..extensions import db, login_manager


api = Blueprint("api", __name__)

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

@login_manager.request_loader
def authorize_user(request):
    # Authorization: Basic username:password
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

@api.route('/activities/', methods=['GET', 'POST'])
@returns_json
def get_activities():
    require_authorization()
    if request.method == 'POST':
        return create_activity()
    activities = Activity.query.all()
    data = [activity.to_dict() for activity in activities]
    return {'activities': data}

def create_activity():
    """creates a new activity from a JSON request"""
    body = request.get_data(as_text='true')
    data = json.loads(body)
    form = ActivityForm(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        activity = Activity.query.filter_by(name=form.name.data).first()
        if activity:
            return ({'name': 'This activity name has already been taken'}, 400)
        else:
            activity = Activity(**form.data)
            db.session.add(activity)
            db.session.commit()
            return (activity.to_dict(), 200)

@api.route('/activities/<int:id>/')
@returns_json
def get_activity(id):
    require_authorization()
    activity = Activity.query.get(id)
    data = activity.to_dict()
    return {'activities': data}

@api.route('/activities/<int:id>/', methods=["DELETE"])
@returns_json
def delete_activity(id):
    require_authorization()
    activity = Activity.query.get(id)
    db.session.delete(activity)
    db.session.commit()
    return {'Deleted': id }


@api.route('/activities/<int:id>/stats')
@returns_json
def get_stats_by_activity(id):
    require_authorization()
    stats = Stat.query.filter(Stat.activity_id == id).all()
    data = [stat.to_dict() for stat in stats]
    return {'stats': data}


@api.route('/activities/<int:id>/', methods=["PUT"])
@returns_json
def edit_activity(id):
    require_authorization()
    body = request.get_data(as_text='true')
    data = json.loads(body)
    form = ActivityForm(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        activity = Activity.query.filter_by(name=form.name.data).first()
        if activity:
            activity.name = form.name.data
            activity.unit = form.unit.data
            db.session.add(activity)
            db.session.commit()
            return activity.to_dict()
        else:
            {"Can't find this activity"}

@api.route('/activities/<int:id>/stats', methods=["PUT", "POST"])
@returns_json
def add_stat(id):
    #require_authorization()
    try:
        body = request.get_data(as_text='true')
        data = json.loads(body)
        form = APIStatForm(data=data, formdata=None, csrf_enabled=False)
    except ValueError:
        form = APIStatForm()
    activity = Activity.query.get(id)
    if form.validate():
        stat = Stat.query.filter_by(date=form.date.data).first()
        if stat:
            stat.value = form.value.data
        else:
            stat = Stat(user_id=current_user.id,
                        activity_id=activity.id,
                        date=form.date.data,
                        value=form.value.data)
        db.session.add(stat)
        db.session.commit()
        return stat.to_dict()
    else:
        return {"You're input is all wrong :("}

@api.route('/activities/<int:id>/stats', methods=["DELETE"])
@returns_json
def delete_stat(id):
    require_authorization()
    body = request.get_data(as_text='true')
    data = json.loads(body)
    form = APIStatForm(data=data, formdata=None, csrf_enabled=False)
    stat = Stat.query.filter(Stat.date == form.date.data).first()
    if stat:
        db.session.delete(stat)
        db.session.commit()
        return {"stat": "deleted"}
    else:
        return {"NO STAT": "LIKE DAT!"}

