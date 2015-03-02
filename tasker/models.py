from . import db, bcrypt, login_manager
from flask.ext.login import UserMixin
from hashids import Hashids
from sqlalchemy import func, and_
from datetime import date, timedelta, datetime
from flask import request, url_for

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(60))

    def get_password(self):
        return getattr(self, "_password", None)

    def set_password(self, password):
        self._password = password
        self.encrypted_password = bcrypt.generate_password_hash(password)

    password = property(get_password, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_name = db.Column(db.String(255), nullable=False)
    t_type = db.Column(db.Integer, nullable=False)
    t_units = db.Column(db.String(255), nullable=False)
    t_user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, t_name, t_units, t_type, t_user):
        self.t_name = t_name
        self.t_units = t_units
        self.t_type = t_type
        self.t_user = t_user


    def to_dict(self):
        return {'id': self.id,
                'name': self.t_name,
                'type': self.t_type,
                'user': self.t_user,
                'units': self.t_units,
                'url': str(request.url_root)+url_for('api.api_task', id=self.id)[1:] }

class Tracking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tr_value = db.Column(db.Integer, nullable=False)
    tr_beg_value = db.Column(db.Integer)
    tr_end_value = db.Column(db.Integer)
    tr_target_date = db.Column(db.Date)
    tr_date = db.Column(db.Date, nullable=False)
    tr_task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    tr_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,
                 user_id,
                 task_id,
                 date,
                 value=0,
                 beg_value=0,
                 end_value=0,
                 target_date=date(3000,1,1),
                 ):
        self.tr_user_id = user_id
        self.tr_value = value
        self.tr_beg_value = beg_value
        self.tr_end_value = end_value
        self.tr_target_date = target_date
        self.tr_date = date
        self.tr_task_id = task_id

    def to_dict(self):
        return {'date': str(self.tr_date),
                'value': self.tr_value}
