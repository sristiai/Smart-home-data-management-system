from flask import Blueprint, jsonify
import jwt
import datetime
from src.models.db import db
from sqlalchemy import text

auth_bp = Blueprint('auth', __name__)


# Fixed secret key for encoding/decoding JWT tokens
secret_key = '3c1a5f1d9c624fe2b8d4c2e4fa1c67dd8e4c1234a8fca9456bfbc43217d9e2a3'

@auth_bp.route('/generate-token/<int:user_id>', methods=['GET'])
def generate_token(user_id):
    """
    Generate a JWT token for a specific user ID by querying PostgreSQL.
    """
    # Query PostgreSQL to get resident_id and house_id
    query = text(
        """
        SELECT r.resident_id, r.house_id
        FROM residents r
        INNER JOIN users u ON r.user_id = u.user_id
        WHERE u.user_id = :user_id
        """
    )

    result = db.session.execute(query, {"user_id": user_id}).fetchone()
    print("Query Result:", result)

    if not result:
        return jsonify({"error": "User or resident data not found"}), 404

    # Prepare the payload for the token
    payload = {
        "resident_id": str(result.resident_id),  # Convert to string for MongoDB compatibility
        "house_id": str(result.house_id),       # Convert to string
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    # Encode the JWT token using the fixed secret key
    token = jwt.encode(payload, secret_key, algorithm='HS256')

    return jsonify({"token": token})
