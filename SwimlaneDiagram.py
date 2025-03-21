# Complaint Management System

from datetime import datetime
from enum import Enum
import uuid
from typing import List, Dict, Optional, Any

# Define enums for status tracking
class ComplaintStatus(Enum):
    NEW = "New"
    VERIFIED = "Verified"
    IN_PROCESS = "In Process"
    ESCALATED = "Escalated"
    RESOLVED = "Resolved"
    CLOSED = "Closed"
    REOPENED = "Reopened"

class UrgencyLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class EscalationLevel(Enum):
    NONE = "None"
    BARANGAY_CAPTAIN = "Barangay Captain"
    MUNICIPAL = "Municipal"

class UserRole(Enum):
    RESIDENT = "Resident"
    BARANGAY_OFFICER = "Barangay Officer"
    BARANGAY_CAPTAIN = "Barangay Captain"
    MUNICIPAL_OFFICER = "Municipal Officer"

class User:
    def __init__(self, user_id: str, name: str, role: UserRole, contact: str):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.contact = contact

class Evidence:
    def __init__(self, evidence_id: str, complaint_id: str, file_path: str, description: str, uploaded_by: str, upload_date: datetime):
        self.evidence_id = evidence_id
        self.complaint_id = complaint_id
        self.file_path = file_path
        self.description = description
        self.uploaded_by = uploaded_by
        self.upload_date = upload_date

class StatusUpdate:
    def __init__(self, update_id: str, complaint_id: str, status: ComplaintStatus, 
                 notes: str, updated_by: str, update_date: datetime):
        self.update_id = update_id
        self.complaint_id = complaint_id
        self.status = status
        self.notes = notes
        self.updated_by = updated_by
        self.update_date = update_date

class Feedback:
    def __init__(self, feedback_id: str, complaint_id: str, rating: int, 
                 comments: str, submitted_by: str, submission_date: datetime):
        self.feedback_id = feedback_id
        self.complaint_id = complaint_id
        self.rating = rating
        self.comments = comments
        self.submitted_by = submitted_by
        self.submission_date = submission_date

class Complaint:
    def __init__(self, complaint_id: str, title: str, description: str, 
                 submitted_by: str, submission_date: datetime):
        self.complaint_id = complaint_id
        self.title = title
        self.description = description
        self.submitted_by = submitted_by
        self.submission_date = submission_date
        self.urgency_level = UrgencyLevel.MEDIUM
        self.status = ComplaintStatus.NEW
        self.escalation_level = EscalationLevel.NONE
        self.assigned_to = None
        self.resolution = None
        self.resolution_date = None
        self.status_updates = []
        self.evidence_list = []
        self.feedback = None
        self.is_satisfied = None

    def add_status_update(self, status: ComplaintStatus, notes: str, updated_by: str) -> StatusUpdate:
        """Add a status update to the complaint"""
        update_id = str(uuid.uuid4())
        update = StatusUpdate(update_id, self.complaint_id, status, notes, updated_by, datetime.now())
        self.status_updates.append(update)
        self.status = status
        return update

    def add_evidence(self, file_path: str, description: str, uploaded_by: str) -> Evidence:
        """Add evidence to the complaint"""
        evidence_id = str(uuid.uuid4())
        evidence = Evidence(evidence_id, self.complaint_id, file_path, description, uploaded_by, datetime.now())
        self.evidence_list.append(evidence)
        return evidence

    def add_feedback(self, rating: int, comments: str, submitted_by: str, is_satisfied: bool) -> Feedback:
        """Add feedback to the complaint"""
        feedback_id = str(uuid.uuid4())
        feedback = Feedback(feedback_id, self.complaint_id, rating, comments, submitted_by, datetime.now())
        self.feedback = feedback
        self.is_satisfied = is_satisfied
        return feedback

    def resolve(self, resolution: str, resolved_by: str) -> StatusUpdate:
        """Resolve the complaint"""
        self.resolution = resolution
        self.resolution_date = datetime.now()
        return self.add_status_update(ComplaintStatus.RESOLVED, f"Resolved: {resolution}", resolved_by)

    def reopen(self, reason: str, reopened_by: str) -> StatusUpdate:
        """Reopen a resolved complaint"""
        if self.status == ComplaintStatus.RESOLVED or self.status == ComplaintStatus.CLOSED:
            return self.add_status_update(ComplaintStatus.REOPENED, f"Reopened: {reason}", reopened_by)
        return None

    def close(self, closed_by: str) -> StatusUpdate:
        """Close the complaint after resolution and satisfaction"""
        if self.status == ComplaintStatus.RESOLVED and self.is_satisfied:
            return self.add_status_update(ComplaintStatus.CLOSED, "Complaint closed", closed_by)
        return None

