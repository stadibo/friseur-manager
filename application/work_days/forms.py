from flask_wtf import FlaskForm
from wtforms import IntegerField, validators
from wtforms.fields.html5 import DateField

class WorkdayForm(FlaskForm):
  date = DateField("Date", format="%Y-%m-%d")

  class Meta:
    csrf = False

class MultipleWorkdayForm(FlaskForm):
  date = DateField("Start from date")
  days_to_create = IntegerField("Work dats to generate")