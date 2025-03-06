print("Entering calendar events route")
from flask import Blueprint, request, jsonify
from src.controllers.calendar_event_controller import (
    get_all_calendar_events,
    get_event_by_id,
    create_event,
    update_event,
    delete_event
)
from src.controllers.calendar_controller import get_calendar_by_id

# Define a blueprint for calendar events
calendar_events_bp = Blueprint('calendar_events', __name__)

@calendar_events_bp.route('/calendar_events', methods=['GET'])
def get_events():
    events = get_all_calendar_events()
    results = [
        {
            "event_id": event.CalendarEvent.event_id,
            "calendar_id": event.CalendarEvent.calendar_id,
            "calendar_name": event.Calendar.calendar_name,
            "title": event.CalendarEvent.title,
            "description": event.CalendarEvent.description,
            "start_time": event.CalendarEvent.start_time,
            "end_time": event.CalendarEvent.end_time,
            "is_recurring": event.CalendarEvent.is_recurring,
            "recurrence_rule": event.CalendarEvent.recurrence_rule,
            "created_at": event.CalendarEvent.created_at,
            "updated_at": event.CalendarEvent.updated_at
        }
        for event in events
    ]
    return jsonify(results), 200

@calendar_events_bp.route('/calendar_events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({
        "event_id": event.CalendarEvent.event_id,
        "calendar_id": event.CalendarEvent.calendar_id,
        "calendar_name": event.Calendar.calendar_name,
        "title": event.CalendarEvent.title,
        "description": event.CalendarEvent.description,
        "start_time": event.CalendarEvent.start_time,
        "end_time": event.CalendarEvent.end_time,
        "is_recurring": event.CalendarEvent.is_recurring,
        "recurrence_rule": event.CalendarEvent.recurrence_rule,
        "created_at": event.CalendarEvent.created_at,
        "updated_at": event.CalendarEvent.updated_at
    }), 200

@calendar_events_bp.route('/calendar_events', methods=['POST'])
def create_event_route():
    data = request.json
    required_fields = ['calendar_id', 'title', 'start_time', 'end_time']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field '{field}'"}), 400

    # Check if calendar exists
    calendar = get_calendar_by_id(data['calendar_id'])
    if not calendar:
        return jsonify({"error": f"Calendar with id {data['calendar_id']} does not exist"}), 400

    try:
        new_event = create_event(data)
        return jsonify({"message": "Event created successfully", "event_id": new_event.event_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@calendar_events_bp.route('/calendar_events/<int:event_id>', methods=['PUT'])
def update_event_route(event_id):
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.json
    updated_event = update_event(event.CalendarEvent, data)
    return jsonify({"message": "Event updated successfully"}), 200


@calendar_events_bp.route('/calendar_events/<int:event_id>', methods=['DELETE'])
def delete_event_route(event_id):
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    delete_event(event.CalendarEvent)
    return jsonify({"message": "Event deleted successfully"}), 200