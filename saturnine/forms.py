from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.fields.html5 import URLField, EmailField
from wtforms.validators import DataRequired, url, Email, EqualTo


class LoginForm(Form):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegisterUser(Form):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired(),
                                         EqualTo("password_verification",
                                         message="Passwords must match")])
    password_verification = PasswordField("Repeat Password",
                                    validators=[DataRequired()])

class AddActivity(Form):
    name = StringField("Name", validators=[DataRequired()])
    description = StringField("Description")

