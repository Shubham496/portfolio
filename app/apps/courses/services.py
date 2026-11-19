import os
import csv
import io
import math
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc

from app.apps.courses.database import engine, Base
from app.apps.courses.models import Batch, StudentLead, AdminUser, User, UserActivityLog
from app.apps.courses.schemas import (
    EnquiryCreate,
    BatchRegistrationCreate,
    BatchCreate,
    BatchUpdate,
    LeadStatusUpdate,
    StudentRegister,
    WaitlistCreate,
    DemoClassCreate,
    LeadMagnetCreate,
)
from app.apps.courses.auth import hash_password, verify_password
from app.core.config import settings

logger = logging.getLogger("courses.services")


def mask_phone(phone: Optional[str]) -> str:
    """Mask phone number for privacy in logs (e.g., +91 987****210)."""
    if not phone:
        return ""
    clean = str(phone).strip()
    if len(clean) <= 4:
        return "****"
    return f"{clean[:3]}****{clean[-2:]}"


def mask_email(email: Optional[str]) -> str:
    """Mask email address for privacy in logs (e.g., ro****@example.com)."""
    if not email or "@" not in email:
        return ""
    parts = email.split("@", 1)
    masked = parts[0][:2] + "****" if len(parts[0]) > 2 else "****"
    return f"{masked}@{parts[1]}"


def _run_startup_migrations(bind_engine):
    """Idempotently add new columns to existing tables for SQLite and PostgreSQL."""
    from sqlalchemy import text
    try:
        with bind_engine.connect() as conn:
            # Check consent_given
            try:
                conn.execute(text("SELECT consent_given FROM student_leads LIMIT 1"))
            except Exception:
                try:
                    conn.execute(text("ALTER TABLE student_leads ADD COLUMN consent_given BOOLEAN DEFAULT 1 NOT NULL"))
                    conn.commit()
                    logger.info("Migrated student_leads: added consent_given column.")
                except Exception as e:
                    logger.warning(f"Could not add consent_given column: {e}")
            # Check consent_at
            try:
                conn.execute(text("SELECT consent_at FROM student_leads LIMIT 1"))
            except Exception:
                try:
                    conn.execute(text("ALTER TABLE student_leads ADD COLUMN consent_at TIMESTAMP"))
                    conn.commit()
                    logger.info("Migrated student_leads: added consent_at column.")
                except Exception as e:
                    logger.warning(f"Could not add consent_at column: {e}")
            # Check subject_interest in student_leads
            try:
                conn.execute(text("SELECT subject_interest FROM student_leads LIMIT 1"))
            except Exception:
                try:
                    conn.execute(text("ALTER TABLE student_leads ADD COLUMN subject_interest VARCHAR(100)"))
                    conn.commit()
                    logger.info("Migrated student_leads: added subject_interest column.")
                except Exception as e:
                    logger.warning(f"Could not add subject_interest column: {e}")
            # Check track in batches
            try:
                conn.execute(text("SELECT track FROM batches LIMIT 1"))
            except Exception:
                try:
                    conn.execute(text("ALTER TABLE batches ADD COLUMN track VARCHAR(50) DEFAULT 'data_analytics' NOT NULL"))
                    conn.commit()
                    logger.info("Migrated batches: added track column.")
                except Exception as e:
                    logger.warning(f"Could not add track column: {e}")
            # Check source_utm in student_leads
            try:
                conn.execute(text("SELECT source_utm FROM student_leads LIMIT 1"))
            except Exception:
                try:
                    conn.execute(text("ALTER TABLE student_leads ADD COLUMN source_utm VARCHAR(255)"))
                    conn.commit()
                    logger.info("Migrated student_leads: added source_utm column.")
                except Exception as e:
                    logger.warning(f"Could not add source_utm column: {e}")
            # Check referrer_url in student_leads
            try:
                conn.execute(text("SELECT referrer_url FROM student_leads LIMIT 1"))
            except Exception:
                try:
                    conn.execute(text("ALTER TABLE student_leads ADD COLUMN referrer_url VARCHAR(255)"))
                    conn.commit()
                    logger.info("Migrated student_leads: added referrer_url column.")
                except Exception as e:
                    logger.warning(f"Could not add referrer_url column: {e}")
            # Check follow_up_date in student_leads
            try:
                conn.execute(text("SELECT follow_up_date FROM student_leads LIMIT 1"))
            except Exception:
                try:
                    conn.execute(text("ALTER TABLE student_leads ADD COLUMN follow_up_date DATE"))
                    conn.commit()
                    logger.info("Migrated student_leads: added follow_up_date column.")
                except Exception as e:
                    logger.warning(f"Could not add follow_up_date column: {e}")
    except Exception as exc:
        logger.warning(f"Startup migration check skipped or failed: {exc}")


def init_courses_db():
    """Create courses tables if they don't exist and seed all institute weekend batches."""
    try:
        Base.metadata.create_all(bind=engine)
        _run_startup_migrations(engine)
        logger.info("Course platform tables verified / created.")
        
        # Seed educational institute batches (2 Digital Marketing, 1 Data Analysis)
        from app.apps.courses.database import SessionLocal
        with SessionLocal() as db:
            institute_batches = [
                {
                    "batch_code": "DA-WKND-2026-B1",
                    "title": "Weekend Data Analysis Masterclass",
                    "course_name": "Data Analysis (Python, SQL, PowerBI, Excel, Tableau)",
                    "track": "data_analytics",
                    "technologies": "Python, SQL, PowerBI, Excel, Tableau",
                    "schedule_days": "Saturday & Sunday",
                    "schedule_time": "6:00 PM – 8:00 PM IST",
                    "start_date": "Upcoming Weekend",
                    "duration": "8-10 Weeks Hands-On Mentorship",
                    "status": "enrolling",
                    "max_seats": 25,
                    "description": (
                        "Live interactive weekend training designed for students and working professionals. "
                        "Complete practical curriculum covering Python programming, SQL databases, "
                        "Power BI dashboards, Excel data modeling, and Tableau visual storytelling."
                    ),
                    "is_active": True
                },
                {
                    "batch_code": "DM-PERF-2026-B1",
                    "title": "Performance Marketing & Paid Advertising Masterclass",
                    "course_name": "Digital Marketing: Performance Marketing & Paid Ads",
                    "track": "digital_marketing",
                    "technologies": "Google Ads, Meta Ads, GA4, GTM, Funnel CRO",
                    "schedule_days": "Saturday & Sunday",
                    "schedule_time": "3:00 PM – 5:00 PM IST",
                    "start_date": "Upcoming Weekend",
                    "duration": "8-10 Weeks Hands-On Mentorship",
                    "status": "enrolling",
                    "max_seats": 25,
                    "description": (
                        "Live online cohort covering high-ROI paid traffic campaigns, Meta Ads Manager, "
                        "Google Search & Performance Max ads, Google Analytics 4, Tag Manager, and conversion rate optimization."
                    ),
                    "is_active": True
                },
                {
                    "batch_code": "DM-GROWTH-2026-B1",
                    "title": "SEO, Content Strategy & Social Media Growth Masterclass",
                    "course_name": "Digital Marketing: SEO & Growth Strategy",
                    "track": "digital_marketing",
                    "technologies": "Technical SEO, Semrush, Content Marketing, Social Media, Email Automation",
                    "schedule_days": "Saturday & Sunday",
                    "schedule_time": "11:00 AM – 1:00 PM IST",
                    "start_date": "Upcoming Weekend",
                    "duration": "8-10 Weeks Hands-On Mentorship",
                    "status": "upcoming",
                    "max_seats": 25,
                    "description": (
                        "Full online practical masterclass in technical & on-page SEO, organic search ranking algorithms, "
                        "viral social media storytelling, B2B LinkedIn growth, and lifecycle email marketing automation."
                    ),
                    "is_active": True
                }
            ]

            for b_spec in institute_batches:
                existing = db.query(Batch).filter(Batch.batch_code == b_spec["batch_code"]).first()
                if not existing:
                    db.add(Batch(**b_spec))
                    logger.info(f"Seeded cohort batch {b_spec['batch_code']}.")
                else:
                    # Ensure track and status are synced if needed
                    if not existing.track or existing.track != b_spec["track"]:
                        existing.track = b_spec["track"]
                    if existing.batch_code == "DM-GROWTH-2026-B1" and existing.status == "enrolling":
                        existing.status = "upcoming"
            db.commit()

            # Seed / ensure default 'admin' user exists with updated password from .env
            admin_user = db.query(AdminUser).filter(AdminUser.username == "admin").first()
            env_password = os.getenv("ADMIN_PASSWORD")
            env_hash = os.getenv("ADMIN_PASSWORD_HASH")

            from app.apps.courses.auth import hash_password

            if env_password:
                target_hash = hash_password(env_password)
            elif env_hash:
                target_hash = env_hash
            else:
                target_hash = "$2b$12$uSiwGr.E6jVYlVLLvQmj/exumDJRDsAT2rJH1H.YKjsRGO9YCfJ8e"

            if not admin_user:
                admin_user = AdminUser(
                    username="admin",
                    email="admin@mythostech.in",
                    hashed_password=target_hash,
                    is_active=True
                )
                db.add(admin_user)
                db.commit()
                logger.info("Admin user 'admin' seeded.")
            else:
                if env_password or env_hash:
                    admin_user.hashed_password = target_hash
                    db.commit()

            # Seed / ensure dedicated 'agent_admin' profile exists for agent operations and automated tests
            agent_user = db.query(AdminUser).filter(AdminUser.username == "agent_admin").first()
            agent_password = os.getenv("AGENT_PASSWORD", "hUrHD1qKvVPQqk_y1itG*ISU")
            agent_hash = hash_password(agent_password)

            if not agent_user:
                agent_user = AdminUser(
                    username="agent_admin",
                    email="agent@mythostech.in",
                    hashed_password=agent_hash,
                    is_active=True
                )
                db.add(agent_user)
                db.commit()
                logger.info("Dedicated agent user 'agent_admin' seeded.")
            else:
                agent_user.hashed_password = agent_hash
                db.commit()
    except Exception as e:
        logger.error(f"Error initializing course database: {e}", exc_info=True)


