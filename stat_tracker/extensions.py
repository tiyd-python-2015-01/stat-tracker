"""Extensions"""
from flask.ext.sqlalchemy import SQLAlchemy, Pagination
from flask.ext.migrate import Migrate
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.appconfig import HerokuConfig

db = SQLAlchemy()
migrate = Migrate()
debug_toolbar = DebugToolbarExtension()
bcrypt = Bcrypt()
login_manager = LoginManager()
config = HerokuConfig()


def flash_errors(form, category="warning"):
    """Show all errors from a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(
                getattr(form, field).label.text, error), category)
