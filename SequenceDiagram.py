import json
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional

class ComplaintStatus(Enum):
    PENDING = "Pending"
    UNDER_REVIEW = "Under Review"
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

class ComplaintCategory(Enum):
    NOISE = "Noise"
    GARBAGE = "Garbage"
    INFRASTRUCTURE = "Infrastructure"
    SECURITY = "Security"
    OTHER = "Other"

class ComplaintType(Enum):
    SIMPLE = "Simple"
    COMPLEX = "Complex"

class ResolutionScope(Enum):
    BARANGAY = "Barangay"
    MUNICIPAL = "Municipal"

class User:
    def __init__(self, user_id: int, name: str, contact_info: str, email: str, password: str):
        self.user_id = user_id
        self.name = name
        self.contact_info = contact_info
        self.email = email
        self.password = password
    
    def authenticate(self) -> bool:
        return True  # Placeholder for authentication logic
    
    def update_profile(self, new_info: Dict):
        self.__dict__.update(new_info)

class Resident(User):
    def submit_complaint(self, title: str, description: str, category: ComplaintCategory, 
                         urgency: UrgencyLevel, system: 'BCCMSSystem') -> 'Complaint':
        """Submit a new complaint and receive a tracking ID"""
        complaint = Complaint(title, description, category, urgency, self)
        tracking_id = system.register_complaint(complaint)
        return tracking_id
    
    def submit_feedback(self, complaint: 'Complaint', rating: int, 
                       comment: str, satisfaction: SatisfactionLevel) -> 'Feedback':
        """Submit feedback for a resolved complaint"""
        feedback = Feedback(rating, comment, satisfaction)
        complaint.add_feedback(feedback)
        return feedback

class BarangayOfficer(User):
    def assess_priority(self, complaint: 'Complaint') -> None:
        """Review and assess the priority of a new complaint"""
        complaint.update_status(ComplaintStatus.UNDER_REVIEW)
    
    def determine_resolution_path(self, complaint: 'Complaint') -> None:
        """Determine if the complaint is simple or complex and how to resolve it"""
        # Logic to determine complaint type and resolution path
        if complaint.urgency_level in [UrgencyLevel.LOW, UrgencyLevel.MEDIUM]:
            complaint.set_type(ComplaintType.SIMPLE)
        else:
            complaint.set_type(ComplaintType.COMPLEX)
    
    def assign_task_directly(self, complaint: 'Complaint', personnel: 'Personnel') -> None:
        """Directly assign a simple complaint to personnel"""
        if complaint.complaint_type == ComplaintType.SIMPLE:
            complaint.assign_to(personnel)
    
    def escalate_complex_issue(self, complaint: 'Complaint', captain: 'BarangayCaptain') -> None:
        """Escalate a complex complaint to the Barangay Captain"""
        if complaint.complaint_type == ComplaintType.COMPLEX:
            complaint.update_status(ComplaintStatus.ESCALATED)
            captain.review_issue(complaint)

class BarangayCaptain(User):
    def review_issue(self, complaint: 'Complaint') -> None:
        """Review a complex complaint"""
        # Logic to review the complaint
        pass
    
    def decide_resolution_path(self, complaint: 'Complaint') -> None:
        """Decide how to resolve the complex complaint"""
        # Determine if it can be resolved within barangay or needs municipal authority
        if complaint.urgency_level == UrgencyLevel.CRITICAL:
            complaint.set_resolution_scope(ResolutionScope.MUNICIPAL)
        else:
            complaint.set_resolution_scope(ResolutionScope.BARANGAY)
    
    def assign_to_personnel(self, complaint: 'Complaint', personnel: 'Personnel') -> None:
        """Assign complaint to specific personnel for resolution"""
        if complaint.resolution_scope == ResolutionScope.BARANGAY:
            complaint.assign_to(personnel)
    
    def escalate_to_municipality(self, complaint: 'Complaint', municipality: 'Municipality') -> None:
        """Escalate the complaint to municipal level if needed"""
        if complaint.resolution_scope == ResolutionScope.MUNICIPAL:
            municipality.handle_escalated_complaint(complaint)

class Personnel(User):
    def execute_solution(self, complaint: 'Complaint') -> None:
        """Execute the solution for an assigned complaint"""
        # Logic to execute the solution
        complaint.update_status(ComplaintStatus.RESOLVED)

class Municipality(User):
    def handle_escalated_complaint(self, complaint: 'Complaint') -> None:
        """Handle a complaint escalated to municipal level"""
        # Logic to handle municipal level complaint
        pass
    
    def execute_solution(self, complaint: 'Complaint') -> None:
        """Execute solution for municipal level complaint"""
        complaint.update_status(ComplaintStatus.RESOLVED)

