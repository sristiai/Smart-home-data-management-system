from pymongo import MongoClient
from datetime import datetime, timedelta
import redis
from src.models.correspondance_model import Correspondence, Sender, ResidentAccess
from src.models.db import db  # For PostgreSQL access

class BillingService:
    def __init__(self):
        # MongoDB Connection
        self.mongo_client = MongoClient("mongodb://localhost:27017/")
        self.mongo_db = self.mongo_client["smart_home"]

        # Redis Connection
        self.redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)

    def aggregate_monthly_sensor_readings(self, house_id, sensor_type, month):
        """
        Aggregate sensor readings for a specific house and month.
        :param house_id: ID of the house
        :param sensor_type: Type of sensor (e.g., "electricity", "water")
        :param month: The month for which to aggregate (e.g., "2025-01")
        :return: Total measurement for the month
        """
        start_date = datetime.strptime(f"{month}-01", "%Y-%m-%d")
        end_date = start_date + timedelta(days=31)
        end_date = end_date.replace(day=1)

        pipeline = [
            {"$match": {
                "meta.house_id": house_id,
                "meta.sensor_type": sensor_type,
                "timestamp": {"$gte": start_date, "$lt": end_date}
            }},
            {"$group": {
                "_id": None,
                "total_measurement": {"$sum": "$measurement"}
            }}
        ]

        result = list(self.mongo_db.sensor_readings.aggregate(pipeline))
        return result[0]["total_measurement"] if result else 0

    def generate_monthly_bill(self, house_id, resident_id, month):
        """
        Generate a bill for a specific house and month, save it to Redis, and persist it in MongoDB.
        """
        # Step 1: Aggregate sensor readings
        electricity_usage = self.aggregate_monthly_sensor_readings(house_id, "electricity", month)
        water_usage = self.aggregate_monthly_sensor_readings(house_id, "water", month)

        # Define rates (e.g., $0.10 per kWh, $2 per cubic meter of water)
        electricity_rate = 0.10
        water_rate = 2.00

        # Calculate the total bill
        electricity_bill = electricity_usage * electricity_rate
        water_bill = water_usage * water_rate
        total_bill = electricity_bill + water_bill

        # Step 2: Save the bill in Redis
        redis_key = f"bill:{house_id}:{month}"
        bill_data = {
            "month": month,
            "house_id": house_id,
            "resident_id": resident_id,
            "electricity_bill": electricity_bill,
            "water_bill": water_bill,
            "total_bill": total_bill,
        }
        self.redis_client.set(redis_key, str(bill_data), ex=60 * 60 * 24 * 30)  # Cache for 30 days

        # Step 3: Persist the bill in MongoDB (Correspondence)
        sender = Sender(
            resident_id=str(resident_id),
            name="Utility Company",
            house_id=str(house_id)
        )
        access_list = [ResidentAccess(resident_id=str(resident_id), status="unread", viewed_at=None)]

        bill_content = f"Electricity: ${electricity_bill:.2f}, Water: ${water_bill:.2f}. Total: ${total_bill:.2f}."

        correspondence = Correspondence(
            title=f"Utility Bill - {month}",
            type="bill",
            content=bill_content,
            timestamp=datetime.utcnow(),
            sender=sender,
            due_date=datetime.strptime(f"{month}-31", "%Y-%m-%d"),
            status="unread",
            privacy_level="private",
            residents_access=access_list,
            source="utility_company"
        )
        correspondence.save()

        # Step 4: Log Notification in PostgreSQL
        notification_message = f"A new bill has been generated for {month}. Total: ${total_bill:.2f}."
        db.session.execute(
            """
            INSERT INTO notification_logs (house_id, notification_type, message, notification_channel)
            VALUES (:house_id, 'electricity', :message, 'mail')
            """,
            {"house_id": house_id, "message": notification_message}
        )
        db.session.commit()

        return {"message": "Bill generated successfully", "total": total_bill}
