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
    course_interest: Optional[str] = Field(
        default="All Programs / Undecided",
        description="Program of interest: Digital Marketing (Performance Ads), Digital Marketing (SEO & Growth), Data Analytics & BI"
    )
    subject_interest: Optional[str] = Field(
        default="",
        description="Subject or topic of interest (e.g. SQL, Excel, Power BI, Python)"
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
    consent: bool = Field(
        default=True,
        description="Consent to be contacted by phone or WhatsApp about this course"
    )
    website_url_hp: Optional[str] = Field(default=None, description="Anti-spam honeypot field")
    source_utm: Optional[str] = Field(default=None, description="Attribution UTM string")
    referrer_url: Optional[str] = Field(default=None, description="Referrer URL")

    @field_validator("website_url_hp")
    @classmethod
    def validate_hp(cls, v) -> Optional[str]:
        if v and str(v).strip():
            raise ValueError("Spam submission detected.")
        return v

    @field_validator("consent", mode="before")
    @classmethod
    def validate_consent(cls, v) -> bool:
        if isinstance(v, str):
            v = v.strip().lower() in ("true", "1", "on", "yes")
        if not bool(v):
            raise ValueError("You must agree to be contacted by phone or WhatsApp about this course.")
        return True

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
        description="ID of specific batch (if omitted, assigned to matching or active weekend batch)"
    )
    course_name: Optional[str] = Field(
        default="Data Analysis",
        description="Program: Digital Marketing (Performance Ads), Digital Marketing (SEO & Growth), Data Analytics & BI"
    )
    current_status: Optional[str] = Field(
        default="Working Professional",
        description="College Student / Working Professional / Fresher / Career Changer"
    )
    prior_experience: Optional[str] = Field(
        default="Beginner",
        description="Experience level in digital marketing, coding, or analytics"
    )
    message: Optional[str] = Field(
        default="",
        max_length=2000,
        description="Learning goals or any notes for instructor"
    )
    preferred_schedule: Optional[str] = Field(
        default="Saturday & Sunday 6:00 PM – 8:00 PM IST"
    )
    consent: bool = Field(
        default=True,
        description="Consent to be contacted by phone or WhatsApp about this course"
    )
    website_url_hp: Optional[str] = Field(default=None, description="Anti-spam honeypot field")
    source_utm: Optional[str] = Field(default=None, description="Attribution UTM string")
    referrer_url: Optional[str] = Field(default=None, description="Referrer URL")

    @field_validator("website_url_hp")
    @classmethod
    def validate_hp(cls, v) -> Optional[str]:
        if v and str(v).strip():
            raise ValueError("Spam submission detected.")
        return v

    @field_validator("consent", mode="before")
    @classmethod
    def validate_consent(cls, v) -> bool:
        if isinstance(v, str):
            v = v.strip().lower() in ("true", "1", "on", "yes")
        if not bool(v):
            raise ValueError("You must agree to be contacted by phone or WhatsApp about this course.")
        return True

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
    status: str = Field(..., description="'new', 'contacted', 'demo_attended', 'enrolled', 'closed', or 'do_not_contact'")
    admin_notes: Optional[str] = Field(default="", description="Counselor or instructor internal notes")
    follow_up_date: Optional[str] = Field(default=None, description="Follow-up scheduled date (YYYY-MM-DD)")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed = ("new", "contacted", "demo_attended", "enrolled", "closed", "do_not_contact")
        v_clean = v.strip().lower()
        if v_clean not in allowed:
            raise ValueError(f"Invalid status '{v}'. Allowed statuses: {', '.join(allowed)}")
        return v_clean



class BatchCreate(BaseModel):
    """Create a new training batch."""
    batch_code: str = Field(..., min_length=3, max_length=50)
    title: str = Field(..., min_length=3, max_length=150)
    course_name: str = Field(default="Data Analysis")
    track: Optional[str] = Field(default="data_analytics", description="Track: 'data_analytics' or 'digital_marketing'")
    technologies: str = Field(default="Python, SQL, PowerBI, Excel, Tableau")
    schedule_days: str = Field(default="Saturday & Sunday")
    schedule_time: str = Field(default="6:00 PM – 8:00 PM IST")
    start_date: str = Field(default="Upcoming Weekend")
    duration: str = Field(default="8-10 Weeks Hands-On")
    status: str = Field(default="enrolling")
    max_seats: Optional[int] = Field(default=25)
    description: Optional[str] = Field(default="")
    is_active: bool = Field(default=True)


