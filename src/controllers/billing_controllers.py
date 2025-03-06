from flask import Blueprint, request, jsonify
from src.services.billing_service import BillingService

billing_bp = Blueprint("billing", __name__)
billing_service = BillingService()

@billing_bp.route("/api/generate-bill", methods=["POST"])
def generate_bill():
    """
    Generate a bill for a house.
    """
    data = request.json
    house_id = data["house_id"]
    resident_id = data["resident_id"]
    month = data["month"]  # Format: YYYY-MM

    result = billing_service.generate_bill(house_id, resident_id, month)
    return jsonify(result)
