# src/controllers/notification_log_controller.py
print("Entering notification log controller")
from src.models.db import db
from src.models.notification_logs_model import NotificationLog
from sqlalchemy.orm import joinedload
from src.models.houses_model import House
from src.models.residents_model import Resident

def get_all_notification_logs():
    return NotificationLog.query.all()

def get_notification_logs_by_resident(resident_id):
    logs = (
        db.session.query(NotificationLog)
        .join(Resident, Resident.house_id == NotificationLog.house_id)
        .filter(Resident.resident_id == resident_id)
        .all()
    )
    return logs

def create_notification_log(data):
    log = NotificationLog(
        house_id=data['house_id'],
        notification_type=data['notification_type'],
        message=data['message'],
        notification_channel=data['notification_channel'],
        timestamp=data.get('timestamp'),
        status=data.get('status', 'unread')
    )
    db.session.add(log)
    db.session.commit()
    return log

def update_notification_log(log, data):
    if 'notification_type' in data:
        log.notification_type = data['notification_type']
    if 'message' in data:
        log.message = data['message']
    if 'notification_channel' in data:
        log.notification_channel = data['notification_channel']
    if 'status' in data:
        log.status = data['status']
    db.session.commit()
    return log

def delete_notification_log(log):
    db.session.delete(log)
    db.session.commit()