from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import URLField, EmailField
from wtforms.validators import DataRequired, url, Email, EqualTo


class LoginForm(Form):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterUser(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         EqualTo('password_verify',
                                         message="Passwords must match")])
    password_verify = PasswordField('Repeat Password',
                                    validators=[DataRequired()])
