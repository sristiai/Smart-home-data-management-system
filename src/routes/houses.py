print("Entering houses route")
from flask import Blueprint, request, jsonify
from src.controllers.users_controller import get_user_by_id 
from src.controllers.house_controller import (
    get_all_houses,
    get_house_by_id,
    create_house,
    update_house,
    delete_house
)

# Define a blueprint for house routes
houses_bp = Blueprint('houses', __name__)

@houses_bp.route('/houses', methods=['GET'])
def route_get_houses():
    houses = get_all_houses()
    results = [
        {
            'house_id': house.house_id,
            'user_id': house.user_id,
            'address': house.address,
            'created_at': house.created_at,
        }
        for house in houses
    ]
    return jsonify(results), 200


@houses_bp.route('/houses/<int:house_id>', methods=['GET'])
def route_get_house(house_id):
    house = get_house_by_id(house_id)
    if not house:
        return jsonify({"error": "House not found"}), 404

    response = {
        'house_id': house.house_id,
        'user_id': house.user_id,
        'address': house.address,
        'created_at': house.created_at,
    }
    return jsonify(response), 200


@houses_bp.route('/houses', methods=['POST'])
def route_create_house():
    data = request.json
    required_fields = ['user_id', 'address']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field '{field}'"}), 400

    # Check if the user_id exists
    user = get_user_by_id(data['user_id'])
    if not user:
        return jsonify({"error": f"User with id {data['user_id']} does not exist"}), 400

    try:
        new_house = create_house(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "message": "House created successfully",
        "house_id": new_house.house_id
    }), 201


@houses_bp.route('/houses/<int:house_id>', methods=['PUT'])
def route_update_house(house_id):
    house = get_house_by_id(house_id)
    if not house:
        return jsonify({"error": "House not found"}), 404

    data = request.json
    updated_house = update_house(house, data)
    return jsonify({"message": "House updated"}), 200


@houses_bp.route('/houses/<int:house_id>', methods=['DELETE'])
def route_delete_house(house_id):
    house = get_house_by_id(house_id)
    if not house:
        return jsonify({"error": "House not found"}), 404

    delete_house(house)
    return jsonify({"message": "House deleted"}), 200
