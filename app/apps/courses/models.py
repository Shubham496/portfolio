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
    """
    __tablename__ = "student_leads"

    id = Column(Integer, primary_key=True, index=True)
    # Type: 'enquiry' (questions/counseling/syllabus) or 'batch_registration' (direct enrollment)
    lead_type = Column(String(30), nullable=False, index=True, default="enquiry")
    
    # Linked batch (if applying for a specific batch)
    batch_id = Column(Integer, ForeignKey("batches.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Student Contact Info
    full_name = Column(String(120), nullable=False)
    email = Column(String(150), nullable=True, index=True)
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
            "created_date": self.created_at.strftime("%b %d, %Y") if self.created_at else "",
            "created_time": self.created_at.strftime("%I:%M %p") if self.created_at else "",
        }


class AdminUser(Base):
    """Admin user accounts for monitoring registrations and enquiries."""
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class User(Base):
    """
    Represents a registered student, fresher, or working professional on the platform.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    phone = Column(String(30), unique=True, index=True, nullable=False)  # WhatsApp / primary contact
    email = Column(String(150), unique=True, index=True, nullable=True)  # Optional
    hashed_password = Column(String(255), nullable=False)
    user_type = Column(String(50), nullable=False, default="student")  # student, fresher, working_professional
    college_or_company = Column(String(150), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    activity_logs = relationship("UserActivityLog", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "phone": self.phone,
            "email": self.email,
            "user_type": self.user_type,
            "college_or_company": self.college_or_company,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class UserActivityLog(Base):
    """
    Tracks student and guest reader engagement across documentation, datasets, and admissions.
    Informs content strategy and cohort counseling readiness.
    """
    __tablename__ = "user_activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    session_id = Column(String(64), index=True, nullable=False)  # Cookie-based session ID linking guest behavior
    event_type = Column(String(50), index=True, nullable=False)  # page_view, note_read, dataset_download, cohort_apply_click, etc.
    resource_type = Column(String(50), nullable=True)  # note, viva, dataset, book, project, general
    resource_slug = Column(String(100), index=True, nullable=True)
    referrer = Column(String(255), nullable=True)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now(), index=True)

    user = relationship("User", back_populates="activity_logs")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "event_type": self.event_type,
            "resource_type": self.resource_type,
            "resource_slug": self.resource_slug,
            "referrer": self.referrer,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
