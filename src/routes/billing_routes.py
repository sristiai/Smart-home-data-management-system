from flask import Blueprint
from src.controllers.billing_controller import BillingController

billing_bp = Blueprint("billing", __name__)
controller = BillingController()

# Route to generate a bill
@billing_bp.route("/api/generate-bill", methods=["POST"])
def generate_bill():
    return controller.generate_bill()
