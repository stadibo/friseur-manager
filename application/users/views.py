from application import app, db
from flask import redirect, render_template, request, url_for
from application.users.models import User

@app.route("/users/list", methods=["GET"])
def users_index():
  return render_template("users/list.html", users = User.query.all())

@app.route("/users/new")
def users_form():
  return render_template("users/new_user.html")

@app.route("/users/edit_user/<user_id>", methods=["GET", "POST"])
def user_edit(user_id):
  user = User.query.get(user_id)
  if request.method == "GET":
    return render_template("users/edit_user.html", user=user)
  
  rf = request.form

  user.name = rf.get("name")
  user.username = rf.get("username")
  user.password = rf.get("password")
  
  db.session().commit()
  
  return redirect(url_for("users_index"))

@app.route("/users/delete/<user_id>", methods=["GET"])
def user_delete(user_id):
  db.session().delete(User.query.get(user_id))
  db.session().commit()

  return redirect(url_for("users_index"))

@app.route("/users/new_user", methods=["POST"])
def users_create():
  rf = request.form
  user = User(
    rf.get("name"),
    rf.get("username"),
    rf.get("password"),
    "loyal"
  )

  db.session().add(user)
  db.session().commit()

  return redirect(url_for("users_index"))