class Attachment:
    def __init__(self, file_name: str, file_type: str, file_size: int):
        self.attachment_id = id(self)
        self.file_name = file_name
        self.file_type = file_type
        self.file_size = file_size
        self.upload_date = datetime.now().isoformat()

class Feedback:
    def __init__(self, rating: int, comment: str, satisfaction_level: SatisfactionLevel):
        self.feedback_id = id(self)
        self.rating = rating
        self.comment = comment
        self.date_submitted = datetime.now().isoformat()
        self.satisfaction_level = satisfaction_level

class Notification:
    def __init__(self, content: str, notification_type: str, recipient: User):
        self.notification_id = id(self)
        self.content = content
        self.timestamp = datetime.now().isoformat()
        self.is_read = False
        self.type = notification_type
        self.recipient = recipient
    
    def mark_as_read(self) -> None:
        self.is_read = True

class Message:
    def __init__(self, sender: User, receiver: User, content: str):
        self.message_id = id(self)
        self.content = content
        self.timestamp = datetime.now().isoformat()
        self.sender = sender
        self.receiver = receiver
    
    def send(self) -> bool:
        return True  # Placeholder for send logic

class Complaint:
    def __init__(self, title: str, description: str, category: ComplaintCategory, 
                 urgency: UrgencyLevel, submitter: Resident):
        self.complaint_id = id(self)
        self.tracking_id = None  # Will be assigned by the system
        self.title = title
        self.description = description
        self.category = category
        self.date_submitted = datetime.now().isoformat()
        self.status = ComplaintStatus.PENDING
        self.urgency_level = urgency
        self.estimated_resolution_time = None
        self.submitter = submitter
        self.assigned_to = None
        self.complaint_type = None  # SIMPLE or COMPLEX
        self.resolution_scope = None  # BARANGAY or MUNICIPAL
        self.attachments = []
        self.feedback = None
    
    def update_status(self, status: ComplaintStatus) -> None:
        """Update the status of the complaint"""
        self.status = status
    
    def set_type(self, complaint_type: ComplaintType) -> None:
        """Set whether the complaint is simple or complex"""
        self.complaint_type = complaint_type
    
    def set_resolution_scope(self, scope: ResolutionScope) -> None:
        """Set whether the complaint can be resolved at barangay or municipal level"""
        self.resolution_scope = scope
    
    def assign_to(self, personnel: User) -> None:
        """Assign the complaint to a specific personnel"""
        self.assigned_to = personnel
        self.status = ComplaintStatus.IN_PROGRESS
    
    def add_attachment(self, attachment: Attachment) -> None:
        """Add an attachment to the complaint"""
        self.attachments.append(attachment)
    
    def add_feedback(self, feedback: Feedback) -> None:
        """Add feedback to the complaint after resolution"""
        self.feedback = feedback

class BCCMSSystem:
    def __init__(self):
        self.complaints = {}
        self.users = {}
        self.notifications = []
        self.next_tracking_id = 1000  # Starting tracking ID
    
    def register_user(self, user: User) -> None:
        """Register a new user in the system"""
        self.users[user.user_id] = user
    
    def register_complaint(self, complaint: Complaint) -> str:
        """Register a new complaint and generate a tracking ID"""
        tracking_id = f"BCCMS-{self.next_tracking_id}"
        self.next_tracking_id += 1
        complaint.tracking_id = tracking_id
        self.complaints[tracking_id] = complaint
        
        # Notify the resident with confirmation
        self.send_confirmation_to_resident(complaint)
        
        # Notify appropriate barangay officer
        self.notify_new_complaint(complaint)
        
        return tracking_id
    
    def send_confirmation_to_resident(self, complaint: Complaint) -> None:
        """Send confirmation with tracking ID to the resident"""
        content = f"Your complaint has been received. Tracking ID: {complaint.tracking_id}"
        notification = Notification(content, "Confirmation", complaint.submitter)
        self.notifications.append(notification)
    
    def notify_new_complaint(self, complaint: Complaint) -> None:
        """Notify barangay officer about a new complaint"""
        # In a real system, you would determine which officer to notify
        # For simplicity, we're assuming there's a method to get the right officer
        officer = self.get_appropriate_officer(complaint)
        if officer:
            content = f"New complaint received: {complaint.title}. Tracking ID: {complaint.tracking_id}"
            notification = Notification(content, "New Complaint", officer)
            self.notifications.append(notification)
    
    def notify_status_update(self, complaint: Complaint) -> None:
        """Notify resident about status update"""
        content = f"Your complaint (ID: {complaint.tracking_id}) status has been updated to: {complaint.status.value}"
        notification = Notification(content, "Status Update", complaint.submitter)
        self.notifications.append(notification)
    
    def notify_resolution(self, complaint: Complaint) -> None:
        """Notify resident about complaint resolution"""
        content = f"Your complaint (ID: {complaint.tracking_id}) has been resolved."
        notification = Notification(content, "Resolution", complaint.submitter)
        self.notifications.append(notification)
    
    def get_appropriate_officer(self, complaint: Complaint) -> Optional[BarangayOfficer]:
        """Get the appropriate officer to handle a complaint based on category"""
        # This would have more complex logic in a real system
        # For now, return None as a placeholder
        return None
    
    def get_complaint_by_tracking_id(self, tracking_id: str) -> Optional[Complaint]:
        """Retrieve a complaint by its tracking ID"""
        return self.complaints.get(tracking_id)

