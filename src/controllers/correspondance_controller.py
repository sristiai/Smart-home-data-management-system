from flask import jsonify, request, abort
from functools import wraps
from src.services.correspondance_service import CorrespondenceService
import jwt


class CorrespondenceController:
    def __init__(self):
        self.service = CorrespondenceService()

    # Mocked function for verifying tokens
    def verify_token(self, token):
        try:
            return jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return None

    # Authentication decorator
    def require_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                abort(401, description="Missing or invalid token")

            token = auth_header.split(' ')[1]
            user = self.verify_token(token)
            if not user:
                abort(401, description="Invalid token")

            request.user = user  # Attach the decoded user payload to the request
            return f(*args, **kwargs)
        return decorated

    # Create correspondence endpoint
    def create_correspondence(self):
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

        correspondence_id = self.service.create_correspondence(
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

    # Retrieve correspondence list endpoint
    def get_correspondence_list(self):
        resident_id = request.user['resident_id']
        correspondence_type = request.args.get('type')  # Optional query parameter

        correspondence_list = self.service.get_correspondence_list(
            resident_id=resident_id,
            type_=correspondence_type
        )

        return jsonify(correspondence_list)

    # Mark correspondence as read endpoint
    def mark_correspondence_read(self, correspondence_id):
        resident_id = request.user['resident_id']

        success = self.service.mark_correspondence_read(
            correspondence_id=correspondence_id,
            resident_id=resident_id
        )

        if not success:
            abort(404, description="Correspondence not found or access denied")

        return jsonify({"message": "Marked as read"})

    # Retrieve correspondence detail endpoint
    def get_correspondence_detail(self, correspondence_id):
        resident_id = request.user['resident_id']

        correspondence = self.service.get_correspondence_detail(
            correspondence_id=correspondence_id,
            resident_id=resident_id
        )

        if not correspondence:
            abort(404, description="Correspondence not found or access denied")

        return jsonify(correspondence)
