import json
from datetime import datetime, timedelta
from enum import Enum
import uuid

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
    
    def authenticate(self, provided_password):
        return self.password == provided_password
    
    def update_profile(self, new_info):
        self.__dict__.update(new_info)

class Resident(User):
    def submit_complaint(self, title, description, category, urgency):
        complaint = Complaint(title, description, category, urgency, self.user_id)
        notification = Notification(f"New complaint submitted: {title}", "NEW_COMPLAINT")
        notification.send()
        return complaint
    
    def upload_evidence(self, complaint, file_name, file_type, file_size):
        attachment = Attachment(file_name, file_type, file_size)
        complaint.add_attachment(attachment)
        return attachment
    
    def track_complaint(self, complaint):
        return complaint.status
    
    def review_resolution(self, complaint):
        # Checking if complaint is resolved
        return complaint.status == ComplaintStatus.RESOLVED
    
    def is_satisfied(self, resolution_quality):
        # Return True or False based on resident's satisfaction
        return resolution_quality >= 3  # 3 out of 5 as minimum satisfaction threshold
    
    def request_further_action(self, complaint, additional_info):
        complaint.request_additional_action(additional_info)
        notification = Notification(f"Further action requested for complaint: {complaint.title}", "ACTION_REQUESTED")
        notification.send()
        return True
    
    def provide_feedback(self, complaint, rating, comment, satisfaction_level, request_further_action=False):
        feedback = Feedback(rating, comment, satisfaction_level, request_further_action)
        complaint.receive_feedback(feedback)
        notification = Notification(f"New feedback received for complaint: {complaint.title}", "FEEDBACK_RECEIVED")
        notification.send()
        return feedback

class MunicipalOfficial(User):
    def handle_escalated_complaint(self, complaint):
        complaint.status = ComplaintStatus.IN_PROGRESS
        notification = Notification(f"Municipal handling of complaint: {complaint.title}", "MUNICIPAL_HANDLING")
        notification.send()
    
    def coordinate_with_barangay(self, complaint, barangay_captain):
        message = Message(self, barangay_captain, f"Coordinating about complaint: {complaint.title}")
        message.send()
        return "Coordinating with Barangay."

class BarangayCaptain(User):
    def review_escalated_issue(self, complaint):
        # Review the escalated issue
        complaint.add_review_note(f"Reviewed by captain {self.name} on {datetime.now().isoformat()}")
        return True
    
    def requires_municipal_escalation(self, complaint):
        # Logic to determine if municipal escalation is needed
        return complaint.urgency_level in [UrgencyLevel.HIGH, UrgencyLevel.CRITICAL]
    
    def escalate_to_municipal(self, complaint, municipal_official):
        complaint.status = ComplaintStatus.ESCALATED
        message = Message(self, municipal_official, f"Escalating complaint: {complaint.title}")
        message.send()
        notification = Notification(f"Complaint escalated to municipal level: {complaint.title}", "ESCALATED_TO_MUNICIPAL")
        notification.send()
        return True
    
    def allocate_resources(self, complaint, resources):
        complaint.allocated_resources = resources
        notification = Notification(f"Resources allocated for complaint: {complaint.title}", "RESOURCES_ALLOCATED")
        notification.send()
        return f"Resources allocated: {resources}"

class BarangayOfficer(User):
    def receive_complaint(self, complaint):
        complaint.received = True
        notification = Notification(f"Complaint received: {complaint.title}", "COMPLAINT_RECEIVED")
        notification.send()
        return True
    
    def verify_complaint(self, complaint):
        complaint.verified = True
        return True
    
    def assess_urgency(self, complaint):
        # Additional logic could adjust urgency based on verification
        return complaint.urgency_level
    
    def requires_escalation(self, complaint):
        # Logic to determine if captain escalation is needed
        return complaint.urgency_level in [UrgencyLevel.HIGH, UrgencyLevel.CRITICAL]
    
    def process_complaint(self, complaint):
        complaint.status = ComplaintStatus.IN_PROGRESS
        # Set estimated resolution time based on urgency
        if complaint.urgency_level == UrgencyLevel.LOW:
            days = 14
        elif complaint.urgency_level == UrgencyLevel.MEDIUM:
            days = 7
        elif complaint.urgency_level == UrgencyLevel.HIGH:
            days = 3
        else:  # CRITICAL
            days = 1
        
        complaint.estimated_resolution_time = (datetime.now() + timedelta(days=days)).isoformat()
        return True
    
    def update_status(self, complaint, status):
        complaint.status = status
        notification = Notification(f"Complaint status updated to {status.value}: {complaint.title}", "STATUS_UPDATED")
        notification.send()
        return True
    
    def resolve_issue(self, complaint, resolution_details):
        complaint.resolution_details = resolution_details
        complaint.resolution_date = datetime.now().isoformat()
        complaint.status = ComplaintStatus.RESOLVED
        notification = Notification(f"Complaint resolved: {complaint.title}", "COMPLAINT_RESOLVED")
        notification.send()
        return True
    
    def document_resolution(self, complaint):
        documentation = f"Resolution for complaint {complaint.complaint_id}: {complaint.resolution_details}"
        complaint.resolution_documentation = documentation
        return documentation
    
    def handle_feedback(self, feedback, complaint):
        if feedback.request_further_action:
            complaint.status = ComplaintStatus.IN_PROGRESS
            notification = Notification(f"Further action required for complaint: {complaint.title}", "FURTHER_ACTION")
            notification.send()
        return True

