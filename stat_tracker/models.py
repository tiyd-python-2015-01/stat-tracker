from collections import Counter
from flask.ext.login import UserMixin
from flask import request
from . import db, bcrypt, login_manager


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    activity_type = db.Column(db.String,nullable=False)
    creator = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))

    def to_web(self):
        return {"name": self.name,
                "website": "{}{}/{}".format(request.url_root, self.creator, self.name)}

    def to_dict(self):
        return {"name": self.name,
                "activity_type": self.activity_type,
                "creator": self.creator,
                "description": self.description}


class Timestamp(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    activity_id = db.Column(db.Integer, nullable=False)
    actor_id = db.Column(db.Integer, nullable=False)

    def daily_frequency(self):
        dates = []
        for stamp in db.session.query(Timestamp).filter_by(url_id=self.url_id).all():
            date = stamp.timestamp.strftime('%Y-%m-%d')
            dates.append(date)
        date_counts = Counter(dates)
        return date_counts

    def to_dict(self):
        return {"timestamp": self.timestamp}

class UnitGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    units = db.Column(db.DateTime, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    activity_id = db.Column(db.Integer, nullable=False)
    actor_id = db.Column(db.Integer, nullable=False)

    def daily_frequency(self):
        dates = []
        for stamp in db.session.query(Timestamp).filter_by(url_id=self.url_id).all():
            date = stamp.timestamp.strftime('%Y-%m-%d')
            dates.append(date)
        date_counts = Counter(dates)
        return date_counts

    def to_dict(self):
        return {"timestamp": self.timestamp,
                "units": self.units}


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

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))