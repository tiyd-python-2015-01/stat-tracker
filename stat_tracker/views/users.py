from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask.ext.login import login_user, logout_user, current_user
from sqlalchemy import desc
from ..extensions import db
from ..forms import LoginForm, RegistrationForm
from ..models import User, Activities


users = Blueprint("users", __name__)


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error),
                                                                   category)

@users.route('/', methods=['GET', 'POST'])
def index():
    return render_template('titlepage.html')


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You were logged in.')
            return redirect(url_for('users.home_view'))
        else:
            flash('Invalid Password')

    flash_errors(form)
    return render_template('login.html', form=form)


@users.route("/logout", methods=['GET', 'POST'])
def logout():
    user = current_user
    logout_user()
    flash('You have been logged out.')
    return render_template('titlepage.html')


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('A user with that email already exists.')
        else:
            user = User(name=form.name.data,
                        email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Registration successful! You have been logged in.')
            return redirect(url_for('users.home_view'))

        flash_errors(form)
        return render_template('register.html', form=form)


@users.route('/home')
def home_view():
    activities = Activities.query.filter_by(user_id=current_user.id).order_by(Activities.id.desc())
    return render_template('home_page.html', activities=activities)


#@users.route('/home/stats')
#def stat_table():
#    links = Links.query.filter_by(user_id=current_user.id).order_by(Links.id.desc())
#    return render_template('stats.html', user_links=links)
