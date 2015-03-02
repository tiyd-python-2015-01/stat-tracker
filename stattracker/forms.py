from flask_wtf import Form
from wtforms import StringField, PasswordField, FloatField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, URL


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

class EnterpriseForm(Form):
    ent_name = StringField('Name', validators=[DataRequired()])
    ent_unit = StringField("Unit Name", validators=[DataRequired()])

class StatForm(Form):
    value = FloatField('Value')
    recorded_at = DateField('Recorded At', validators=[DataRequired()])
