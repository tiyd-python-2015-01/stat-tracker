from datetime import date
from io import BytesIO
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show

"""Add your views here."""

from flask import Blueprint, render_template, flash, redirect, url_for, send_file
from flask.ext.login import login_required, current_user

from ..extensions import db
from ..forms import TaskForm, TrackingForm
from ..models import Task, Tracking

from sqlalchemy.sql import and_

tasksb = Blueprint("tasksb",__name__)


@tasksb.route("/")
def index():
    if current_user.is_authenticated():
        tasks = Task.query.filter_by(t_user=current_user.id).order_by(Task.id.desc())
        return render_template("tasks.html",tasks=tasks)
    else:
        return render_template("tasks.html",tasks=[])


@tasksb.route("/task/<int:id>")
@login_required
def show_task(id):
    task = Task.query.get(id)
    stats = Tracking.query.filter_by(tr_task_id=id).order_by(Tracking.tr_date.desc())
    return render_template("task_details.html",stats=stats, task=task)


@tasksb.route("/task/new", methods=["GET", "POST"])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(form.name.data,
                        form.units.data,
                        form.t_type.data,
                        current_user.id
                        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("tasksb.index"))
    return render_template("add_task.html",
                            form=form,
                            post_url=url_for("tasksb.add_task"),
                            b_label="Add Task")


@tasksb.route("/task/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    tasks = Task.query.filter_by(t_user=current_user.id).order_by(Task.id.desc())
    return render_template("tasks.html",tasks=tasks)


@tasksb.route('/task/<int:id>/edit', methods=["GET", "POST"])
@login_required
def update_task(id):
    task = Task.query.get(id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        form.populate_obj(task)
        db.session.commit()
        return redirect(url_for("tasksb.index"))
    return render_template("add_task.html",
                            post_url = url_for("tasksb.update_task",id=task.id),
                            form=form, b_label="Update")


@tasksb.route('/task/<int:id>/stats', methods=["GET", "POST"])
@login_required
def add_daily_value(id):
    form = TrackingForm()
    if form.validate_on_submit():
        date_read = form.tr_date.data
        value_read = form.tr_value.data
        stat = Tracking.query.filter(and_(Tracking.tr_date==date_read,Tracking.tr_task_id==id)).first()
        if stat:
            stat.tr_value = value_read
        else:
            stat = Tracking(id, date_read, value_read)
        db.session.add(stat)
        db.session.commit()
        return redirect(url_for("tasksb.show_task",id=id))
    return render_template("add_value.html", form=form, task_id=id)


@tasksb.route("/task/<int:id>_stats.png")
def stat_chart(id):
    stats = Tracking.query.filter_by(tr_task_id=id).all()
    values = [stat.tr_value for stat in stats]
    dates = [stat.tr_date for stat in stats]
    date_labels = [d.strftime("%b %d") for d in dates]
    every_other_date_label = [d if i % 2 else "" for i, d in enumerate(date_labels)]
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    plt.title("Values")
    fig = plt.gcf()
    fig.set_size_inches(6,4)
    plt.plot_date(x=dates, y=values, fmt="-")
    plt.xticks(dates, every_other_date_label, rotation=45, size="x-small")
    plt.tight_layout()

    fig = BytesIO()  # will store the plot as bytes
    plt.savefig(fig)
    plt.clf()
    fig.seek(0) #go back to the beginning
    return send_file(fig, mimetype="image/png")
