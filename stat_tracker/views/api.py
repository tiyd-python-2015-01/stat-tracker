import json
from functools import wraps
from flask import Blueprint, request, jsonify, g, Response, url_for, abort
from ..models import Activity, Stat
from ..forms import ActivityForm, StatForm
from ..extensions import db


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

@api.route('/activities', methods=['GET', 'POST'])
@returns_json
def get_activities():
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
            return (activity, 200)

@api.route('/activities/<int:id>')
@returns_json
def get_activity(id):
    activity = Activity.query.get(id)
    data = activity.to_dict()
    return {'activities': data}

@api.route('/activity/<int:id>/stats')
@returns_json
def get_stats_by_activity(id):
    stats = Stat.query.filter(Stat.activity_id == id).all()
    data = [stat.to_dict() for stat in stats]
    return {'stats': data}

@api.route('/user/<int:id>/stats')
@returns_json
def get_stats_by_user(id):
    stats = Stat.query.filter(Stat.user_id == id).all()
    data = [stat.to_dict() for stat in stats]
    return {'stats': data}



