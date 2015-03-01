from flask_wtf import Form
from wtforms import StringField, PasswordField, TextField
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
    title = StringField('Activity', validators=[DataRequired()])
