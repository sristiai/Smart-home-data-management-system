print("Entering calendar route")
from flask import Blueprint, request, jsonify
from src.controllers.residents_controller import get_resident_by_id
from src.controllers.calendar_controller import (
    get_all_calendars,
    get_calendar_by_id,
    create_calendar,
    update_calendar,
    delete_calendar
)

# Define a blueprint for calendar routes
calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/calendars', methods=['GET'])
def get_calendars():
    calendars = get_all_calendars()
    results = [
        {
            "calendar_id": cal.calendar_id,
            "resident_id": cal.resident_id,
            "calendar_name": cal.calendar_name,
            "created_at": cal.created_at
        }
        for cal in calendars
    ]
    return jsonify(results), 200

@calendar_bp.route('/calendars/<int:calendar_id>', methods=['GET'])
def get_calendar(calendar_id):
    calendar = get_calendar_by_id(calendar_id)
    if not calendar:
        return jsonify({"error": "Calendar not found"}), 404
    return jsonify({
        "calendar_id": calendar.calendar_id,
        "resident_id": calendar.resident_id,
        "calendar_name": calendar.calendar_name,
        "created_at": calendar.created_at
    }), 200

@calendar_bp.route('/calendars', methods=['POST'])
def create_calendar_route():
    data = request.json
    required_fields = ['resident_id', 'calendar_name']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field '{field}'"}), 400

    try:
        new_calendar = create_calendar(data)
        return jsonify({"message": "Calendar created successfully", "calendar_id": new_calendar.calendar_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@calendar_bp.route('/calendars/<int:calendar_id>', methods=['PUT'])
def update_calendar_route(calendar_id):
    calendar = get_calendar_by_id(calendar_id)
    if not calendar:
        return jsonify({"error": "Calendar not found"}), 404

    data = request.json
    try:
        updated_calendar = update_calendar(calendar, data)
        return jsonify({
            "message": "Calendar updated successfully",
            "calendar_id": updated_calendar.calendar_id,
            "resident_id": updated_calendar.resident_id,
            "calendar_name": updated_calendar.calendar_name,
            "created_at": updated_calendar.created_at
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@calendar_bp.route('/calendars/<int:calendar_id>', methods=['DELETE'])
def delete_calendar_route(calendar_id):
    calendar = get_calendar_by_id(calendar_id)
    if not calendar:
        return jsonify({"error": "Calendar not found"}), 404

    delete_calendar(calendar)
    return jsonify({"message": "Calendar deleted successfully"}), 200