from flask import render_template, flash, request, url_for, redirect, Blueprint
from flask.ext.login import login_required
import plotly
import plotly.tools as tls
from ..forms import BasicActivityForm
from ..extensions import db

stats = Blueprint('stats', __name__)

credentials = tls.get_credentials_file()

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@login_required
@stats.route('/make_basic')
def make_basic():
    form = BasicActivityForm
    if form.validate_on_submit():




        

