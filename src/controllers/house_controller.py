# src/controllers/house_controller.py
print("Entering house controller")
from src.models.db import db
from src.models.houses_model import House

def get_all_houses():
    """Return all House records."""
    return House.query.all()

def get_house_by_id(house_id):
    """Return one house by primary key."""
    return House.query.get(house_id)

def create_house(data):
    """Create a new house."""
    house = House(
        user_id=data['user_id'],
        address=data['address']
    )
    db.session.add(house)
    db.session.commit()
    return house

def update_house(house, data):
    """Update an existing house object."""
    for field in ['user_id', 'address']:
        if field in data:
            setattr(house, field, data[field])
    db.session.commit()
    return house

def delete_house(house):
    """Delete a house."""
    db.session.delete(house)
    db.session.commit()
