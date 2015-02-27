from flask import Flask
from flask.ext.wtf import CsrfProtect

from .extensions import db, migrate, bcrypt, login_manager, config

from . import models
from .views.users import users
from .views.activities import activities
#from .views.api import api

SQLALCHEMY_DATABASE_URI = "postgres://localhost/stat_tracker"
DEBUG = True
SECRET_KEY = 'development key'


def create_app():
    app = Flask("Self dot Quantify")
    app.config.from_object(__name__)
    app.register_blueprint(users)
    app.register_blueprint(activities)
    #app.register_blueprint(api, url_prefix='/api/v1')

    config.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    return app
