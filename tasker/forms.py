from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.fields.html5 import EmailField, URLField, IntegerField, DateField
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


class TaskForm(Form):
    t_name = StringField('Task Name', validators=[DataRequired()])
#    t_type = IntegerField('Task Type', validators=[DataRequired()])
    t_type = SelectField('Task Type',
                         choices=[(1, 'Input a Daily Value'),
                                  (2, 'Click button to add 1 to value'),
                                  (3, 'Time Goal'),
                                  (4, 'Yes/No'),
                                  (5, 'Scale')])
    t_units = StringField('Units', validators=[DataRequired()])

class TrackingForm(Form):
    tr_date = DateField('Date', validators =[DataRequired()])
    tr_value = IntegerField("Today's Value", validators=[DataRequired()])

class DeleteTrackingForm(Form):
    tr_date = DateField('Date', validators =[DataRequired()])
