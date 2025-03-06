# src/controllers/resident_preference_controller.py
print("Entering resident preference controller")
from src.controllers.appliance_controller import get_appliance_by_id
from src.controllers.house_controller import get_house_by_id
from src.controllers.residents_controller import get_resident_by_id
from src.models.db import db
from src.models.resident_preferences_model import ResidentPreference

def get_all_preferences():
    return ResidentPreference.query.all()

def get_preferences_by_resident(resident_id):
    return ResidentPreference.query.filter_by(resident_id=resident_id).all()

def create_preference(data):
    # Validate Resident existence
    resident = get_resident_by_id(data['resident_id'])
    if not resident:
        raise ValueError(f"Resident with id {data['resident_id']} does not exist.")

    # Validate Appliance existence
    appliance = get_appliance_by_id(data['appliance_id'])
    if not appliance:
        raise ValueError(f"Appliance with id {data['appliance_id']} does not exist.")

    # Validate House existence
    house = get_house_by_id(data['house_id'])
    if not house:
        raise ValueError(f"House with id {data['house_id']} does not exist.")

    # Create preference
    preference = ResidentPreference(
        resident_id=data['resident_id'],
        appliance_id=data['appliance_id'],
        house_id=data['house_id'],
        notification_type=data['notification_type'],
        frequency=data.get('frequency', 'real-time'),
        notification_channel=data['notification_channel']
    )
    db.session.add(preference)
    db.session.commit()
    return preference

def update_preference(preference, data):
    if 'notification_type' in data:
        preference.notification_type = data['notification_type']
    if 'frequency' in data:
        preference.frequency = data['frequency']
    if 'notification_channel' in data:
        preference.notification_channel = data['notification_channel']
    db.session.commit()
    return preference

def delete_preference(preference):
    db.session.delete(preference)
    db.session.commit()
