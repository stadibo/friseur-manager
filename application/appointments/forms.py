from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

# Form for prividing name when reserving while not logged in
class AppointmentForm(FlaskForm):
    customer = StringField("Name", [validators.Length(min=2, max=100)])
    
    confirm = SubmitField("Confirm")

    # class Meta:
    #     csrf = False