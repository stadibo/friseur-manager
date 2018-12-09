from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required, login_manager, bcrypt
from application.auth.models import User, Role
from application.work_days.models import Work_day
from application.auth.forms import UserForm, LoginForm, PasswordForm
from application.appointments.models import Appointment


# Route to display the page for showing information about a friseur or customer

@app.route("/account/", methods=["GET"])
@login_required()
def account_page():
    user = User.query.get(current_user.id)
    appointments = []
    if user:
      if user.role.name == "FRISEUR":
          appointments = Appointment.friseur_full_appointment_data(user.id)
          upcoming = Appointment.how_many_upcoming_appointments_for_user(current_user.id)[0].get("upcoming")
          return render_template("account/friseur.html", user=user, appointments=appointments, upcoming=upcoming)
      elif user.role.name == "USER":
          appointments = Appointment.upcoming_appointment_data(user.id)
          return render_template("account/customer.html", user=user, appointments=appointments)
    
    return redirect(url_for("index"))


@app.route("/account/change_password", methods=["GET", "POST"])
@login_required()
def account_change_password():
    user = User.query.get(current_user.id)
    if user:
      if request.method == "GET":
          form = PasswordForm()
          return render_template("account/edit_password.html", form=form)

      form = PasswordForm(request.form)

      if not form.validate():
          return render_template("account/edit_password.html", form=form)

      if user is None or not bcrypt.check_password_hash(user.password, form.old_password.data):
          return render_template("account/edit_password.html", form=form)

      user.password = bcrypt.generate_password_hash(form.new_password.data)

      db.session().commit()

    return redirect(url_for("account_page"))

  
@app.route("/account/appointments/<appointment_id>/single", methods=["GET"])
@login_required("FRISEUR")
def account_appointments_single(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        date = Work_day.query.get(appointment.work_day_id)
        return render_template("account/friseur_appointment.html", appointment=appointment, date=date)
    return redirect(url_for("account_page"))

    
@app.route("/account/appointments/<appointment_id>/single/change_status", methods=["GET"])
@login_required("FRISEUR")
def account_appointments_single_complete(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        appointment.fulfilled = not appointment.fulfilled
        db.session().commit()

        return redirect(url_for("account_appointments_single", appointment_id=appointment_id))
    return redirect(url_for("account_page"))


@app.route("/account/appointments/<appointment_id>/single/delete", methods=["GET"])
@login_required()
def account_appointments_single_delete(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    has_appointment = User.has_appointment(appointment_id, current_user.id)

    if appointment and has_appointment:
      db.session().delete(appointment)
      db.session().commit()
    return redirect(url_for("account_page"))