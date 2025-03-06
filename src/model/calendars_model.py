# my_smart_home_app/src/models/calendar.py
print("Entering calendar model")
from datetime import datetime
from src.models.db import db

class Calendar(db.Model):
    __tablename__ = 'calendars'

    calendar_id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('residents.resident_id'), nullable=False)
    calendar_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    resident = db.relationship('Resident', back_populates='calendars')
    events = db.relationship('CalendarEvent', back_populates='calendar', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Calendar id={self.calendar_id} name={self.calendar_name}>"
