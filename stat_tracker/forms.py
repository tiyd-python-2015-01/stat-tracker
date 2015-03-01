from flask.ext.wtf import Form
from wtforms import (StringField, PasswordField, TextField,
                     RadioField, DecimalField, validators)
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Email, EqualTo, url


class LoginForm(Form):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
        validators=[DataRequired(),
                    EqualTo('password_verification',
                            message="Passwords must match.")])
    password_verification = PasswordField('Repeat Password')


class ActivityForm(Form):
    title = StringField('Activity', validators=[DataRequired(),
                                                validators.Length(max=255)])
    activity_type = RadioField('Track Method', choices=[
        ('numeric', 'Numeric'), ('once', 'Once-a-day'),
        ('clicker', 'Clicker')])


class UpdateForm(Form):
    value = DecimalField("Stat value", validators=[DataRequired()], places=2)
