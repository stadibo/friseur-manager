from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
import os

# database

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///friseur.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

# login authorization

from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please log in to use this functionality."

from functools import wraps

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            
            unauthorized = False

            if role != "ANY":
                unauthorized = True
                
                user_role = current_user.role.name
                
                if user_role == role:
                    unauthorized = False

            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# login functionality

from application.auth.models import User, Role

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# application
from application import views

from application.auth import views
from application.auth import models

from application.appointments import models
from application.appointments import views

from application.work_days import models
from application.work_days import views


# database table creation
try:
    db.create_all()
except:
    pass

try:
    from application.auth.models import Role

    role = Role.query.filter_by(name="USER").first()

    if not role:
        role = Role("USER")
        db.session().add(role)
        db.session().commit()

    role = Role.query.filter_by(name="FRISEUR").first()

    if not role:
        role = Role("FRISEUR")
        db.session().add(role)
        db.session().commit()

    role = Role.query.filter_by(name="ADMIN").first()

    if not role:
        role = Role("ADMIN")
        db.session().add(role)
        db.session().commit()
except:
    pass
