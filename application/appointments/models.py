from application import db
from application.models import Base

users = db.Table("account_appointment",
    db.Column("account_id", db.Integer, db.ForeignKey("account.id"), primary_key=True),
    db.Column("appointment_id", db.Integer, db.ForeignKey("appointment.id"), primary_key=True))

class Appointment(Base):

    time_reserved = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    reservation_number = db.Column(db.String(144), nullable=False)
    fullfilled = db.Column(db.Boolean, nullable=False)

    users = db.relationship("User", secondary=users, lazy=True, backref=db.backref("appointments", lazy=True))

    work_day_id = db.Column(db.Integer, db.ForeignKey("work_day.id"), nullable=False)

    def __init__(self, date, start, end, reservation_number):
        self.date = date
        self.start = start
        self.end = end
        self.reservation_number = reservation_number