def get_default_active_batch(db: Session) -> Optional[Batch]:
    """Retrieve the primary currently enrolling weekend batch."""
    return db.query(Batch).filter(
        Batch.is_active == True,
        Batch.status == "enrolling"
    ).order_by(Batch.id.asc()).first() or db.query(Batch).filter(Batch.is_active == True).first()


def list_batches(db: Session, active_only: bool = True) -> List[Dict[str, Any]]:
    """List batches with registration stats in ascending order so primary batch is first."""
    query = db.query(Batch)
    if active_only:
        query = query.filter(Batch.is_active == True)
    batches = query.order_by(Batch.id.asc()).all()
    return [b.to_dict() for b in batches]


def get_grouped_batches(db: Session) -> Dict[str, Any]:
    """
    Returns batches categorized by Track and Lifecycle:
    - Tracks: 'data_analytics' vs 'digital_marketing'
    - Lifecycles:
        - enrolling: Now Enrolling
        - running: Running / Ongoing
        - next: Next / Upcoming
        - past: Archived / Completed / Inactive (for collapsed drawer)
    """
    all_batches = db.query(Batch).order_by(Batch.id.asc()).all()
    grouped: Dict[str, Any] = {
        "data_analytics": {
            "title": "Data Analytics & BI Track",
            "enrolling": [],
            "running": [],
            "next": [],
            "past": []
        },
        "digital_marketing": {
            "title": "Digital Marketing Track",
            "enrolling": [],
            "running": [],
            "next": [],
            "past": []
        },
        "all_active": [],
        "all": []
    }

    for b in all_batches:
        b_dict = b.to_dict()
        grouped["all"].append(b_dict)
        if b.is_active:
            grouped["all_active"].append(b_dict)

        track_key = b_dict.get("track") or "data_analytics"
        if track_key not in grouped:
            track_key = "data_analytics"

        status_lower = (b.status or "enrolling").lower().strip()
        if not b.is_active or status_lower in ("completed", "archived", "closed"):
            grouped[track_key]["past"].append(b_dict)
        elif status_lower in ("enrolling", "open"):
            grouped[track_key]["enrolling"].append(b_dict)
        elif status_lower in ("ongoing", "running"):
            grouped[track_key]["running"].append(b_dict)
        elif status_lower in ("upcoming", "next"):
            grouped[track_key]["next"].append(b_dict)
        else:
            grouped[track_key]["enrolling"].append(b_dict)

    return grouped


def create_batch(db: Session, batch_data: BatchCreate) -> Batch:
    """Create a new batch."""
    batch = Batch(**batch_data.model_dump())
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


def update_batch(db: Session, batch_id: int, update_dict: Dict[str, Any]) -> Optional[Batch]:
    """Update existing batch attributes."""
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        return None
    for field, val in update_dict.items():
        if val is not None and hasattr(batch, field):
            setattr(batch, field, val)
    db.commit()
    db.refresh(batch)
    return batch


def toggle_batch_active(db: Session, batch_id: int) -> Optional[Batch]:
    """Toggle active state or archive batch."""
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        return None
    batch.is_active = not batch.is_active
    db.commit()
    db.refresh(batch)
    return batch


