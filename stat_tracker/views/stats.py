from flask import render_template, flash, redirect, request, url_for, Blueprint
from flask.ext.login import login_user, login_required, current_user
from flask.ext.login import logout_user
from ..extensions import db
from ..forms import ActivityForm, InstanceForm
from ..models import User, Activity, Instance
from datetime import datetime
import plotly.plotly as py
from plotly.graph_objs import *
from datetime import *


py.sign_in("dknewell1", "x0oz9ikryp")
stats = Blueprint("stats", __name__)


def sort_dates(instances):
    """turns from string to date, sorts, returns as string"""


@stats.route("/")
def index():
    return render_template("index.html")


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error),
                  category)


@stats.route("/user_page", methods=["GET", "POST"])
@login_required
def user_page():
    form = ActivityForm()
    activities = Activity.query.filter_by(user=current_user)
    if form.validate_on_submit():
        activity = Activity(user=current_user,
                            title=form.title.data,
                            unit=form.unit.data)
        db.session.add(activity)
        db.session.commit()
        flash("Activity Added")
        return redirect(url_for("stats.user_page"))
    return render_template("user_page.html", form=form, activities=activities)


@stats.route("/delete", methods=["GET", "POST"])
def delete_activity():
    activity_id = request.form['activity_to_delete']
    activity = Activity.query.filter_by(id=activity_id).first()
    instances = Instance.query.filter_by(activity_id=activity_id).all()
    for instance in instances:
        db.session.delete(instance)

    db.session.delete(activity)
    db.session.commit()
    flash("Activity deleted")
    return redirect(url_for("stats.user_page"))


@stats.route("/user_page/<int:id>", methods=["GET", "POST"])
def view_activity(id):
    activity = Activity.query.filter_by(id=id).first()
    instances = Instance.query.filter_by(activity_id=id).all()
    form = InstanceForm()
    if form.validate_on_submit():
        instance = Instance(user_id=current_user.id,
                            activity_id=id,
                            date=str(date.today()),
                            freq=form.freq.data)
        db.session.add(instance)
        db.session.commit()
        flash("Activity instance has been updated.")
        return redirect(url_for("stats.view_activity",
                                id=instance.activity.id))

    instance_list = []
    for instance in instances:
        instance_list.append((instance.date, instance.freq))
    dates = [d[0] for d in instance_list]
    freqs = [f[1] for f in instance_list]
    click_chart = Bar(x=dates, y=freqs)
    data = Data([click_chart])
    chart_url = py.plot(data, auto_open=False)
    return render_template("instance_page.html", chart_url=chart_url,
                           form=form, instances=instances,
                           activity=activity)


@stats.route("/user_page/instance/<int:id>", methods=["GET", "POST"])
@login_required
def edit_instance(id):
    instance = Instance.query.get(id)
    form = InstanceForm(obj=instance)
    if form.validate_on_submit():
        form.populate_obj(instance)
        db.session.add(instance)
        db.session.commit()
        flash("Activity instance has been updated.")
        return redirect(url_for("stats.view_activity",
                                id=instance.activity.id))

    return render_template("edit_instance.html",
                           form=form,
                           post_url=url_for("stats.edit_instance",
                                            id=instance.id),
                           button="Update Instance")
