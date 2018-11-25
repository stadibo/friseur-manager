from flask_wtf import FlaskForm
from wtforms import StringField, validators

# Form for logging in
class AppointmentForm(FlaskForm):
    customer = StringField("Name", [validators.Length(min=2)])

    class Meta:
        csrf = False