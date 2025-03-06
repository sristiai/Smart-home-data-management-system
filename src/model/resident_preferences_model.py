# my_smart_home_app/src/models/resident_preference.py
print("Entering resident preference model")
from datetime import datetime
from src.models.db import db

class ResidentPreference(db.Model):
    __tablename__ = 'resident_preferences'

    resident_id = db.Column(db.Integer, db.ForeignKey('residents.resident_id'), primary_key=True)
    appliance_id = db.Column(db.Integer, db.ForeignKey('appliances.appliance_id'), primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.house_id'), nullable=False)
    notification_type = db.Column(db.String(50), primary_key=True)
    frequency = db.Column(db.String(20))
    notification_channel = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    resident = db.relationship('Resident', back_populates='preferences')
    house = db.relationship('House', back_populates='preferences')
    appliance = db.relationship('Appliance', back_populates='preferences')  # Ensure no conflicting name

    def __repr__(self):
        return (f"<ResidentPreference resident_id={self.resident_id} "
                f"appliance_id={self.appliance_id} "
                f"notification_type={self.notification_type}>")