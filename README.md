# BaranGuide: Barangay Community Complaint Management System


## 📄 Overview

BaranGuide is a digital platform designed to simplify and optimize the submission, tracking, and resolution of community complaints at the barangay level. By facilitating direct communication between residents and barangay officials, our system enhances transparency, accountability, and efficiency in local governance.

### Purpose

The Barangay Community Complaint Management System (BCCMS) ensures that residents' concerns are addressed promptly, fostering a more responsive and engaged community. It digitalizes the traditional complaint management process to improve service delivery and community satisfaction.

### SDG Alignment

This project aligns with:
- **SDG 11**: Sustainable Cities and Communities
- **SDG 16**: Peace, Justice, and Strong Institutions

## 👥 Target Users

- **Residents**: Community members who need to report issues
- **Barangay Officers**: Officials responsible for addressing complaints
- **Barangay Captain**: Oversees the complaint resolution process
- **Municipal Officials**: Handle escalated issues beyond barangay capacity

## ✨ Key Features

### 📝 Complaint Submission
- User-friendly form for residents to submit complaints
- Categorization system for different types of community issues
- Evidence attachment capability (photos, videos, documents)

### 🔍 Complaint Tracking
- Unique tracking ID generation
- Real-time status updates
- Estimated resolution time based on urgency

### ⚡ Urgency Assessment
- Multi-level urgency classification system
- Automatic escalation of high-priority issues
- Resource allocation based on severity

### 📱 Communication
- Automated notifications via SMS, email, or in-app alerts
- Post-resolution feedback system
- Direct messaging between officials

### 🔐 User Management
- Role-based access control
- Secure authentication
- Profile management

## 🏗️ Architecture

### Class Structure
The system follows an object-oriented design with the following main classes:
- User (abstract base class)
  - Resident
  - BarangayOfficer
  - BarangayCaptain
  - MunicipalOfficial
- Complaint
- Attachment
- Feedback
- Notification
- Message

### Complaint Workflow
1. Submission by resident
2. Processing by barangay officer
3. Escalation (if necessary)
4. Resolution implementation
5. Feedback collection

## 💻 Technical Details

### Built With
- **Language**: Python 3.9+
- **Data Handling**: Standard Python libraries (DateTime, enum, json)
- **Type Annotations**: Python typing module
- **State Management**: Enum-based status tracking
- **Paradigm**: Object-Oriented Programming

### Key Components

#### Status & Urgency Management
```python
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
```

#### Complaint Processing
```python
class BarangayOfficer(User):
    def verify_complaint(self, complaint):
        complaint.status = ComplaintStatus.IN_PROGRESS
        # Verification logic
        
    def assess_urgency(self, complaint, urgency_level):
        complaint.urgency_level = urgency_level
        complaint.estimated_resolution_time = self._calculate_resolution_time(urgency_level)
```

## 🛠️ Development Challenges

- **Frontend Focus**: Limited experience with database integration
- **Time Constraints**: Balancing development with academic workload
- **Authentication Complexity**: Implementing role-based access control
- **UML Diagramming**: Learning curve in creating proper system diagrams

## 📊 UML Diagrams

The repository includes the following UML diagrams:
- Class Diagram
- Sequence Diagram
- Swimlane Diagram

## 👨‍💻 Team

- Mary Kristine A. De Jose
- Dorothy C. Salva
- Clarence C. Zamora

## 💼 Course Information

- **Course**: CS 322: Software Engineering
- **Lab Activity**: 2
- **Instructor**: Ms. Fatima Marie P. Agdon, MSCS
- **Date**: March 24, 2025

## 📚 References

- Barangay Tetuan Council. [Barangay Complain Automated Record System](https://www.scribd.com/document/449952428/Barangay-Complain-Automated-Record-System-for-Barangay-Tetuan-Z-C-1-docx)
- [BARS Barangay Blotter System](https://www.bars.com.ph/barangay-blotter-system/)
- [eBarangayPH](https://ebarangayph.com/)