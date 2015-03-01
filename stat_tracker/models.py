from . import db, bcrypt, login_manager
from datetime import date, timedelta, datetime
# from sqlalchemy import func, and_
from flask.ext.login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(60))

    def set_password(self, password):
        self.encrypted_password = bcrypt.generate_password_hash(password)

    password = property(None, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)


class Activity(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey(User.id))
    activity_type = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<Activity {}>".format(self.title)

    def to_dict(self):
        return {"id": self.id,
                "title": self.title,
                "type": self.activity_type,
                "created": str(self.date)}


class Stat(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.Integer, db.ForeignKey(Activity.id))
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<Stat {}>".format(self.value)

    def to_dict(self):
        return {"id": self.id,
                "activity": self.activity,
                "value": self.value,
                "date": str(self.date)}
