from flask_wtf import Form
from wtforms import StringField, PasswordField,DateField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(Form):

    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])


class RegistrationForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password',
        validators=[DataRequired(),
                    EqualTo('password_verification',
                            message="Passwords must match")])
    password_verification = PasswordField('Repeat password')



class ActivityForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired()])

class InstanceForm(Form):
    date = DateField('date', validators=[DataRequired()])
    freq = IntegerField('frequency', validators=[DataRequired()])
