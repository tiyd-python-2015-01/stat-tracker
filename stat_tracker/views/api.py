import json

from flask import Blueprint, jsonify, request, abort, url_for, g
from flask.ext.login import login_user

from ..api_helpers import returns_json, APIView, api_form
from ..models import User, Item, Action
from ..forms import LoginForm, AddActivity, LogActivity
from ..extensions import login_manager, db
from .items import pick_activity


api = Blueprint("api", __name__)

@api.app_errorhandler(401)
@returns_json
def unauthorized(request):
    return {"error": "This API call requires authentication."}, 401


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
    if not current_user.is_authenticated():
        abort(401)

class ActivitiesView(APIView):

    def get(self):
        activities = Item.query.filter_by(user_id=current_user.id).all()
        activities = [activity.to_dict() for activity in activities]
        return {'activities': activities}

    def post(self):
        require_authorization()
        form = api_form(AddActivity, data=g.data)

        if form.validate():
            activity = Item(**form.data)
            activity.user_id = current_user.id
            db.session.add(activity)
            db.session.commit()
            return activity.to_dict(), 201
        else:
            return form.errors, 400


class SingleActView(APIView):

    def get(self, id):
        activity = Item.query.get_or_404(id)
        return activity.to_dict()

    def put(self, id):
        require_authorization()
        activity = Item.query.get_or_404(id)
        for key, value in g.data.items():
            setattr(activity, key, value)
        form = api_form(AddActivity, obj=activity)
        if form.validate():
            form.populate_obj(activity)
            db.session.commit()
            return activity.to_dict(), 201
        else:
            return form.errors, 400


    def delete(self, id):
        require_authorization()
        activity = Item.query.get_or_404(id)
        db.session.delete(activity)
        db.session.commit()
        return 201


class LogsView(APIView):

    def get(self):
        logs = Action.query.filter(Action.item.has(user_id=current_user.id))
        logs = [log.to_dict() for log in logs]
        return {"logs": logs}

    def post(self):

        require_authorization()
        form = api_form(LogActivity, data=g.data)
        form.item_id.choices = pick_activity()

        if form.validate():
            log = Action(**form.data)
            db.session.add(log)
            db.session.commit()
            return log.to_dict(), 201
        else:
            return form.errors, 400


class SingleLogView(APIView):

    def get(self, id):
        log = Action.query.get_or_404(id)
        return log.to_dict()

    def put(self, id):
        require_authorization()
        log = Action.query.get_or_404(id)

        for key, value in g.data.items():
            setattr(log, key, value)
        form = api_form(LogActivity, obj=log)
        if form.validate():
            form.populate_obj(log)
            db.session.commit()
            return log.to_dict(), 201
        else:
            return form.errors, 400

    def delete(self, id):
        require_authorization()
        log = Action.query.get_or_404(id)
        db.session.delete(log)
        db.session.commit()
        return 201


api.add_url_rule('/activities', view_func=ActivitiesView.as_view('activities'))
api.add_url_rule('/activity/<int:id>', view_func=SingleActView.as_view('activity'))
api.add_url_rule('/logs', view_func=LogsView.as_view('logs'))
api.add_url_rule('/log/<int:id>', view_func=SingleLogView.as_view('log'))
