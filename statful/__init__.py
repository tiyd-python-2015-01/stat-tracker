from flask import Flask

from .extensions import db, migrate, debug_toolbar, bcrypt, login_manager, config
from . import models
from .views.users import users
from .views.stats import stats


SQLALCHEMY_DATABASE_URI = "postgres://localhost/stats"
DEBUG = True
SECRET_KEY = 'development-key'


def create_app():
    app = Flask('statful')
    app.config.from_object(__name__)
    app.config.from_pyfile('application.cfg', silent=True)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.register_blueprint(users)
    app.register_blueprint(stats)

    config.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    return app