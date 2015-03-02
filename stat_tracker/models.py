from flask.ext.login import UserMixin

from . import db, bcrypt, login_manager
from sqlalchemy import func, and_
from datetime import date, timedelta, datetime


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(60))
    activity = db.relationship('Activity', backref='user', lazy='dynamic')
    stat = db.relationship('Stat', backref='user', lazy='dynamic')


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


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_name = db.Column(db.String(255), nullable=False)
    measurement = db.Column(db.String(255), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    stat = db.relationship('Stat', backref='activity',
                                lazy='dynamic')

    def stat_by_day(self, days=30):
        days = timedelta(days=days)
        date_from = date.today() - days

        stat_date = func.date_trunc('day', Stat.recorded_at)
        return db.session.query(stat_date, func.count(Stat.id)). \
            group_by(stat_date). \
            filter(and_(Stat.activity_id == self.id,
                        stat_date >= str(date_from))). \
            order_by(stat_date).all()


    def to_dict(self):
        return {"id": self.id,
                "activity_name": self.activity_name,
                "measurement": self.measurment}

    def __repr__(self):
        return "<Activity {}>".format(self.activity_name)


class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Integer)
    recorded_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
