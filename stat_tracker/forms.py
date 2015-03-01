from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(Form):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])


class RegistrationForm(Form):
    name = StringField('Name:', validators=[DataRequired()])
    email = EmailField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password:',
        validators=[DataRequired(),
                    EqualTo('password_verification',
                            message="Passwords must match")])
    password_verification = PasswordField('Repeat password:')

class ActivityForm(Form):
    title = StringField('Type of Activity:', validators=[DataRequired()])
    value = StringField('Repetitions/Time Spent:', validators=[DataRequired()])
#    units = SelectField('Select Units', choices=([("Hours/Day","Hours/Day"),("Min/Day","Min/Day"),("Repetitions/Day","Repetitions/Day")]))
    description = StringField('Brief Description:', validators=[DataRequired()])
    recorded_at = DateField('Date:', validators=[DataRequired()])
