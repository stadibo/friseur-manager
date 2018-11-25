from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user
from application import app, db, login_required, login_manager
from application.auth.models import User, Role
from application.auth.forms import UserForm, LoginForm, PasswordForm


# Route to display and handle the login page

@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(
        username=form.username.data).first()
    if not user:
        return render_template("auth/loginform.html", form=form, error="No such username or password")

    login_user(user)
    return redirect(url_for("index"))


# Route to display and handle the page for creating new users

@app.route("/auth/new_user", methods=["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/new_user.html", form=UserForm())

    form = UserForm(request.form)

    if not form.validate():
        print("Validate error")
        return render_template("auth/new_user.html", form=form)

    if form.password.data != form.passwordConfirmation.data:
        print("password not same")
        return render_template("auth/new_user.html", form=form)

    user = User(form.name.data, form.username.data, form.password.data)
    user.role = Role.query.get(1)

    db.session().add(user)
    db.session().commit()

    return redirect(url_for("auth_login"))


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

    user = User(form.name.data, form.username.data, form.password.data)
    user.role = Role.query.get(2)
    print(user.role)

    db.session().add(user)
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
        print("Validate error")
        return render_template("auth/edit_password.html", form=form, user_id=user_id)

    if form.new_password.data != form.passwordConfirmation.data:
        print("password not same")
        return render_template("auth/edit_password.html", form=form, user_id=user_id, error="confirmation does not match")

    if form.old_password.data != user.password:
        print("old password not same")
        return render_template("auth/edit_password.html", form=form, user_id=user_id, error="old password does not match")

    user.password = form.new_password.data

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