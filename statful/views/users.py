from flask import render_template, flash, request, url_for, redirect, Blueprint
from flask.ext.login import login_user, logout_user, login_required

from ..forms import LoginForm, RegisterForm
from ..extensions import db
from ..models import User


users = Blueprint('users', __name__)


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@users.route('/')
def index():
    return render_template('index.html', base_url=request.url_root)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get('next') or url_for("links.index"))
        else:
            flash("That user name or password is not correct.")
    flash_errors(form)

    return render_template('login.html', form=form)


@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user:
            flash("A user with that user name already exists.")
        else:
            user = User(name=form.name.data,
                        email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("You have been registered and logged in.")
            return redirect(url_for("links.index"))
    else:
        flash_errors(form)

    return render_template("registration.html", form=form)


@users.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out")

    return redirect(url_for('links.index'))