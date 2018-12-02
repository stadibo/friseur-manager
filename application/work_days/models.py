from application import db
from application.models import Base
from sqlalchemy.sql import text


class Work_day(Base):

    date = db.Column(db.DateTime, nullable=False, unique=True)
    
    friseur_work_days = db.relationship("Friseur_work_day", cascade="delete", lazy=True)
    appointments = db.relationship("Appointment", cascade="delete", backref="work_day", lazy=True)

    def __init__(self, date):
        self.date = date

    def __repr__(self):
        return self.date.strftime("%Y-%m-%d")
    
    @staticmethod
    def upcoming_work_days():
        stmt = text("SELECT work_day.id, work_day.date "
                    "FROM work_day "
                    "WHERE CURRENT_TIMESTAMP < work_day.date "
                    "ORDER BY work_day.date ASC;")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id": row[0], "date": row[1]})
        
        return response

class Friseur_work_day(db.Model):
    user_id = db.Column("account_id", db.Integer, db.ForeignKey("account.id"), primary_key=True)
    work_day_id = db.Column("work_day_id", db.Integer, db.ForeignKey("work_day.id"), primary_key=True)
    start = db.Column(db.Integer)
    finish = db.Column(db.Integer)

    user = db.relationship("User")
    work_day = db.relationship("Work_day")

    def __init__(self, user_id, work_day_id, start, finish):
        self.user_id = user_id
        self.work_day_id = work_day_id
        self.start = start
        self.finish = finish

    def __repr__(self):
        return "{} -> {}".format(self.start, self.finish)