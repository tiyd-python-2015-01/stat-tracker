from flask import Flask, render_template
from flask.ext.wtf import CsrfProtect

from .extensions import (db,
                         migrate,
                         config,
                         debug_toolbar,
                         bcrypt,
                         login_manager)
# from .views import stattracker

from . import models
from .views.users import users
from .views.enterprises import enterprises
from .views.api import api


SQLALCHEMY_DATABASE_URI = "postgres://localhost/stattracker"
DEBUG = True
SECRET_KEY = 'development-key'


def create_app():
    app = Flask("stattracker")
    app.config.from_object(__name__)
    app.register_blueprint(users)
    app.register_blueprint(enterprises)
    app.register_blueprint(api, url_prefix="/api/v1")

    config.init_app(app)
    db.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "users.login"

    return app
