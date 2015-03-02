from flask import Blueprint, render_template, flash, redirect, url_for
from ..models import Activity
from ..forms import AddActivity
from . import flash_errors

from flask.ext.login import login_required, current_user

activities = Blueprint('activities', __name__)


@activities.route("/")
def index():
    """ Display prompt to log in or register if user is not logged in.
    If user is logged in, give option to add new activity, and list tracked activities.
    """
    if current_user.is_authenticated():
        activities = Activity.query.filterby(user=current_user.id).all()
        return render_template("home.html", activities=activities)
    else:
        return render_template("index.html")


@activities.route('/add', methods=["GET", "POST"])
@login_required
def add_activity():
    form = AddActivity()
    if form.validate_on_submit():
        activity = Activity(**form.data)
        db.session.add(activity)
        db.commit()
        flash("Activity added!")
        return redirect(url_for("index.index"))
    return render_template("activity_form.html",
                           form=form,
                           post_url=url_for("activities.add_activity"),
                           button="Add activity")


