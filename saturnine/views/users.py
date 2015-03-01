from flask import Blueprint, render_template, redirect
from ..models import User
from ..forms import LoginForm, RegisterUser

users = Blueprint("users", __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in!")
            return redirect(request.args.get("next") or url_for('index'))
        else:
            flash("Email or password is not correct.")
    return render_template('login.html', form=form)


@users.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('index'))


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("User with that email already exists.")
        else:
            user = User(name=form.name.data,
                        email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("You have been registered and logged in.")
            return redirect(url_for("index"))
    else:
        flash_errors(form)
    return render_template('register.html',
                           form=form)
