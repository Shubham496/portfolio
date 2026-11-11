from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship
from app.apps.courses.database import Base


class Batch(Base):
    """Represents a scheduled course batch."""
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    batch_code = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(150), nullable=False)
    course_name = Column(String(150), nullable=False, default="Data Analysis")
    technologies = Column(
        String(255),
        nullable=False,
        default="Python, SQL, PowerBI, Excel, Tableau"
    )
    schedule_days = Column(String(100), nullable=False, default="Saturday & Sunday")
    schedule_time = Column(String(100), nullable=False, default="6:00 PM – 8:00 PM IST")
    start_date = Column(String(50), nullable=False, default="Upcoming Weekend")
    duration = Column(String(50), nullable=False, default="8-10 Weeks Hands-On")
    status = Column(String(50), nullable=False, default="enrolling")  # enrolling, upcoming, ongoing, completed
    max_seats = Column(Integer, nullable=True, default=25)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())

    # Relationship to registrations/leads
    registrations = relationship("StudentLead", back_populates="batch", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "batch_code": self.batch_code,
            "title": self.title,
            "course_name": self.course_name,
            "technologies": [t.strip() for t in self.technologies.split(",") if t.strip()],
            "schedule_days": self.schedule_days,
            "schedule_time": self.schedule_time,
            "start_date": self.start_date,
            "duration": self.duration,
            "status": self.status,
            "max_seats": self.max_seats,
            "total_registrations": len(self.registrations) if self.registrations else 0,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class StudentLead(Base):
    """
    Represents either a prospective student enquiry or a direct batch registration.
    No fees are recorded or required on public forms.
    """
    __tablename__ = "student_leads"

    id = Column(Integer, primary_key=True, index=True)
    # Type: 'enquiry' (questions/counseling/syllabus) or 'batch_registration' (direct enrollment)
    lead_type = Column(String(30), nullable=False, index=True, default="enquiry")
    
    # Linked batch (if applying for a specific batch)
    batch_id = Column(Integer, ForeignKey("batches.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Student Contact Info
    full_name = Column(String(120), nullable=False)
    email = Column(String(150), nullable=False, index=True)
    phone = Column(String(30), nullable=False, index=True)
    
    # Student Profile / Goals
    current_status = Column(String(80), nullable=True)  # e.g., "College Student", "Working Professional", "Career Changer"
    prior_experience = Column(String(80), nullable=True)  # e.g., "Beginner", "Basic Python", "Excel User"
    preferred_schedule = Column(
        String(100),
        nullable=False,
        default="Saturday & Sunday 6:00 PM – 8:00 PM IST"
    )
    message = Column(Text, nullable=True)  # Student questions, notes, or expectations
    
    # Lead / Admission Pipeline Tracking
    status = Column(String(30), nullable=False, default="new", index=True)  # new, contacted, enrolled, closed
    admin_notes = Column(Text, nullable=True)
    source_ip = Column(String(50), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    batch = relationship("Batch", back_populates="registrations")

    def to_dict(self):
        return {
            "id": self.id,
            "lead_type": self.lead_type,
            "batch_id": self.batch_id,
            "batch_title": self.batch.title if self.batch else None,
            "batch_code": self.batch.batch_code if self.batch else None,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "current_status": self.current_status,
            "prior_experience": self.prior_experience,
            "preferred_schedule": self.preferred_schedule,
            "message": self.message,
            "status": self.status,
            "admin_notes": self.admin_notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
