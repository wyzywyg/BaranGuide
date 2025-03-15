import json
from datetime import date
from enum import Enum




# ----- Enums -----
class ComplaintStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
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




# ----- Helper Functions -----
def custom_serializer(obj):
    """Convert objects to JSON-serializable format"""
    if isinstance(obj, (Enum, date)):
        return obj.value if isinstance(obj, Enum) else obj.isoformat()
    return obj.__dict__




def generate_id(cls):
    """Generic ID generator for any class"""
    if not hasattr(cls, "_id_counter"):
        cls._id_counter = 1
    id_value = cls._id_counter
    cls._id_counter += 1
    return id_value




# ----- User Classes -----
class User:
    def __init__(self, userID, name, contactInfo, email, password):
        self.userID = userID
        self.name = name
        self.contactInfo = contactInfo
        self.email = email
        self.password = password  # Should be hashed in production




class Resident(User):
    def submit_complaint(self, title, description, category, urgency):
        return Complaint(title, description, category, urgency, self.userID)




# ----- Complaint System -----
class Complaint:
    def __init__(self, title, description, category, urgency, resident_id):
        self.complaintID = generate_id(Complaint)
        self.title = title
        self.description = description
        self.category = category
        self.urgencyLevel = urgency
        self.dateSubmitted = date.today()
        self.status = ComplaintStatus.PENDING
        self.feedbacks = []
        self.residentID = resident_id


    def update_status(self, status):
        self.status = status


    def escalate(self):
        self.status = ComplaintStatus.ESCALATED


    def add_feedback(self, feedback):
        self.feedbacks.append(feedback)




# ----- Feedback -----
class Feedback:
    def __init__(self, rating, comment, satisfaction):
        self.feedbackID = generate_id(Feedback)
        self.rating = rating
        self.comment = comment
        self.dateSubmitted = date.today()
        self.satisfactionLevel = satisfaction




# ----- Example Usage -----
if __name__ == "__main__":
    resident = Resident(1, "John Doe", "123-456-789", "john@example.com", "password123")
    complaint = resident.submit_complaint("Noise Complaint", "Loud music at night", "Noise", UrgencyLevel.HIGH)
   
    feedback = Feedback(4, "Resolved, but took too long", SatisfactionLevel.NEUTRAL)
    complaint.add_feedback(feedback)


    print("Complaint:", json.dumps(complaint, default=custom_serializer, indent=4))
    print("\nFeedback:", json.dumps(feedback, default=custom_serializer, indent=4))



