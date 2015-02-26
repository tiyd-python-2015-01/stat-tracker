from flask import render_template, flash, redirect, request, Blueprint
from flask import url_for, request, send_file
from flask.ext.login import login_user, logout_user
from flask.ext.login import login_required, current_user

from ..forms import LoginForm, RegistrationForm, AddBookmark
from ..models import Bookmark, User, BookmarkUser, Click
from ..extensions import db
from datetime import datetime
from sqlalchemy import desc, and_
from .bookmarks import flash_errors


users = Blueprint("users", __name__)

@users.route("/", defaults={'page': 1})
@users.route('/<int:page>')
def index(page):
    top_bookmarks = BookmarkUser.query.order_by(desc(BookmarkUser.id))[:10]
    return render_template("index.html", bookmarks=top_bookmarks)

@users.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    form = AddBookmark()
    user = current_user.name.capitalize()
    bookmarks = BookmarkUser.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html",
                           bookmarks=bookmarks,
                           form=form,
                           user=user)

@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("users.dashboard"))
        else:
            flash("That email or password is not correct.")

    flash_errors(form)
    return render_template("login.html", form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.index'))

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
            return redirect(url_for("users.dashboard"))
    else:
        flash_errors(form)
    return render_template("register.html", form=form)
