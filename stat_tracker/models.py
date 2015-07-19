from . import db, bcrypt, login_manager
from flask.ext.login import UserMixin
from sqlalchemy import func
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(60))
    activities = db.relationship('Activity', backref='user')
    stats = db.relationship('Stats', backref='user')

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
        return User.query.get(id)


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    statistics = db.relationship('Stats', backref='activity')

    def to_dict(self):
        return {"id":self.id,
                "title": self.title,
                "description": self.description,
                "user_id": self.user_id}

class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(255), nullable=False)
    recorded_at = db.Column(db.DateTime)
    act_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
