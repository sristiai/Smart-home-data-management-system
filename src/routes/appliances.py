print("Entering appliances route")
from flask import Blueprint, request, jsonify
from src.controllers.appliance_controller import (
    get_all_appliances,
    get_appliance_by_id,
    create_appliance,
    update_appliance,
    delete_appliance
)

appliances_bp = Blueprint('appliances', __name__)

@appliances_bp.route('/appliances', methods=['GET'])
def route_get_appliances():
    """Fetch all appliances."""
    appliances = get_all_appliances()
    results = [
        {
            'appliance_id': appliance.appliance_id,
            'house_id': appliance.house_id,
            'name': appliance.name,
            'status': appliance.status,
            'notify_on_change': appliance.notify_on_change,
            'created_at': appliance.created_at
        }
        for appliance in appliances
    ]
    return jsonify(results), 200

@appliances_bp.route('/appliances/<int:appliance_id>', methods=['GET'])
def route_get_appliance(appliance_id):
    """Fetch a specific appliance."""
    appliance = get_appliance_by_id(appliance_id)
    if not appliance:
        return jsonify({"error": "Appliance not found"}), 404

    response = {
        'appliance_id': appliance.appliance_id,
        'house_id': appliance.house_id,
        'name': appliance.name,
        'status': appliance.status,
        'notify_on_change': appliance.notify_on_change,
        'created_at': appliance.created_at
    }
    return jsonify(response), 200

@appliances_bp.route('/appliances', methods=['POST'])
def route_create_appliance():
    """Create a new appliance."""
    data = request.json
    required_fields = ['house_id', 'name']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field '{field}'"}), 400

    try:
        new_appliance = create_appliance(data)
        return jsonify({
            "message": "Appliance created successfully",
            "appliance_id": new_appliance.appliance_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@appliances_bp.route('/appliances/<int:appliance_id>', methods=['PUT'])
def route_update_appliance(appliance_id):
    """Update an appliance."""
    appliance = get_appliance_by_id(appliance_id)
    if not appliance:
        return jsonify({"error": "Appliance not found"}), 404

    data = request.json
    updated_appliance = update_appliance(appliance, data)
    return jsonify({"message": "Appliance updated successfully"}), 200

@appliances_bp.route('/appliances/<int:appliance_id>', methods=['DELETE'])
def route_delete_appliance(appliance_id):
    """Delete an appliance."""
    appliance = get_appliance_by_id(appliance_id)
    if not appliance:
        return jsonify({"error": "Appliance not found"}), 404

    delete_appliance(appliance)
    return jsonify({"message": "Appliance deleted successfully"}), 200
