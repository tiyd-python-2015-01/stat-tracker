from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show

"""Add your views here."""

from flask import Blueprint, render_template, flash, redirect, url_for, send_file
from flask.ext.login import login_required, current_user

from ..extensions import db
#from ..forms import LinkAddForm, LinkUpdateForm
#from ..models import Links, Clicks

tasksb = Blueprint("tasksb",__name__)


@tasksb.route("/")
def index():
    #if current_user.is_authenticated():
        return render_template("index.html")
