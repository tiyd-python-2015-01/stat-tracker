from . import db, bcrypt, login_manager
from flask.ext.login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    encrypted_password = db.Column(db.String(60))
    activity_id = db.relationship('Activity', backref='user')

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
    activity = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    record_id = db.relationship('RecordByDay', backref='activity', uselist=False)
    yes_id = db.relationship('YesNo', backref='activity', uselist=False)


class RecordByDay(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day = db.Column(db.DateTime)
    occurrences = db.Column(db.Integer)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)


class YesNo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    yes_no = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)



