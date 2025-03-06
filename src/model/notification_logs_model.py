# my_smart_home_app/src/models/notification_log.py
print("Entering notification log model")
from datetime import datetime
from src.models.db import db

class NotificationLog(db.Model):
    __tablename__ = 'notification_logs'

    notification_id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.house_id'), nullable=False)  # Add house_id
    notification_type = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)
    notification_channel = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50))  # e.g., 'sent', 'pending', 'failed'

    # Relationship
    house = db.relationship('House', back_populates='notification_logs')

    def __repr__(self):
        return f"<NotificationLog id={self.notification_id} type={self.notification_type} status={self.status}>"

from src.models.db import db

# class NotificationLog(db.Model):
#     __tablename__ = 'notification_logs'
#
#     notification_id = db.Column(db.Integer, primary_key=True)
#     house_id = db.Column(db.Integer, nullable=False)  # Linked to a house
#     notification_type = db.Column(
#         db.String(50), nullable=False,
#         check=db.CheckConstraint("notification_type IN ('electricity', 'water', 'heat')")
#     )
#     message = db.Column(db.Text, nullable=False)
#     notification_channel = db.Column(
#         db.String(50), nullable=False,
#         check=db.CheckConstraint("notification_channel IN ('sms', 'mail')")
#     )
#     timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
#     status = db.Column(db.String(20), nullable=False, default='unread')
