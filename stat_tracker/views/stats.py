from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask.ext.login import login_required, current_user
from ..forms import ActivityForm, StatForm, APIStatForm

from ..extensions import db
from ..models import Activity, Stat


stats = Blueprint("stats", __name__)


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                    .format(getattr(form, field).label.text, error), category)


@stats.route("/")
def index():
    form = StatForm()
    form.activity.choices = [(activity.id, activity.name + " - "  + activity.unit) for activity in Activity.query.all()]
    print("add_stat ran")
    if form.validate_on_submit():
        print("validating, yo")
        activity_id = form.activity.data
        activity = Activity.query.get(activity_id)
        stat = Stat(user_id=current_user.id,
                    activity_id=activity.id,
                    date=form.date.data,
                    value=form.value.data)
        db.session.add(stat)
        db.session.commit()
        flash("Stat Attack has added your stat!")

    activities = Activity.query.all()
    data = [[stat.value for stat in activity.stats] for activity in activities]
    return render_template('index.html', activities=activities,
                                         data=data,
                                         form=form,
                                         button='submit',
                                         post_url=url_for("stats.add_stat"))

@stats.route("/activity", methods=['GET', 'POST'])
@login_required
def add_activity():
    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activity(name=form.name.data,
                            user_id=current_user.id,
                            unit=form.unit.data)
        db.session.add(activity)
        db.session.commit()
        flash("Activity has been added")
        return redirect(url_for("stats.index"))
    return render_template("activity.html", form=form)

@stats.route("/stats", methods=['GET', 'POST'])
@login_required
def add_stat():
    form = StatForm()
    form.activity.choices = [(activity.id, activity.name + " - "  + activity.unit) for activity in Activity.query.all()]
    if form.validate_on_submit():
        activity_id = form.activity.data
        activity = Activity.query.get(activity_id)
        stat = Stat(user_id=current_user.id,
                    activity_id=activity.id,
                    date=form.date.data,
                    value=form.value.data)
        db.session.add(stat)
        db.session.commit()
        flash("Stat Attack has added your stat!")

    return render_template("stats.html", form=form,
                                         button='submit',
                                         post_url=url_for("stats.add_stat"),
                                         activity='activity')

@stats.route("/stats/<int:id>/edit", methods=['GET', 'POST'])
@login_required
def edit_stat(id):
    stat = Stat.query.get(id)
    form = StatForm(obj=stat)
    activity_id = stat.activity_id
    activity = Activity.query.get(activity_id)
    if request.method == 'POST':
        form.populate_obj(stat)
        stat.date = form.date.data
        stat.value = form.value.data
        db.session.add(stat)
        db.session.commit()
        flash("Stat Attack has updated your stat!")
    return render_template("edit.html", form=form,
                                        button="edit",
                                        activity=activity,
                                        post_url=url_for("stats.edit_stat", id=stat.id))


@stats.route("/stats/<int:id>/chart", methods=['GET', 'POST'])
@login_required
def stat_chart(id):
    form = APIStatForm()
    activity = Activity.query.get(id)
    data = [stat.value for stat in activity.stats]
    return render_template("specificStats.html", activity=activity,
                                                 data=data,
                                                 form=form,
                                                 button="add stat")


