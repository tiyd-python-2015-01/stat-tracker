from flask import render_template, flash, request, url_for, redirect, Blueprint
from flask.ext.login import login_required, current_user
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import Data, Scatter
from datetime import datetime
from ..forms import ActivityForm, UpdateForm
from ..extensions import db
from ..models import Activity, Stat

today_date = datetime.today()

stats = Blueprint('stats', __name__)

credentials = tls.get_credentials_file()

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@stats.route('/create_activity', methods=["GET", "POST"])
@login_required
def create_activity():
    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activity(user=current_user,
                            unit=form.unit.data,
                            name=form.name.data,
                            type=form.type.data)
        db.session.add(activity)
        db.session.commit()
        flash("You've created a new activity!")
        return redirect(url_for('stats.create_activity'))
    else:
        flash_errors(form)

    return render_template('create_activity.html', form=form)

@stats.route('/show_activities', methods=["GET"])
@login_required
def show_activities():
    return render_template('show_activities.html')


@stats.route("/activity/<int:id>", methods=["GET", "POST"])
@login_required
def update_activity(id):
    activity = Activity.query.filter(Activity.id == id).first()
    form = UpdateForm()

    if activity.type == 'clicker':
        if form.validate_on_submit():
            stat = Stat(activity_id=activity.id,
                        occurrences=form.occurrences.data,
                        when=form.date.data)
            db.session.add(stat)
            db.session.commit()
            flash("You've updated you activity!")
        else:
            flash_errors(form)

    if activity.type == 'yes_no':
        if form.validate_on_submit():
            stat = Stat(activity_id=activity.id,
                        yes_no=form.yes_no.data,
                        when=form.date.data)
            db.session.add(stat)
            db.session.commit()
            flash("You've updated you activity!")
        else:
            flash_errors(form)

    if activity.type == 'scale':
        if form.validate_on_submit():
            stat = Stat(activity_id=activity.id,
                        scale=form.scale.data,
                        when=form.date.data)
            db.session.add(stat)
            db.session.commit()
            flash("You've updated you activity!")
        else:
            flash_errors(form)

    return render_template('update_activity.html', form=form, activity=activity, today=today_date,
                           update_url=url_for('stats.update_activity',
                                              id=activity.id))

@stats.route('/activity/<int:act_id>/stat/delete/<int:stat_id>', methods=["GET"])
@login_required
def delete_stat(act_id, stat_id):
    stat = Stat.query.filter_by(id=stat_id).first()
    activity = Activity.query.filter_by(id=act_id).first()
    db.session.delete(stat)
    db.session.commit()
    return redirect(url_for('stats.show_stats', id=activity.id))

@stats.route("/activity/<int:id>/stats")
@login_required
def show_stats(id):
    form = UpdateForm()
    activity = Activity.query.filter(Activity.id == id).first()
    stat_data = Stat.query.filter(Stat.activity_id == activity.id).order_by(Stat.when.desc())
    dates = [date.when.strftime("%b %d") for date in stat_data]
    occurrences = [stat.occurrences for stat in stat_data]
    stat_chart = Scatter(
        x=dates,
        y=occurrences)
    data = Data([stat_chart])
    chart_url = py.plot(data, auto_open=False)
    return render_template('show_stats.html', activity=activity, chart_url=chart_url, form=form, stats=stat_data)

@stats.route("/activity/edit/stat/<int:id>", methods=['GET', "POST"])
@login_required
def edit_stat(id):
    stat = Stat.query.filter(Stat.id == id).first()
    activity = Activity.query.filter(Activity.id == stat.activity_id).first()
    form = UpdateForm(obj=stat)
    if form.validate_on_submit():
        form.populate_obj(stat)
        db.session.commit()
        flash("Your edits have been made.")
        return redirect(url_for('stats.show_stats', id=activity.id))
    else:
        flash_errors(form)

    return render_template('update_activity.html', activity=activity, form=form)







        

