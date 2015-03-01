from flask import render_template, flash, redirect, request, Blueprint
from flask import url_for, send_file
from flask.ext.login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import desc, and_, between
import plotly.plotly as py
import plotly.tools as plotly_tools
from plotly.graph_objs import *
from io import BytesIO

from ..forms import LoginForm, RegistrationForm, AddActivity, \
                    LogActivity, ChartDate
from ..extensions import db
from ..models import User, Item, Action


items = Blueprint('items', __name__)

@items.route('/')
def index():
    recent_activities = Item.query.order_by(desc(Item.id))[:10]
    return render_template("index.html", recent_activities=recent_activities)


@items.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    form = LogActivity()
    form.item_id.choices = pick_activity()
    user = current_user.name.capitalize()
    current_activities = Item.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html",
                           user=user,
                           current_activities=current_activities,
                           form=form)

@items.route("/add_log", methods=['POST', 'GET'])
@login_required
def add_log():
    form = LogActivity()
    form.item_id.choices = pick_activity()

    if form.validate_on_submit():
        log = Action(item_id=form.item_id.data,
                     value=form.value.data,
                     logged_at=form.logged_at.data)
        db.session.add(log)
        db.session.commit()
        flash("You successfully added a log")
        return redirect(url_for('items.dashboard'))
    else:
        flash_errors(form)
        return redirect(url_for('items.dashboard'))


@items.route('/dashboard/add_activity', methods=['POST', 'GET'])
@login_required
def add_activity():
    form = AddActivity()
    if form.validate_on_submit():
        item = Item(user_id=current_user.id,
                    name=form.name.data,
                    goal=form.goal.data,
                    description=form.description.data)
        db.session.add(item)
        db.session.commit()
        flash("You successfully added an activity")
        return redirect(url_for('items.dashboard'))
    else:
        flash_errors(form)
        return render_template("add_update_activity.html", form=form)


@items.route('/dashboard/activity/delete/<int:int_id>', methods=["GET"])
@login_required
def delete_activity(int_id):
    deleted_object = Item.query.filter_by(id=int_id).first()
    db.session.delete(deleted_object)
    db.session.commit()
    flash("You successfully removed that activity")
    return redirect(url_for('items.dashboard'))

@items.route('/dashboard/log/delete/<int:int_id>', methods=["GET"])
@login_required
def delete_log(int_id):
    deleted_object = Action.query.filter_by(id=int_id).first()
    db.session.delete(deleted_object)
    db.session.commit()
    flash("You successfully removed that log of your activity")
    return redirect(url_for('items.view_logs'))

@items.route('/dashboard/log/edit/<int:int_id>', methods=['POST', 'GET'])
@login_required
def edit_log(int_id):
    edited_object = Action.query.filter_by(id=int_id).first()
    form = LogActivity(item_id=edited_object.item.id)
    form.item_id.choices = pick_activity()
    if form.validate_on_submit():
        print('heyyyyyyy')
        edited_object.value = form.value.data
        edited_object.logged_at = form.logged_at.data
        db.session.commit()
        flash("You successfully updated your log")
        return redirect(url_for('items.view_logs'))
    else:
        flash_errors(form)
        return render_template("edit_logs.html",
                               form=form,
                               edited_object=edited_object)

@items.route('/dashboard/activity/edit/<int:int_id>', methods=['POST', 'GET'])
@login_required
def edit_activity(int_id):
    form = AddActivity()
    edited_object = Item.query.filter_by(id=int_id).first()

    if form.validate_on_submit():
        edited_object.name = form.name.data
        edited_object.goal = form.goal.data
        edited_object.description = form.description.data
        db.session.commit()
        flash("You successfully updated your activty")
        return redirect(url_for('items.dashboard'))
    else:
        flash_errors(form)
        return render_template("add_update_activity.html",
                               form=form,
                               edited_object=edited_object)

@items.route('/dashboard/view_logs', methods=['GET'])
@login_required
def view_logs():
    all_logs = Action.query.filter(Action.item.has(user_id=current_user.id))\
               .order_by(Action.logged_at.desc())
    return render_template("view_logs.html", all_logs=all_logs)

@items.route('/dashboard/activity/chart/<int:int_id>', methods=['POST', 'GET'])
@login_required
def chart(int_id):

    form = ChartDate()
    if form.start_date.data:
        start_date = form.start_date.data
        end_date = form.end_date.data
    else:
        start_date = datetime.now().date() - timedelta(days=30)
        end_date = datetime.now().date()
    chart_activity = Item.query.filter_by(id=int_id).first()
    activities = Action.query.filter(Action.logged_at.between(start_date, \
                 end_date)).filter_by(item_id=int_id).order_by(\
                 Action.logged_at.desc()).all()
    dates = [activity.logged_at for activity in activities]
    values = [activity.value for activity in activities]
    chart_url = create_chart(dates, values)
    return render_template("chart.html", chart_activity=chart_activity,
                           chart_url=chart_url)


def create_chart(dates, values):
    py.sign_in("xacrucesalus", "tdddyf0aea")
    mov_avg = Scatter(x=dates, y=values, line=Line(width=2, color='#007095',
                      opacity=0.5),name='Moving average')
    data = Data([mov_avg])
    py.iplot(data, filename='activity moving average')
    first_plot_url = py.plot(data, filename='activity moving average',
                             auto_open=False,)
    return first_plot_url

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form,
                  field).label.text, error), category)

def pick_activity():
    item_list = Item.query.filter_by(user_id=current_user.id).all()
    return [(item.id, item.name) for item in item_list]
