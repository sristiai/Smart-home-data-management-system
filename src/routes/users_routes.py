print("entering user routes")
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from src.controllers.users_controller import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user
)

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def route_get_users():
    users = get_all_users()
    results = [
        {
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'birth_date': user.birth_date,
            'created_at': user.created_at,
        }
        for user in users
    ]
    return jsonify(results), 200


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def route_get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    response = {
        'user_id': user.user_id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'birth_date': user.birth_date,
        'created_at': user.created_at,
    }
    return jsonify(response), 200


@user_bp.route('/users', methods=['POST'])
def route_create_user():
    data = request.json
    required_fields = ['first_name', 'last_name', 'username', 'email', 'password_hash', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field '{field}'"}), 400

    try:
        new_user = create_user(data)
    except IntegrityError:
        return jsonify({"error": "Username or email already exists"}), 400

    return jsonify({
        "message": "User created successfully",
        "user_id": new_user.user_id
    }), 201


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def route_update_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    updated_user = update_user(user, data)
    return jsonify({"message": "User updated"}), 200


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def route_delete_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    delete_user(user)
    return jsonify({"message": "User deleted"}), 200
