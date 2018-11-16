from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required
from application import app, db
from application.auth.models import User
from application.auth.forms import UserForm, LoginForm


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


@app.route("/auth/list", methods=["GET"])
@login_required
def users_index():
    return render_template("auth/list.html", users=User.query.all())


@app.route("/auth/<user_id>/edit_user", methods=["GET", "POST"])
@login_required
def user_edit(user_id):
    user = User.query.get(user_id)
    if request.method == "GET":
        return render_template("auth/edit_user.html", user=user)

    rf = request.form

    user.name = rf.get("name")
    user.username = rf.get("username")
    user.password = rf.get("password")

    db.session().commit()

    return redirect(url_for("users_index"))


@app.route("/auth/delete/<user_id>", methods=["GET"])
@login_required
def user_delete(user_id):
    db.session().delete(User.query.get(user_id))
    db.session().commit()

    return redirect(url_for("users_index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))