class Complaint:
    def __init__(self, title, description, category, urgency, resident_id):
        self.complaint_id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.category = category
        self.date_submitted = datetime.now().isoformat()
        self.status = ComplaintStatus.PENDING
        self.urgency_level = urgency
        self.estimated_resolution_time = None
        self.resolution_details = None
        self.resolution_date = None
        self.resolution_documentation = None
        self.attachments = []
        self.feedback = None
        self.resident_id = resident_id
        self.received = False
        self.verified = False
        self.allocated_resources = None
        self.review_notes = []
        self.additional_action_requests = []

    def update_status(self, status):
        self.status = status
    
    def escalate(self):
        self.status = ComplaintStatus.ESCALATED
    
    def generate_tracking_id(self):
        return f"C-{self.complaint_id[:8]}"
    
    def add_attachment(self, attachment):
        self.attachments.append(attachment)
    
    def receive_feedback(self, feedback):
        self.feedback = feedback
    
    def add_review_note(self, note):
        self.review_notes.append(note)
    
    def request_additional_action(self, additional_info):
        self.additional_action_requests.append({
            "date_requested": datetime.now().isoformat(),
            "details": additional_info
        })
        self.status = ComplaintStatus.IN_PROGRESS  # Reopen the complaint

class Attachment:
    def __init__(self, file_name, file_type, file_size):
        self.attachment_id = str(uuid.uuid4())
        self.file_name = file_name
        self.file_type = file_type
        self.file_size = file_size
        self.upload_date = datetime.now().isoformat()
        self.uploaded = True

class Feedback:
    def __init__(self, rating, comment, satisfaction_level, request_further_action):
        self.feedback_id = str(uuid.uuid4())
        self.rating = rating
        self.comment = comment
        self.date_submitted = datetime.now().isoformat()
        self.satisfaction_level = satisfaction_level
        self.request_further_action = request_further_action

class Notification:
    def __init__(self, content, notification_type):
        self.notification_id = str(uuid.uuid4())
        self.content = content
        self.timestamp = datetime.now().isoformat()
        self.is_read = False
        self.type = notification_type

    def mark_as_read(self):
        self.is_read = True
    
    def send(self):
        # Logic to send notification would go here
        # For now, just print the notification
        print(f"NOTIFICATION: {self.content}")
        return True

class Message:
    def __init__(self, sender, receiver, content):
        self.message_id = str(uuid.uuid4())
        self.content = content
        self.timestamp = datetime.now().isoformat()
        self.sender = sender
        self.receiver = receiver
        self.is_read = False
    
    def mark_as_read(self):
        self.is_read = True
    
    def send(self):
        # Logic to send message would go here
        # For now, just print the message
        print(f"MESSAGE from {self.sender.name} to {self.receiver.name}: {self.content}")
        return True