class BatchUpdate(BaseModel):
    """Update existing batch attributes."""
    title: Optional[str] = None
    course_name: Optional[str] = None
    track: Optional[str] = None
    technologies: Optional[str] = None
    schedule_days: Optional[str] = None
    schedule_time: Optional[str] = None
    start_date: Optional[str] = None
    duration: Optional[str] = None
    status: Optional[str] = None
    max_seats: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class BatchOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    batch_code: str
    title: str
    course_name: str
    track: str = "data_analytics"
    technologies: List[str]
    schedule_days: str
    schedule_time: str
    start_date: str
    duration: str
    status: str
    max_seats: Optional[int]
    total_registrations: int = 0
    remaining_seats: int = 25
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
    subject_interest: Optional[str] = ""
    message: Optional[str]
    source_utm: Optional[str] = None
    referrer_url: Optional[str] = None
    follow_up_date: Optional[str] = None
    status: str
    admin_notes: Optional[str]
    consent_given: bool = True
    consent_at: Optional[str] = None
    created_at: Optional[str]


class WaitlistCreate(BaseModel):
    """Schema for 'Notify Me for Next Batch' waitlist registrations."""
    full_name: str = Field(..., min_length=2, max_length=120, description="Full name of student")
    phone: str = Field(..., min_length=7, max_length=25, description="Mobile / WhatsApp contact number")
    email: Optional[str] = Field(default="", description="Student email address (optional)")
    subject_interest: str = Field(..., min_length=1, max_length=100, description="Target subject (SQL, Excel, Power BI, Python, etc.)")
    message: Optional[str] = Field(default="", max_length=1000, description="Optional notes or questions")
    consent: bool = Field(default=True, description="Consent to be contacted")
    website_url_hp: Optional[str] = Field(default=None, description="Anti-spam honeypot field")
    source_utm: Optional[str] = Field(default=None, description="Attribution UTM string")
    referrer_url: Optional[str] = Field(default=None, description="Referrer URL")

    @field_validator("website_url_hp")
    @classmethod
    def validate_hp(cls, v) -> Optional[str]:
        if v and str(v).strip():
            raise ValueError("Spam submission detected.")
        return v

    @field_validator("consent", mode="before")
    @classmethod
    def validate_consent(cls, v) -> bool:
        if isinstance(v, str):
            v = v.strip().lower() in ("true", "1", "on", "yes")
        if not bool(v):
            raise ValueError("You must agree to be contacted by phone or WhatsApp about this course.")
        return True

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return ""
        v = v.strip().lower()
        if v and not EMAIL_REGEX.match(v):
            raise ValueError("Invalid email format")
        return v


class DemoClassCreate(BaseModel):
    """Schema for free live demo class reservations."""
    full_name: str = Field(..., min_length=2, max_length=120, description="Full name of student")
    phone: str = Field(..., min_length=7, max_length=25, description="Mobile / WhatsApp contact number")
    email: Optional[str] = Field(default="", description="Student email address (optional)")
    preferred_subject: Optional[str] = Field(
        default=None,
        description="Preferred subject (Data Analytics, Digital Marketing, etc.)"
    )
    course_interest: Optional[str] = Field(
        default="Data Analytics & BI Track (SQL, Python, Power BI)",
        description="Track or program of interest"
    )
    subject_interest: Optional[str] = Field(
        default=None,
        description="Subject interest"
    )
    message: Optional[str] = Field(default="", max_length=2000)
    preferred_schedule: Optional[str] = Field(default="Live Demo Session")
    consent: bool = Field(default=True, description="Consent to be contacted by phone or WhatsApp")
    website_url_hp: Optional[str] = Field(default=None, description="Anti-spam honeypot field")
    source_utm: Optional[str] = Field(default=None, description="Attribution UTM string")
    referrer_url: Optional[str] = Field(default=None, description="Referrer URL")

    @field_validator("website_url_hp")
    @classmethod
    def validate_hp(cls, v) -> Optional[str]:
        if v and str(v).strip():
            raise ValueError("Spam submission detected.")
        return v

    @field_validator("consent", mode="before")
    @classmethod
    def validate_consent(cls, v) -> bool:
        if isinstance(v, str):
            v = v.strip().lower() in ("true", "1", "on", "yes")
        if not bool(v):
            raise ValueError("You must agree to be contacted by phone or WhatsApp about this course.")
        return True

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return ""
        v = v.strip().lower()
        if v and not EMAIL_REGEX.match(v):
            raise ValueError("Invalid email format")
        return v


