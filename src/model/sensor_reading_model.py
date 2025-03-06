from mongoengine import Document, EmbeddedDocument, fields


# Embedded document for metadata in SensorReadings
class MetaData(EmbeddedDocument):
    house_id = fields.IntField(required=True)  # ID of the house
    sensor_id = fields.IntField(required=True)  # Unique ID for the specific sensor
    sensor_type = fields.StringField(required=True)  # Type of sensor (e.g., heating)
    location = fields.StringField()  # Location of the sensor (optional)
    unit = fields.StringField(required=True)  # Unit of measurement


# SensorReadings model
class SensorReadings(Document):
    timestamp = fields.DateTimeField(required=True)  # Time of the sensor reading
    measurement = fields.FloatField(required=True)  # Sensor reading value
    metadata = fields.EmbeddedDocumentField(MetaData, required=True)  # Metadata of the sensor reading

    # Metadata for MongoDB collection
    meta = {
        'collection': 'sensor_readings',  # Collection name in MongoDB
        'indexes': [
            {'fields': ['metadata.house_id']},  # Index on house_id in metadata
            {'fields': ['metadata.sensor_id']},  # Index on sensor_id in metadata
            {'fields': ['timestamp']}          # Index on timestamp
        ]
    }
