from flask import Flask
from flask_wtf.csrf import CsrfProtect
from .extensions import (
   db,
   migrate,
   debug_toolbar,
   bcrypt,
   login_manager,
   config
)

from . import models
from .views.users import usersb
from .views.tasks import tasksb
from .views.api import api

SQLALCHEMY_DATABASE_URI = "postgres://localhost/tasker"
DEBUG = True
SECRET_KEY = 'development-key'
DEBUG_TB_INTERCEPT_REDIRECTS = False

def create_app():
    app = Flask("tasker")
    app.config.from_object(__name__)
    app.register_blueprint(usersb)
    app.register_blueprint(tasksb)
    app.register_blueprint(api, url_prefix="/tasker/api/v1")
    config.init_app(app)
    db.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "usersb.login"
    return app
