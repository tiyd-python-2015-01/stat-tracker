"""Extensions module."""

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.migrate import Migrate
migrate = Migrate()

from flask.ext.debugtoolbar import DebugToolbarExtension
debug_toolbar = DebugToolbarExtension()

from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask.ext.login import LoginManager
login_manager = LoginManager()

from flask.ext.appconfig import AppConfig
config = AppConfig()
