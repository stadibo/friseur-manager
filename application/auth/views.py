from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db, login_required, login_manager, bcrypt
from application.auth.models import User, Role
from application.work_days.models import Work_day, Friseur_work_day
from application.auth.forms import UserForm, LoginForm, PasswordForm


# Route to display and handle the login page

@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)

    if form.validate():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not bcrypt.check_password_hash(user.password, form.password.data):
            return render_template("auth/loginform.html", form=form, error="No such username or password")

        login_user(user)

        return redirect(url_for("index"))
    
    return render_template("auth/loginform.html", form=form)


# Route to display and handle the page for creating new users

@app.route("/auth/new_user", methods=["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/new_user.html", form=UserForm())

    form = UserForm(request.form)

    if not form.validate():
        return render_template("auth/new_user.html", form=form)

    user = User.query.filter_by(username=form.username.data).first()
    if user:
        return render_template("auth/new_user.html", form=form)

    # Encrypt password
    password_hash = bcrypt.generate_password_hash(form.password.data)
    user = User(form.name.data, form.username.data, password_hash)

    # if this is first user make them an admin
    if User.query.count() == 0:
        user.role = Role.query.get(3) # admin
    else:
        user.role = Role.query.get(1) # user

    db.session().add(user)
    db.session().commit()

    # Log in user
    created_user = User.query.filter_by(username=user.username).first()

    login_user(created_user)
    # return redirect(url_for("auth_login"))
    return redirect(url_for("index"))


# Route to display and handle the page for an admin to create a new employee level user

@app.route("/auth/admin/new_friseur", methods=["GET", "POST"])
@login_required(role="ADMIN")
def auth_new_friseur():
    if request.method == "GET":
        return render_template("auth/new_friseur.html", form=UserForm())

    form = UserForm(request.form)

    if not form.validate():
        print("Validate error")
        return render_template("auth/new_friseur.html", form=form)

    if form.password.data != form.passwordConfirmation.data:
        print("password not same")
        return render_template("auth/new_friseur.html", form=form)

    # Encrypt password and assign friseur role
    password_hash = bcrypt.generate_password_hash(form.password.data)
    user = User(form.name.data, form.username.data, password_hash)
    user.role = Role.query.get(2)

    db.session().add(user)
    db.session().flush()

    # Add all upcoming work days to friseur
    upcoming_work_days = Work_day.upcoming_work_days()
    for day in upcoming_work_days:
        friseur_work_day = Friseur_work_day(user.id, day.get("id"), 10, 17)
        db.session().add(friseur_work_day)
        db.session().flush()

    db.session().commit()
    return redirect(url_for("users_index"))


# Route to display the page for listing all existing users

@app.route("/auth/admin/all", methods=["GET"])
@login_required(role="ADMIN")
def users_index():
    return render_template("auth/list.html", users=User.query.order_by("role_id").all())


# Route to display the page for showing information about a single user

@app.route("/auth/admin/<user_id>/single", methods=["GET"])
@login_required(role="ADMIN")
def user_single(user_id):
    user = User.query.get(user_id)
    return render_template("auth/single.html", user=user)


# Route to display and handle the page for an admin to change the password of a user

@app.route("/auth/admin/<user_id>/single/change_password", methods=["GET", "POST"])
@login_required(role="ADMIN")
def user_change_password(user_id):
    user = User.query.get(user_id)
    if request.method == "GET":
        form = PasswordForm()
        return render_template("auth/edit_password.html", form=form, user_id=user_id)

    form = PasswordForm(request.form)

    if not form.validate():
        return render_template("auth/edit_password.html", form=form, user_id=user_id)

    if user is None or not bcrypt.check_password_hash(user.password, form.old_password.data):
        return render_template("auth/edit_password.html", form=form, user_id=user_id)

    user.password = bcrypt.generate_password_hash(form.new_password.data)

    db.session().commit()

    return redirect(url_for("users_index"))


# Route for an admin to delete a user other than the admin themselves

@app.route("/auth/admin/<user_id>/single/delete", methods=["GET"])
@login_required(role="ADMIN")
def user_delete(user_id):
    user = User.query.get(user_id)

    if user.username != current_user.username:
        db.session().delete(user)
        db.session().commit()

    return redirect(url_for("users_index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))
