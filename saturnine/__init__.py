from flask import Flask, render_template

from . import models
from .extensions import (
    db,
    migrate,
    bcrypt,
    login_manager,
    config,
)
from .views import saturnine, users


SQLALCHEMY_DATABASE_URI = "postgres://localhost/saturnine"
DEBUG = True
SECRET_KEY = 'development-key'


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.register_blueprint(saturnine)
    app.register_blueprint(users)
    app.register_blueprint(api, url_prefix="/api/v1")

    config.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    return app
