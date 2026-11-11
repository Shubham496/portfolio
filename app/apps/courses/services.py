import csv
import io
import logging
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc

from app.apps.courses.database import engine, Base
from app.apps.courses.models import Batch, StudentLead
from app.apps.courses.schemas import (
    EnquiryCreate,
    BatchRegistrationCreate,
    BatchCreate,
    LeadStatusUpdate
)
from app.core.config import settings

logger = logging.getLogger("courses.services")


def init_courses_db():
    """Create courses tables if they don't exist and seed the default weekend batch."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Course platform tables verified / created.")
        
        # Seed default weekend Data Analysis batch if none exists
        from app.apps.courses.database import SessionLocal
        with SessionLocal() as db:
            existing_batch = db.query(Batch).filter(Batch.is_active == True).first()
            if not existing_batch:
                default_batch = Batch(
                    batch_code="DA-WKND-2026-B1",
                    title="Weekend Data Analysis Masterclass",
                    course_name="Data Analysis (Python, SQL, PowerBI, Excel, Tableau)",
                    technologies="Python, SQL, PowerBI, Excel, Tableau",
                    schedule_days="Saturday & Sunday",
                    schedule_time="6:00 PM – 8:00 PM IST",
                    start_date="Upcoming Weekend",
                    duration="8-10 Weeks Hands-On Mentorship",
                    status="enrolling",
                    max_seats=25,
                    description=(
                        "Live interactive weekend training designed for students and working professionals. "
                        "Complete practical curriculum covering Python programming, SQL databases, "
                        "Power BI dashboards, Excel data modeling, and Tableau visual storytelling."
                    ),
                    is_active=True
                )
                db.add(default_batch)
                db.commit()
                logger.info("Default Weekend Data Analysis batch seeded.")
    except Exception as e:
        logger.error(f"Error initializing course database: {e}", exc_info=True)


def get_default_active_batch(db: Session) -> Optional[Batch]:
    """Retrieve the primary currently enrolling weekend batch."""
    return db.query(Batch).filter(
        Batch.is_active == True,
        Batch.status == "enrolling"
    ).order_by(desc(Batch.id)).first() or db.query(Batch).filter(Batch.is_active == True).first()


def list_batches(db: Session, active_only: bool = True) -> List[Dict[str, Any]]:
    """List batches with registration stats."""
    query = db.query(Batch)
    if active_only:
        query = query.filter(Batch.is_active == True)
    batches = query.order_by(desc(Batch.id)).all()
    return [b.to_dict() for b in batches]


def create_batch(db: Session, batch_data: BatchCreate) -> Batch:
    """Create a new batch."""
    batch = Batch(**batch_data.model_dump())
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


def create_student_enquiry(
    db: Session,
    enquiry: EnquiryCreate,
    client_ip: Optional[str] = None
) -> Dict[str, Any]:
    """Record a general student enquiry or counseling request."""
    # Associate with default weekend batch if available
    default_batch = get_default_active_batch(db)
    
    lead = StudentLead(
        lead_type="enquiry",
        batch_id=default_batch.id if default_batch else None,
        full_name=enquiry.full_name.strip(),
        email=enquiry.email.strip().lower(),
        phone=enquiry.phone.strip(),
        current_status=enquiry.current_status,
        prior_experience=None,
        preferred_schedule=enquiry.preferred_schedule or "Saturday & Sunday 6:00 PM – 8:00 PM IST",
        message=enquiry.message.strip() if enquiry.message else "",
        status="new",
        source_ip=client_ip
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    
    return {
        "success": True,
        "message": "Your enquiry has been received. Shubham will reach out shortly to discuss syllabus, schedule, and answer your questions.",
        "lead_id": lead.id,
        "lead_type": lead.lead_type,
        "schedule": lead.preferred_schedule,
        "data": lead.to_dict()
    }


def create_batch_registration(
    db: Session,
    reg: BatchRegistrationCreate,
    client_ip: Optional[str] = None
) -> Dict[str, Any]:
    """Record a direct batch registration for the Weekend Data Analysis class."""
    target_batch = None
    if reg.batch_id:
        target_batch = db.query(Batch).filter(Batch.id == reg.batch_id, Batch.is_active == True).first()
    
    if not target_batch:
        target_batch = get_default_active_batch(db)

    lead = StudentLead(
        lead_type="batch_registration",
        batch_id=target_batch.id if target_batch else None,
        full_name=reg.full_name.strip(),
        email=reg.email.strip().lower(),
        phone=reg.phone.strip(),
        current_status=reg.current_status,
        prior_experience=reg.prior_experience,
        preferred_schedule=reg.preferred_schedule or "Saturday & Sunday 6:00 PM – 8:00 PM IST",
        message=reg.message.strip() if reg.message else "",
        status="new",
        source_ip=client_ip
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    batch_info = target_batch.to_dict() if target_batch else None

    return {
        "success": True,
        "message": f"Successfully registered for the Weekend Data Analysis batch! Classes run Saturday & Sunday from 6:00 PM to 8:00 PM.",
        "registration_id": lead.id,
        "lead_type": lead.lead_type,
        "batch": batch_info,
        "schedule": "Saturday & Sunday 6:00 PM – 8:00 PM IST",
        "data": lead.to_dict()
    }


def get_leads(
    db: Session,
    lead_type: Optional[str] = None,
    batch_id: Optional[int] = None,
    status: Optional[str] = None,
    search: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieve student leads with flexible filtering."""
    query = db.query(StudentLead)

    if lead_type and lead_type != "all":
        query = query.filter(StudentLead.lead_type == lead_type)

    if batch_id:
        query = query.filter(StudentLead.batch_id == batch_id)

    if status and status != "all":
        query = query.filter(StudentLead.status == status)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                StudentLead.full_name.ilike(search_term),
                StudentLead.email.ilike(search_term),
                StudentLead.phone.ilike(search_term)
            )
        )

    leads = query.order_by(desc(StudentLead.id)).all()
    return [l.to_dict() for l in leads]


