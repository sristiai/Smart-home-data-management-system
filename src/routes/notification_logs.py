print("Entering notification logs route")
from flask import Blueprint, request, jsonify
from src.controllers.residents_controller import get_resident_by_id
from src.models.notification_logs_model import NotificationLog
from src.controllers.house_controller import get_house_by_id
from src.controllers.notification_logs_controller import  (
    get_all_notification_logs,
    get_notification_logs_by_resident,
    create_notification_log,
    update_notification_log,
    delete_notification_log
)

notification_logs_bp = Blueprint('notification_logs', __name__)


@notification_logs_bp.route('/notification_logs', methods=['GET'])
def get_logs():
    logs = get_all_notification_logs()
    results = [
        {
            "notification_id": log.notification_id,
            "house_id": log.house_id,
            "notification_type": log.notification_type,
            "message": log.message,
            "notification_channel": log.notification_channel,
            "timestamp": log.timestamp,
            "status": log.status
        }
        for log in logs
    ]
    return jsonify(results), 200

@notification_logs_bp.route('/notification_logs/<int:resident_id>', methods=['GET'])
def get_logs_by_resident(resident_id):
    logs = get_logs_by_resident(resident_id)
    if not logs:
        return jsonify({"error": "No logs found for this resident"}), 404

    results = [
        {
            "notification_id": log.notification_id,
            "house_id": log.house_id,
            "notification_type": log.notification_type,
            "message": log.message,
            "notification_channel": log.notification_channel,
            "timestamp": log.timestamp,
            "status": log.status
        }
        for log in logs
    ]
    return jsonify(results), 200

@notification_logs_bp.route('/notification_logs', methods=['POST'])
def create_log():
    data = request.json
    required_fields = ['house_id', 'notification_type', 'message', 'notification_channel', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field '{field}'"}), 400

    try:
        new_log = create_notification_log(data)
        return jsonify({"message": "Log created successfully", "notification_id": new_log.notification_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@notification_logs_bp.route('/notification_logs/<int:notification_id>', methods=['PUT'])
def update_log(notification_id):
    log = NotificationLog.query.get(notification_id)
    if not log:
        return jsonify({"error": "Notification log not found"}), 404
    data = request.json
    updated_log = update_notification_log(log, data)
    return jsonify({"message": "Log updated successfully"}), 200

@notification_logs_bp.route('/notification_logs/<int:notification_id>', methods=['DELETE'])
def delete_log(notification_id):
    log = NotificationLog.query.get(notification_id)
    if not log:
        return jsonify({"error": "Notification log not found"}), 404

    delete_notification_log(log)
    return jsonify({"message": "Log deleted successfully"}), 200
