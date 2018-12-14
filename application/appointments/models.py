from application import db
from application.models import Base
from sqlalchemy.sql import text
import datetime

users = db.Table("account_appointment",
    db.Column("account_id", db.Integer, db.ForeignKey("account.id"), primary_key=True),
    db.Column("appointment_id", db.Integer, db.ForeignKey("appointment.id"), primary_key=True))

class Appointment(Base):

    time_reserved = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    customer = db.Column(db.String(144), nullable=False)
    friseur = db.Column(db.String(144), nullable=False)
    reservation_number = db.Column(db.String(8), nullable=False)
    fulfilled = db.Column(db.Boolean, nullable=False)

    users = db.relationship("User", secondary=users, lazy=True, backref=db.backref("appointments", lazy=True))

    work_day_id = db.Column(db.Integer, db.ForeignKey("work_day.id"), nullable=False)

    def __init__(self, time, duration, customer, friseur, reservation_number, fulfilled):
        self.time_reserved = time
        self.duration = duration
        self.customer = customer
        self.friseur = friseur
        self.reservation_number = reservation_number
        self.fulfilled = fulfilled
    
    def get_time(self):
        if isinstance(self.time_reserved, datetime.time):
            time = self.time_reserved.strftime("%H:%M")
        else:
            time = self.time_reserved[0:5]
        return time

    def get_customer(self):
        for user in self.users:
            if user.role.name == "USER":
                return user.name
        return self.customer

    def get_friseur(self):
        for user in self.users:
            if user.role.name == "FRISEUR":
                return user.name
        return self.friseur

    
    @staticmethod
    def account_appointment_for_day(user_id, work_day_id):
        stmt = text("SELECT appointment.time_reserved, appointment.duration, appointment.customer, appointment.reservation_number, appointment.fulfilled "
                    "FROM appointment "
                    "INNER JOIN account_appointment "
                    "ON account_appointment.account_id = :user "
                    "AND account_appointment.appointment_id = appointment.id "
                    "WHERE appointment.work_day_id = :work_day "
                    "ORDER BY appointment.time_reserved ASC ;").params(user=user_id, work_day=work_day_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            # Check type of object because of difference in returned object between development db and production db
            if isinstance(row[0], datetime.time):
                time = row[0].strftime("%H:%M")
            else:
                time = row[0][0:5]
            response.append({"time_reserved": time, "duration": row[1], "customer": row[2], "reservation_number": row[3], "fulfilled": row[4]})
        
        return response


    @staticmethod
    def full_appointment_data():
        stmt = text("SELECT DISTINCT appointment.time_reserved, appointment.duration, appointment.customer, appointment.reservation_number, appointment.friseur, appointment.fulfilled, appointment.id, work_day.date "
                    "FROM appointment "
                    "INNER JOIN work_day "
                    "ON appointment.work_day_id = work_day.id "
                    "LEFT JOIN account_appointment "
                    "ON account_appointment.appointment_id = appointment.id "
                    "LEFT JOIN account "
                    "ON account.role_id = 2 "
                    "AND account.id = account_appointment.account_id "
                    "ORDER BY work_day.date DESC, appointment.time_reserved ASC ;")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            # Check type of object because of difference in returned object between development db and production db
            if isinstance(row[0], datetime.time):
                time = row[0].strftime("%H:%M")
            else:
                time = row[0][0:5]
            if isinstance(row[7], datetime.datetime):
                date = row[7].strftime("%Y-%m-%d")
            else:
                date = row[7][0:10]
            
            response.append({"time_reserved": time, "duration": row[1], "customer": row[2], "reservation_number": row[3], "friseur": row[4], "fulfilled": row[5], "id": row[6], "date": date})
        
        return response

    @staticmethod
    def full_appointment_data_paginate(offset=0, count=5):
        stmt = text("SELECT DISTINCT appointment.time_reserved, appointment.duration, appointment.customer, appointment.reservation_number, appointment.friseur, appointment.fulfilled, appointment.id, work_day.date "
                    "FROM appointment "
                    "INNER JOIN work_day "
                    "ON appointment.work_day_id = work_day.id "
                    "LEFT JOIN account_appointment "
                    "ON account_appointment.appointment_id = appointment.id "
                    "LEFT JOIN account "
                    "ON account.role_id = 2 "
                    "AND account.id = account_appointment.account_id "
                    "ORDER BY work_day.date DESC, appointment.time_reserved ASC "
                    "LIMIT :offset, :count ;").params(offset=offset, count=count)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            # Check type of object because of difference in returned object between development db and production db
            if isinstance(row[0], datetime.time):
                time = row[0].strftime("%H:%M")
            else:
                time = row[0][0:5]
            if isinstance(row[7], datetime.datetime):
                date = row[7].strftime("%Y-%m-%d")
            else:
                date = row[7][0:10]
            
            response.append({"time_reserved": time, "duration": row[1], "customer": row[2], "reservation_number": row[3], "friseur": row[4], "fulfilled": row[5], "id": row[6], "date": date})
        
        return response

    @staticmethod
    def how_many_appointments():
        stmt = text("SELECT COUNT(DISTINCT appointment.id) "
                    "FROM appointment;")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"total": row[0]})
        
        return response[0].get("total")
    
    @staticmethod
    def friseur_full_appointment_data(user_id):
        stmt = text("SELECT DISTINCT appointment.time_reserved, appointment.duration, appointment.customer, appointment.reservation_number, account.name, appointment.fulfilled, appointment.id, work_day.date "
                    "FROM appointment "
                    "INNER JOIN work_day "
                    "ON appointment.work_day_id = work_day.id "
                    "INNER JOIN account_appointment "
                    "ON account_appointment.appointment_id = appointment.id "
                    "INNER JOIN account "
                    "ON account.id = :user "
                    "WHERE account.role_id = 2 "
                    "AND account_appointment.account_id = :user "
                    "ORDER BY work_day.date DESC, appointment.time_reserved ASC ;").params(user=user_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            # Check type of object because of difference in returned object between development db and production db
            if isinstance(row[0], datetime.time):
                time = row[0].strftime("%H:%M")
            else:
                time = row[0][0:5]
            if isinstance(row[7], datetime.datetime):
                date = row[7].strftime("%Y-%m-%d")
            else:
                date = row[7][0:10]
            
            response.append({"time_reserved": time, "duration": row[1], "customer": row[2], "reservation_number": row[3], "friseur": row[4], "fulfilled": row[5], "id": row[6], "date": date})
        
        return response

    @staticmethod
    def customer_full_appointment_data(user_id):
        stmt = text("SELECT DISTINCT appointment.time_reserved, appointment.duration, appointment.customer, appointment.reservation_number, account.name, appointment.fulfilled, appointment.id, work_day.date "
                    "FROM appointment "
                    "INNER JOIN work_day "
                    "ON appointment.work_day_id = work_day.id "
                    "INNER JOIN account_appointment "
                    "ON account_appointment.appointment_id = appointment.id "
                    "INNER JOIN account "
                    "ON account.id = :user "
                    "WHERE account.role_id = 1 "
                    "AND account_appointment.account_id = :user "
                    "ORDER BY work_day.date ASC, appointment.time_reserved ASC ;").params(user=user_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            # Check type of object because of difference in returned object between development db and production db
            if isinstance(row[0], datetime.time):
                time = row[0].strftime("%H:%M")
            else:
                time = row[0][0:5]
            if isinstance(row[7], datetime.datetime):
                date = row[7].strftime("%Y-%m-%d")
            else:
                date = row[7][0:10]
            
            response.append({"time_reserved": time, "duration": row[1], "customer": row[2], "reservation_number": row[3], "friseur": row[4], "fulfilled": row[5], "id": row[6], "date": date})
        
        return response
    
    @staticmethod
    def upcoming_appointment_data(user_id):
        stmt = text("SELECT DISTINCT appointment.time_reserved, appointment.duration, appointment.customer, appointment.reservation_number, appointment.friseur, appointment.fulfilled, appointment.id, work_day.date "
                    "FROM appointment "
                    "INNER JOIN work_day "
                    "ON appointment.work_day_id = work_day.id "
                    "INNER JOIN account_appointment "
                    "ON account_appointment.appointment_id = appointment.id "
                    "INNER JOIN account "
                    "ON account_appointment.account_id = :user "
                    "WHERE account.id = :user "
                    "AND CURRENT_TIMESTAMP < work_day.date OR CURRENT_TIME < appointment.time_reserved "
                    "ORDER BY work_day.date ASC, appointment.time_reserved ASC ;").params(user=user_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            # Check type of object because of difference in returned object between development db and production db
            if isinstance(row[0], datetime.time):
                time = row[0].strftime("%H:%M")
            else:
                time = row[0][0:5]
            if isinstance(row[7], datetime.datetime):
                date = row[7].strftime("%Y-%m-%d")
            else:
                date = row[7][0:10]
            
            response.append({"time_reserved": time, "duration": row[1], "customer": row[2], "reservation_number": row[3], "friseur": row[4], "fulfilled": row[5], "id": row[6], "date": date})
        
        return response

    @staticmethod
    def work_day_appointment_data(work_day_id):
        stmt = text("SELECT appointment.time_reserved, appointment.duration, appointment.customer, appointment.reservation_number, appointment.friseur, appointment.fulfilled, appointment.id, work_day.date "
                    "FROM appointment, work_day "
                    "WHERE appointment.work_day_id = :id "
                    "AND appointment.work_day_id = work_day.id "
                    "ORDER BY appointment.time_reserved ASC ;").params(id=work_day_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            # Check type of object because of difference in returned object between development db and production db
            if isinstance(row[0], datetime.time):
                time = row[0].strftime("%H:%M")
            else:
                time = row[0][0:5]
            if isinstance(row[7], datetime.datetime):
                date = row[7].strftime("%Y-%m-%d")
            else:
                date = row[7][0:10]
            
            response.append({"time_reserved": time, "duration": row[1], "customer": row[2], "reservation_number": row[3], "friseur": row[4], "fulfilled": row[5], "id": row[6], "date": date})
        
        return response

    @staticmethod
    def how_many_upcoming_appointments():
        stmt = text("SELECT COUNT(DISTINCT appointment.id) "
                    "FROM appointment "
                    "INNER JOIN work_day "
                    "ON appointment.work_day_id = work_day.id "
                    "WHERE CURRENT_TIMESTAMP < work_day.date;")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"upcoming": row[0]})
        
        return response

    # @staticmethod
    # def how_many_upcoming_appointments_test():
    #     stmt = text("SELECT COUNT(*) "
    #                 "FROM ("
    #                 "SELECT appointment.id "
    #                 "FROM appointment "
    #                 "INNER JOIN work_day "
    #                 "ON appointment.work_day_id = work_day.id "
    #                 "WHERE CURRENT_TIMESTAMP < work_day.date "
    #                 " UNION "
    #                 ""
    #                 "SELECT appointment.id "
    #                 "FROM appointment "
    #                 "INNER JOIN work_day "
    #                 "ON appointment.work_day_id = work_day.id "
    #                 "WHERE CURRENT_TIMESTAMP = work_day.date AND CURRENT_TIME < appointment.time_reserved "
    #                 ") matches"
    #                 ";")
    #     res = db.engine.execute(stmt)

    #     response = []
    #     for row in res:
    #         response.append({"upcoming": row[0]})
        
    #     return response

    @staticmethod
    def how_many_upcoming_appointments_for_user(user_id):
        stmt = text("SELECT COUNT(DISTINCT appointment.id) "
                    "FROM appointment "
                    "INNER JOIN account_appointment "
                    "ON appointment.id = account_appointment.appointment_id "
                    "INNER JOIN account "
                    "ON account_appointment.account_id = :user "
                    "INNER JOIN work_day "
                    "ON appointment.work_day_id = work_day.id "
                    "WHERE CURRENT_TIMESTAMP < work_day.date;").params(user=user_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"upcoming": row[0]})
        
        return response
    
    @staticmethod
    def how_many_appointments_fulfilled():
        stmt = text("SELECT COUNT(DISTINCT appointment.id) "
                    "FROM appointment "
                    "WHERE appointment.fulfilled IS true;")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"fulfilled": row[0]})
        
        return response

    