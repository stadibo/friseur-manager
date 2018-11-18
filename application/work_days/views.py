from flask import redirect, render_template, request, url_for
from flask_login import login_required
from application import app, db
from application.work_days.models import Work_day
from application.work_days.forms import WorkdayForm, MultipleWorkdayForm

@app.route("/work_days/all", methods="GET", "POST")
@login_required
def work_days_index():
  return render_template("work_days/list.html", work_days=Work_day.query.all())

@app.route("/work_days/<work_day_id>/delete", methods=["GET"])
@login_required
def work_days_delete(work_day_id):
  db.session().delete(Work_day.query.get(work_day_id))
  db.session().commit()

  return redirect(url_for("work_days_index"))

@app.route("/work_days/<work_day_id>/single", methods=["GET"])
@login_required
def work_day_appointments(work_day_id):
  work_day = Work_day.query.get(work_day_id)
  return render_template("work_days/single.html", work_day=work_day)