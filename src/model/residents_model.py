# my_smart_home_app/src/models/resident.py
print("Entering resident model")
from datetime import date
from src.models.db import db

class Resident(db.Model):
    __tablename__ = 'residents'

    resident_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.house_id'), nullable=False)
    move_in_date = db.Column(db.Date, nullable=True)
    move_out_date = db.Column(db.Date, nullable=True)

    # Relationship
    user = db.relationship('User', back_populates='residents')
    house = db.relationship('House', back_populates='residents')
    calendars = db.relationship('Calendar', back_populates='resident',cascade='all, delete-orphan')
    permissions = db.relationship('CalendarEventPermission', back_populates='resident', cascade='all, delete-orphan')
    notification_logs = db.relationship(
        'NotificationLog',
        primaryjoin="and_(Resident.house_id == foreign(NotificationLog.house_id))",
        viewonly=True
    )
    preferences = db.relationship('ResidentPreference', back_populates='resident',cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Resident id={self.resident_id}>"
