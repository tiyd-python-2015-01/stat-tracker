from flask import (Blueprint, render_template, flash, redirect, request,
                   url_for, session)
from flask.ext.login import (login_user, login_required, logout_user,
                             current_user)
from ..extensions import db, flash_errors
from ..models import User
from ..forms import LoginForm, RegistrationForm


users = Blueprint("users", __name__)


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("You were logged in!")
            return redirect(request.args.get("next") or url_for("links.index"))
        else:
            flash("E-mail address or password invalid.")
    flash_errors(form)
    return render_template("login.html", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("links.index"))


@users.route("/create_user", methods=["GET", "POST"])
def create_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("E-mail address already in use.")
        else:
            user = User(name=form.name.data,
                        email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            session["username"] = user.name
            flash("Registration Successful!  You have been logged in.")
            return redirect(url_for("stats.index"))
    else:
        flash_errors(form)
    return render_template("register.html", form=form)
