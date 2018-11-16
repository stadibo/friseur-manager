from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


# Form for logging in
class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False


# Form for user creation
class UserForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2)])
    username = StringField("Username", [validators.Length(min=3)])
    password = PasswordField("Password", [validators.Length(min=8)])
    passwordConfirmation = PasswordField(
        "Confirm password", [validators.Length(min=8)])

    class Meta:
        csrf = False
