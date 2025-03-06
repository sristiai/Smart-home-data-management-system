# my_smart_home_app/src/models/calendar_events_permissions.py
print("Entering calendar event permissions model")
from datetime import datetime
from src.models.db import db
from sqlalchemy.dialects.postgresql import ENUM

role_type_enum = ENUM('owner', 'editor', 'viewer', name='role_type', create_type=False)

class CalendarEventPermission(db.Model):
    __tablename__ = 'calendar_events_permissions'

    permission_id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('residents.resident_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('calendar_events.event_id'), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # e.g. 'owner', 'editor', 'viewer'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    resident = db.relationship('Resident', back_populates='permissions')
    event = db.relationship('CalendarEvent', back_populates='permissions')

    def __repr__(self):
        return f"<CalendarEventPermission id={self.permission_id} role={self.role}>"
