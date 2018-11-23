from application import db
from application.models import Base

users = db.Table("account_work_day",
    db.Column("account_id", db.Integer, db.ForeignKey("account.id"), primary_key=True),
    db.Column("work_day_id", db.Integer, db.ForeignKey("work_day.id"), primary_key=True))

class Work_day(Base):

    date = db.Column(db.DateTime, nullable=False, unique=True)
    users = db.relationship("User", secondary=users, lazy=True, backref=db.backref("work_days", lazy=True))
    appointments = db.relationship("Appointment", backref="work_day", lazy=True)

    def __init__(self, date):
        self.date = date