"""Add your views here.

We have started you with an initial blueprint. Add more as needed.
"""

from flask import Blueprint, flash, render_template, redirect, url_for
from flask.ext.login import current_user, login_required

generic = Blueprint("generic", __name__)


@generic.route("/")
def index():
    if current_user.is_authenticated():
        return render_template("index.html")
    else:
        return redirect(url_for("users.login"))


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                    .format(getattr(form, field).label.text, error), category)

