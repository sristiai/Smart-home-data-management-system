print("Entering appliance controller")
from src.models.db import db
from src.models.appliances_model import Appliance
from src.models.houses_model import House

def get_all_appliances():
    """Fetch all appliances."""
    return Appliance.query.all()

def get_appliance_by_id(appliance_id):
    """Fetch an appliance by its ID."""
    return Appliance.query.get(appliance_id)

def create_appliance(data):
    """Create a new appliance."""
    appliance = Appliance(
        house_id=data['house_id'],
        name=data['name'],
        status=data.get('status', 'off'),
        notify_on_change=data.get('notify_on_change', False)
    )
    db.session.add(appliance)
    db.session.commit()
    return appliance

def update_appliance(appliance, data):
    """Update an existing appliance."""
    for field in ['name', 'status', 'notify_on_change']:
        if field in data:
            setattr(appliance, field, data[field])
    db.session.commit()
    return appliance

def delete_appliance(appliance):
    """Delete an appliance."""
    db.session.delete(appliance)
    db.session.commit()
