# my_smart_home_app/src/models/house.py
print("Entering house model")
from datetime import datetime
from src.models.db import db

class House(db.Model):
    __tablename__ = 'houses'

    house_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    user = db.relationship('User', back_populates='houses')
    residents = db.relationship('Resident', back_populates='house', cascade='all, delete-orphan')
    preferences = db.relationship('ResidentPreference', back_populates='house', cascade='all, delete-orphan')
    notification_logs = db.relationship('NotificationLog', back_populates='house', cascade='all, delete-orphan')
    appliances = db.relationship('Appliance', back_populates='house', cascade='all, delete-orphan') 
    
    def __repr__(self):
        return f"<House id={self.house_id} address={self.address}>"