def get_lead_summary(db: Session) -> Dict[str, Any]:
    """Provide dashboard analytics for leads and batch admissions."""
    all_leads = db.query(StudentLead).all()
    total = len(all_leads)
    enquiries = len([l for l in all_leads if l.lead_type == "enquiry"])
    registrations = len([l for l in all_leads if l.lead_type == "batch_registration"])
    new_count = len([l for l in all_leads if l.status == "new"])
    contacted_count = len([l for l in all_leads if l.status == "contacted"])
    enrolled_count = len([l for l in all_leads if l.status == "enrolled"])

    return {
        "total_leads": total,
        "enquiries": enquiries,
        "batch_registrations": registrations,
        "new": new_count,
        "contacted": contacted_count,
        "enrolled": enrolled_count,
    }


def update_lead_status(
    db: Session,
    lead_id: int,
    status_update: LeadStatusUpdate
) -> Optional[Dict[str, Any]]:
    """Update pipeline status and internal notes for a lead."""
    lead = db.query(StudentLead).filter(StudentLead.id == lead_id).first()
    if not lead:
        return None

    lead.status = status_update.status
    if status_update.admin_notes is not None:
        lead.admin_notes = status_update.admin_notes

    db.commit()
    db.refresh(lead)
    return lead.to_dict()


def export_leads_csv(db: Session) -> str:
    """Generate a clean CSV string containing all enquiries and batch registrations."""
    leads = db.query(StudentLead).order_by(desc(StudentLead.id)).all()

    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "ID",
        "Type",
        "Batch Title",
        "Batch Code",
        "Full Name",
        "Email",
        "Phone",
        "Current Status",
        "Prior Experience",
        "Schedule",
        "Message / Questions",
        "Status",
        "Admin Notes",
        "Submitted At"
    ])

    for l in leads:
        writer.writerow([
            l.id,
            l.lead_type,
            l.batch.title if l.batch else "General",
            l.batch.batch_code if l.batch else "-",
            l.full_name,
            l.email,
            l.phone,
            l.current_status or "",
            l.prior_experience or "",
            l.preferred_schedule or "",
            l.message or "",
            l.status,
            l.admin_notes or "",
            l.created_at.strftime("%Y-%m-%d %H:%M:%S") if l.created_at else ""
        ])

    return output.getvalue()


def get_instructor_curriculum_profile() -> Dict[str, Any]:
    """
    Returns structured data about the instructor, curriculum, and schedule.
    Explicitly enforces NO fee mention.
    """
    return {
        "instructor": {
            "name": settings.OWNER_NAME,
            "title": "Lead Python & Data Architecture Consultant | Technical Instructor",
            "bio": (
                "Lead Consultant and Instructor with deep production experience across enterprise data pipelines, "
                "relational databases, and executive BI dashboards. Mentored 120+ developers and students in practical, "
                "hands-on Python, SQL, Power BI, Excel modeling, and Tableau."
            ),
            "experience_highlights": [
                "Lead Python & Data Architecture Consultant at Ducat (Mentored 120+ senior developers & data engineers)",
                "Data Analyst & Automation Engineer at LNP Infotech (U.S. financial & compliance transaction analysis)",
                "Data Analyst & Technical Instructor at Netmax Technologies (Enterprise ETL, SQL, and Power BI dashboards)"
            ],
            "phone": settings.OWNER_PHONE,
            "email": settings.EMAIL,
            "linkedin": settings.LINKEDIN_URL,
            "github": settings.GITHUB_URL
        },
        "course": {
            "name": "Complete Data Analysis Masterclass",
            "tools": ["Python", "SQL", "PowerBI", "Excel", "Tableau"],
            "schedule": {
                "days": "Saturday & Sunday only",
                "timings": "6:00 PM – 8:00 PM IST",
                "frequency": "Weekend only (2 hours/day, 4 hours/week)"
            },
            "syllabus_modules": [
                {
                    "module": "Excel Advanced Modeling",
                    "topics": ["Advanced Formulas (XLOOKUP, INDEX/MATCH)", "Pivot Tables & Pivot Charts", "Data Validation & Cleansing", "What-If Analysis & Financial Modeling"]
                },
                {
                    "module": "SQL (Structured Query Language)",
                    "topics": ["Relational Database Design", "Multi-table Complex JOINs", "Window Functions (RANK, DENSE_RANK, ROW_NUMBER)", "CTEs & Subqueries", "Aggregations & Grouping Sets"]
                },
                {
                    "module": "Python for Data Analysis",
                    "topics": ["Python Foundations & Data Structures", "NumPy Numerical Computing", "Pandas DataFrames & Manipulation", "Cleaning Missing/Duplicate Data", "Automated Scripting & File Processing"]
                },
                {
                    "module": "Power BI Interactive Dashboards",
                    "topics": ["Power Query ETL Transformation", "Star Schema Data Modeling", "DAX Measures & Calculated Columns", "Executive KPI Dashboards & Drill-throughs"]
                },
                {
                    "module": "Tableau Visual Analytics",
                    "topics": ["Connecting to Diverse Data Sources", "Visual Best Practices & Chart Types", "Calculated Fields & Parameters", "Storyboards & Interactive Visualizations"]
                }
            ],
            "fees": None  # Explicitly None - NO fees on page
        }
    }
