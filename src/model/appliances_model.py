print("Entering appliance model")
from datetime import datetime
from src.models.db import db

class Appliance(db.Model):
    __tablename__ = 'appliances'

    appliance_id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.house_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum('on', 'off', name='appliance_status'), nullable=False)  # Enum for appliance status
    notify_on_change = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    
    house = db.relationship('House', back_populates='appliances')
    preferences = db.relationship('ResidentPreference', back_populates='appliance', cascade='all, delete')

    def __repr__(self):
        return f"<Appliance id={self.appliance_id} name={self.name}>"
