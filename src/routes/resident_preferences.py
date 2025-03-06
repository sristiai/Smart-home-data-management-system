# src/routes/resident_preferences.py
print("Entering resident preferences route")
from flask import Blueprint, request, jsonify

from src.controllers.resident_preferences_controller import(
    get_all_preferences,
    get_preferences_by_resident,
    create_preference,
    update_preference,
    delete_preference
)
resident_preferences_bp = Blueprint('preferences', __name__)

@resident_preferences_bp.route('/preferences', methods=['GET'], endpoint='get_all_preferences')
def get_preferences():
    """Fetch all resident preferences."""
    preferences = get_all_preferences()
    results = [
        {
            "resident_id": pref.resident_id,
            "appliance_id": pref.appliance_id,
            "house_id": pref.house_id,
            "notification_type": pref.notification_type,
            "frequency": pref.frequency,
            "notification_channel": pref.notification_channel,
            "created_at": pref.created_at
        }
        for pref in preferences
    ]
    return jsonify(results), 200

@resident_preferences_bp.route('/preferences/<int:resident_id>', methods=['GET'], endpoint='get_preferences_by_resident')
def get_preferences(resident_id):
    preferences = get_preferences_by_resident(resident_id)
    results = [

        {
            "resident_id": pref.resident_id,
            "appliance_id": pref.appliance_id,
            "house_id": pref.house_id,
            "notification_type": pref.notification_type,
            "frequency": pref.frequency,
            "notification_channel": pref.notification_channel,
            "created_at": pref.created_at
        }
        for pref in preferences
    ]
    return jsonify(results), 200

@resident_preferences_bp.route('/preferences', methods=['POST'])
def create_preference_route():
    data = request.json
    required_fields = ['resident_id', 'appliance_id', 'house_id', 'notification_type', 'notification_channel']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field '{field}'"}), 400

    try:
        new_preference = create_preference(data)
        return jsonify({
            "message": "Preference created successfully",
            "data": {
                "resident_id": new_preference.resident_id,
                "appliance_id": new_preference.appliance_id,
                "house_id": new_preference.house_id,
                "notification_type": new_preference.notification_type
            }
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400  # Validation error
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Generic error
    
@resident_preferences_bp.route('/preferences/<int:resident_id>', methods=['PUT'])
def update_preference_route(resident_id):
    preferences = get_preferences_by_resident(resident_id)
    if not preferences:
        return jsonify({"error": "Preferences not found"}), 404
    data = request.json
    for pref in preferences:
        update_preference(pref, data)
    return jsonify({"message": "Preferences updated successfully"}), 200

@resident_preferences_bp.route('/preferences/<int:resident_id>', methods=['DELETE'])
def delete_preference_route(resident_id):
    preferences = get_preferences_by_resident(resident_id)
    if not preferences:
        return jsonify({"error": "Preferences not found"}), 404

    for pref in preferences:
        delete_preference(pref)

    return jsonify({"message": "Preferences deleted successfully"}), 200