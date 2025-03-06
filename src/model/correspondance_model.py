from mongoengine import Document, EmbeddedDocument, fields


# Embedded document for sender information
class Sender(EmbeddedDocument):
    resident_id = fields.StringField(required=True)  # Sender's ID
    name = fields.StringField(required=True)  # Sender's name or organization
    house_id = fields.StringField(required=True)  # ID of the sender's house


# Embedded document for resident access information
class ResidentAccess(EmbeddedDocument):
    resident_id = fields.StringField(required=True)  # Resident ID who has access
    status = fields.StringField(
        choices=['unread', 'read', 'archived'], default='unread'
    )  # Status of correspondence for the resident
    viewed_at = fields.DateTimeField()  # Timestamp when the resident viewed the correspondence


# Main Correspondence model
class Correspondence(Document):
    title = fields.StringField(required=True)  # Title of the correspondence
    type = fields.StringField(
        choices=['letter', 'advertisement', 'bill', 'government_letter'], required=True
    )  # Type of correspondence
    content = fields.StringField(required=True)  # Content of the correspondence
    timestamp = fields.DateTimeField(required=True)  # Date and time correspondence was sent
    sender = fields.EmbeddedDocumentField(Sender, required=True)  # Sender's information
    due_date = fields.DateTimeField()  # Relevant due date (e.g., for bills)
    status = fields.StringField(
        choices=['unread', 'read', 'archived'], default='unread'
    )  # Status of the correspondence
    privacy_level = fields.StringField(
        choices=['private', 'public', 'restricted'], default='private'
    )  # Privacy level of the correspondence
    residents_access = fields.EmbeddedDocumentListField(
        ResidentAccess
    )  # List of residents with access to the correspondence
    source = fields.StringField(
        choices=['government', 'utility_company', 'resident', 'other'],
        default='resident'
    )

    # Metadata for MongoDB collection
    meta = {
        'collection': 'correspondence',  # Collection name in MongoDB
        'indexes': [
            'timestamp',  # Index on timestamp for time-based queries
            'sender.house_id',  # Index on house_id for sender
            'residents_access.resident_id',
            'type'# Index for resident access
        ]
    }
