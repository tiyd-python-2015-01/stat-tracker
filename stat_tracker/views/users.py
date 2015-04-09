from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask.ext.login import login_user , login_required, current_user
from flask.ext.login import logout_user
from ..extensions import db
from ..forms import LoginForm, RegistrationForm
from ..models import User


users = Blueprint("users", __name__)

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("stats.index"))
        else:
            flash("That email or password is not correct.")

    flash_errors(form)
    return render_template("login.html", form=form)



@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("A user with that email address already exists.")
        else:
            user = User(name=form.name.data,
                        email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("You have been registered and logged in.")
            return redirect(url_for("stats.index"))
    else:
        flash_errors(form)

    return render_template("register.html", form=form)


@users.route("/logoff", methods = ["GET"])
def logoff():
    logout_user()
    return redirect(url_for("stats.index"))
