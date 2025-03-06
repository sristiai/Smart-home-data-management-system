# src/controllers/calendar_controller.py
print("Entering calendar controller")
from src.models.db import db
from src.models.calendars_model import Calendar
from src.controllers.residents_controller import get_resident_by_id

def get_all_calendars():
    return Calendar.query.all()

def get_calendar_by_id(calendar_id):
    return Calendar.query.get(calendar_id)

def create_calendar(data):
    """Create a new calendar."""
    resident = get_resident_by_id(data['resident_id'])
    if not resident:
        raise ValueError(f"Resident with ID {data['resident_id']} does not exist")

    calendar = Calendar(
        resident_id=data['resident_id'],
        calendar_name=data['calendar_name']
    )
    db.session.add(calendar)
    db.session.commit()
    return calendar

def update_calendar(calendar, data):
    """Update an existing calendar."""
    if 'resident_id' in data:
        resident = get_resident_by_id(data['resident_id'])
        if not resident:
            raise ValueError(f"Resident with ID {data['resident_id']} does not exist")
        calendar.resident_id = data['resident_id']

    if 'calendar_name' in data:
        calendar.calendar_name = data['calendar_name']

    db.session.commit()
    return calendar

def delete_calendar(calendar):
    db.session.delete(calendar)
    db.session.commit()
