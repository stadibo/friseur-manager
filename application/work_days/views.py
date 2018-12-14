from flask import redirect, render_template, request, url_for, flash
from application import app, db, login_required, login_manager
from application.work_days.models import Work_day, Friseur_work_day
from application.auth.models import User
from application.appointments.models import Appointment
from application.work_days.forms import WorkdayForm
from datetime import datetime, date


# Route for admin to view and add work days

@app.route("/workdays/admin/all", methods=["GET", "POST"])
@login_required(role="ADMIN")
def work_days_index():
    work_days = Work_day.query.order_by(Work_day.date.asc()).all()
    work_days_with_amount = []
    for work_day in work_days:
        work_days_with_amount.append({"work_day": work_day, "amount": len(work_day.appointments)})

    if request.method == "GET":
        return render_template("work_days/list.html", form=WorkdayForm(), work_days=work_days_with_amount)

    form = WorkdayForm(request.form)

    if not form.validate():
        return render_template("work_days/list.html", form=form, work_days=work_days_with_amount)

    current_date = datetime.now()
    new_date = datetime.combine(form.date.data, datetime.min.time())

    work_day = Work_day.query.filter_by(date=new_date).first()

    if current_date > new_date or work_day:
        flash("Work day already passed. Add on that is in the future.", "alert-warning")
        return render_template("work_days/list.html", form=form, work_days=work_days_with_amount)

    work_day = Work_day(new_date)
    db.session().add(work_day)
    db.session().commit()

    flash("Work day successfully added.", "alert-success")

    friseurs = User.query.filter_by(role_id=2)
    added_work_day = Work_day.query.filter_by(date=work_day.date).first()
    for friseur in friseurs:
        db.session().add(Friseur_work_day(friseur.id, added_work_day.id, 10, 17))
        db.session().commit()

    return redirect(url_for("work_days_index"))


# Route for showing more information about day, like friseurs working and appointments

@app.route("/workdays/admin/<work_day_id>/info", methods=["GET"])
@login_required(role="ADMIN")
def work_days_info(work_day_id):
    work_day = Work_day.query.get(work_day_id)
    if work_day:
        appointments = Appointment.work_day_appointment_data(work_day_id)
        average = Work_day.average_amount_of_appointments_for_day(work_day_id)
        return render_template("work_days/single.html", appointments=appointments, average_amount=average, amount=len(appointments), date=work_day)
    
    return redirect(url_for("work_days_index"))


# Route for deleting work days

@app.route("/workdays/admin/<work_day_id>/delete", methods=["GET"])
@login_required(role="ADMIN")
def work_days_delete(work_day_id):
    work_day = Work_day.query.get(work_day_id)
    if work_day:
        flash("Work day successfully deleted")
        db.session().delete(work_day)
        db.session().commit()
    return redirect(url_for("work_days_index"))
