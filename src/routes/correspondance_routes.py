# from flask import Blueprint
# from src.controllers.correspondance_controller import CorrespondenceController
# # Create a Blueprint for correspondence routes
# correspondence_bp = Blueprint('correspondence', __name__)
#
# # Define routes
# @correspondence_bp.route('/correspondence', methods=['GET'])
# def get_correspondence():
#     return CorrespondenceController.get_all_correspondence()
#
#
# @correspondence_bp.route('/correspondence', methods=['POST'])
# def add_correspondence():
#     return CorrespondenceController.add_correspondence()

from flask import Blueprint, jsonify, request, abort
from functools import wraps
from src.services.correspondance_service import CorrespondenceService

import jwt
from jwt import InvalidTokenError


# Create a Flask Blueprint for correspondence routes
correspondence_bp = Blueprint('correspondence', __name__)
service = CorrespondenceService()

# Mocked function for verifying tokens
def verify_token(token):
    try:
        secret_key = '3c1a5f1d9c624fe2b8d4c2e4fa1c67dd8e4c1234a8fca9456bfbc43217d9e2a3'
        decoded =  jwt.decode(token, secret_key, algorithms=['HS256'])
        print(decoded)
        return decoded

    except InvalidTokenError:
        print("Invalid token ")
        return None


# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            abort(401, description="Missing or invalid token")

        token = auth_header.split(' ')[1]
        user = verify_token(token)
        if not user:
            abort(401, description="Invalid token")

        request.user = user  # Attach the decoded user payload to the request
        return f(*args, **kwargs)
    return decorated


# Route to create a correspondence
@correspondence_bp.route('/api/correspondence', methods=['POST'])
@require_auth
def create_correspondence():
    data = request.json
    required_fields = ['title', 'content', 'type', 'residents_access']

    # Validate required fields
    if not all(field in data for field in required_fields):
        abort(400, description="Missing required fields")

    sender_data = {
        'resident_id': request.user['resident_id'],
        'name': request.user.get('name', 'System'),
        'house_id': request.user['house_id']
    }

    correspondence_id = service.create_correspondence(
        title=data['title'],
        content=data['content'],
        sender_data=sender_data,
        type_=data['type'],
        residents_access=data['residents_access'],
        due_date=data.get('due_date'),
        privacy_level=data.get('privacy_level', 'private'),
        source=data.get('source', 'resident')
    )

    return jsonify({"message": "Correspondence created", "id": correspondence_id}), 201


# Route to retrieve correspondence for a resident
@correspondence_bp.route('/api/correspondence', methods=['GET'])
@require_auth
def get_correspondence_list():
    resident_id = request.user['resident_id']
    print(f"Fetching correspondence for resident_id: {resident_id}")
    correspondence_type = request.args.get('type')  # Optional query parameter

    correspondence_list = service.get_correspondence_list(
        resident_id=resident_id,
        type_=correspondence_type
    )



    return jsonify(correspondence_list)


# Route to mark correspondence as read
@correspondence_bp.route('/api/correspondence/<correspondence_id>/mark-read', methods=['POST'])
@require_auth
def mark_correspondence_read(correspondence_id):
    resident_id = request.user['resident_id']

    success = service.mark_correspondence_read(
        correspondence_id=correspondence_id,
        resident_id=resident_id
    )

    if not success:
        abort(404, description="Correspondence not found or access denied")

    return jsonify({"message": "Marked as read"})


# Route to retrieve correspondence details
@correspondence_bp.route('/api/correspondence/<correspondence_id>', methods=['GET'])
@require_auth
def get_correspondence_detail(correspondence_id):
    resident_id = request.user['resident_id']

    correspondence = service.get_correspondence_detail(
        correspondence_id=correspondence_id,
        resident_id=resident_id
    )

    if not correspondence:
        abort(404, description="Correspondence not found or access denied")

    return jsonify(correspondence)