# Example usage demonstrating the sequence flow
def run_example():
    # Initialize the system and users
    system = BCCMSSystem()
    
    # Create users
    resident = Resident(1, "John Doe", "123456789", "john@example.com", "password")
    barangay_officer = BarangayOfficer(2, "Officer Smith", "987654321", "smith@barangay.gov", "officer_pwd")
    barangay_captain = BarangayCaptain(3, "Captain Johnson", "555123456", "captain@barangay.gov", "captain_pwd")
    personnel = Personnel(4, "Tech Support", "555987654", "tech@barangay.gov", "tech_pwd")
    municipality = Municipality(5, "Municipal Office", "555111222", "info@municipality.gov", "muni_pwd")
    
    # Register users in the system
    system.register_user(resident)
    system.register_user(barangay_officer)
    system.register_user(barangay_captain)
    system.register_user(personnel)
    
    # SEQUENCE FLOW IMPLEMENTATION
    
    # 1. Resident submits complaint
    tracking_id = resident.submit_complaint(
        "Noise Complaint", 
        "Loud music at night from neighbor", 
        ComplaintCategory.NOISE, 
        UrgencyLevel.MEDIUM,
        system
    )
    
    # Get the complaint from the system
    complaint = system.get_complaint_by_tracking_id(tracking_id)
    
    # 2. Barangay Officer assesses priority
    barangay_officer.assess_priority(complaint)
    
    # Notify resident of status update
    system.notify_status_update(complaint)
    
    # 3. Barangay Officer determines resolution path
    barangay_officer.determine_resolution_path(complaint)
    
    # Handle based on complaint type
    if complaint.complaint_type == ComplaintType.SIMPLE:
        # 4a. For simple issues
        barangay_officer.assign_task_directly(complaint, personnel)
        
        # Personnel executes solution
        personnel.execute_solution(complaint)
        
        # Notify resolution
        system.notify_resolution(complaint)
        
    else:
        # 4b. For complex issues
        barangay_officer.escalate_complex_issue(complaint, barangay_captain)
        
        # Captain reviews and decides
        barangay_captain.review_issue(complaint)
        barangay_captain.decide_resolution_path(complaint)
        
        # Handle based on resolution scope
        if complaint.resolution_scope == ResolutionScope.BARANGAY:
            # Can be resolved within Barangay
            barangay_captain.assign_to_personnel(complaint, personnel)
            personnel.execute_solution(complaint)
        else:
            # Requires Municipal Authority
            barangay_captain.escalate_to_municipality(complaint, municipality)
            municipality.execute_solution(complaint)
        
        # Notify resolution
        system.notify_resolution(complaint)
    
    # 5. Resident submits feedback
    resident.submit_feedback(
        complaint, 
        4, 
        "Issue was resolved promptly", 
        SatisfactionLevel.SATISFIED
    )
    
    # Output the final complaint status
    print(f"Complaint Status: {complaint.status.value}")
    print(f"Resolution Time: {datetime.now().isoformat()}")
    if complaint.feedback:
        print(f"Satisfaction: {complaint.feedback.satisfaction_level.value}")
    
    return complaint

if __name__ == "__main__":
    result = run_example()
    print(json.dumps({
        "tracking_id": result.tracking_id,
        "title": result.title,
        "status": result.status.value,
        "type": result.complaint_type.value if result.complaint_type else None,
        "scope": result.resolution_scope.value if result.resolution_scope else None
    }, indent=4))
