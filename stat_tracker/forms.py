from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField, DateField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo


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


class ActivityForm(Form):
    activity_name = StringField('Activity', validators=[DataRequired()])
    measurement = StringField('Your Unit of Measure', validators=[DataRequired()])

class StatForm(Form):
    value = DecimalField("Enter Your Value", places=2, validators=[DataRequired()])
    recorded_at = DateField("What Day Was It", validators=[DataRequired()])
