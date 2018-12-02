from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators


# Form for logging in
class LoginForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired(), validators.Length(min=3, max=100)])
    password = PasswordField("Password", [validators.DataRequired(), validators.Length(min=8, max=50)])

    class Meta:
        csrf = False


# Form for user creation
class UserForm(FlaskForm):
    name = StringField("Name", [validators.DataRequired(), validators.Length(min=2, max=200)])
    username = StringField("Username", [validators.DataRequired(), validators.Length(min=3, max=200)])
    password = PasswordField("Password", [validators.DataRequired(), validators.Length(min=8, max=50)])
    passwordConfirmation = PasswordField(
        "Confirm password", [validators.DataRequired(), validators.Length(min=8, max=50), validators.EqualTo("password", message="Passwords do not match")])
        
    class Meta:
        csrf = False

# Form for changing password
class PasswordForm(FlaskForm):
    old_password = PasswordField("Old password", [validators.DataRequired(), validators.Length(min=8, max=50)])
    new_password = PasswordField("New password", [validators.DataRequired(), validators.Length(min=8, max=50)])
    passwordConfirmation = PasswordField(
        "Confirm new password", [validators.DataRequired(), validators.Length(min=8, max=50), validators.EqualTo("password", message="Passwords do not match")])

    class Meta:
        csrf = False
