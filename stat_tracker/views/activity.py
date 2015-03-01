from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user

from ..extensions import db
from ..forms import LoginForm, RegistrationForm,ActivityForm
from ..models import Activity, User, Stats

activity = Blueprint("activity", __name__)


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@activity.route("/activity", methods=["GET", "POST"])
def act():
    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activity.query.filter_by(title=form.title.data).first()
        if activity:
            flash("An activity with that title aready exists")
        else:
            activity = Activity(title=form.title.data,
                                description=form.description.data)
            stats = Stats(value=form.value.data,
                          recorded_at=form.recorded_at.data)
            db.session.add(activity)
            db.session.add(stats)
            db.session.commit()
            flash("You have successfully logged an activity")
            return render_template("activities.html", form=form)
    else:
        flash_errors(form)
    return render_template("activities.html", form=form)


@activity.route('/activity/<int:id>', methods=['GET'])
def delete_activity(id):
    current = Activity.query.get(id)
    db.session.delete(current)
    db.session.commit()
    flash('Activity Deleted')
    return redirect(url_for('act'))