class LeadMagnetCreate(BaseModel):
    """Schema for free lead magnet asset downloads (cheat sheets, sample datasets)."""
    full_name: str = Field(..., min_length=2, max_length=120, description="Full name of student")
    phone: str = Field(..., min_length=7, max_length=25, description="Mobile / WhatsApp contact number")
    email: Optional[str] = Field(default="", description="Student email address (optional)")
    resource_name: str = Field(..., min_length=2, max_length=150, description="Name of lead magnet asset requested")
    subject_interest: Optional[str] = Field(default="", max_length=100)
    consent: bool = Field(default=True, description="Consent to be contacted by phone or WhatsApp")
    website_url_hp: Optional[str] = Field(default=None, description="Anti-spam honeypot field")
    source_utm: Optional[str] = Field(default=None, description="Attribution UTM string")
    referrer_url: Optional[str] = Field(default=None, description="Referrer URL")

    @field_validator("website_url_hp")
    @classmethod
    def validate_hp(cls, v) -> Optional[str]:
        if v and str(v).strip():
            raise ValueError("Spam submission detected.")
        return v

    @field_validator("consent", mode="before")
    @classmethod
    def validate_consent(cls, v) -> bool:
        if isinstance(v, str):
            v = v.strip().lower() in ("true", "1", "on", "yes")
        if not bool(v):
            raise ValueError("You must agree to be contacted by phone or WhatsApp about this course.")
        return True

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return ""
        v = v.strip().lower()
        if v and not EMAIL_REGEX.match(v):
            raise ValueError("Invalid email format")
        return v


class StudentRegister(BaseModel):
    """Schema for student registration / account creation."""
    full_name: str = Field(..., min_length=2, max_length=120, description="Full name of student")
    phone: str = Field(..., min_length=7, max_length=25, description="Mobile / WhatsApp contact number (mandatory)")
    password: str = Field(..., min_length=6, max_length=100, description="Account password (min 6 chars)")
    email: Optional[str] = Field(default="", description="Email address (strictly optional)")
    user_type: Optional[str] = Field(
        default="student",
        description="Background: student, fresher, working_professional"
    )
    college_or_company: Optional[str] = Field(default="", description="College, university, or company name")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return ""
        v = v.strip().lower()
        if v and not EMAIL_REGEX.match(v):
            raise ValueError("Invalid email format")
        return v


class StudentLogin(BaseModel):
    """Schema for student login via phone or email."""
    identifier: str = Field(..., min_length=3, max_length=150, description="Registered phone number or email")
    password: str = Field(..., min_length=1, description="Account password")


class StudentOut(BaseModel):
    """Safe public representation of a registered student."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    phone: str
    email: Optional[str] = ""
    user_type: str
    college_or_company: Optional[str] = ""
    is_active: bool
    created_at: Optional[str] = None


class ActivityLogCreate(BaseModel):
    """Schema for recording user or guest interaction events."""
    event_type: str = Field(..., description="page_view, note_read, dataset_download, etc.")
    resource_type: Optional[str] = Field(default="general", description="note, viva, dataset, book, project")
    resource_slug: Optional[str] = Field(default="", description="Identifier or slug of resource")
    referrer: Optional[str] = Field(default="", description="Traffic origin or referrer URL")
