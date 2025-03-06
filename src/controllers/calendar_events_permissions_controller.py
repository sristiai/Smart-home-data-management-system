# src/controllers/calendar_events_permissions_controller.py
print("Entering calendar event permissions controller")
from src.models.db import db
from src.models.calendar_events_permissions_model import CalendarEventPermission

def get_all_permissions():
    return CalendarEventPermission.query.all()

def get_permission_by_id(permission_id):
    return CalendarEventPermission.query.get(permission_id)

def create_permission(data):
    permission = CalendarEventPermission(
        resident_id=data['resident_id'],
        event_id=data['event_id'],
        role=data['role']
    )
    db.session.add(permission)
    db.session.commit()
    return permission

def update_permission(permission, data):
    if 'role' in data:
        permission.role = data['role']
    db.session.commit()
    return permission

def delete_permission(permission):
    db.session.delete(permission)
    db.session.commit()