def create_demo_lead(
    db: Session,
    demo_data: DemoClassCreate,
    client_ip: Optional[str] = None
) -> Dict[str, Any]:
    """Record a student reservation for a free live demo class."""
    target_batch = None
    kw = (demo_data.course_interest or "").lower()
    if "performance" in kw or "paid" in kw or "meta" in kw:
        target_batch = db.query(Batch).filter(Batch.batch_code == "DM-PERF-2026-B1").first()
    elif "seo" in kw or "growth" in kw or "marketing" in kw:
        target_batch = db.query(Batch).filter(Batch.batch_code == "DM-GROWTH-2026-B1").first()
    else:
        target_batch = db.query(Batch).filter(Batch.batch_code == "DA-WKND-2026-B1").first()

    if not target_batch:
        target_batch = get_default_active_batch(db)

    subj = (
        demo_data.preferred_subject
        or demo_data.subject_interest
        or demo_data.course_interest
        or "Live Demo Session"
    ).strip()
    lead = StudentLead(
        lead_type="demo_class",
        batch_id=target_batch.id if target_batch else None,
        full_name=demo_data.full_name.strip(),
        email=demo_data.email.strip().lower() if demo_data.email else "",
        phone=demo_data.phone.strip(),
        current_status="Demo Student",
        prior_experience=None,
        preferred_schedule=demo_data.preferred_schedule or "Free Live Weekend Demo",
        subject_interest=subj,
        message=demo_data.message.strip() if demo_data.message else f"Free Demo Class reservation: {subj}",
        status="new",
        source_ip=client_ip,
        source_utm=getattr(demo_data, "source_utm", None),
        referrer_url=getattr(demo_data, "referrer_url", None),
        consent_given=bool(demo_data.consent),
        consent_at=datetime.utcnow()
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    return {
        "success": True,
        "message": "Your seat for the free live demo class is confirmed! Meeting link will be delivered via WhatsApp.",
        "lead_id": lead.id,
        "lead_type": lead.lead_type,
        "subject_interest": lead.subject_interest,
        "data": lead.to_dict()
    }


def create_lead_magnet_lead(
    db: Session,
    lm_data: LeadMagnetCreate,
    client_ip: Optional[str] = None
) -> Dict[str, Any]:
    """Record a student lead magnet download request."""
    lead = StudentLead(
        lead_type="lead_magnet",
        batch_id=None,
        full_name=lm_data.full_name.strip(),
        email=lm_data.email.strip().lower() if lm_data.email else "",
        phone=lm_data.phone.strip(),
        current_status="Lead Magnet Reader",
        prior_experience=None,
        preferred_schedule="Self-Paced / Resource Download",
        subject_interest=(lm_data.subject_interest or lm_data.resource_name or "Resource Download").strip(),
        message=f"Lead magnet download request: {lm_data.resource_name}",
        status="new",
        source_ip=client_ip,
        source_utm=getattr(lm_data, "source_utm", None),
        referrer_url=getattr(lm_data, "referrer_url", None),
        consent_given=bool(lm_data.consent),
        consent_at=datetime.utcnow()
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    # Resolve download URL based on resource name
    download_url = "/course/syllabus/download"
    res_lower = lm_data.resource_name.lower()
    if "dataset" in res_lower:
        download_url = "/library/datasets"
    elif "sql" in res_lower or "cheat" in res_lower:
        download_url = "/course/syllabus/download"

    return {
        "success": True,
        "message": f"Your download for '{lm_data.resource_name}' is ready!",
        "lead_id": lead.id,
        "lead_type": lead.lead_type,
        "resource_name": lm_data.resource_name,
        "download_url": download_url,
        "data": lead.to_dict()
    }


def create_waitlist_lead(
    db: Session,
    waitlist_data: WaitlistCreate,
    client_ip: Optional[str] = None
) -> Dict[str, Any]:
    """Record a student waitlist submission for an upcoming subject or cohort."""
    kw = (waitlist_data.subject_interest or "").lower()
    target_batch = None
    if "seo" in kw or "growth" in kw or "content" in kw:
        target_batch = db.query(Batch).filter(Batch.batch_code == "DM-GROWTH-2026-B1").first()
    elif "performance" in kw or "meta" in kw or "google ads" in kw:
        target_batch = db.query(Batch).filter(Batch.batch_code == "DM-PERF-2026-B1").first()
    else:
        target_batch = db.query(Batch).filter(Batch.batch_code == "DA-WKND-2026-B1").first()

    if not target_batch:
        target_batch = get_default_active_batch(db)

    lead = StudentLead(
        lead_type="waitlist",
        batch_id=target_batch.id if target_batch else None,
        full_name=waitlist_data.full_name.strip(),
        email=waitlist_data.email.strip().lower() if waitlist_data.email else "",
        phone=waitlist_data.phone.strip(),
        current_status="Waitlist Student",
        prior_experience=None,
        preferred_schedule="Saturday & Sunday 6:00 PM – 8:00 PM IST",
        subject_interest=waitlist_data.subject_interest.strip(),
        message=waitlist_data.message.strip() if waitlist_data.message else f"Waitlist interest for upcoming {waitlist_data.subject_interest} batch",
        status="new",
        source_ip=client_ip,
        source_utm=getattr(waitlist_data, "source_utm", None),
        referrer_url=getattr(waitlist_data, "referrer_url", None),
        consent_given=bool(waitlist_data.consent),
        consent_at=datetime.utcnow()
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    return {
        "success": True,
        "message": f"You are on the waitlist for {waitlist_data.subject_interest}! We will notify you via WhatsApp as soon as enrollment opens.",
        "lead_id": lead.id,
        "lead_type": lead.lead_type,
        "subject_interest": lead.subject_interest,
        "data": lead.to_dict()
    }


def create_student_enquiry(
    db: Session,
    enquiry: EnquiryCreate,
    client_ip: Optional[str] = None
) -> Dict[str, Any]:
    """Record a student enquiry or counseling request."""
    target_batch = None
    if getattr(enquiry, "course_interest", None):
        kw = enquiry.course_interest.lower()
        if "performance" in kw or "paid" in kw:
            target_batch = db.query(Batch).filter(Batch.batch_code == "DM-PERF-2026-B1").first()
        elif "seo" in kw or "growth" in kw or "content" in kw or "social" in kw:
            target_batch = db.query(Batch).filter(Batch.batch_code == "DM-GROWTH-2026-B1").first()
        elif "data" in kw or "bi" in kw or "python" in kw:
            target_batch = db.query(Batch).filter(Batch.batch_code == "DA-WKND-2026-B1").first()

    if not target_batch:
        target_batch = get_default_active_batch(db)
    
    subj = enquiry.subject_interest.strip() if getattr(enquiry, "subject_interest", None) else (getattr(enquiry, "course_interest", "") or "General Counseling")
    lead = StudentLead(
        lead_type="enquiry",
        batch_id=target_batch.id if target_batch else None,
        full_name=enquiry.full_name.strip(),
        email=enquiry.email.strip().lower() if enquiry.email else "",
        phone=enquiry.phone.strip(),
        current_status=enquiry.current_status,
        prior_experience=None,
        preferred_schedule=enquiry.preferred_schedule or "Saturday & Sunday 6:00 PM – 8:00 PM IST",
        subject_interest=subj,
        message=enquiry.message.strip() if enquiry.message else "",
        status="new",
        source_ip=client_ip,
        source_utm=getattr(enquiry, "source_utm", None),
        referrer_url=getattr(enquiry, "referrer_url", None),
        consent_given=bool(getattr(enquiry, "consent", True)),
        consent_at=datetime.utcnow()
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    
    return {
        "success": True,
        "message": "Your enquiry has been received. Our admissions desk will reach out shortly to discuss syllabus, schedule, and answer your questions.",
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
    """Record a direct batch registration for an institute cohort."""
    target_batch = None
    if reg.batch_id:
        target_batch = db.query(Batch).filter(Batch.id == reg.batch_id, Batch.is_active == True).first()
    elif getattr(reg, "course_name", None):
        kw = reg.course_name.lower()
        if "performance" in kw or "paid" in kw:
            target_batch = db.query(Batch).filter(Batch.batch_code == "DM-PERF-2026-B1").first()
        elif "seo" in kw or "growth" in kw or "content" in kw or "social" in kw:
            target_batch = db.query(Batch).filter(Batch.batch_code == "DM-GROWTH-2026-B1").first()
        elif "data" in kw or "bi" in kw or "python" in kw:
            target_batch = db.query(Batch).filter(Batch.batch_code == "DA-WKND-2026-B1").first()
    
    if not target_batch:
        target_batch = get_default_active_batch(db)

    pref_sched = reg.preferred_schedule
    if not pref_sched and target_batch:
        pref_sched = f"{target_batch.schedule_days} {target_batch.schedule_time}"
    if not pref_sched:
        pref_sched = "Saturday & Sunday 6:00 PM – 8:00 PM IST"

    lead = StudentLead(
        lead_type="batch_registration",
        batch_id=target_batch.id if target_batch else None,
        full_name=reg.full_name.strip(),
        email=reg.email.strip().lower() if reg.email else "",
        phone=reg.phone.strip(),
        current_status=reg.current_status,
        prior_experience=reg.prior_experience,
        preferred_schedule=pref_sched,
        subject_interest=getattr(reg, "course_name", "Data Analysis"),
        message=reg.message.strip() if reg.message else "",
        status="new",
        source_ip=client_ip,
        source_utm=getattr(reg, "source_utm", None),
        referrer_url=getattr(reg, "referrer_url", None),
        consent_given=bool(getattr(reg, "consent", True)),
        consent_at=datetime.utcnow()
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    batch_info = target_batch.to_dict() if target_batch else None

    return {
        "success": True,
        "message": f"Successfully registered for {target_batch.title if target_batch else 'the cohort'}! Classes run Saturday & Sunday.",
        "registration_id": lead.id,
        "lead_type": lead.lead_type,
        "batch": batch_info,
        "schedule": pref_sched,
        "data": lead.to_dict()
    }


def get_leads(
    db: Session,
    lead_type: Optional[str] = None,
    batch_id: Optional[int] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    traffic_source: Optional[str] = None,
    subject_interest: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieve student leads with flexible filtering."""
    query = db.query(StudentLead)

    if lead_type and lead_type != "all":
        query = query.filter(StudentLead.lead_type == lead_type)

    if batch_id:
        query = query.filter(StudentLead.batch_id == batch_id)

    if status and status != "all":
        query = query.filter(StudentLead.status == status)

    if traffic_source and traffic_source != "all":
        query = query.filter(StudentLead.source_utm.ilike(f"%{traffic_source}%"))

    if subject_interest and subject_interest != "all":
        query = query.filter(StudentLead.subject_interest.ilike(f"%{subject_interest}%"))

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                StudentLead.full_name.ilike(search_term),
                StudentLead.email.ilike(search_term),
                StudentLead.phone.ilike(search_term),
                StudentLead.subject_interest.ilike(search_term),
                StudentLead.source_utm.ilike(search_term)
            )
        )

    leads = query.order_by(desc(StudentLead.id)).all()
    return [l.to_dict() for l in leads]


def get_leads_paginated(
    db: Session,
    lead_type: Optional[str] = None,
    batch_id: Optional[int] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    traffic_source: Optional[str] = None,
    subject_interest: Optional[str] = None,
    page: int = 1,
    per_page: int = 10
) -> Dict[str, Any]:
    """Retrieve paginated student leads with filtering and pagination metadata."""
    query = db.query(StudentLead)

    if lead_type and lead_type != "all":
        query = query.filter(StudentLead.lead_type == lead_type)

    if batch_id:
        query = query.filter(StudentLead.batch_id == batch_id)

    if status and status != "all":
        query = query.filter(StudentLead.status == status)

    if traffic_source and traffic_source != "all":
        query = query.filter(StudentLead.source_utm.ilike(f"%{traffic_source}%"))

    if subject_interest and subject_interest != "all":
        query = query.filter(StudentLead.subject_interest.ilike(f"%{subject_interest}%"))

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                StudentLead.full_name.ilike(search_term),
                StudentLead.email.ilike(search_term),
                StudentLead.phone.ilike(search_term),
                StudentLead.subject_interest.ilike(search_term),
                StudentLead.source_utm.ilike(search_term)
            )
        )

    total_count = query.count()
    per_page = max(1, min(per_page, 100))
    total_pages = max(1, math.ceil(total_count / per_page)) if total_count > 0 else 1
    page = max(1, min(page, total_pages)) if total_count > 0 else 1
    offset = (page - 1) * per_page

    leads = query.order_by(desc(StudentLead.id)).offset(offset).limit(per_page).all()

    start_item = offset + 1 if total_count > 0 else 0
    end_item = min(offset + per_page, total_count)

    return {
        "items": [l.to_dict() for l in leads],
        "total": total_count,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "start_item": start_item,
        "end_item": end_item,
        "has_prev": page > 1,
        "has_next": page < total_pages,
        "prev_page": page - 1 if page > 1 else None,
        "next_page": page + 1 if page < total_pages else None,
    }


def classify_lead_source(source_utm: Optional[str], referrer_url: Optional[str]) -> str:
    """Classify lead acquisition traffic into: 'whatsapp', 'google', 'direct', or 'referral'."""
    text = f"{source_utm or ''} {referrer_url or ''}".strip().lower()
    if not text:
        return "direct"
    if "whatsapp" in text or "wa.me" in text:
        return "whatsapp"
    if "google" in text or "organic" in text or "google.com" in text:
        return "google"
    if text in ("direct", "none", "unknown"):
        return "direct"
    return "referral"


def get_lead_summary(db: Session) -> Dict[str, Any]:
    """Provide dashboard analytics for leads and batch admissions."""
    all_leads = db.query(StudentLead).all()
    total = len(all_leads)
    enquiries = len([l for l in all_leads if l.lead_type == "enquiry"])
    registrations = len([l for l in all_leads if l.lead_type == "batch_registration"])
    demo_classes = len([l for l in all_leads if l.lead_type == "demo_class"])
    waitlists = len([l for l in all_leads if l.lead_type == "waitlist"])
    lead_magnets = len([l for l in all_leads if l.lead_type == "lead_magnet"])

    new_count = len([l for l in all_leads if l.status == "new"])
    contacted_count = len([l for l in all_leads if l.status == "contacted"])
    demo_attended_count = len([l for l in all_leads if l.status == "demo_attended"])
    enrolled_count = len([l for l in all_leads if l.status == "enrolled"])
    closed_count = len([l for l in all_leads if l.status == "closed"])
    dnc_count = len([l for l in all_leads if l.status == "do_not_contact"])

    # Executive Funnel Metrics (Task 5.2)
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    weekly_leads = []
    for l in all_leads:
        dt = getattr(l, "created_at", None)
        if dt:
            if isinstance(dt, str):
                try:
                    dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
                except Exception:
                    dt = None
            if dt and dt.tzinfo is not None:
                dt = dt.replace(tzinfo=None)
            if dt and dt >= one_week_ago:
                weekly_leads.append(l)

    active_sample = weekly_leads if weekly_leads else all_leads
    weekly_sources = {"whatsapp": 0, "google": 0, "direct": 0, "referral": 0, "total": len(weekly_leads)}
    for l in active_sample:
        src = classify_lead_source(getattr(l, "source_utm", None), getattr(l, "referrer_url", None))
        weekly_sources[src] += 1
    weekly_sources["total"] = len(weekly_leads)

    denom = max(sum(weekly_sources[s] for s in ("whatsapp", "google", "direct", "referral")), 1)
    weekly_sources_pct = {
        s: round((weekly_sources[s] / denom) * 100, 1) for s in ("whatsapp", "google", "direct", "referral")
    }

    demo_registrants = demo_classes
    demo_attended = len([l for l in all_leads if l.status == "demo_attended" or (l.lead_type == "demo_class" and l.status == "enrolled")])
    demo_attendance_rate = round((demo_attended / max(demo_registrants, 1)) * 100, 1) if demo_registrants > 0 else 0.0

    cohort_conversion_rate = round((enrolled_count / max(total, 1)) * 100, 1) if total > 0 else 0.0
    batch_conversion_rate = round((enrolled_count / max(registrations, 1)) * 100, 1) if registrations > 0 else 0.0

    funnel = {
        "weekly_sources": weekly_sources,
        "weekly_sources_pct": weekly_sources_pct,
        "demo_registrants": demo_registrants,
        "demo_attended": demo_attended,
        "demo_attendance_rate": demo_attendance_rate,
        "total_enrolled": enrolled_count,
        "cohort_conversion_rate": cohort_conversion_rate,
        "batch_conversion_rate": batch_conversion_rate,
    }

    return {
        "total_leads": total,
        "enquiries": enquiries,
        "batch_registrations": registrations,
        "demo_classes": demo_classes,
        "waitlists": waitlists,
        "lead_magnets": lead_magnets,
        "new": new_count,
        "contacted": contacted_count,
        "demo_attended": demo_attended_count,
        "enrolled": enrolled_count,
        "closed": closed_count,
        "do_not_contact": dnc_count,
        "funnel": funnel,
        "weekly_sources": weekly_sources,
        "cohort_conversion_rate": cohort_conversion_rate,
        "demo_attendance_rate": demo_attendance_rate,
    }


def update_lead_status(
    db: Session,
    lead_id: int,
    status_update: LeadStatusUpdate
) -> Optional[Dict[str, Any]]:
    """Update pipeline status, internal notes, and follow-up date for a lead."""
    lead = db.query(StudentLead).filter(StudentLead.id == lead_id).first()
    if not lead:
        return None

    lead.status = status_update.status
    if status_update.admin_notes is not None:
        lead.admin_notes = status_update.admin_notes
    if getattr(status_update, "follow_up_date", None) is not None:
        val = str(status_update.follow_up_date).strip()
        if val:
            try:
                lead.follow_up_date = datetime.strptime(val, "%Y-%m-%d").date()
            except Exception:
                pass
        else:
            lead.follow_up_date = None

    db.commit()
    db.refresh(lead)
    return lead.to_dict()


def export_leads_csv(db: Session) -> str:
    """Generate a clean CSV string containing all student leads, demo requests, and registrations."""
    leads = db.query(StudentLead).order_by(desc(StudentLead.id)).all()

    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "ID",
        "Type",
        "Batch Title",
        "Batch Code",
        "Subject Interest",
        "Full Name",
        "Email",
        "Phone",
        "Current Status",
        "Prior Experience",
        "Schedule",
        "Traffic Source / UTM",
        "Referrer URL",
        "Follow-Up Date",
        "Message / Questions",
        "Status",
        "Admin Notes",
        "Consent Given",
        "Consent At",
        "Submitted At"
    ])

    for l in leads:
        writer.writerow([
            l.id,
            l.lead_type,
            l.batch.title if l.batch else "General",
            l.batch.batch_code if l.batch else "-",
            l.subject_interest or "",
            l.full_name,
            l.email,
            l.phone,
            l.current_status or "",
            l.prior_experience or "",
            l.preferred_schedule or "",
            l.source_utm or "",
            l.referrer_url or "",
            l.follow_up_date.isoformat() if l.follow_up_date else "",
            l.message or "",
            l.status,
            l.admin_notes or "",
            "Yes" if l.consent_given else "No",
            l.consent_at.strftime("%Y-%m-%d %H:%M:%S") if l.consent_at else "",
            l.created_at.strftime("%Y-%m-%d %H:%M:%S") if l.created_at else ""
        ])

    return output.getvalue()


def get_instructor_curriculum_profile() -> Dict[str, Any]:
    """
    Returns structured data about the educational institute, curriculum, and schedules.
    """
    # 6 Data Analysis Modules
    da_modules = [
        {
            "module": "Excel Advanced Modeling, Power Query & VBA",
            "badge": "Spreadsheets & Automation",
            "icon": "excel",
            "topics": [
                "Advanced Formulas: XLOOKUP, INDEX/MATCH, Dynamic Arrays",
                "Pivot Tables, Slicers & Executive Pivot Charts",
                "Power Query Editor: Multi-file Ingestion & ETL Cleansing",
                "VBA & Macro Automation for Routine Reporting"
            ],
            "detailed_sections": [
                {
                    "title": "Power Query Editor & ETL",
                    "bullets": [
                        "Connecting to multiple CSVs, Excels, and folder directories",
                        "Unpivoting cross-tabulated data into normalized rows",
                        "Custom & conditional columns, data type casting, error handling",
                        "Merging queries (VLOOKUP replacement) & Append queries (stacking datasets)",
                        "Automated data refreshes without manual copy-pasting"
                    ]
                },
                {
                    "title": "VBA & Macro Automation",
                    "bullets": [
                        "Recording and editing macros for repetitive weekly tasks",
                        "VBA core syntax: Subroutines, Variables, For/While Loops, If-Then logic",
                        "Building User Defined Functions (UDFs) for proprietary business formulas",
                        "Automating one-click workbook report generation and formatting"
                    ]
                },
                {
                    "title": "Advanced Formula Engineering & What-If",
                    "bullets": [
                        "Dynamic Arrays: FILTER, UNIQUE, SORT, XLOOKUP, XMATCH",
                        "Modern formulas: LET (named variables) & LAMBDA custom reusable logic",
                        "Nested conditionals: SUMIFS, COUNTIFS, AVERAGEIFS, IFS, SWITCH",
                        "What-If Analysis: Goal Seek, Data Tables, Scenario Manager, Sensitivity modeling"
                    ]
                },
                {
                    "title": "Data Cleansing & Executive Dashboards",
                    "bullets": [
                        "Text wrangling: TEXTSPLIT, SUBSTITUTE, TRIM, Flash Fill",
                        "Data validation rules, custom dropdown lists, IFERROR sanitization",
                        "Multi-slicer linked dashboards with dynamic KPI cards & sparklines"
                    ]
                }
            ]
        },
        {
            "module": "SQL for Data Analysis & Relational Databases",
            "badge": "Database Architecture",
            "icon": "sql",
            "topics": [
                "Relational Database Architecture & 3NF Normalization",
                "Complex Multi-Table JOINs & Nested Subqueries",
                "Analytical Window Functions (RANK, DENSE_RANK, ROW_NUMBER)",
                "Common Table Expressions (CTEs) & Query Optimization"
            ],
            "detailed_sections": [
                {
                    "title": "Analytical Window Functions Deep-Dive",
                    "bullets": [
                        "Ranking metrics: ROW_NUMBER, RANK, DENSE_RANK, NTILE",
                        "Lead & Lag analysis: Comparing period-over-period sales without self-joins",
                        "Cumulative statistics: Running totals, moving averages with window frames",
                        "Frame specifications: ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW"
                    ]
                },
                {
                    "title": "CTEs & Advanced Query Structuring",
                    "bullets": [
                        "Common Table Expressions (WITH clauses) for modular SQL architecture",
                        "Correlated subqueries vs Non-correlated subqueries",
                        "Recursive CTEs for hierarchical organizational trees & bill-of-materials",
                        "Complex aggregations: GROUP BY, HAVING, GROUPING SETS, ROLLUP, CUBE"
                    ]
                },
                {
                    "title": "Relational Modeling & Schema Design",
                    "bullets": [
                        "Primary keys, Foreign keys, Composite keys, Unique constraints, Cascading",
                        "Database normalization principles: 1NF, 2NF, 3NF design",
                        "Entity Relationship Diagrams (ERD) & schema mapping"
                    ]
                },
                {
                    "title": "Performance Tuning & Business Analytics Queries",
                    "bullets": [
                        "B-Tree indexing strategies, composite indexes, avoiding table scans",
                        "Query execution analysis using EXPLAIN and EXPLAIN ANALYZE",
                        "Real business queries: Cohort retention analysis, customer churn velocity, active users"
                    ]
                }
            ]
        },
        {
            "module": "Python for Data Analysis & Automation",
            "badge": "Core Programming & ETL",
            "icon": "python",
            "topics": [
                "Python Foundations, Control Flow & Data Structures",
                "High-Performance NumPy Array Matrix Computing",
                "Pandas DataFrames Manipulation & Multi-Source Cleansing",
                "Automated Data Extraction & Production Scripting"
            ],
            "detailed_sections": [
                {
                    "title": "Pandas Data Wrangling Masterclass",
                    "bullets": [
                        "DataFrame indexing, slicing, boolean filtering, query() method",
                        "High-performance vector operations: apply(), map(), transform()",
                        "Reshaping datasets: pivot_table(), melt(), stack(), unstack()",
                        "Multi-level GroupBy aggregations and statistical summarization",
                        "Merging, joining, and concatenating heterogeneous sources"
                    ]
                },
                {
                    "title": "Data Sanitization & Missing Value Handling",
                    "bullets": [
                        "Detecting, imputing, and dropping null values (isna, fillna, dropna)",
                        "Vectorized string manipulation (.str methods) and Regex extraction",
                        "Datetime parsing, time-series resampling, and business calendars"
                    ]
                },
                {
                    "title": "NumPy Matrix Operations & Mathematics",
                    "bullets": [
                        "Creating and reshaping 1D, 2D, and 3D ndarrays",
                        "Broadcasting rules, boolean masking, fast numerical filtering",
                        "Vectorized mathematical computations & statistical arrays"
                    ]
                },
                {
                    "title": "Data Visualization & Scripted Automation",
                    "bullets": [
                        "Visualizing distributions, correlations & outliers with Matplotlib & Seaborn",
                        "Connecting Python to SQL databases via SQLAlchemy & psycopg2",
                        "Automating batch CSV/Excel processing and scheduling pipeline execution"
                    ]
                }
            ]
        },
        {
            "module": "Power BI Interactive Business Intelligence",
            "badge": "Enterprise BI & Modeling",
            "icon": "powerbi",
            "topics": [
                "Power Query ETL Ingestion & Data Transformation",
                "Star Schema Relational Data Modeling & Cardinality",
                "Advanced DAX Measures & Time Intelligence Calculations",
                "Executive KPI Dashboards, Bookmarks & Drill-Throughs"
            ],
            "detailed_sections": [
                {
                    "title": "Data Modeling & Power Query ETL",
                    "bullets": [
                        "Power Query data shaping, unpivoting, merging queries, column profiling",
                        "Star Schema vs Snowflake Schema: Fact tables vs Dimension tables",
                        "Managing 1-to-Many and Many-to-Many relationships, active vs inactive (USERELATIONSHIP)",
                        "Designing robust calendar tables for enterprise time-series"
                    ]
                },
                {
                    "title": "Advanced DAX Measures & Virtual Tables",
                    "bullets": [
                        "Evaluation contexts: Row context, Filter context, Context transition",
                        "Core DAX functions: CALCULATE, FILTER, ALL, ALLEXCEPT, VALUES, RELATED, RELATEDTABLE",
                        "Virtual table manipulation: SUMMARIZE, ADDCOLUMNS, GENERATE",
                        "Safe numerical calculations using DIVIDE, COALESCE, SELECTEDVALUE"
                    ]
                },
                {
                    "title": "Time Intelligence Calculations",
                    "bullets": [
                        "Year-to-Date (YTD), Quarter-to-Date (QTD), Month-to-Date (MTD)",
                        "Period-over-period comparisons: SAMEPERIODLASTYEAR, DATEADD, PARALLELPERIOD",
                        "Rolling metrics: 30-day moving averages and trailing 12-month metrics"
                    ]
                },
                {
                    "title": "Executive Visual Storytelling & UX",
                    "bullets": [
                        "Building interactive drill-through pages and custom tooltip report pages",
                        "Interactive UI bookmarks, buttons, slicer panels, dynamic measure selectors",
                        "Designing responsive executive dashboard layouts optimized for leadership"
                    ]
                }
            ]
        },
        {
            "module": "Tableau Visual Storytelling & Dashboards",
            "badge": "Visual Analytics",
            "icon": "tableau",
            "topics": [
                "Connecting to Files, Cloud Databases & Live Extracts",
                "Visual Dimensions vs Measures & Granularity Controls",
                "Level of Detail (LOD) Calculations (FIXED, INCLUDE, EXCLUDE)",
                "Interactive Storyboards, Dynamic Actions & Cloud Publishing"
            ],
            "detailed_sections": [
                {
                    "title": "LOD Expressions & Advanced Calculations",
                    "bullets": [
                        "Level of Detail (LOD) calculations: FIXED, INCLUDE, EXCLUDE syntax",
                        "Calculating customer lifetime value and first-purchase cohorts with LODs",
                        "Table calculations: Percent of total, running total, rank, difference from previous",
                        "Dynamic parameters, parameter actions, and calculated field logic"
                    ]
                },
                {
                    "title": "Interactive Actions & Dashboard Architecture",
                    "bullets": [
                        "Filter actions, highlight actions, set actions, and URL external actions",
                        "Creating collapsible containers, custom navigation buttons, dynamic icons",
                        "Geographic mapping with latitude/longitude, spatial data, and regional layers"
                    ]
                },
                {
                    "title": "Advanced Chart Types & Visual Best Practices",
                    "bullets": [
                        "Dual-axis combination charts, Pareto charts, waterfall charts, donut charts",
                        "Cognitive design: Color theory, visual hierarchy, avoiding chart clutter",
                        "Formatting guidelines for C-level executive consumption"
                    ]
                },
                {
                    "title": "Storyboarding & Tableau Public Portfolio",
                    "bullets": [
                        "Building multi-chapter story points presenting narrative business insights",
                        "Extract performance tuning, dashboard latency optimization",
                        "Publishing interactive web portfolios on Tableau Public"
                    ]
                }
            ]
        },
        {
            "module": "Career Acceleration: GitHub, Resume & LinkedIn Setup",
            "badge": "Job Readiness & Portfolio",
            "icon": "career",
            "topics": [
                "GitHub Portfolio Setup & Open-Source Code Architecture",
                "ATS-Compliant Data Analyst Resume Engineering",
                "LinkedIn Profile Optimization & Inbound Recruiter Strategy",
                "1-on-1 Mock Technical Interviews & Live SQL Screenings"
            ],
            "detailed_sections": [
                {
                    "title": "GitHub Portfolio Architecture",
                    "bullets": [
                        "Setting up a clean, professional GitHub developer profile with profile README",
                        "Git version control fundamentals: commits, branching, pushing repository updates",
                        "Writing production-grade README.md files: Problem statements, architecture schemas, key insights, screenshots",
                        "Hosting 3+ complete capstone portfolios with downloadable data dictionaries"
                    ]
                },
                {
                    "title": "ATS-Optimized Tech Resume Building",
                    "bullets": [
                        "Line-by-line resume engineering specifically for Data Analyst & BI roles",
                        "Quantifiable business impact formula: Action + Tool + Business Result (e.g., 'Reduced query latency by 45%')",
                        "Strategic technical keyword placement to pass automated ATS recruiter screeners",
                        "Removing rookie formatting flaws and organizing technical skills hierarchy"
                    ]
                },
                {
                    "title": "LinkedIn Personal Branding & Inbound Networking",
                    "bullets": [
                        "High-converting profile headline, about section, and featured portfolio media",
                        "Documenting learning in public: Sharing live dashboard demos and SQL insights",
                        "High-response direct messaging templates for reaching hiring managers and team leads",
                        "Leveraging alumni networks and technical community groups for interview referrals"
                    ]
                },
                {
                    "title": "Mock Technical Interviews & Capstone Deployment",
                    "bullets": [
                        "Live timed SQL query solving on CoderPad & HackerRank under interview pressure",
                        "Python data wrangling live screening challenges using Pandas & NumPy",
                        "Dashboard defense: Answering business stakeholder questions on DAX logic and metrics",
                        "Publishing live web-accessible dashboards on Power BI Service and Tableau Public"
                    ]
                }
            ]
        }
    ]

    # Digital Marketing 1: Performance Marketing & Paid Advertising
    dm_perf_modules = [
        {
            "module": "Performance Marketing Core & Funnel Economics",
            "badge": "Paid Acquisition Foundations",
            "icon": "target",
            "topics": [
                "Unit Economics: CAC, LTV, ROAS, AOV & Contribution Margins",
                "Full-Funnel Paid Acquisition Frameworks (TOF, MOF, BOF)",
                "Tracking Infrastructure: Pixels, CAPI, UTM Taxonomy & Attribution",
                "Competitor Creative & Offer Tear-Downs via Ad Libraries"
            ],
            "detailed_sections": [
                {
                    "title": "Funnel Economics & Metrics Calculation",
                    "bullets": [
                        "Calculating break-even ROAS and maximum allowable CPA across product categories",
                        "Structuring Top of Funnel (TOF), Middle of Funnel (MOF), and Bottom of Funnel (BOF)",
                        "Understanding first-click, last-click, linear, and data-driven attribution models",
                        "Designing UTM tracking conventions for clean cross-channel analytics reporting"
                    ]
                },
                {
                    "title": "Direct Response Offer Engineering",
                    "bullets": [
                        "Constructing high-converting irresistible offers and risk-reversal guarantees",
                        "Pricing psychology, bundle architecture, and bump offer optimization",
                        "Auditing competitor ad copy, angles, and positioning in Meta Ad Library"
                    ]
                }
            ]
        },
        {
            "module": "Meta Ads Masterclass (Facebook & Instagram Advertising)",
            "badge": "Paid Social & Scaling",
            "icon": "share-2",
            "topics": [
                "Meta Ads Manager Architecture & Account Governance",
                "Campaign Budget Optimization (CBO) vs Ad Set Budget (ABO)",
                "Dynamic Creative Testing (DCT) & Hook Permutation Frameworks",
                "Server-Side Conversions API (CAPI) & Custom Audience Retargeting"
            ],
            "detailed_sections": [
                {
                    "title": "Campaign Structure & Creative Testing",
                    "bullets": [
                        "Broad targeting vs Interest stacking vs 1%-5% Lookalike audience strategy",
                        "Dynamic Creative Testing (DCT) matrix: 3 Hooks x 2 Bodies x 2 Visuals",
                        "User-Generated Content (UGC), founder stories, and product demonstration formats",
                        "Mitigating ad fatigue with creative sprint cycles and hook iteration"
                    ]
                },
                {
                    "title": "Retargeting & Audience Workflows",
                    "bullets": [
                        "Building custom audiences: 30-day website visitors, video 50%+ viewers, add-to-carts",
                        "Dynamic Product Ads (DPA) catalog integration for Shopify & WooCommerce",
                        "Exclusion lists and frequency capping rules to prevent budget cannibalization"
                    ]
                }
            ]
        },
        {
            "module": "Google Ads Search, Display & Performance Max (PMax)",
            "badge": "High-Intent Paid Search",
            "icon": "search",
            "topics": [
                "Google Ads Architecture & Intent-Based Keyword Research",
                "Broad, Phrase & Exact Match Keyword Grouping Strategies",
                "Responsive Search Ads (RSA) Copywriting & Ad Assets",
                "Performance Max (PMax) Campaigns & Smart Bidding Strategies"
            ],
            "detailed_sections": [
                {
                    "title": "Search Network Mastery & Quality Score",
                    "bullets": [
                        "Negative keyword master lists to eliminate wasted spend and unqualified clicks",
                        "Boosting Quality Score: Ad relevance, expected CTR, and landing page alignment",
                        "Ad extensions & assets: Sitelinks, callouts, structured snippets, lead form assets"
                    ]
                },
                {
                    "title": "Performance Max (PMax) & Bidding Algorithms",
                    "bullets": [
                        "Building asset groups with high-converting imagery, video, and headlines",
                        "Audience signals: Customer match lists, custom intent search queries",
                        "Target CPA (tCPA), Target ROAS (tROAS), and Maximize Conversions bidding triggers"
                    ]
                }
            ]
        },
        {
            "module": "Web Analytics, GA4 & Google Tag Manager (GTM)",
            "badge": "Tracking & Measurement",
            "icon": "bar-chart-2",
            "topics": [
                "Google Tag Manager (GTM) Container Setup & Data Layer Architecture",
                "GA4 Event-Based Data Model & Custom Dimensions / Metrics",
                "E-Commerce Purchase Tracking, Cart Additions & Checkout Steps",
                "Custom Exploration Reports: Funnel Exploration & Path Analysis"
            ],
            "detailed_sections": [
                {
                    "title": "GTM Tags, Triggers & Variables",
                    "bullets": [
                        "Deploying Meta Pixel, Google Ads Conversion Tags, and GA4 Configuration via GTM",
                        "Configuring scroll depth triggers, outbound click listeners, and form submissions",
                        "Testing events with GTM Preview Mode and GA4 DebugView"
                    ]
                },
                {
                    "title": "GA4 Advanced Funnels & Reporting",
                    "bullets": [
                        "Building custom checkout funnel exploration reports to locate drop-off points",
                        "Cross-channel attribution analysis: Discovering assisted conversions",
                        "Exporting GA4 events to BigQuery for automated custom reporting"
                    ]
                }
            ]
        },
        {
            "module": "Landing Page Engineering & Conversion Rate Optimization (CRO)",
            "badge": "CRO & Copywriting",
            "icon": "layout",
            "topics": [
                "Above-The-Fold Architecture & Conversion Visual Hierarchy",
                "Direct-Response Copywriting: AIDA, PAS & Emotional Triggers",
                "Heatmap & Session Replay Analysis (Clarity / Hotjar)",
                "Scientific A/B Split Testing & Statistical Significance"
            ],
            "detailed_sections": [
                {
                    "title": "Landing Page UX & Mobile Optimization",
                    "bullets": [
                        "Speed optimization: Image compression, zero CLS, sub-2-second mobile load time",
                        "Form design: Minimizing friction, multi-step forms, micro-commitments",
                        "Social proof placement: Trust badges, real reviews, case study video embeds"
                    ]
                },
                {
                    "title": "Scientific Split Testing",
                    "bullets": [
                        "Formulating data-backed A/B testing hypotheses based on session recordings",
                        "Testing single elements: Headline hooks, CTA button copy, pricing displays",
                        "Calculating sample sizes and statistical significance thresholds"
                    ]
                }
            ]
        },
        {
            "module": "Budget Scaling, Ad Spend Simulation & Capstone Campaign",
            "badge": "Live Execution & Capstone",
            "icon": "zap",
            "topics": [
                "Vertical vs Horizontal Budget Scaling Playbooks",
                "Creative Fatigue Mitigation & Rapid Ad Iteration Sprints",
                "Compliance, Policy Adherence & Ad Account Security",
                "End-to-End Multi-Channel E-Commerce Paid Campaign Capstone"
            ],
            "detailed_sections": [
                {
                    "title": "Budget Scaling & Account Safeguards",
                    "bullets": [
                        "The 20% incremental scaling rule vs intraday surge budget management",
                        "Horizontal scaling: Duplicating top performers into new lookalikes and interest buckets",
                        "Compliance rules: Avoiding common triggers for Meta/Google account suspensions"
                    ]
                },
                {
                    "title": "Capstone Ad Campaign Presentation",
                    "bullets": [
                        "Building an end-to-end multi-channel campaign strategy for a real brand",
                        "Designing ad creatives, writing sales copy, setting up GA4 events, and projecting ROAS",
                        "Presenting the campaign strategy to faculty panel and peer marketers"
                    ]
                }
            ]
        }
    ]

    # Digital Marketing 2: SEO, Content Strategy & Social Media Growth
    dm_growth_modules = [
        {
            "module": "Inbound Marketing & Organic Acquisition Foundations",
            "badge": "Organic Foundations",
            "icon": "compass",
            "topics": [
                "The Inbound Marketing Flywheel vs Outbound Interruption",
                "Search Engine Crawling, Indexing & Ranking Mechanisms",
                "Search Intent Classification: Informational, Navigational, Commercial, Transactional",
                "Google E-E-A-T Quality Guidelines & Brand Topical Authority"
            ],
            "detailed_sections": [
                {
                    "title": "How Search Engines Work",
                    "bullets": [
                        "Googlebot architecture: Rendering DOM, JavaScript indexing, mobile-first index",
                        "Topical authority: Why niche depth beats broad, shallow content",
                        "Demonstrating Experience, Expertise, Authoritativeness, and Trust (E-E-A-T)"
                    ]
                },
                {
                    "title": "Audience Persona & Competitor Audits",
                    "bullets": [
                        "Mapping customer pain points to high-value organic search queries",
                        "Using Semrush & Ahrefs to identify competitor top-performing pages and traffic sources"
                    ]
                }
            ]
        },
        {
            "module": "Keyword Intelligence, Semantic SEO & Topic Clusters",
            "badge": "Keyword Engineering",
            "icon": "cpu",
            "topics": [
                "Long-Tail Keyword Discovery via Search Console & Intent Tools",
                "Keyword Clustering & Topic Pillar Silo Architecture",
                "SERP Feature Targeting: Featured Snippets, PAA & Knowledge Panels",
                "Content Gap Identification: Uncovering Zero-Competition Queries"
            ],
            "detailed_sections": [
                {
                    "title": "Keyword Clustering & Semantic Search",
                    "bullets": [
                        "Grouping thousands of search queries by semantic intent and entity relevance",
                        "Designing hub-and-spoke pillar pages with structured internal links",
                        "Optimizing content for Google's Natural Language Processing (NLP) models"
                    ]
                },
                {
                    "title": "SERP Real Estate Domination",
                    "bullets": [
                        "Structuring tables, bullet points, and definitions to win Position 0 featured snippets",
                        "Optimizing for People Also Ask (PAA) accordions and FAQ schema embeds"
                    ]
                }
            ]
        },
        {
            "module": "Technical SEO, Core Web Vitals & Schema Markup",
            "badge": "Technical SEO",
            "icon": "code",
            "topics": [
                "Full Technical Site Auditing with Screaming Frog",
                "Indexation Control: Robots.txt, Canonical Tags, XML Sitemaps",
                "Core Web Vitals Optimization: LCP, INP, and CLS Benchmarks",
                "Structured Data Engineering: JSON-LD Schemas for Articles, FAQs & Products"
            ],
            "detailed_sections": [
                {
                    "title": "Crawl Budget & Technical Hygiene",
                    "bullets": [
                        "Locating and fixing crawl errors, 404s, redirect chains, and duplicate URLs",
                        "Configuring canonical tags, hreflang for multi-region, and clean URL permalinks",
                        "Log file analysis: Monitoring search engine bot visits and crawl frequency"
                    ]
                },
                {
                    "title": "Speed & Rich Snippets",
                    "bullets": [
                        "Compressing WebP/AVIF images, minifying CSS/JS, and setting browser caching headers",
                        "Hand-crafting Schema.org JSON-LD structured data to trigger rich stars and FAQ badges"
                    ]
                }
            ]
        },
        {
            "module": "High-Converting Content Marketing & Copywriting",
            "badge": "Content Strategy",
            "icon": "edit-3",
            "topics": [
                "Editorial Calendar Management & Content Production Frameworks",
                "High-Ranking SEO Long-Form Article Writing Frameworks",
                "High-Value Lead Magnets: Guides, Toolkits, Cheatsheets & Free Audits",
                "Content Repurposing: Turning 1 Core Piece into 15 Social Posts"
            ],
            "detailed_sections": [
                {
                    "title": "Content Creation & On-Page SEO",
                    "bullets": [
                        "Drafting comprehensive content that satisfies intent better than top 3 competitors",
                        "Strategic keyword placement: Title tag, H1-H3 headers, meta descriptions, image alt text",
                        "Formatting for digital readability: Short paragraphs, callout quotes, custom diagrams"
                    ]
                },
                {
                    "title": "Lead Magnet Funnel Architecture",
                    "bullets": [
                        "Designing downloadable assets that compel visitors to exchange email addresses",
                        "Setting up automated instant delivery and thank-you onboarding pages"
                    ]
                }
            ]
        },
        {
            "module": "Organic Social Media Growth (LinkedIn, Instagram & Video)",
            "badge": "Social Growth & Branding",
            "icon": "users",
            "topics": [
                "B2B LinkedIn Personal Branding & Thought Leadership Playbooks",
                "Instagram Organic Reach: Reels, Carousels & Engagement Loops",
                "YouTube Search Optimization: High-CTR Thumbnails, Titles & Hooks",
                "Community Building: Transforming Casual Followers into Brand Advocates"
            ],
            "detailed_sections": [
                {
                    "title": "LinkedIn Inbound Engine",
                    "bullets": [
                        "Optimizing personal profiles into high-converting landing pages",
                        "Crafting scroll-stopping text hooks, visual PDF carousels, and case studies",
                        "Outbound DM connection strategies for networking and agency client acquisition"
                    ]
                },
                {
                    "title": "Short-Form Video & YouTube SEO",
                    "bullets": [
                        "Scripting viral 30-60 second Reels, Shorts, and TikToks with tight pacing",
                        "Optimizing YouTube long-form videos with timestamp chapters, tags, and cards"
                    ]
                }
            ]
        },
        {
            "module": "Email Marketing Automation & Inbound Growth Capstone",
            "badge": "Lifecycle & Capstone",
            "icon": "mail",
            "topics": [
                "Email Platform Setup (Klaviyo / ConvertKit / Mailchimp)",
                "Automated Nurture Sequences: Welcome Series, Drips, Re-engagement",
                "Deliverability Mastery: SPF, DKIM, DMARC & Inbox Placement",
                "Full 0-to-50K Monthly Organic Traffic Playbook Capstone"
            ],
            "detailed_sections": [
                {
                    "title": "Email Sequences & Automation Rules",
                    "bullets": [
                        "5-part welcome email sequence that builds trust and introduces core offerings",
                        "Behavioral segmentation based on link clicks, purchases, and engagement history",
                        "A/B testing email subject lines, preview text, and send time optimization"
                    ]
                },
                {
                    "title": "Organic Growth Strategy Capstone",
                    "bullets": [
                        "Developing an end-to-end 6-month organic growth roadmap for a chosen business",
                        "Auditing technical health, mapping keyword clusters, and planning content output",
                        "Presenting the complete inbound roadmap and projected organic traffic growth"
                    ]
                }
            ]
        }
    ]

    all_institute_courses = [
        {
            "id": "dm-perf",
            "code": "DM-PERF-2026-B1",
            "name": "Digital Marketing: Performance Marketing & Paid Ads",
            "short_name": "Performance Marketing",
            "category": "Digital Marketing",
            "tagline": "Master High-ROI Paid Acquisition, Meta & Google Ads, and Conversion Funnels",
            "badge": "Paid Media & ROAS",
            "icon": "target",
            "duration": "8–10 Weeks (Live Online)",
            "schedule": {
                "days": "Saturday & Sunday",
                "timings": "3:00 PM – 5:00 PM IST",
                "frequency": "Weekend live online cohort (2 hours/day)"
            },
            "tools": ["Meta Ads", "Google Ads", "GA4", "Google Tag Manager", "Funnel CRO", "Canva"],
            "highlights": [
                "Meta Ads Manager: Broad vs Interest vs Lookalike CAPI Workflows",
                "Google Search, Performance Max (PMax) & YouTube Bidding Systems",
                "Server-Side Tagging & Google Analytics 4 (GA4) Funnel Tracking",
                "Landing Page A/B Testing, Hook Copywriting & ROAS Scaling Frameworks"
            ],
            "syllabus_modules": dm_perf_modules
        },
        {
            "id": "dm-growth",
            "code": "DM-GROWTH-2026-B1",
            "name": "Digital Marketing: SEO, Content Strategy & Social Media Growth",
            "short_name": "SEO & Growth Strategy",
            "category": "Digital Marketing",
            "tagline": "Build Organic Inbound Engines, Search Authority, and Viral Social Proof",
            "badge": "Organic & Inbound Growth",
            "icon": "trending-up",
            "duration": "8–10 Weeks (Live Online)",
            "schedule": {
                "days": "Saturday & Sunday",
                "timings": "11:00 AM – 1:00 PM IST",
                "frequency": "Weekend live online cohort (2 hours/day)"
            },
            "tools": ["Technical SEO", "Semrush / Ahrefs", "Google Search Console", "Content Marketing", "LinkedIn", "Email Automation"],
            "highlights": [
                "Technical SEO Auditing: Crawl Budgets, Core Web Vitals, Schema JSON-LD",
                "Semantic Keyword Clustering & Topic Pillar Architecture",
                "High-Converting Direct Copywriting & Lead Magnet Funnels",
                "Organic LinkedIn & Instagram Growth Algorithms & Email Drip Automation"
            ],
            "syllabus_modules": dm_growth_modules
        },
        {
            "id": "da-core",
            "code": "DA-WKND-2026-B1",
            "name": "Data Analysis & Business Intelligence Masterclass",
            "short_name": "Data Analytics & BI",
            "category": "Data Analytics",
            "tagline": "Enterprise Data Pipelines, Advanced Relational SQL & Interactive Dashboards",
            "badge": "Data Systems & BI",
            "icon": "database",
            "duration": "8–10 Weeks (Live Online)",
            "schedule": {
                "days": "Saturday & Sunday",
                "timings": "6:00 PM – 8:00 PM IST",
                "frequency": "Weekend live online cohort (2 hours/day)"
            },
            "tools": ["Python", "SQL", "PowerBI", "Excel", "Tableau"],
            "highlights": [
                "Excel Advanced Modeling: Power Query Multi-File ETL & VBA Macro Automation",
                "Relational SQL Architecture: Window Functions, CTEs, 3NF & Query Tuning",
                "Python Data Wrangling: Vectorized Pandas, NumPy Arrays & Automated Ingestion",
                "Power BI & Tableau Storyboarding: Fact/Dim Star Schemas, DAX & LOD Calculations"
            ],
            "syllabus_modules": da_modules
        }
    ]

    return {
        "institute": {
            "name": "MYTHOS Online Institute",
            "tagline": "Premier Live Online Educational Institute",
            "description": (
                "Mythos is a full online educational institute delivering rigorous live cohort programs in "
                "Digital Marketing (Performance Marketing, Paid Ads, SEO, Content Growth) and "
                "Data Analytics (Python, SQL, Power BI, Excel, Tableau). 100% online, live faculty mentorship."
            ),
            "phone": settings.BUSINESS_WHATSAPP,
            "email": settings.BUSINESS_EMAIL,
            "whatsapp": settings.whatsapp_url
        },
        "instructor": {
            "name": settings.OWNER_NAME,
            "title": settings.OWNER_TITLE,
            "bio": settings.OWNER_BIO,
            "experience_highlights": [
                "Live Online Faculty Mentorship: Digital Marketing & Data Analytics Cohorts",
                "Real Industry Simulations: Live Paid Ad Spends, GA4 Tracking & Multi-Source SQL Data Warehouses",
                f"Career Acceleration: {settings.TRUST_CLAIM} with ATS Resumes & Portfolios"
            ],
            "phone": settings.BUSINESS_WHATSAPP,
            "email": settings.BUSINESS_EMAIL,
            "linkedin": settings.LINKEDIN_URL,
            "github": settings.GITHUB_URL
        },
        "courses": all_institute_courses,
        "course": {
            "name": "Complete Data Analysis Masterclass",
            "tools": ["Python", "SQL", "PowerBI", "Excel", "Tableau"],
            "schedule": {
                "days": "Saturday & Sunday only",
                "timings": "6:00 PM – 8:00 PM IST",
                "frequency": "Weekend only (2 hours/day, 4 hours/week)"
            },
            "syllabus_modules": da_modules,
            "fees": None
        }
    }



def generate_syllabus_html_brochure() -> str:
    """Generate a clean, standalone, printable syllabus brochure HTML document."""
    profile = get_instructor_curriculum_profile()
    instructor = profile["instructor"]
    course = profile["course"]
    modules = course["syllabus_modules"]

    modules_html = ""
    for i, m in enumerate(modules, start=1):
        topics_li = "".join([f"<li style='margin-bottom:6px;'>• {t}</li>" for t in m["topics"]])
        modules_html += f"""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:18px; margin-bottom:14px; page-break-inside:avoid;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
                <span style="background:#2563eb; color:#ffffff; font-weight:bold; font-size:12px; width:24px; height:24px; border-radius:6px; display:inline-flex; align-items:center; justify-content:center;">{i}</span>
                <h3 style="margin:0; font-size:15px; font-weight:700; color:#0f172a;">{m['module']}</h3>
            </div>
            <ul style="margin:0; padding-left:18px; font-size:13px; color:#475569; line-height:1.6;">
                {topics_li}
            </ul>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Complete Data Analysis Masterclass Syllabus | MYTHOS</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 40px 20px;
            background-color: #ffffff;
            color: #0f172a;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .header {{
            border-bottom: 2px solid #2563eb;
            padding-bottom: 20px;
            margin-bottom: 25px;
        }}
        .badge {{
            display: inline-block;
            background: #dbeafe;
            color: #1e40af;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 9999px;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .schedule-box {{
            background: #0f172a;
            color: #ffffff;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .footer {{
            border-top: 1px solid #e2e8f0;
            margin-top: 30px;
            padding-top: 15px;
            font-size: 12px;
            color: #64748b;
            text-align: center;
        }}
        @media print {{
            body {{ padding: 0; }}
            .no-print {{ display: none; }}
            .schedule-box {{ background: #1e293b !important; -webkit-print-color-adjust: exact; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="no-print" style="margin-bottom:20px; text-align:right;">
            <button onclick="window.print()" style="background:#2563eb; color:#fff; border:none; padding:8px 16px; border-radius:8px; font-weight:600; cursor:pointer;">
                🖨️ Print / Save as PDF
            </button>
        </div>

        <div class="header">
            <span class="badge">Official Course Curriculum</span>
            <h1 style="margin:0 0 6px 0; font-size:28px; font-weight:800; color:#0f172a;">Complete Data Analysis Masterclass</h1>
            <p style="margin:0; font-size:14px; color:#475569;">
                Comprehensive Hands-On Mentorship: <strong>Python, SQL, Power BI, Excel & Tableau</strong>
            </p>
            <p style="margin:4px 0 0 0; font-size:13px; color:#64748b;">
                Mentorship: <strong>{instructor['name']}</strong> · {instructor['title']}
            </p>
        </div>

        <div class="schedule-box">
            <div>
                <div style="font-size:11px; text-transform:uppercase; color:#94a3b8; font-weight:600;">Fixed Batch Schedule</div>
                <div style="font-size:16px; font-weight:bold; color:#ffffff; margin-top:2px;">Saturday & Sunday Only</div>
            </div>
            <div>
                <div style="font-size:11px; text-transform:uppercase; color:#94a3b8; font-weight:600;">Timings</div>
                <div style="font-size:16px; font-weight:bold; color:#60a5fa; margin-top:2px;">6:00 PM – 8:00 PM IST</div>
            </div>
            <div>
                <div style="font-size:11px; text-transform:uppercase; color:#94a3b8; font-weight:600;">Duration</div>
                <div style="font-size:16px; font-weight:bold; color:#ffffff; margin-top:2px;">8–10 Weeks (Live Online)</div>
            </div>
        </div>

        <h2 style="font-size:18px; font-weight:700; margin-bottom:14px; color:#0f172a;">Course Syllabus by Module</h2>
        {modules_html}

        <div style="background:#f1f5f9; border-radius:12px; padding:18px; margin-top:20px;">
            <h3 style="margin:0 0 8px 0; font-size:14px; font-weight:700;">Mentorship & Hands-On Projects</h3>
            <p style="margin:0; font-size:13px; color:#475569; line-height:1.6;">
                Every module includes hands-on industry datasets (E-commerce retail, financial transactions, marketing analytics). 
                Students graduate with end-to-end portfolio projects ready for resume and LinkedIn showcase.
            </p>
        </div>

        <div class="footer">
            <p style="margin:0 0 4px 0;">Admissions & Mentorship Desk: Phone/WhatsApp: {instructor['phone']} · Email: {instructor['email']}</p>
            <p style="margin:0;">© 2026 MYTHOS. Weekend Data Analysis Mentorship Program.</p>
        </div>
    </div>
</body>
</html>"""
    return html


# ═══════════════════════════════════════════════════════════════════════════════
# STUDENT USER SERVICES & ACTIVITY TRACKING ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def register_student(db: Session, student_in: StudentRegister) -> User:
    """
    Registers a new student, fresher, or professional on the platform.
    Phone is mandatory & unique. Email is optional.
    """
    clean_phone = student_in.phone.strip()
    
    # 1. Check duplicate phone
    existing_phone = db.query(User).filter(User.phone == clean_phone).first()
    if existing_phone:
        raise ValueError("A student with this phone/WhatsApp number is already registered.")

    # 2. Check duplicate email (if provided)
    clean_email = student_in.email.strip().lower() if student_in.email else None
    if clean_email:
        existing_email = db.query(User).filter(User.email == clean_email).first()
        if existing_email:
            raise ValueError("A student with this email address is already registered.")

    # 3. Hash password and persist
    new_user = User(
        full_name=student_in.full_name.strip(),
        phone=clean_phone,
        email=clean_email if clean_email else None,
        hashed_password=hash_password(student_in.password),
        user_type=student_in.user_type or "student",
        college_or_company=student_in.college_or_company.strip() if student_in.college_or_company else None,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"New student registered successfully: id={new_user.id}, phone={mask_phone(new_user.phone)}")
    return new_user


def authenticate_student(db: Session, identifier: str, password: str) -> Optional[User]:
    """
    Authenticates a student by either their registered Phone or Email.
    Returns User if valid credentials and active, else None.
    """
    ident = identifier.strip()
    if not ident or not password:
        return None

    # Query by phone or email
    if "@" in ident:
        user = db.query(User).filter(User.email == ident.lower(), User.is_active == True).first()
    else:
        user = db.query(User).filter(User.phone == ident, User.is_active == True).first()

    if not user:
        return None

    if verify_password(password, user.hashed_password):
        return user

    return None


def log_user_activity(
    db: Session,
    session_id: str,
    event_type: str,
    user_id: Optional[int] = None,
    resource_type: Optional[str] = "general",
    resource_slug: Optional[str] = None,
    referrer: Optional[str] = None,
    ip_address: Optional[str] = None,
) -> UserActivityLog:
    """
    Records an engagement event (page_view, note_read, dataset_download, cohort_apply_click).
    Works for both logged-in students and anonymous guests.
    """
    try:
        activity = UserActivityLog(
            user_id=user_id,
            session_id=session_id or "anonymous",
            event_type=event_type,
            resource_type=resource_type,
            resource_slug=resource_slug,
            referrer=referrer[:250] if referrer else None,
            ip_address=ip_address[:45] if ip_address else None,
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity
    except Exception as e:
        db.rollback()
        logger.warning(f"Failed to record activity log: {e}")
        return None


def link_guest_activities_to_user(db: Session, session_id: str, user_id: int) -> int:
    """
    Links past anonymous guest activities to a newly registered or authenticated student.
    Returns number of records updated.
    """
    if not session_id or not user_id:
        return 0
    try:
        updated = db.query(UserActivityLog).filter(
            UserActivityLog.session_id == session_id,
            UserActivityLog.user_id.is_(None)
        ).update({"user_id": user_id}, synchronize_session=False)
        db.commit()
        return updated
    except Exception as e:
        db.rollback()
        logger.warning(f"Failed to link guest activities: {e}")
        return 0


def get_student_activities(db: Session, user_id: int, limit: int = 20) -> List[UserActivityLog]:
    """Retrieve recent activity history for a student."""
    return db.query(UserActivityLog).filter(
        UserActivityLog.user_id == user_id
    ).order_by(desc(UserActivityLog.created_at)).limit(limit).all()
