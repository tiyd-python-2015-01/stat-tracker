from . import db, bcrypt, login_manager
from flask.ext.login import UserMixin
from sqlalchemy import func, and_
from datetime import date, timedelta, datetime
from stat_tracker import db


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
    unit = db.Column(db.String(255))

    @property
    def activity_stat_total(self):
        count = 0
        stats = Stat.query.filter_by(activity_id=self.id).all()
        for stat in stats:
            count += stat.ammount
        return count


    #clicks = property(link_clicks)

    #@property
    #def clicks_last_30(self):
    #    return len(self.clicks_per_day())

    #def clicks_per_day(self, days=30):
    #    days = timedelta(days=days)
    #    date_from = date.today() - days


    #    click_date = func.cast(Click.timestamp, db.Date)
    #    return db.session.query(click_date, func.count(Click.id)). \
    #        group_by(click_date). \
    #        filter(and_(Click.link_id == self.id,
    #                    click_date >= str(date_from))). \
    #        order_by(click_date).all()


    #def to_dict(self):
    #    return {'id': self.id,
    #            'url': self.url,
    #            'text': self.text,
    #            'short': self.short}

    def __repr__(self):
        return "Activity: {}".format(self.name)


class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id', ondelete='CASCADE'))
    ammount = db.Column(db.Integer)
    time = db.Column(db.Date)
