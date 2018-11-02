from application import app, db
from flask import redirect, render_template, request, url_for
from application.accounts.models import Account

@app.route("/accounts/", methods=["GET"])
def accounts_index():
  return render_template("accounts/list.html", accounts = Account.query.all())

@app.route("/accounts/new/")
def accounts_form():
  return render_template("accounts/new.html")

@app.route("/accounts/<account_id>/", methods=["POST"])
def accounts_change_password(account_id):
  a = Account.query.get(account_id)
  a.password = request.form.get("new_password")
  db.session().commit()

  return redirect(url_for("accounts_index"))

@app.route("/accounts/", methods=["POST"])
def accounts_create():
  rf = request.form
  a = Account(
    rf.get("name"),
    rf.get("username"),
    rf.get("password"),
    "loyal"
  )

  db.session().add(a)
  db.session().commit()

  return redirect(url_for("accounts_index"))