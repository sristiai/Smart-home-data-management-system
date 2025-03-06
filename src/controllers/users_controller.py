# src/controllers/user_controller.py
print("Entering user controller")
from src.models.db import db
from src.models.user_model import User

def get_all_users():
    """Return all User records."""
    return User.query.all()

def get_user_by_id(user_id):
    """Return one user by primary key."""
    return User.query.get(user_id)

def create_user(data):
    """Create a new user."""
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        username=data['username'],
        birth_date=data.get('birth_date'),
        password_hash=data['password_hash'],
        email=data['email'],
        role=data['role']
    )
    db.session.add(user)
    db.session.commit()
    return user

def update_user(user, data):
    """Update an existing user object."""
    for field in ['first_name', 'last_name', 'username', 'birth_date', 'password_hash', 'email', 'role']:
        if field in data:
            setattr(user, field, data[field])
    db.session.commit()
    return user

def delete_user(user):
    """Delete a user."""
    db.session.delete(user)
    db.session.commit()
