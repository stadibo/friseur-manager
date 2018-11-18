from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required
from application import app, db
from application.auth.models import User
from application.auth.forms import UserForm, LoginForm, PasswordForm


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(
        username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form=form, error="No such username or password")

    login_user(user)
    return redirect(url_for("index"))


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

    db.session().add(user)
    db.session().commit()

    return redirect(url_for("users_index"))


@app.route("/auth/all", methods=["GET"])
@login_required
def users_index():
    return render_template("auth/list.html", users=User.query.all())


@app.route("/auth/<user_id>/single", methods=["GET"])
@login_required
def user_single(user_id):
    user = User.query.get(user_id)
    return render_template("auth/single.html", user=user)


@app.route("/auth/<user_id>/single/change_password", methods=["GET", "POST"])
@login_required
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


@app.route("/auth/<user_id>/single/delete", methods=["GET"])
@login_required
def user_delete(user_id):
    db.session().delete(User.query.get(user_id))
    db.session().commit()

    return redirect(url_for("users_index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))