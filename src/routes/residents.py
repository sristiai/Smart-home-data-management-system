# src/routes/residents.py
from flask import Blueprint, request, jsonify
from src.controllers.users_controller import get_user_by_id
from src.controllers.house_controller import get_house_by_id
from src.controllers.residents_controller import (
    get_all_residents,
    get_resident_by_id,
    create_resident,
    update_resident,
    delete_resident
)

resident_bp = Blueprint('residents', __name__)

@resident_bp.route('/residents', methods=['GET'])
def get_residents():
    residents = get_all_residents()
    results = [
        {
            "resident_id": resident.resident_id,
            "user_id": resident.user_id,
            "house_id": resident.house_id,
            "user_name": f"{user.first_name} {user.last_name}",
            "house_address": house.address,
            "move_in_date": resident.move_in_date,
            "move_out_date": resident.move_out_date
        }
        for resident, user, house in residents
    ]
    return jsonify({"message": "Residents fetched successfully", "data": results}), 200

@resident_bp.route('/residents/<int:resident_id>', methods=['GET'])
def get_resident(resident_id):
    """Fetch a specific resident by ID."""
    result = get_resident_by_id(resident_id)
    if not result:
        return jsonify({"error": "Resident not found"}), 404

    resident = result["resident"]
    user = result["user"]
    house = result["house"]

    response = {
        "resident_id": resident.resident_id,
        "user_id": resident.user_id,
        "user_name": f"{user.first_name} {user.last_name}",
        "house_id": resident.house_id,
        "house_address": house.address,
        "move_in_date": resident.move_in_date,
        "move_out_date": resident.move_out_date
    }
    return jsonify(response), 200

@resident_bp.route('/residents', methods=['POST'])
def create_resident_route():
    """Create a new resident."""
    data = request.json
    required_fields = ['user_id', 'house_id']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field '{field}'"}), 400

    # Validate house existence
    house = get_house_by_id(data['house_id'])
    if not house:
        return jsonify({"error": f"House with id {data['house_id']} does not exist"}), 400

    try:
        new_resident = create_resident(data)
        response = {
            "resident_id": new_resident.resident_id,
            "user_id": new_resident.user_id,
            "house_id": new_resident.house_id,
            "move_in_date": new_resident.move_in_date,
            "move_out_date": new_resident.move_out_date
        }
        return jsonify({"message": "Resident created successfully", "data": response}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@resident_bp.route('/residents/<int:resident_id>', methods=['PUT'])
def update_resident_route(resident_id):
    """Update an existing resident."""
    result = get_resident_by_id(resident_id)
    if not result:
        return jsonify({"error": "Resident not found"}), 404

    resident = result["resident"]  # Extract the Resident object
    data = request.json
    try:
        updated_resident = update_resident(resident, data)  # Pass only the Resident object
        response = {
            "resident_id": updated_resident.resident_id,
            "user_id": updated_resident.user_id,
            "house_id": updated_resident.house_id,
            "move_in_date": updated_resident.move_in_date,
            "move_out_date": updated_resident.move_out_date
        }
        return jsonify({"message": "Resident updated successfully", "data": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@resident_bp.route('/residents/<int:resident_id>', methods=['DELETE'])
def delete_resident_route(resident_id):
    """Delete a resident."""
    result = get_resident_by_id(resident_id)  # Get the dictionary containing resident, user, and house
    if not result:
        return jsonify({"error": "Resident not found"}), 404

    resident = result["resident"]  # Extract the Resident object

    try:
        delete_resident(resident)  # Pass only the Resident object to delete function
        return jsonify({"message": "Resident deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
