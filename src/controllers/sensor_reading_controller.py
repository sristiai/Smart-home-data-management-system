from flask import request, jsonify
from src.models.sensor_reading_model import SensorReadings, MetaData
from mongoengine.errors import ValidationError


class SensorReadingController:
    @staticmethod
    def get_all_sensor_readings():
        """Get all sensor readings or filter by house_id/sensor_id."""
        house_id = request.args.get('house_id')
        sensor_id = request.args.get('sensor_id')

        try:
            if house_id and sensor_id:
                readings = SensorReadings.objects(metadata__house_id=house_id, metadata__sensor_id=sensor_id)
            elif house_id:
                readings = SensorReadings.objects(metadata__house_id=house_id)
            elif sensor_id:
                readings = SensorReadings.objects(metadata__sensor_id=sensor_id)
            else:
                readings = SensorReadings.objects()

            # Convert QuerySet to a list of dictionaries and handle ObjectId serialization
            readings_data = [
                SensorReadingController._convert_objectid_to_str(reading.to_mongo().to_dict())
                for reading in readings
            ]

            return jsonify(readings_data), 200

        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def add_sensor_reading():
        """Add a new sensor reading."""
        try:
            data = request.get_json()
            meta_data = MetaData(
                house_id=data["metadata"]["house_id"],
                sensor_id=data["metadata"]["sensor_id"],
                sensor_type=data["metadata"]["sensor_type"],
                location=data["metadata"].get("location"),
                unit=data["metadata"]["unit"]
            )

            sensor_reading = SensorReadings(
                timestamp=data["timestamp"],
                measurement=data["measurement"],
                metadata=meta_data
            )
            sensor_reading.save()

            return {"message": "Sensor reading added successfully"}, 201

        except ValidationError as e:
            return {"error": str(e)}, 400

        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def _convert_objectid_to_str(data):
        """
        Recursively converts ObjectId fields in a dictionary to strings.
        """
        if isinstance(data, dict):
            return {k: SensorReadingController._convert_objectid_to_str(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [SensorReadingController._convert_objectid_to_str(v) for v in data]
        elif hasattr(data, "__str__"):
            return str(data)
        else:
            return data
