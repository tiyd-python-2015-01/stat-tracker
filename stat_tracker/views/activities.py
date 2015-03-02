import random
from flask import Blueprint, render_template, redirect, flash, url_for, request, send_file
from flask.ext.login import current_user
from sqlalchemy import desc
from ..forms import AddNewAction, EditAction, AddNewStat, DateRange, EditStat
from ..models import Activities, Stat
from ..extensions import db
from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt
import time

activities = Blueprint("activities", __name__)


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error),
                                                                   category)



@activities.route('/add', methods=['GET', 'POST'])
def add_activity():
    user = current_user
    form = AddNewAction()
    if form.validate_on_submit():
        activity = Activities.query.filter_by(name=form.name.data).first()
        if activity in user.activities:
            flash('You are already monitoring that activity.')
            flash_errors(form)
            return render_template('add_activity.html', form=form)
        else:
            activity = Activities(user_id = current_user.id,
                         name = form.name.data)
            db.session.add(activity)
            db.session.commit()
            flash('New Activity Added')
            return redirect(url_for('users.home_view'))
    else:
        flash_errors(form)
        return render_template('add_activity.html', form=form)


@activities.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_activity(id):
    current = Activities.query.get(id)
    form = EditAction(obj=current)
    if form.validate_on_submit():
        form.populate_obj(current)
        db.session.commit()
        flash('Activity Updated')
        return redirect(url_for('users.home_view'))
    else:
        flash_errors(form)
    return render_template('edit_activity.html', form=form)


@activities.route('/delete/<int:id>', methods=['GET'])
def delete_activity(id):
    current = Activities.query.get(id)
    current_stats = Stat.query.filter_by(activity_id = id)
    for stats in current_stats:
        db.session.delete(stats)
    db.session.delete(current)
    db.session.commit()
    flash('Activity Deleted!!')
    return redirect(url_for('users.home_view'))


@activities.route('/<int:id>/add', methods=['GET', 'POST'])
def add_stat(id):
    current = Activities.query.get_or_404(id)
    name = current.name
    form = AddNewStat()
    if form.validate_on_submit():
        date = Stat.query.filter_by(activity_id=current.id).filter_by(time=form.date.data).first()
        if date:
            flash('You have already entered an ammount for that date!'
                   'Edit the exisiting entry!')
        else:
            s = Stat(user_id = current_user.id,
                     activity_id = current.id,
                     ammount = form.ammount.data,
                     time = form.date.data)
            db.session.add(s)
            db.session.commit()
            flash('Stats Updated!')
            return redirect(url_for('users.home_view'))
    else:
        flash_errors(form)
    return render_template('addstat.html', form=form, name=name)


@activities.route('/activity/<int:id>')
def stat_table(id):
    a = Activities.query.get_or_404(id)
    stat = Stat.query.filter_by(activity_id=a.id).order_by(Stat.time.desc())
    return render_template('activity_data.html', stat=stat, a=a)


@activities.route('/activity/<int:id>/stats/<time>/edit', methods=['GET', 'POST'])
def edit_stat(id, time):
    s = Stat.query.filter_by(activity_id=id).filter_by(time=time).first()
    a = Activities.query.get_or_404(id)
    stat = Stat.query.filter_by(activity_id=a.id).order_by(Stat.time.desc())
    form = EditStat(obj=s)
    if form.validate_on_submit():
        form.populate_obj(s)
        db.session.commit()
        flash('Stat Updated')
        return render_template('activity_data.html', stat=stat, a=a)
    else:
        flash_errors(form)
    return render_template('edit_stat.html', form=form, a=a, s=s)

@activities.route('/activity/<int:id>/stats/<time>/delete', methods=['GET'])
def delete_stat(id, time):
    s = Stat.query.filter_by(activity_id=id).filter_by(time=time).first()
    db.session.delete(s)
    db.session.commit()
    a = Activities.query.get_or_404(id)
    stat = Stat.query.filter_by(activity_id=a.id).order_by(Stat.time.desc())
    flash('Stat Deleted!!')
    return render_template('activity_data.html', stat=stat, a=a)


@activities.route('/activity/<int:id>/set_range', methods=['GET', 'POST'])
def set_range(id):
    form = DateRange()
    if form.validate_on_submit():
        redirect(url_for('chart_view', start=form.start.data, stop=form.stop.data))
    else:
        flash_errors(form)
    return render_template('chart_dates.html', form=form)


@activities.route('/activity/<int:id>/chart', methods=['GET', 'POST'])
def chart_view(id):
    a = Activities.query.get_or_404(id)
    form = DateRange()
    if form.validate_on_submit():
        return render_template('chart.html', form=form, a=a, start=form.start.data, stop=form.stop.data)
    else:
        flash_errors(form)
    return render_template('chart_dates.html', a=a, form=form)


#def make_chart(a, start, stop):
#    stop = datetime.strptime(stop, '%Y-%m-%d').date()
#    start = datetime.strptime(start, '%Y-%m-%d').date()
#    a_data = a.custom_time(stop, start)
#    dates = [c[0] for c in a_data]
#    stat_count = [c[1] for c in a_data]
#    date_labels = [d.strftime("%b %d") for d in dates]
#    every_other_date_label = [d if i % 2 else ""
#                              for i, d in enumerate(date_labels)]
#
#    ax = plt.subplot(111)
#    ax.spines["top"].set_visible(False)
#    ax.spines["right"].set_visible(False)
#    ax.get_xaxis().tick_bottom()
#    ax.get_yaxis().tick_left()
#
#    plt.plot_date(x=dates, y=stat_count)
#    plt.xticks(dates, every_other_date_label, rotation=45, size="x-small")
#    plt.tight_layout()
#
#
#@activities.route('/activity/<start>/<stop>/<int:id>_chart.png/')
#def a_chart(id, start, stop):
#    a = Activities.query.get_or_404(id)
#    make_chart(a, start, stop)
#
#    plt.savefig(fig)
#    plt.clf()
#    fig.seek(0)
#    return send_file(fig, mimetype="image/png")
