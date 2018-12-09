from flask import redirect, render_template, request, url_for
from flask_login import current_user
from application import app, db, login_required, login_manager
from application.appointments.models import Appointment
from application.appointments.forms import AppointmentForm
from application.auth.models import User
from application.work_days.models import Work_day, Friseur_work_day
import datetime
import random


@app.route("/appointments/admin/all", methods=["GET"])
@login_required(role="ADMIN")
def appointments_index():
    appointments = Appointment.full_appointment_data()
    upcoming = Appointment.how_many_upcoming_appointments()[0].get("upcoming")
    fulfilled = Appointment.how_many_appointments_fulfilled()[0].get("fulfilled")
    return render_template("appointments/list.html", appointments=appointments, upcoming=upcoming, fulfilled=fulfilled)


@app.route("/appointments/reserve/select_friseur", methods=["GET"])
def appointments_select_friseur():
    return render_template("appointments/select_friseur.html", friseurs=User.query.filter_by(role_id=2).all())


@app.route("/appointments/reserve/<user_id>/select_date", methods=["GET"])
def appointments_select_date(user_id):
    friseur_work_days = Friseur_work_day.upcoming_friseur_work_days(user_id)
    return render_template("appointments/select_date.html", work_days=friseur_work_days, user_id=user_id)


@app.route("/appointments/reserve/<user_id>/<work_day_id>", methods=["GET"])
def appointments_select_time(user_id, work_day_id):
    appointments = Appointment.account_appointment_for_day(user_id, work_day_id)

    # Filter timeslots so that only non occupied appointment time possibilities are shown
    friseur_times = list(map(lambda a: datetime.time(int(a.get("time_reserved")[0:2])), appointments))
    available_times = []

    # Display only open timeslots
    for timeslot in range(10, 18):
        if datetime.time(timeslot) not in friseur_times:
            available_times.append(datetime.time(timeslot).strftime("%H:%M"))

    return render_template("appointments/select_time.html", user_id=user_id, work_day_id=work_day_id, times=available_times)


@app.route("/appointments/reserve/<user_id>/<work_day_id>/<time>/new", methods=["GET", "POST"])
def appointments_reserve_form(user_id, work_day_id, time):
    # Add the appointment based on the logged in user or display the form if not customer("USER")
    if request.method == "GET":
      role = "ANY"
      try:
        role = current_user.role.name
      except AttributeError:
        pass
      
      if role == "USER":
        res_nr = "{:08}".format(random.randrange(0, 10**8))
        time_as_int = int(time[0:2])
        time_formatted = datetime.time(time_as_int, 0)

        appointment = Appointment(time_formatted, 1, current_user.name, res_nr, False)
      
        friseur = User.query.get(user_id)
        appointment.users.append(current_user)
        appointment.users.append(friseur)
        appointment.work_day_id = work_day_id
      
        db.session().add(appointment)
        db.session().commit()
        return render_template("appointments/appointment_created.html", reservation_number=res_nr)

      return render_template("appointments/appointment_new.html", form=AppointmentForm(), user_id=user_id, work_day_id=work_day_id, time=time)
    
    # Get information for non logged in customer and add their appointment
    form = AppointmentForm(request.form)

    if not form.validate():
      return render_template("appointments/appointment_new.html", form=form, user_id=user_id, work_day_id=work_day_id, time=time)
    
    res_nr = "{:08}".format(random.randrange(0, 10**8))
    time_as_int = int(time[0:2])
    time_formatted = datetime.time(time_as_int, 0)

    appointment = Appointment(time_formatted, 1, form.customer.data, res_nr, False)

    friseur = User.query.get(user_id)
    appointment.users.append(friseur)
    appointment.work_day_id = work_day_id
      
    db.session().add(appointment)
    db.session().commit()
    return render_template("appointments/appointment_created.html", reservation_number=res_nr)


@app.route("/appointments/admin/<appointment_id>/single", methods=["GET"])
@login_required(role="ADMIN")
def appointments_single(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
      date = Work_day.query.get(appointment.work_day_id)
      return render_template("appointments/single.html", appointment=appointment, date=date)
    return redirect(url_for("appointments_index"))

    
@app.route("/appointments/admin/<appointment_id>/single/change_status", methods=["GET"])
@login_required(role="ADMIN")
def appointments_single_complete(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
      appointment.fulfilled = not appointment.fulfilled
      db.session().commit()

      return redirect(url_for("appointments_single", appointment_id=appointment_id))
    return redirect(url_for("appointments_index"))

@app.route("/appointments/admin/<appointment_id>/single/delete", methods=["GET"])
@login_required(role="ADMIN")
def appointments_single_delete(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
      db.session().delete(appointment)
      db.session().commit()
      return redirect(url_for("appointments_index"))