class ComplaintManager:
    def __init__(self):
        self.complaints = {}
        self.users = {}

    def register_user(self, name: str, role: UserRole, contact: str) -> User:
        """Register a new user in the system"""
        user_id = str(uuid.uuid4())
        user = User(user_id, name, role, contact)
        self.users[user_id] = user
        return user

    def submit_complaint(self, title: str, description: str, user_id: str) -> Complaint:
        """Submit a new complaint"""
        if user_id not in self.users:
            raise ValueError("User not found")
        
        user = self.users[user_id]
        if user.role != UserRole.RESIDENT:
            raise ValueError("Only residents can submit complaints")
        
        complaint_id = str(uuid.uuid4())
        complaint = Complaint(complaint_id, title, description, user_id, datetime.now())
        self.complaints[complaint_id] = complaint
        
        # Add initial status update
        complaint.add_status_update(ComplaintStatus.NEW, "Complaint submitted", user_id)
        
        return complaint

    def verify_complaint(self, complaint_id: str, officer_id: str, is_valid: bool, notes: str) -> Optional[Complaint]:
        """Verify a complaint"""
        if complaint_id not in self.complaints or officer_id not in self.users:
            return None
        
        officer = self.users[officer_id]
        if officer.role != UserRole.BARANGAY_OFFICER:
            raise ValueError("Only Barangay Officers can verify complaints")
        
        complaint = self.complaints[complaint_id]
        
        if is_valid:
            complaint.add_status_update(ComplaintStatus.VERIFIED, notes, officer_id)
        else:
            complaint.add_status_update(ComplaintStatus.CLOSED, f"Invalid complaint: {notes}", officer_id)
            
        return complaint

    def assess_urgency(self, complaint_id: str, officer_id: str, urgency: UrgencyLevel, notes: str) -> Optional[Complaint]:
        """Assess the urgency of a complaint"""
        if complaint_id not in self.complaints or officer_id not in self.users:
            return None
        
        officer = self.users[officer_id]
        if officer.role != UserRole.BARANGAY_OFFICER:
            raise ValueError("Only Barangay Officers can assess urgency")
            
        complaint = self.complaints[complaint_id]
        complaint.urgency_level = urgency
        complaint.add_status_update(complaint.status, f"Urgency assessed as {urgency.value}: {notes}", officer_id)
        
        return complaint

    def escalate_complaint(self, complaint_id: str, escalated_by: str, 
                           escalation_level: EscalationLevel, reason: str) -> Optional[Complaint]:
        """Escalate a complaint to the Barangay Captain or Municipal level"""
        if complaint_id not in self.complaints or escalated_by not in self.users:
            return None
        
        user = self.users[escalated_by]
        if user.role != UserRole.BARANGAY_OFFICER and user.role != UserRole.BARANGAY_CAPTAIN:
            raise ValueError("Only Barangay Officers or Captains can escalate complaints")
            
        complaint = self.complaints[complaint_id]
        complaint.escalation_level = escalation_level
        
        status_notes = f"Escalated to {escalation_level.value}: {reason}"
        complaint.add_status_update(ComplaintStatus.ESCALATED, status_notes, escalated_by)
        
        return complaint

    def process_complaint(self, complaint_id: str, officer_id: str, notes: str, assigned_to: str) -> Optional[Complaint]:
        """Process a non-escalated complaint"""
        if complaint_id not in self.complaints or officer_id not in self.users:
            return None
        
        officer = self.users[officer_id]
        if officer.role != UserRole.BARANGAY_OFFICER and officer.role != UserRole.BARANGAY_CAPTAIN:
            raise ValueError("Only Barangay Officers or Captains can process complaints")
            
        complaint = self.complaints[complaint_id]
        complaint.assigned_to = assigned_to
        complaint.add_status_update(ComplaintStatus.IN_PROCESS, notes, officer_id)
        
        return complaint

    def update_status(self, complaint_id: str, user_id: str, status: ComplaintStatus, notes: str) -> Optional[StatusUpdate]:
        """Update the status of a complaint"""
        if complaint_id not in self.complaints or user_id not in self.users:
            return None
        
        user = self.users[user_id]
        if user.role == UserRole.RESIDENT:
            raise ValueError("Residents cannot update complaint status")
            
        complaint = self.complaints[complaint_id]
        return complaint.add_status_update(status, notes, user_id)

    def resolve_issue(self, complaint_id: str, user_id: str, resolution: str) -> Optional[Complaint]:
        """Resolve a complaint"""
        if complaint_id not in self.complaints or user_id not in self.users:
            return None
        
        user = self.users[user_id]
        if user.role == UserRole.RESIDENT:
            raise ValueError("Residents cannot resolve complaints")
            
        complaint = self.complaints[complaint_id]
        complaint.resolve(resolution, user_id)
        
        return complaint

    def submit_feedback(self, complaint_id: str, user_id: str, rating: int, 
                       comments: str, is_satisfied: bool) -> Optional[Feedback]:
        """Submit feedback for a resolved complaint"""
        if complaint_id not in self.complaints or user_id not in self.users:
            return None
        
        user = self.users[user_id]
        if user.role != UserRole.RESIDENT:
            raise ValueError("Only residents can submit feedback")
            
        complaint = self.complaints[complaint_id]
        
        if complaint.status != ComplaintStatus.RESOLVED:
            return None
            
        feedback = complaint.add_feedback(rating, comments, user_id, is_satisfied)
        
        if is_satisfied:
            complaint.close(user_id)
        else:
            complaint.reopen(f"User not satisfied: {comments}", user_id)
            
        return feedback

    def request_further_action(self, complaint_id: str, user_id: str, request: str) -> Optional[StatusUpdate]:
        """Request further action on a resolved complaint"""
        if complaint_id not in self.complaints or user_id not in self.users:
            return None
        
        user = self.users[user_id]
        if user.role != UserRole.RESIDENT:
            raise ValueError("Only residents can request further action")
            
        complaint = self.complaints[complaint_id]
        
        if complaint.status != ComplaintStatus.RESOLVED:
            return None
            
        return complaint.reopen(f"Further action requested: {request}", user_id)

    def get_complaint(self, complaint_id: str) -> Optional[Complaint]:
        """Get a complaint by ID"""
        return self.complaints.get(complaint_id)

    def get_user_complaints(self, user_id: str) -> List[Complaint]:
        """Get all complaints submitted by a user"""
        return [c for c in self.complaints.values() if c.submitted_by == user_id]

    def get_assigned_complaints(self, officer_id: str) -> List[Complaint]:
        """Get all complaints assigned to an officer"""
        return [c for c in self.complaints.values() if c.assigned_to == officer_id]