# Example demonstrating the full complaint flow
def demonstrate_complaint_flow():
    # Create users
    resident = Resident(1, "John Doe", "123456789", "john@example.com", "password")
    officer = BarangayOfficer(2, "Officer Smith", "987654321", "smith@barangay.gov", "officer123")
    captain = BarangayCaptain(3, "Captain Johnson", "555123456", "johnson@barangay.gov", "captain456")
    municipal = MunicipalOfficial(4, "Director Williams", "555987654", "williams@municipal.gov", "director789")
    
    # Step 1: Resident submits complaint
    print("\n=== Resident Submits Complaint ===")
    complaint = resident.submit_complaint(
        "Drainage Issue", 
        "The storm drain on Main St is clogged causing flooding during rain", 
        "Infrastructure", 
        UrgencyLevel.HIGH
    )
    
    # Step 2: Resident uploads evidence
    print("\n=== Resident Uploads Evidence ===")
    attachment = resident.upload_evidence(complaint, "flood_photo.jpg", "image/jpeg", 1024)
    
    # Step 3: Officer receives complaint
    print("\n=== Officer Receives Complaint ===")
    officer.receive_complaint(complaint)
    
    # Step 4: Officer verifies complaint
    print("\n=== Officer Verifies Complaint ===")
    officer.verify_complaint(complaint)
    
    # Step 5: Officer assesses urgency
    print("\n=== Officer Assesses Urgency ===")
    urgency = officer.assess_urgency(complaint)
    print(f"Assessed urgency: {urgency.value}")
    
    # Step 6: Check if escalation is required
    print("\n=== Officer Checks If Escalation Is Required ===")
    if officer.requires_escalation(complaint):
        print("Complaint requires escalation to Barangay Captain")
        
        # Step 7a: Captain reviews escalated issue
        print("\n=== Captain Reviews Escalated Issue ===")
        captain.review_escalated_issue(complaint)
        
        # Step 8a: Check if municipal escalation is required
        print("\n=== Captain Checks If Municipal Escalation Is Required ===")
        if captain.requires_municipal_escalation(complaint):
            print("Complaint requires escalation to Municipal level")
            
            # Step 9a: Escalate to municipal
            print("\n=== Captain Escalates to Municipal ===")
            captain.escalate_to_municipal(complaint, municipal)
            
            # Step 10a: Municipal handles the complaint
            print("\n=== Municipal Handles Complaint ===")
            municipal.handle_escalated_complaint(complaint)
            municipal.coordinate_with_barangay(complaint, captain)
        
        # Step 11a: Captain allocates resources
        print("\n=== Captain Allocates Resources ===")
        captain.allocate_resources(complaint, "2 maintenance workers, drain cleaning equipment")
    else:
        # Step 7b: Officer processes complaint
        print("\n=== Officer Processes Complaint ===")
        officer.process_complaint(complaint)
    
    # Step 8b: Resident tracks complaint
    print("\n=== Resident Tracks Complaint ===")
    status = resident.track_complaint(complaint)
    print(f"Current status: {status.value}")
    
    # Step 9b: Officer updates status
    print("\n=== Officer Updates Status ===")
    officer.update_status(complaint, ComplaintStatus.IN_PROGRESS)
    
    # Step 10b: Officer resolves issue
    print("\n=== Officer Resolves Issue ===")
    officer.resolve_issue(complaint, "Drain cleared of debris and tested with water flow")
    
    # Step 11b: Officer documents resolution
    print("\n=== Officer Documents Resolution ===")
    documentation = officer.document_resolution(complaint)
    
    # Step 12: Resident reviews resolution
    print("\n=== Resident Reviews Resolution ===")
    is_resolved = resident.review_resolution(complaint)
    print(f"Is complaint resolved? {is_resolved}")
    
    # Step 13: Resident decides if satisfied
    print("\n=== Resident Decides If Satisfied ===")
    satisfaction_rating = 4  # On a scale of 1-5
    is_satisfied = resident.is_satisfied(satisfaction_rating)
    
    if not is_satisfied:
        # Step 14a: Resident requests further action
        print("\n=== Resident Requests Further Action ===")
        resident.request_further_action(complaint, "The drain is still partially clogged")
    else:
        # Step 14b: Resident provides feedback
        print("\n=== Resident Provides Feedback ===")
        feedback = resident.provide_feedback(
            complaint, 
            satisfaction_rating, 
            "Good job on resolving this quickly", 
            SatisfactionLevel.SATISFIED
        )
        
        # Step 15: Officer handles feedback
        print("\n=== Officer Handles Feedback ===")
        officer.handle_feedback(feedback, complaint)
    
    # Return the final state of the complaint for inspection
    return complaint

# Run the demonstration
if __name__ == "__main__":
    final_complaint = demonstrate_complaint_flow()
    print("\n=== Final Complaint State ===")
    print(json.dumps(final_complaint.__dict__, indent=4, default=lambda o: o.value if hasattr(o, 'value') else str(o)))