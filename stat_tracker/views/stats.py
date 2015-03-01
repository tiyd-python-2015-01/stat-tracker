from flask import (Blueprint, render_template, flash, redirect, request,
                   url_for, session, send_file)
from flask.ext.login import login_required, current_user
from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt
from ..forms import ActivityForm
from ..models import Activity, Stat
from ..extensions import db, flash_errors


stats = Blueprint("stats", __name__)


@stats.route("/")
def index():
    if current_user.is_authenticated():
        return redirect(url_for("stats.user_activities", page=1))
    else:
        return redirect(url_for("users.login"))


@stats.route("/<int:page>")
@login_required
def user_activities(page):
    activities = Activity.query.filter_by(owner=current_user.id).paginate(
        page, per_page=10, error_out=False)
    return render_template("index.html", activities=activities)


@stats.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = ActivityForm()
    if form.validate_on_submit():
        submission = Activity(title=form.title.data,
                              date=datetime.utcnow(),
                              owner=current_user.id)
        db.session.add(submission)
        db.session.commit()
        flash("Activity successfully added!")
        return redirect(url_for("stats.index"))
    else:
        flash_errors(form)
        return render_template("add_activity.html", form=form)


@stats.route("/delete/<int:activity_id>")
@login_required
def delete_activity(activity_id):
    stats = Stat.query.filter_by(id=activity_id).all()
    record = Activity.query.get(activity_id)
    for stat in stats:
        db.session.delete(stat)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for("stats.index"))


@stats.route("/update/<int:activity_id>")
@login_required
def update_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    stats = Stat.query.filter_by(activity=activity_id).all()



@stats.route("/activity_data/<int:activity_id>")
@login_required
def activity_data(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    return render_template("activity_data.html", activity=activity)
