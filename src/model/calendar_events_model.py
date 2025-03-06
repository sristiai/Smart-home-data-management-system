# my_smart_home_app/src/models/calendar_event.py
print("Entering calendar event model")
from datetime import datetime
from src.models.db import db

class CalendarEvent(db.Model):
    __tablename__ = 'calendar_events'

    event_id = db.Column(db.Integer, primary_key=True)
    calendar_id = db.Column(db.Integer, db.ForeignKey('calendars.calendar_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_recurring = db.Column(db.Boolean, default=False)
    recurrence_rule = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    calendar = db.relationship('Calendar', back_populates='events')
    permissions = db.relationship('CalendarEventPermission', back_populates='event',cascade='all, delete-orphan')

    def __repr__(self):
        return f"<CalendarEvent id={self.event_id} title='{self.title}'>"
