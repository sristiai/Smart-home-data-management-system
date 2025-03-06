# my_smart_home_app/src/models/user.py
print("Entering user model")
from datetime import datetime
from src.models.db import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    birth_date = db.Column(db.Date, nullable=True)  # Added birth_date
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Added role ('resident', 'owner', 'admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    houses = db.relationship('House', back_populates='user', cascade='all, delete-orphan')
    residents = db.relationship('Resident', back_populates='user', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User id={self.user_id} username={self.username}>"