# Role-Based Demo
def main():
    manager = ComplaintManager()
    
    # Register users with clear roles
    resident = manager.register_user("Juan Dela Cruz", UserRole.RESIDENT, "juan@example.com")
    officer = manager.register_user("Maria Santos", UserRole.BARANGAY_OFFICER, "maria@barangay.gov")
    captain = manager.register_user("Pedro Reyes", UserRole.BARANGAY_CAPTAIN, "pedro@barangay.gov")
    municipal = manager.register_user("Elena Marcos", UserRole.MUNICIPAL_OFFICER, "elena@municipal.gov")
    
    print("\n========== COMPLAINT MANAGEMENT PROCESS DEMO ==========\n")
    
    # RESIDENT ACTIONS
    print("======= RESIDENT ACTIONS =======")
    print(f"Resident {resident.name} submits a complaint...")
    complaint = manager.submit_complaint(
        "Noise Complaint", 
        "Loud construction noise from the neighbor during quiet hours",
        resident.user_id
    )
    print(f"✓ Complaint #{complaint.complaint_id[:8]} submitted successfully")
    
    print(f"\nResident {resident.name} uploads evidence...")
    evidence = complaint.add_evidence("noise_recording.mp3", "Audio recording of noise", resident.user_id)
    print(f"✓ Evidence #{evidence.evidence_id[:8]} uploaded successfully")
    
    # BARANGAY OFFICER ACTIONS
    print("\n======= BARANGAY OFFICER ACTIONS =======")
    print(f"Barangay Officer {officer.name} receives and verifies the complaint...")
    manager.verify_complaint(complaint.complaint_id, officer.user_id, True, "Verified with audio evidence")
    print(f"✓ Complaint #{complaint.complaint_id[:8]} verified")
    
    print(f"\nBarangay Officer {officer.name} assesses urgency...")
    manager.assess_urgency(complaint.complaint_id, officer.user_id, UrgencyLevel.HIGH, "Affects multiple residents")
    print(f"✓ Urgency assessed as {complaint.urgency_level.value}")
    
    print(f"\nBarangay Officer {officer.name} decides escalation is needed...")
    manager.escalate_complaint(
        complaint.complaint_id, 
        officer.user_id,
        EscalationLevel.BARANGAY_CAPTAIN, 
        "High urgency requires captain's attention"
    )
    print(f"✓ Complaint escalated to {complaint.escalation_level.value}")
    
    # BARANGAY CAPTAIN ACTIONS
    print("\n======= BARANGAY CAPTAIN ACTIONS =======")
    print(f"Barangay Captain {captain.name} reviews the escalated issue...")
    
    print(f"\nBarangay Captain {captain.name} decides if municipal escalation is needed...")
    # In this case, decides NO municipal escalation is needed
    print("Decision: No municipal escalation required")
    
    print(f"\nBarangay Captain {captain.name} allocates resources...")
    manager.update_status(
        complaint.complaint_id,
        captain.user_id, 
        ComplaintStatus.IN_PROCESS,
        "Allocated enforcement team to investigate"
    )
    print(f"✓ Resources allocated, complaint now {complaint.status.value}")
    
    # Back to BARANGAY OFFICER
    print("\n======= BARANGAY OFFICER ACTIONS =======")
    print(f"Barangay Officer {officer.name} processes the complaint...")
    manager.process_complaint(
        complaint.complaint_id,
        officer.user_id,
        "Enforcement team visited the site, issued warning",
        officer.user_id
    )
    print(f"✓ Complaint in progress")
    
    print(f"\nBarangay Officer {officer.name} updates status...")
    manager.update_status(
        complaint.complaint_id,
        officer.user_id,
        ComplaintStatus.IN_PROCESS,
        "Second visit scheduled for tomorrow"
    )
    print(f"✓ Status updated")
    
    print(f"\nBarangay Officer {officer.name} resolves the issue...")
    manager.resolve_issue(
        complaint.complaint_id,
        officer.user_id,
        "Issued citation to neighbor and resolved noise issue. Neighbor agreed to restrict construction to allowed hours."
    )
    print(f"✓ Issue resolved")
    
    print(f"\nBarangay Officer {officer.name} documents resolution...")
    manager.update_status(
        complaint.complaint_id,
        officer.user_id,
        ComplaintStatus.RESOLVED,
        "Documented resolution with fine payment details and compliance agreement"
    )
    print(f"✓ Resolution documented")
    
    # Back to RESIDENT
    print("\n======= RESIDENT ACTIONS =======")
    print(f"Resident {resident.name} reviews resolution...")
    print(f"Resolution: {complaint.resolution}")
    
    print(f"\nResident {resident.name} provides feedback...")
    feedback = manager.submit_feedback(
        complaint.complaint_id,
        resident.user_id,
        4,  # Rating out of 5
        "Issue has been resolved but took longer than expected",
        True  # Satisfied
    )
    print(f"✓ Feedback submitted: {feedback.rating}/5 - {feedback.comments}")
    print(f"✓ Resident indicated they are satisfied with the resolution")
    print(f"✓ Complaint status updated to: {complaint.status.value}")
    
    # MUNICIPAL ACTIONS - would happen only if escalated to municipal level
    print("\n======= MUNICIPAL ACTIONS =======")
    print("Note: No municipal actions were required for this complaint as it was resolved at the barangay level.")
    print("If the complaint had been escalated to municipal level, the Municipal Officer would have additional steps.")
    
    # Demonstration of what happens when resident is NOT satisfied
    print("\n========== ALTERNATE SCENARIO: RESIDENT NOT SATISFIED ==========")
    print("If the resident was not satisfied, they could request further action:")
    
    # Create a new instance for the alternate scenario
    alternate_complaint = manager.submit_complaint(
        "Similar Noise Complaint", 
        "Loud construction noise continues despite previous resolution",
        resident.user_id
    )
    # Fast-forward to resolution for demo purposes
    manager.verify_complaint(alternate_complaint.complaint_id, officer.user_id, True, "Verified")
    manager.assess_urgency(alternate_complaint.complaint_id, officer.user_id, UrgencyLevel.MEDIUM, "Recurring issue")
    manager.process_complaint(alternate_complaint.complaint_id, officer.user_id, "Processing", officer.user_id)
    manager.resolve_issue(alternate_complaint.complaint_id, officer.user_id, "Applied standard noise resolution")
    
    print(f"Resident {resident.name} reviews resolution but is NOT satisfied...")
    
    print(f"Resident {resident.name} requests further action...")
    request = manager.request_further_action(
        alternate_complaint.complaint_id,
        resident.user_id,
        "Noise problem persists. Need stricter enforcement and monitoring."
    )
    print(f"✓ Further action requested")
    print(f"✓ Complaint status updated to: {alternate_complaint.status.value}")
    
    print("\n========== COMPLAINT SUMMARY ==========")
    complaint = manager.get_complaint(complaint.complaint_id)
    print(f"Complaint ID: {complaint.complaint_id[:8]}")
    print(f"Title: {complaint.title}")
    print(f"Description: {complaint.description}")
    print(f"Status: {complaint.status.value}")
    print(f"Urgency: {complaint.urgency_level.value}")
    print(f"Escalation Level: {complaint.escalation_level.value}")
    print(f"Resolution: {complaint.resolution}")
    print(f"Resolution Date: {complaint.resolution_date}")
    print("\nStatus Updates:")
    for i, update in enumerate(complaint.status_updates, 1):
        user = manager.users[update.updated_by]
        print(f"{i}. [{user.role.value}] {update.update_date}: {update.status.value} - {update.notes}")
    
    if complaint.feedback:
        print(f"\nFeedback: {complaint.feedback.rating}/5 - {complaint.feedback.comments}")
        print(f"Resident Satisfied: {'Yes' if complaint.is_satisfied else 'No'}")

if __name__ == "__main__":
    main()