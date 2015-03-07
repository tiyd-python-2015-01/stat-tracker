from datetime import date
from io import BytesIO
import matplotlib.pyplot as plt

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
        return render_template("index.html",tasks=[])


@tasksb.route("/stats", methods=["GET"])
@login_required
def get_task():
    if current_user.is_authenticated():
        tasks = Task.query.filter_by(t_user=current_user.id).order_by(Task.id.desc())
        return render_template("tasks.html",tasks=tasks)


@tasksb.route("/stats", methods=["POST"])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(form.t_name.data,
                        form.t_units.data,
                        form.t_type.data,
                        current_user.id
                        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("tasksb.index"))
    return render_template("task_form.html",
                            form=form,
                            post_url=url_for("tasksb.add_task"),
                            b_label="Add Task")


@tasksb.route("/stats/<int:id>", methods=["GET"])
@login_required
def show_one_task(id):
    tasks = Task.query.filter_by(t_user=current_user.id).order_by(Task.id.desc())
    return render_template("index.html",tasks=tasks)


@tasksb.route("/stats/<int:id>", methods=["DELETE"])
@login_required
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    tasks = Task.query.filter_by(t_user=current_user.id).order_by(Task.id.desc())
    return render_template("index.html",tasks=tasks)


@tasksb.route('/stats/<int:id>', methods=["PUT"])
@login_required
def update_task(id):
    task = Task.query.get(id)
    form = TaskForm(t_name=task.t_name,
                    t_type=task.t_type,
                    t_units=task.t_units)
    if form.validate_on_submit():
        form.populate_obj(task)
        db.session.commit()
        return redirect(url_for("tasksb.index"))
    return render_template("task_form.html",
                            post_url = url_for("tasksb.update_task",id=task.id),
                            form=form, b_label="Update")



@tasksb.route("/stats/<int:id>/data", methods=["GET"])
@login_required
def show_task(id):
    form = TrackingForm()
    if form.validate_on_submit():
        date_read = form.tr_date.data
        value_read = form.tr_value.data
        stat = Tracking.query.filter(and_(Tracking.tr_date==date_read,Tracking.tr_task_id==id)).first()
        if stat:
            stat.tr_value = value_read
        else:
            stat = Tracking(current_user.id, id, date_read, value_read)
        db.session.add(stat)
        db.session.commit()
    task = Task.query.get(id)
    stats = Tracking.query.filter_by(tr_task_id=id).order_by(Tracking.tr_date.desc())

    return render_template("task_details.html", stats = stats, form=form, task=task)



@tasksb.route('/stats/<int:id>/data', methods=["POST", "PUT"])
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
            stat = Tracking(current_user.id, id, date_read, value_read)
        db.session.add(stat)
        db.session.commit()
        return redirect(url_for("tasksb.show_task",id=id))
    else:
        return render_template("task_details.html", form=form, task_id=id)


@tasksb.route("/stats/<int:id>_stats.png")
def stat_chart(id):
    stats = Tracking.query.filter_by(tr_task_id=id).order_by(Tracking.tr_date).all()
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
