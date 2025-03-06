print("Entering calendar events permission route")
from flask import Blueprint, request, jsonify
from src.controllers.calendar_events_permissions_controller import (
    get_all_permissions,
    get_permission_by_id,
    create_permission,
    update_permission,
    delete_permission
)
from src.controllers.residents_controller import get_resident_by_id
from src.controllers.calendar_event_controller import get_event_by_id
# Define a blueprint
permissions_bp = Blueprint('permissions', __name__)

@permissions_bp.route('/calendar_events_permissions', methods=['GET'])
def get_permissions():
    permissions = get_all_permissions()
    results = [
        {
            "permission_id": perm.permission_id,
            "resident_id": perm.resident_id,
            "event_id": perm.event_id,
            "role": perm.role,
            "created_at": perm.created_at
        }
        for perm in permissions
    ]
    return jsonify(results), 200

@permissions_bp.route('/calendar_events_permissions', methods=['POST'])
def create_permission_route():
    data = request.json
    required_fields = ['resident_id', 'event_id', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field '{field}'"}), 400

    # Verify resident and event existence
    resident = get_resident_by_id(data['resident_id'])
    if not resident:
        return jsonify({"error": "Resident not found"}), 404

    event = get_event_by_id(data['event_id'])
    if not event:
        return jsonify({"error": "Event not found"}), 404

    try:
        new_permission = create_permission(data)
        return jsonify({"message": "Permission created successfully", "permission_id": new_permission.permission_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@permissions_bp.route('/calendar_events_permissions/<int:permission_id>', methods=['PUT'])
def update_permission_route(permission_id):
    permission = get_permission_by_id(permission_id)
    if not permission:
        return jsonify({"error": "Permission not found"}), 404

    data = request.json
    updated_permission = update_permission(permission, data)
    return jsonify({"message": "Permission updated successfully"}), 200

@permissions_bp.route('/calendar_events_permissions/<int:permission_id>', methods=['DELETE'])
def delete_permission_route(permission_id):
    permission = get_permission_by_id(permission_id)
    if not permission:
        return jsonify({"error": "Permission not found"}), 404

    delete_permission(permission)
    return jsonify({"message": "Permission deleted successfully"}), 200
