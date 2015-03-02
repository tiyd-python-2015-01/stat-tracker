from flask import Blueprint, jsonify, request, abort, url_for
from ..models import Activities, User, Stat
from ..extensions import login_manager, db
from ..forms import AddNewAction, EditAction, AddNewStat, EditStat, DateSearch
from flask.ext.login import login_user, current_user


import json
import base64

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
    require_authorization()
    activities = Activities.query.all()
    activities = [a.to_dict() for a in activities]
    return jsonify({'activities': activities})


@api.route('/activities/<int:id>')
def activity(id):
    require_authorization()
    activities = Activities.query.get_or_404(id)
    stats = Stat.query.filter_by(activity_id=id).all()
    stats = [stat.stat_to_dict() for stat in stats]
    activities = activities.to_dict()
    return jsonify({'activities': activities, 'stats': stats})


@api.route('/activities', methods=['POST'])
def create_activity():
    require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = AddNewAction(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        a = Activities.query.filter_by(user_id=current_user.id).filter_by(name=form.name.data).first()
        if a:
            return('You are already tracking that activity!')
        else:
            act = Activities(name=form.name.data)
            db.session.add(act)
            db.session.commit()
            return json.dumps(act.to_dict(), 201)
    else:
        return json_response(400, form.errors)


@api.route('/activities/<int:id>', methods=['PUT'])
def edit_activity(id):
    require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    form = EditAction(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        ac = Activities.query.get_or_404(id)
        ac.name = form.name.data
        db.session.commit()
        return json.dumps(ac.to_dict(), 201)
    else:
        return json_response(400, form.errors)


@api.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    act = Activities.query.get_or_404(id)
    db.session.delete(act)
    db.session.commit()
    return json_response(201, 'Activity Deleted')


@api.route('/activities/<int:id>/stats')
def get_stats(id):
    require_authorization()
    stats = Stat.query.filter_by(activity_id=id).all()
    stats = [stat.stat_to_dict() for stat in stats]
    return jsonify({'stats': stats})


@api.route('/activities/<int:id>/stats', methods=['PUT', 'POST'])
def create_stat(id):
    require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    act = Activities.query.get_or_404(id)
    form = AddNewStat(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        check = Stat.query.filter_by(activity_id=act.id).filter_by(time=form.date.data).first()
        if check:
            check.ammount = form.ammount.data
            db.session.commit()
            return json.dumps(check.stat_to_dict(), 201)
        else:
            new = Stat(user_id=current_user.id,
                       activity_id=act.id,
                       ammount=form.ammount.data,
                       time=form.date.data)
            db.session.add(new)
            db.session.commit()
            return json.dumps(new.stat_to_dict(), 201)
    else:
        return json_response(400, form.errors)


@api.route('/activities/<int:id>/stats', methods=['DELETE'])
def delete_stat(id):
    require_authorization()
    body = request.get_data(as_text=True)
    data = json.loads(body)
    act = Activities.query.get_or_404(id)
    form = DateSearch(data=data, formdata=None, csrf_enabled=False)
    if form.validate():
        stat = Stat.query.filter_by(activity_id=act.id).filter_by(time=form.date.data).first()
        if not stat:
            return 'Entry does not exist.'
        else:
            db.session.delete(stat)
            db.session.commit()
            return(201, 'Stat Deleted')
    else:
        return json_response(400, form.errors)
