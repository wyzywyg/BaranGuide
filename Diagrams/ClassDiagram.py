import json
from datetime import datetime
from enum import Enum

class ComplaintStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "InProgress"
    RESOLVED = "Resolved"
    ESCALATED = "Escalated"

class UrgencyLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class SatisfactionLevel(Enum):
    SATISFIED = "Satisfied"
    NEUTRAL = "Neutral"
    UNSATISFIED = "Unsatisfied"

class User:
    def __init__(self, user_id, name, contact_info, email, password):
        self.user_id = user_id
        self.name = name
        self.contact_info = contact_info
        self.email = email
        self.password = password

    def authenticate(self):
        return True  # Placeholder for authentication logic

    def update_profile(self, new_info):
        self.__dict__.update(new_info)

class Resident(User):
    def submit_complaint(self, title, description, category, urgency):
        return Complaint(title, description, category, urgency)

class MunicipalOfficial(User):
    def handle_escalated_complaint(self, complaint):
        complaint.status = ComplaintStatus.ESCALATED

class BarangayCaptain(User):
    def escalate_complaint(self, complaint):
        complaint.status = ComplaintStatus.ESCALATED

class BarangayOfficer(User):
    def review_complaint(self, complaint):
        complaint.status = ComplaintStatus.IN_PROGRESS

class Complaint:
    def __init__(self, title, description, category, urgency):
        self.complaint_id = id(self)
        self.title = title
        self.description = description
        self.category = category
        self.date_submitted = datetime.now().isoformat()
        self.status = ComplaintStatus.PENDING
        self.urgency_level = urgency
        self.estimated_resolution_time = None

    def update_status(self, status):
        self.status = status

    def escalate(self):
        self.status = ComplaintStatus.ESCALATED

class Attachment:
    def __init__(self, file_name, file_type, file_size):
        self.attachment_id = id(self)
        self.file_name = file_name
        self.file_type = file_type
        self.file_size = file_size
        self.upload_date = datetime.now().isoformat()

class Feedback:
    def __init__(self, rating, comment, satisfaction_level):
        self.feedback_id = id(self)
        self.rating = rating
        self.comment = comment
        self.date_submitted = datetime.now().isoformat()
        self.satisfaction_level = satisfaction_level

class Notification:
    def __init__(self, content, notification_type):
        self.notification_id = id(self)
        self.content = content
        self.timestamp = datetime.now().isoformat()
        self.is_read = False
        self.type = notification_type

    def mark_as_read(self):
        self.is_read = True

class Message:
    def __init__(self, sender, receiver, content):
        self.message_id = id(self)
        self.content = content
        self.timestamp = datetime.now().isoformat()
        self.sender = sender
        self.receiver = receiver

    def send(self):
        return True  # Placeholder for send logic

# Example Usage:
resident = Resident(1, "John Doe", "123456789", "john@example.com", "password")
complaint = resident.submit_complaint("Noise Complaint", "Loud music at night", "Noise", UrgencyLevel.HIGH)
print(json.dumps(complaint.__dict__, indent=4, default=str))