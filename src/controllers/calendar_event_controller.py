# src/controllers/calendar_event_controller.py
print("Entering calendar event controller")
from src.models.db import db
from src.models.calendar_events_model import CalendarEvent
from src.models.calendars_model import Calendar


def get_all_calendar_events():
    return db.session.query(CalendarEvent, Calendar).join(Calendar).all()

def get_event_by_id(event_id):
    return db.session.query(CalendarEvent, Calendar).join(Calendar).filter(CalendarEvent.event_id == event_id).first()

def create_event(data):
    event = CalendarEvent(
        calendar_id=data['calendar_id'],
        title=data['title'],
        description=data.get('description'),
        start_time=data['start_time'],
        end_time=data['end_time'],
        is_recurring=data.get('is_recurring', False),
        recurrence_rule=data.get('recurrence_rule')
    )
    db.session.add(event)
    db.session.commit()
    return event

def update_event(event, data):
    if 'title' in data:
        event.title = data['title']
    if 'description' in data:
        event.description = data['description']
    if 'start_time' in data:
        event.start_time = data['start_time']
    if 'end_time' in data:
        event.end_time = data['end_time']
    if 'is_recurring' in data:
        event.is_recurring = data['is_recurring']
    if 'recurrence_rule' in data:
        event.recurrence_rule = data['recurrence_rule']
    db.session.commit()
    return event

def delete_event(event):
    db.session.delete(event)
    db.session.commit()