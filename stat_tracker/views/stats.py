from flask import render_template, flash, redirect, request, url_for, Blueprint
from flask.ext.login import login_user , login_required, current_user
from flask.ext.login import logout_user
from ..extensions import db
from ..forms import ActivityForm, InstanceForm
from ..models import User, Activity, Instance


stats = Blueprint("stats", __name__)

@stats.route("/")
def index():
    return render_template("index.html")


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@stats.route("/user_page", methods = ["GET", "POST"])
@login_required
def user_page():
    form = ActivityForm()
    activities = Activity.query.filter_by(user = current_user)

    if form.validate_on_submit():
        activity = Activity(user = current_user,
                            title = form.title.data,
                            unit = form.unit.data)
        db.session.add(activity)
        db.session.commit()
        flash("Activity Added")
        return redirect(url_for("stats.user_page"))

    return render_template("user_page.html", form = form, activities = activities)

@stats.route("/delete", methods = ["GET", "POST"])
def delete_activity():
    activity = Activity.query.filter_by(id = request.form \
                                       ['activity_to_delete']).first()
    db.session.delete(activity)
    db.session.commit()
    flash("Activity deleted")
    return redirect(url_for("stats.user_page"))

@stats.route("/user_page/<int:id>", methods = ["GET", "POST"])
def view_activity(id):
    activity = Activity.query.filter_by(id = id).first()
    instances = Instance.query.filter_by(activity_id = id)
    form = InstanceForm()

    if form.validate_on_submit():
        instance = Intstance(user = current_user,
                             activity_id = id,
                             date = form.date.data,
                             freq = form.freq.data)
        db.session.add(instance)
        db.session.commit()
        flash("Instance Added!")
        return redirect(url_for("stats.view_activity"))

    return render_template("instance_page.html", form = form, instances = instances,
                           activity = activity)
