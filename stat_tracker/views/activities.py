import random
from flask import Blueprint, render_template, redirect, flash, url_for, request, send_file
from flask.ext.login import current_user
from sqlalchemy import desc
from ..forms import AddNewAction, EditAction, AddNewStat
from ..models import Activities, Stat
from ..extensions import db
from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt

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
    current = Activities.query.get(id)
    name = current.name
    form = AddNewStat()
    if form.validate_on_submit():
        s = Stat(user_id = current_user.id,
                 activity_id = current.id,
                 ammount = form.quantity.data,
                 time = form.date.data)
        db.session.add(s)
        db.session.commit()
        flash('Stats Updated!')
        return redirect(url_for('users.home_view'))
    else:
        flash_errors(form)
    return render_template('addstat.html', form=form, name=name)
