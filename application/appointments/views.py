from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user
from flask_paginate import Pagination, get_page_args

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

    page, per_page, offset = get_page_args()
    appointments_total = len(appointments)
    appointments_paginated = appointments_for_page(appointments, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=appointments_total,
                            css_framework="bootstrap4", record_name="appointments")

    return render_template("appointments/list.html", appointments=appointments_paginated,
                           upcoming=upcoming,
                           fulfilled=fulfilled,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)

# Get appointments limited by the page the user is currently on
def appointments_for_page(appointments, offset=0, per_page=10):
  return appointments[offset: offset + per_page]


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
    friseur_times = list(map(lambda a: datetime.time(
        int(a.get("time_reserved")[0:2])), appointments))
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
        # Check if a customer is logged in and create an appointment
        reservation_number = logged_in_user_reserves(
            user_id, work_day_id, time)
        if reservation_number:
            # New appointment created for user
            return render_template("appointments/appointment_created.html", reservation_number=reservation_number)
        else:
            # Show the reservation form for non logged in customers
            return render_template("appointments/appointment_new.html", form=AppointmentForm(), user_id=user_id, work_day_id=work_day_id, time=time)
    else:
        # Get information for non logged in customer and add their appointment
        form = AppointmentForm(request.form)

        if not form.validate():
            return render_template("appointments/appointment_new.html", form=form, user_id=user_id, work_day_id=work_day_id, time=time)

        # Create information necessary to identify appointment
        reservation_number = generate_unique_reservation_number()
        time_formatted = format_time_for_appointment(time)
        friseur = User.query.get(user_id)
        appointment = Appointment(
            time_formatted, 1, form.customer.data, friseur.name, reservation_number, False)

        appointment.users.append(friseur)
        appointment.work_day_id = work_day_id

        db.session().add(appointment)
        db.session().commit()
        return render_template("appointments/appointment_created.html", reservation_number=reservation_number)


def logged_in_user_reserves(user_id, work_day_id, time):
    # Check if a user is logged in and what role they have
    role = "ANY"
    try:
        role = current_user.role.name
    except AttributeError:
        pass

    if role == "USER":
        # Create information necessary to identify appointment
        reservation_number = generate_unique_reservation_number()
        time_formatted = format_time_for_appointment(time)
        friseur = User.query.get(user_id)
        appointment = Appointment(
            time_formatted, 1, current_user.name, friseur.name, reservation_number, False)

        appointment.users.append(current_user)
        appointment.users.append(friseur)
        appointment.work_day_id = work_day_id

        db.session().add(appointment)
        db.session().commit()
        return reservation_number
        # return render_template("appointments/appointment_created.html", reservation_number=res_nr)
    return None


def generate_unique_reservation_number():
    notUnique = True
    while notUnique:
        reservation_number = generate_reservation_number()
        notUnique = Appointment.query.filter_by(
            reservation_number=reservation_number).first()
    return reservation_number


def generate_reservation_number():
    number = "{:08}".format(random.randrange(0, 10**8))
    return number


# Time from the selection form comes in the form of a string and is converted to datetime.time
def format_time_for_appointment(time):
    time_as_int = int(time[0:2])
    time_formatted = datetime.time(time_as_int, 0)
    return time_formatted


# Show the full information about an appointment
@app.route("/appointments/admin/<appointment_id>/single", methods=["GET"])
@login_required(role="ADMIN")
def appointments_single(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        date = Work_day.query.get(appointment.work_day_id)
        return render_template("appointments/single.html", appointment=appointment, date=date)
    return redirect(url_for("appointments_index"))


# Change the state of an appointment from not fulfilled to fullfilled - or vice versa
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
        flash("Appointment %s successfully removed." % appointment.reservation_number)
    return redirect(url_for("appointments_index"))
