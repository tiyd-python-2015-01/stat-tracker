from flask import Blueprint, render_template, flash, redirect, url_for
from ..models import Activity
from ..forms import AddActivity

from flask.ext.login import login_required, current_user

activities = Blueprint('activities', __name__)


@activities.route('/add', methods=["GET", "POST"])
@login_required
def add_activity():
    form = AddActivity()
    if form.validate_on_submit():
