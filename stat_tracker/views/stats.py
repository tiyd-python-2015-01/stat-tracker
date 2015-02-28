from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask.ext.login import login_required, current_user
from ..forms import ActivityForm

from ..extensions import db
from ..models import Activity


stats = Blueprint("stats", __name__)


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                    .format(getattr(form, field).label.text, error), category)


@stats.route("/")
def index():
    return render_template('index.html')

@stats.route("/activity", methods=['GET', 'POST'])
@login_required
def add_activity():
    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activity(name=form.name.data,
                            user_id=current_user.id)
        db.session.add(activity)
        db.session.commit()
        flash("Activity has been added")
        return redirect(url_for("stats.index"))
    return render_template("activity.html", form=form)


