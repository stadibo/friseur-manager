from application import db
from application.models import Base
from sqlalchemy.sql import text

users = db.Table("account_appointment",
    db.Column("account_id", db.Integer, db.ForeignKey("account.id"), primary_key=True),
    db.Column("appointment_id", db.Integer, db.ForeignKey("appointment.id"), primary_key=True))

class Appointment(Base):

    time_reserved = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    customer = db.Column(db.String(144), nullable=False)
    reservation_number = db.Column(db.String(8), nullable=False)
    fulfilled = db.Column(db.Boolean, nullable=False)

    users = db.relationship("User", secondary=users, lazy=True, backref=db.backref("appointments", lazy=True))

    work_day_id = db.Column(db.Integer, db.ForeignKey("work_day.id"), nullable=False)

    def __init__(self, time, duration, customer, reservation_number, fulfilled):
        self.time_reserved = time
        self.duration = duration
        self.customer = customer
        self.reservation_number = reservation_number
        self.fulfilled = fulfilled

    @staticmethod
    def account_appointment_for_day(user_id, work_day_id):
        stmt = text("SELECT appointment.time_reserved, appointment.duration, appointment.customer, appointment.reservation_number, appointment.fulfilled "
                    "FROM appointment "
                    "INNER JOIN account_appointment "
                    "WHERE account_appointment.account_id = :user "
                    "AND account_appointment.appointment_id = appointment.id "
                    "AND appointment.work_day_id = :work_day "
                    "ORDER BY appointment.time_reserved ASC ;").params(user=user_id, work_day=work_day_id)
        res =db.engine.execute(stmt)

        response = []
        for row in res:
            response.append(Appointment(row[0], row[1], row[2], row[3], row[4]))
        
        return response