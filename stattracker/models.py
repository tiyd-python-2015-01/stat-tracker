from .extensions import db

"""Add your models here."""

from . import db, bcrypt, login_manager
from flask.ext.login import UserMixin
from sqlalchemy import func


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

    def to_dict(self):
        return {"id": self.id,
                "name": self.name,
                "email": self.email}

    def __repr__(self):
        return "<User {}>".format(self.email)


class Enterprise(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ent_name = db.Column(db.String(255), nullable=False)
    ent_unit = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('enterprises', lazy='dynamic'))

    def to_dict(self):
        return {"id": self.id,
                "ent_name": self.ent_name,
                "ent_unit": self.ent_unit,
                "user_id": self.user_id}

    def __repr__(self):
        return "<Enterprise: {}>".format(self.ent_name)

class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, nullable=False)
    enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprise.id'))
    enterprise = db.relationship('Enterprise',
        backref=db.backref('stats', lazy='dynamic'))

    def to_dict(self):
        return {"id": self.id,
                "value": self.value,
                "recorded_at": self.recorded_at,
                "enterprise_id": self.enterprise_id}
