from flask import (Blueprint, render_template, flash, redirect, request,
                   url_for, session, send_file)
from flask.ext.login import login_required, current_user
from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt
from ..forms import ActivityForm, UpdateForm
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
                              date=datetime.today().date(),
                              owner=current_user.id,
                              activity_type=form.activity_type.data)
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
    stats = Stat.query.filter_by(activity=activity_id).all()
    record = Activity.query.get(activity_id)
    for stat in stats:
        db.session.delete(stat)
    db.session.commit()
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for("stats.index"))


@stats.route("/update/<int:activity_id>", methods=["GET", "POST"])
@login_required
def update_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    stats = Stat.query.filter_by(activity=activity.id).all()
    form = UpdateForm()
    if form.validate_on_submit():
        if stats and stats[-1].date == datetime.today().date():
            updated_stat = Stat.query.get_or_404(stats[-1].id)
            updated_stat.value = form.value.data
            db.session.commit()
            flash("Updated value for today.")
            return render_template("update.html", activity=activity,
                                   stats=stats, form=form)
        else:
            new_stat = Stat(activity=activity.id,
                            value=form.value.data,
                            date=datetime.today().date())
            db.session.add(new_stat)
            db.session.commit()
            flash("New value added for today.")
            stats = Stat.query.filter_by(activity=activity.id).all()
            return render_template("update.html", activity=activity,
                                   stats=stats, form=form)
    flash_errors(form)
    return render_template("update.html", activity=activity, stats=stats,
                           form=form)


@stats.route("/edit/<int:activity_id>", methods=["GET", "POST"])
@login_required
def edit_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    stats = Stat.query.filter_by(activity=activity.id).all()
    form = ActivityForm(obj=activity)
    if form.validate_on_submit():
        activity.title = form.title.data
        db.session.commit()
        flash("Activity updated.")
        return redirect(url_for("stats.index"))
    else:
        flash_errors(form)
        return render_template("edit_activity.html", activity=activity,
                               stats=stats, form=form)


@stats.route("/editstat/<int:stat_id>", methods=["GET", "POST"])
@login_required
def edit_stat(stat_id):
    stat = Stat.query.get_or_404(stat_id)
    form = UpdateForm(obj=stat)
    if form.validate_on_submit():
        stat.value = form.value.data
        db.session.commit()
        flash("Stat updated.")
        return redirect(url_for("stats.update_activity",
                                activity_id=stat.activity))
    else:
        flash_errors(form)
        return render_template("edit_stat.html", stat=stat, form=form)


@stats.route("/deletestat/<int:stat_id>")
@login_required
def delete_stat(stat_id):
    stat = Stat.query.get_or_404(stat_id)
    db.session.delete(stat)
    db.session.commit()
    return redirect(url_for("stats.update_activity",
                            activity_id=stat.activity))


@stats.route("/activity_data/<int:activity_id>")
@login_required
def activity_data(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    return render_template("activity_data.html", activity=activity)


@stats.route("/activity_data<int:activity_id>.png")
@login_required
def activity_data_chart(activity_id):
    make_chart(activity_id)
    fig = BytesIO()
    plt.savefig(fig)
    plt.clf()
    fig.seek(0)
    return send_file(fig, mimetype="image/png")


def make_chart(activity_id):
    data = Stat.query.filter_by(activity=activity_id).all()
    dates = [item.date for item in data]
    date_labels = [date.strftime("%b %d") if i % 2 else ""
                   for i, date in enumerate(dates)]
    values = [item.value for item in data]
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    plt.title("Stats by Day")
    plt.plot_date(x=dates, y=values, fmt="-")
    plt.xticks(dates, date_labels, rotation=45, size="x-small")
    plt.tight_layout()
