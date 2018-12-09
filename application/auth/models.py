from application import db
from application.models import Base
from sqlalchemy.sql import text

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False, unique=True)
    password = db.Column(db.Binary(72), nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=True)
    role = db.relationship("Role")

    friseur_work_days = db.relationship("Friseur_work_day", cascade="delete", lazy=True)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def has_appointment(appointment_id, user_id):
        stmt = text("SELECT * "
                    "FROM account_appointment, account "
                    "WHERE account_appointment.account_id = :user "
                    "AND account_appointment.appointment_id = :appointment "
                    "AND account.id = :user;").params(user=user_id, appointment=appointment_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"count": row[0]})

        print(len(response))
        
        return len(response) > 0

    # @staticmethod
    # def customer_has_appointment(appointment_id, user_id):
    #     stmt = text("SELECT COUNT(*) AS count "
    #                 "FROM account_appointment, account "
    #                 "WHERE account_appointment.account_id = :user "
    #                 "AND account_appointment.appointment_id = :appointment "
    #                 "AND account.id = :user "
    #                 "AND account.role_id = 1;").params(user=user_id, appointment=appointment_id)
    #     res = db.engine.execute(stmt)

    #     response = []
    #     for row in res:
    #         response.append({"count": row[0]})
        
    #     return response
        

class Role(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
