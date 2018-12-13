from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, validators
from wtforms.fields.html5 import DateField

class WorkdayForm(FlaskForm):
  date = DateField("New work day", format="%Y-%m-%d")
  
  create = SubmitField("Create")
  

class MultipleWorkdayForm(FlaskForm):
  date = DateField("Start from date")
  days_to_create = IntegerField("Work days to generate")

  create = SubmitField("Create")