from application import db
from application.models import Base

# users = db.Table("account_work_day",
#     db.Column("account_id", db.Integer, db.ForeignKey("account.id"), primary_key=True),
#     db.Column("work_day_id", db.Integer, db.ForeignKey("work_day.id"), primary_key=True))

# users = db.relationship("User", secondary=users, lazy=True, backref=db.backref("work_days", lazy=True))

class Work_day(Base):

    date = db.Column(db.DateTime, nullable=False, unique=True)
    
    Friseur_work_days = db.relationship("Friseur_work_day", cascade="delete", lazy=True)
    appointments = db.relationship("Appointment", backref="work_day", lazy=True)

    def __init__(self, date):
        self.date = date

class Friseur_work_day(db.Model):
    user_id = db.Column("account_id", db.Integer, db.ForeignKey("account.id"), primary_key=True)
    work_day_id = db.Column("work_day_id", db.Integer, db.ForeignKey("work_day.id"), primary_key=True)
    start = db.Column(db.Integer)
    finish = db.Column(db.Integer)

    user = db.relationship("User", lazy=True)
    work_day = db.relationship("Work_day", lazy=True)

    def __init__(self, user, work_day, start, end):
        self.user_id = user.id
        self.work_day_id = work_day.id
        self.start = start
        self.end = end

    def __repr__(self):
        return '{} - {} - {} - {}'.format(self.user_id, self.work_day_id, self.start, self.end)