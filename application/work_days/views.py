from flask import redirect, render_template, request, url_for
from application import app, db, login_required, login_manager
from application.work_days.models import Work_day
from application.work_days.forms import WorkdayForm, MultipleWorkdayForm
from datetime import datetime, date


@app.route("/workdays/all", methods=["GET", "POST"])
def work_days_index():
    if request.method == "GET":
        return render_template("work_days/list.html", form=WorkdayForm(),  work_days=Work_day.query.all())

    form = WorkdayForm(request.form)

    if not form.validate():
        print("Validate error")
        return render_template("work_days/list.html", form=form, work_days=Work_day.query.all())

    current_date = datetime.now()
    new_date = datetime.combine(form.date.data, datetime.min.time())

    if current_date > new_date:
        return render_template("work_days/list.html", form=form, work_days=Work_day.query.all())

    work_day = Work_day(new_date)
    db.session().add(work_day)
    db.session().commit()

    return redirect(url_for("work_days_index"))


@app.route("/workdays/<work_day_id>/info", methods=["GET"])
def work_days_info(work_day_id):
    return redirect(url_for("work_days_index"))
