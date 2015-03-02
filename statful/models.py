from . import db, bcrypt, login_manager
from flask import request, url_for
from flask.ext.login import UserMixin
from sqlalchemy import func


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    encrypted_password = db.Column(db.String(60))
    activity_id = db.relationship('Activity', backref='user', cascade="all,delete")

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

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255))
    unit = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stat_id = db.relationship('Stat', backref='activity', cascade="all,delete")

    def stats_by_day(self):
        stat_date = func.cast(Stat.when, db.Date)
        return db.session.query(stat_date, func.count(Stat.occurrences)). \
            group_by(stat_date).filter_by(activity_id=self.id). \
            order_by(stat_date).all()

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'unit': self.unit,
                'type': self.type,
                'user id': self.user_id,
                'url': str(request.url_root)[:-1:]+str(url_for('api.activity', id=self.id))}

class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    occurrences = db.Column(db.Integer)
    yes_no = db.Column(db.Integer)
    scale = db.Column(db.Integer)
    when = db.Column(db.DateTime)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)

    def to_dict(self):
        return {'id': self.id,
                'occurrences': self.occurrences,
                'Completed': self.yes_no,
                'scale': self.scale,
                'Date': str(self.when)
               }











