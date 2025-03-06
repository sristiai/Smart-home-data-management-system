from flask import Blueprint
from src.controllers.sensor_reading_controller import SensorReadingController

# Create a Blueprint for sensor reading routes
sensor_reading_bp = Blueprint('sensor_readings', __name__)

# Define routes
@sensor_reading_bp.route('/sensor_readings', methods=['GET'])
def get_sensor_readings():
    """Route to fetch all sensor readings or filter by house_id/sensor_id."""
    return SensorReadingController.get_all_sensor_readings()


@sensor_reading_bp.route('/sensor_readings', methods=['POST'])
def add_sensor_reading():
    """Route to add a new sensor reading."""
    return SensorReadingController.add_sensor_reading()
