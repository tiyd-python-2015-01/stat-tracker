from flask.ext.wtf.recaptcha import validators
from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Optional


class LoginForm(Form):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(Form):
    name = StringField('User Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password',
        validators=[DataRequired(),
                    EqualTo('password_verification',
                            message='Passwords must match')])
    password_verification = PasswordField('Repeat password')


class ActivityForm(Form):
    name = StringField('What Activity would you like to track?', validators=[DataRequired()])
    type = SelectField("Activity type", choices=[('clicker', "Clicker"), ('yes_no', "Seinfeld"), ('scale', "Scale")])
    unit = StringField('Unit')


class UpdateForm(Form):
    occurrences = IntegerField('Occurrences')
    scale = SelectField('How would you rate this activity?', choices=[(1, 'Bad'), (2, 'Not great'),
                                                                      (3, 'Okay'), (4, "Good"), (5, "Awesome")],
                        coerce=int, validators=[Optional()])
    yes_no = SelectField("Did you do it today?", choices=[(0, "No"), (1, "Yes")], coerce=int,
                         validators=[Optional()])
    date = DateField('DatePicker', format='%Y-%m-%d')


