from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.fields.html5 import EmailField, URLField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, EqualTo

class APIForm(Form):
    def __init__(self, *args, **kwargs):
        default_kwargs = {"formdata": None, "csrf_enabled": False}
        default_kwargs.update(kwargs)
        super().__init__(*args, **default_kwargs)

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


class TaskForm(APIForm):
    t_name = StringField('Task Name', validators=[DataRequired()])
    t_type = IntegerField('Task Type', validators=[DataRequired()])
    t_units = StringField('Units', validators=[DataRequired()])

class TrackingForm(APIForm):
    tr_date = DateField('Date', validators =[DataRequired()])
    tr_value = IntegerField("Today's Value", validators=[DataRequired()])

class DeleteTrackingForm(APIForm):
    tr_date = DateField('Date', validators =[DataRequired()])
