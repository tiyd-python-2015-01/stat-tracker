from .app import db
from .extensions import bcrypt, login_manager
from flask.ext.login import UserMixin


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
        return self._password

    def set_password(self, password):
        self._password = password
        self.encrypted_password = bcrypt.generate_password_hash(password)

    password = property(get_password, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(255), nullable=False, unique=False)
    goal = db.Column(db.String(255), nullable=True, unique=False)
    description = db.Column(db.String(255), nullable=True, unique=False)

    user = db.relationship('User')

    def to_dict(self):
        return {"id": self.id,
                "user": self.user_id,
                "name": self.name,
                "goal": self.goal,
                "description": self.description}

    def __repr__(self):
        return "<name {}>".format(self.name)

class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    value = db.Column(db.Integer, unique=False, nullable=True)
    logged_at = db.Column(db.Date)

    item = db.relationship('Item')

    def to_dict(self):
        return {"id": self.id,
                "item_id": self.item_id,
                "value": self.value,
                "logged_at": str(self.logged_at)}

    def __repr__(self):
        return "<item_id {} | datetime {}>".format(self.item_id, self.datetime)
