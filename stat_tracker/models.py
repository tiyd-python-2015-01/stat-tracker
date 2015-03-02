from . import db, bcrypt, login_manager
from flask.ext.login import UserMixin
from sqlalchemy import func, and_
from datetime import date, timedelta, datetime
from stat_tracker import db
from flask import request, url_for

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(60))

    def get_password(self):
        return getattr(self, "_password", None)

    def set_password(self, password):
        self._password = password
        self.encrypted_password = bcrypt.generate_password_hash(password)

    password = property(get_password, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    @property
    def user_action(self):
        return [activity.name for activity in self.activities]

    def __repr__(self):
        return "<User {}>".format(self.email)


class Activities(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(255), unique=True)
    user = db.relationship('User', backref=db.backref('activities', lazy='dynamic'))
    stat = db.relationship('Stat', backref=db.backref('activities'))


    @property
    def times_total(self):
        count = 0
        stats = Stat.query.filter_by(activity_id=self.id).all()
        for stat in stats:
            count += stat.ammount
        return count


    @property
    def times_last_7(self):
        times = (self.times_range(7))
        count = 0
        for time in times:
            count += time[1]
        return count

    @property
    def times_last_30(self):
        times = (self.times_range())
        count = 0
        for time in times:
            count += time[1]
        return count

    @property
    def times_last_365(self):
        times = (self.times_range(365))
        count = 0
        for time in times:
            count += time[1]
        return count


    def times_range(self, days=30):
        days = timedelta(days=days)
        date_from = date.today() - days

        stat_date = func.cast(Stat.time, db.Date)
        return db.session.query(stat_date, func.sum(Stat.ammount)). \
            group_by(stat_date). \
            filter(and_(Stat.activity_id == self.id,
                    stat_date >= str(date_from))). \
            order_by(stat_date).all()


    def custom_time(self, stop, start):
        stat_date = func.cast(Stat.time, db.Date)
        return db.session.query(stat_date, func.sum(Stat.ammount)). \
            group_by(stat_date). \
            filter(and_(Stat.activity_id == self.id,
                stat_date >= str(start), stat_date <= str(stop))). \
            order_by(stat_date).all()



    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'url': str(request.url_root)[:-1:]+str(url_for('api.activity', id=self.id))}

    def __repr__(self):
        return "Activity: {}".format(self.name)


class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id', ondelete='CASCADE'))
    ammount = db.Column(db.Integer)
    time = db.Column(db.Date)

    def stat_to_dict(self):
        return {'ammount': self.ammount,
                'time': str(self.time)}
