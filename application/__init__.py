import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from functools import wraps

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

# Login functionality
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth_login"
login_manager.login_message = "Please log in to use this functionality."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

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

# application
from application import views

from application.auth import views
from application.auth import models

from application.account import views

from application.appointments import models
from application.appointments import views

from application.work_days import models
from application.work_days import views

from application.auth.models import User, Role


# database table creation
try:
    db.create_all()
except:
    pass

try:
    from application.auth.models import Role

    role = Role.query.filter_by(name='USER').first()

    if not role:
        role = Role('USER')
        db.session().add(role)
        db.session().commit()

    role = Role.query.filter_by(name='FRISEUR').first()

    if not role:
        role = Role('FRISEUR')
        db.session().add(role)
        db.session().commit()

    role = Role.query.filter_by(name='ADMIN').first()

    if not role:
        role = Role('ADMIN')
        db.session().add(role)
        db.session().commit()
except:
    pass
