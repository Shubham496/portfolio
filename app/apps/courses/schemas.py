import re
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class EnquiryCreate(BaseModel):
    """Schema for a prospective student enquiry or callback request."""
    full_name: str = Field(..., min_length=2, max_length=120, description="Full name of student")
    email: Optional[str] = Field(default="", description="Student email address (optional)")
    phone: str = Field(..., min_length=7, max_length=25, description="Mobile / WhatsApp contact number")
    current_status: Optional[str] = Field(
        default="Working Professional",
        description="Current background: College Student, Working Professional, Fresher, Career Changer"
    )
    message: Optional[str] = Field(
        default="",
        max_length=2000,
        description="Questions regarding course, syllabus, mentorship, or callback timings"
    )
    preferred_schedule: Optional[str] = Field(
        default="Saturday & Sunday 6:00 PM – 8:00 PM IST",
        description="Schedule preference"
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return ""
        v = v.strip().lower()
        if v and not EMAIL_REGEX.match(v):
            raise ValueError("Invalid email format")
        return v


class BatchRegistrationCreate(BaseModel):
    """Schema for direct registration into an upcoming weekend batch."""
    full_name: str = Field(..., min_length=2, max_length=120, description="Full name of student")
    email: Optional[str] = Field(default="", description="Student email address (optional)")
    phone: str = Field(..., min_length=7, max_length=25, description="Mobile / WhatsApp contact number")
    batch_id: Optional[int] = Field(
        default=None,
        description="ID of specific batch (if omitted, assigned to current active weekend batch)"
    )
    current_status: Optional[str] = Field(
        default="Working Professional",
        description="College Student / Working Professional / Fresher / Career Changer"
    )
    prior_experience: Optional[str] = Field(
        default="Beginner",
        description="Experience level in Python, SQL, or BI"
    )
    message: Optional[str] = Field(
        default="",
        max_length=2000,
        description="Learning goals or any notes for instructor"
    )
    preferred_schedule: Optional[str] = Field(
        default="Saturday & Sunday 6:00 PM – 8:00 PM IST"
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return ""
        v = v.strip().lower()
        if v and not EMAIL_REGEX.match(v):
            raise ValueError("Invalid email format")
        return v


class LeadStatusUpdate(BaseModel):
    """Update lead pipeline stage and counseling notes."""
    status: str = Field(..., description="'new', 'contacted', 'enrolled', or 'closed'")
    admin_notes: Optional[str] = Field(default="", description="Counselor or instructor internal notes")


class BatchCreate(BaseModel):
    """Create a new training batch."""
    batch_code: str = Field(..., min_length=3, max_length=50)
    title: str = Field(..., min_length=3, max_length=150)
    course_name: str = Field(default="Data Analysis")
    technologies: str = Field(default="Python, SQL, PowerBI, Excel, Tableau")
    schedule_days: str = Field(default="Saturday & Sunday")
    schedule_time: str = Field(default="6:00 PM – 8:00 PM IST")
    start_date: str = Field(default="Upcoming Weekend")
    duration: str = Field(default="8-10 Weeks Hands-On")
    status: str = Field(default="enrolling")
    max_seats: Optional[int] = Field(default=25)
    description: Optional[str] = Field(default="")
    is_active: bool = Field(default=True)


class BatchOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    batch_code: str
    title: str
    course_name: str
    technologies: List[str]
    schedule_days: str
    schedule_time: str
    start_date: str
    duration: str
    status: str
    max_seats: Optional[int]
    total_registrations: int = 0
    is_active: bool


class LeadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_type: str
    batch_id: Optional[int]
    batch_title: Optional[str]
    batch_code: Optional[str]
    full_name: str
    email: Optional[str] = ""
    phone: str
    current_status: Optional[str]
    prior_experience: Optional[str]
    preferred_schedule: str
    message: Optional[str]
    status: str
    admin_notes: Optional[str]
    created_at: Optional[str]
