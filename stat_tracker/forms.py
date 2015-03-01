from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, DateField
from wtforms.fields.html5 import EmailField
from wtforms_components import TimeField
from wtforms.validators import DataRequired, Email, EqualTo
from datetime import datetime


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password',
        validators=[DataRequired(),
                    EqualTo('password_verification',
                            message="Passwords must match")])
    password_verification = PasswordField('Repeat password')


class AddActivity(Form):
    name = StringField('Name', validators=[DataRequired()])
    goal = StringField('Goal')
    description = StringField('Description')


class LogActivity(Form):
    item_id = SelectField('Activity Type', coerce=int,
                          validators=[DataRequired()])
    value = StringField('Add Log', validators=[DataRequired()])
    logged_at = DateField('Action Date', validators=[DataRequired()])

class ChartDate(Form):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
