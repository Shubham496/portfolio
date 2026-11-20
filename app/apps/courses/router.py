import time
from collections import defaultdict
from typing import Optional, List, Dict
from fastapi import APIRouter, Depends, Request, Query, HTTPException, status
from fastapi.responses import JSONResponse, Response, RedirectResponse
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.apps.courses.database import get_db
from app.apps.courses.models import Batch, StudentLead, AdminUser
from app.apps.courses.auth import require_admin
from app.apps.courses.schemas import (
    EnquiryCreate,
    BatchRegistrationCreate,
    BatchCreate,
    BatchUpdate,
    LeadStatusUpdate,
    LeadOut,
    BatchOut,
    WaitlistCreate,
    DemoClassCreate,
    LeadMagnetCreate
)
from app.apps.courses.services import (
    init_courses_db,
    create_student_enquiry,
    create_batch_registration,
    create_waitlist_lead,
    create_demo_lead,
    create_lead_magnet_lead,
    list_batches,
    get_grouped_batches,
    create_batch,
    update_batch,
    toggle_batch_active,
    get_leads,
    get_lead_summary,
    update_lead_status,
    export_leads_csv,
    get_instructor_curriculum_profile
)

router = APIRouter(prefix="/api/courses", tags=["Courses & Admissions"])

# Ensure database tables and initial weekend batch are created on module load
init_courses_db()

# In-memory IP rate limiter for public student forms
_RATE_LIMIT_STORE: Dict[str, List[float]] = defaultdict(list)
RATE_LIMIT_MAX = 30  # Max 30 requests per minute per IP
RATE_LIMIT_WINDOW = 60.0  # seconds


def check_submission_rate_limit(request: Request, force: bool = False):
    """Enforce in-memory sliding-window IP rate limiting to prevent spam floods."""
    client_ip = request.client.host if request.client else "unknown"
    if not force and client_ip in ("testclient", "127.0.0.1", "localhost"):
        return
    now = time.time()
    timestamps = [t for t in _RATE_LIMIT_STORE[client_ip] if now - t < RATE_LIMIT_WINDOW]
    if len(timestamps) >= RATE_LIMIT_MAX:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many submission requests. Please wait a minute before trying again."
        )
    timestamps.append(now)
    _RATE_LIMIT_STORE[client_ip] = timestamps


def _format_validation_errors(ve: ValidationError) -> List[dict]:
    """Helper to convert Pydantic validation errors to clean JSON-serializable dictionaries."""
    formatted = []
    for err in ve.errors():
        formatted.append({
            "loc": list(err.get("loc", [])),
            "msg": str(err.get("msg", "")),
            "type": str(err.get("type", ""))
        })
    return formatted


# -------------------------------------------------------------
# Public Endpoints: Batches & Instructor Profile
# -------------------------------------------------------------

@router.get("/instructor", summary="Instructor profile, curriculum, and weekend schedule")
async def get_instructor_details():
    """
    Returns verified instructor profile (Shubham Singh), course syllabus (Python, SQL,
    PowerBI, Excel, Tableau), and weekend schedule (Sat & Sun 6-8 PM).
    """
    return get_instructor_curriculum_profile()


@router.get("/batches", response_model=List[BatchOut], summary="List all active batches")
async def get_active_batches(db: Session = Depends(get_db)):
    """Returns available batches with schedule (Saturday & Sunday 6:00 PM – 8:00 PM IST)."""
    return list_batches(db=db, active_only=True)


@router.get("/batches/grouped", summary="Get batches grouped by track and lifecycle")
async def get_grouped_batches_endpoint(db: Session = Depends(get_db)):
    """Returns batches grouped into data_analytics and digital_marketing with lifecycle stages (enrolling, running, next, past)."""
    return get_grouped_batches(db=db)


@router.get("/batches/{batch_id}", summary="Get specific batch details")
async def get_batch_by_id(batch_id: int, db: Session = Depends(get_db)):
    """Get batch details by ID."""
    from app.apps.courses.models import Batch
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch.to_dict()


# -------------------------------------------------------------
# Student Registrations & Enquiries (JSON & Form Compatible)
# -------------------------------------------------------------

@router.post("/enquiry", summary="Submit a general student enquiry or counseling request")
async def submit_enquiry(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Register a prospective student enquiry.
    Accepts either JSON payload (via AJAX/Fetch) or URL-encoded Form fields.
    """
    check_submission_rate_limit(request)
    client_ip = request.client.host if request.client else None
    content_type = request.headers.get("content-type", "")

    try:
        if "application/json" in content_type:
            raw_data = await request.json()
            if raw_data.get("website_url_hp"):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Spam submission detected.")
            if not raw_data.get("source_utm"):
                raw_data["source_utm"] = request.cookies.get("mythos_utm")
            if not raw_data.get("referrer_url"):
                raw_data["referrer_url"] = request.headers.get("referer")
            enquiry_obj = EnquiryCreate(**raw_data)
        else:
            form = await request.form()
            hp = form.get("website_url_hp")
            if hp and str(hp).strip():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Spam submission detected.")
            raw_consent = form.get("consent")
            consent_flag = raw_consent in ("on", "true", "1", "yes", True) if raw_consent is not None else False
            enquiry_obj = EnquiryCreate(
                full_name=str(form.get("full_name") or ""),
                email=str(form.get("email") or ""),
                phone=str(form.get("phone") or ""),
                current_status=str(form.get("current_status") or "Working Professional"),
                course_interest=str(form.get("course_interest") or "All Programs / Undecided"),
                subject_interest=str(form.get("subject_interest") or ""),
                message=str(form.get("message") or ""),
                preferred_schedule=str(form.get("preferred_schedule") or "Saturday & Sunday 6:00 PM – 8:00 PM IST"),
                consent=consent_flag,
                website_url_hp=str(hp or "") if hp else None,
                source_utm=str(form.get("source_utm") or "") or request.cookies.get("mythos_utm"),
                referrer_url=str(form.get("referrer_url") or "") or request.headers.get("referer")
            )
    except HTTPException:
        raise
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=_format_validation_errors(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

    result = create_student_enquiry(db=db, enquiry=enquiry_obj, client_ip=client_ip)

    # Redirect for browser HTML form posts
    if "text/html" in request.headers.get("accept", "") and "application/json" not in content_type:
        return RedirectResponse(url="/#enquiry-success", status_code=303)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)


@router.post("/register", summary="Register student for an institute cohort")
async def register_for_batch(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Register student directly into an institute cohort.
    """
    check_submission_rate_limit(request)
    client_ip = request.client.host if request.client else None
    content_type = request.headers.get("content-type", "")

    try:
        if "application/json" in content_type:
            raw_data = await request.json()
            if raw_data.get("website_url_hp"):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Spam submission detected.")
            if not raw_data.get("source_utm"):
                raw_data["source_utm"] = request.cookies.get("mythos_utm")
            if not raw_data.get("referrer_url"):
                raw_data["referrer_url"] = request.headers.get("referer")
            reg_obj = BatchRegistrationCreate(**raw_data)
        else:
            form = await request.form()
            hp = form.get("website_url_hp")
            if hp and str(hp).strip():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Spam submission detected.")
            batch_id_raw = form.get("batch_id")
            batch_id = int(batch_id_raw) if batch_id_raw and str(batch_id_raw).isdigit() else None
            raw_consent = form.get("consent")
            consent_flag = raw_consent in ("on", "true", "1", "yes", True) if raw_consent is not None else False
            
            reg_obj = BatchRegistrationCreate(
                full_name=str(form.get("full_name") or ""),
                email=str(form.get("email") or ""),
                phone=str(form.get("phone") or ""),
                batch_id=batch_id,
                course_name=str(form.get("course_name") or "Data Analysis"),
                current_status=str(form.get("current_status") or "Working Professional"),
                prior_experience=str(form.get("prior_experience") or "Beginner"),
                message=str(form.get("message") or ""),
                preferred_schedule=str(form.get("preferred_schedule") or "Saturday & Sunday 6:00 PM – 8:00 PM IST"),
                consent=consent_flag,
                website_url_hp=str(hp or "") if hp else None,
                source_utm=str(form.get("source_utm") or "") or request.cookies.get("mythos_utm"),
                referrer_url=str(form.get("referrer_url") or "") or request.headers.get("referer")
            )
    except HTTPException:
        raise
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=_format_validation_errors(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

    result = create_batch_registration(db=db, reg=reg_obj, client_ip=client_ip)

    if "text/html" in request.headers.get("accept", "") and "application/json" not in content_type:
        return RedirectResponse(url="/registration-success", status_code=303)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)


@router.post("/demo", summary="Reserve seat for upcoming live demo class")
async def submit_demo(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Reserve a seat for the free live weekend demo class.
    Accepts JSON payload or Form fields.
    """
    check_submission_rate_limit(request)
    client_ip = request.client.host if request.client else None
    content_type = request.headers.get("content-type", "")

    try:
        if "application/json" in content_type:
            raw_data = await request.json()
            if raw_data.get("website_url_hp"):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Spam submission detected.")
            if not raw_data.get("source_utm"):
                raw_data["source_utm"] = request.cookies.get("mythos_utm")
            if not raw_data.get("referrer_url"):
                raw_data["referrer_url"] = request.headers.get("referer")
            demo_obj = DemoClassCreate(**raw_data)
        else:
            form = await request.form()
            hp = form.get("website_url_hp")
            if hp and str(hp).strip():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Spam submission detected.")
            raw_consent = form.get("consent")
            consent_flag = raw_consent in ("on", "true", "1", "yes", True) if raw_consent is not None else False
            demo_obj = DemoClassCreate(
                full_name=str(form.get("full_name") or ""),
                phone=str(form.get("phone") or ""),
                email=str(form.get("email") or ""),
                course_interest=str(form.get("course_interest") or form.get("track") or "Data Analytics & BI Track (SQL, Python, Power BI)"),
                subject_interest=str(form.get("subject_interest") or "Live Demo Session"),
                message=str(form.get("message") or ""),
                preferred_schedule=str(form.get("preferred_schedule") or "Free Live Weekend Demo"),
                consent=consent_flag,
                website_url_hp=str(hp or "") if hp else None,
                source_utm=str(form.get("source_utm") or "") or request.cookies.get("mythos_utm"),
                referrer_url=str(form.get("referrer_url") or "") or request.headers.get("referer")
            )
    except HTTPException:
        raise
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=_format_validation_errors(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

    result = create_demo_lead(db=db, demo_data=demo_obj, client_ip=client_ip)

    if "application/json" not in content_type:
        return RedirectResponse(
            url=f"/registration-success?type=demo&track={demo_obj.course_interest}",
            status_code=303
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)


@router.post("/lead-magnet", summary="Download free lead magnet (cheat sheet / clean dataset)")
async def submit_lead_magnet(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Capture student details before downloading a free cheat sheet or practice dataset.
    Accepts JSON or Form data.
    """
    check_submission_rate_limit(request)
    client_ip = request.client.host if request.client else None
    content_type = request.headers.get("content-type", "")

    try:
        if "application/json" in content_type:
            raw_data = await request.json()
            if raw_data.get("website_url_hp"):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Spam submission detected.")
            if not raw_data.get("source_utm"):
                raw_data["source_utm"] = request.cookies.get("mythos_utm")
            if not raw_data.get("referrer_url"):
                raw_data["referrer_url"] = request.headers.get("referer")
            lm_obj = LeadMagnetCreate(**raw_data)
        else:
            form = await request.form()
            hp = form.get("website_url_hp")
            if hp and str(hp).strip():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Spam submission detected.")
            raw_consent = form.get("consent")
            consent_flag = raw_consent in ("on", "true", "1", "yes", True) if raw_consent is not None else False
            lm_obj = LeadMagnetCreate(
                full_name=str(form.get("full_name") or ""),
                phone=str(form.get("phone") or ""),
                email=str(form.get("email") or ""),
                resource_name=str(form.get("resource_name") or "SQL Interview Traps Cheat Sheet (PDF)"),
                subject_interest=str(form.get("subject_interest") or form.get("resource_name") or ""),
                consent=consent_flag,
                website_url_hp=str(hp or "") if hp else None,
                source_utm=str(form.get("source_utm") or "") or request.cookies.get("mythos_utm"),
                referrer_url=str(form.get("referrer_url") or "") or request.headers.get("referer")
            )
    except HTTPException:
        raise
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=_format_validation_errors(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

    result = create_lead_magnet_lead(db=db, lm_data=lm_obj, client_ip=client_ip)

    if "application/json" not in content_type:
        import urllib.parse
        dl_url = result.get("download_url", "/course/syllabus/download")
        encoded_res = urllib.parse.quote(lm_obj.resource_name)
        encoded_dl = urllib.parse.quote(dl_url)
        return RedirectResponse(
            url=f"/registration-success?type=lead_magnet&resource={encoded_res}&download_url={encoded_dl}",
            status_code=303
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)


# -------------------------------------------------------------
# Admin & Lead Management Endpoints (Protected by require_admin)
# -------------------------------------------------------------

@router.get("/leads", response_model=List[LeadOut], summary="List all student leads and registrations")
async def list_student_leads(
    lead_type: Optional[str] = Query(None, description="'enquiry', 'batch_registration', 'demo_class', 'waitlist', 'lead_magnet'"),
    batch_id: Optional[int] = Query(None, description="Filter by batch ID"),
    lead_status: Optional[str] = Query(None, alias="status", description="'new', 'contacted', 'demo_attended', 'enrolled', 'closed', 'do_not_contact'"),
    search: Optional[str] = Query(None, description="Search by student name, email, or phone"),
    traffic_source: Optional[str] = Query(None, description="Filter by UTM or traffic origin"),
    subject_interest: Optional[str] = Query(None, description="Filter by subject or topic interest"),
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """View student leads with filtering for enquiries, demo sessions, and batch admissions (Admin session required)."""
    return get_leads(
        db=db,
        lead_type=lead_type,
        batch_id=batch_id,
        status=lead_status,
        search=search,
        traffic_source=traffic_source,
        subject_interest=subject_interest
    )


@router.get("/leads/summary", summary="Lead pipeline metrics and admission counts")
async def get_leads_summary_stats(
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Retrieve statistical breakdown of enquiries vs registrations (Admin session required)."""
    return get_lead_summary(db=db)


@router.get("/leads/export.csv", summary="Export student leads to CSV")
async def export_leads(
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Download CSV file of all student registrations and enquiries for spreadsheet analysis (Admin session required).
    Defined before /leads/{lead_id} to prevent path collision.
    """
    csv_data = export_leads_csv(db=db)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=student_leads_and_registrations.csv"
        }
    )


@router.get("/leads/{lead_id}", response_model=LeadOut, summary="Retrieve a single lead")
async def get_lead_detail(
    lead_id: int,
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Retrieve specific student details (Admin session required)."""
    lead = db.query(StudentLead).filter(StudentLead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead.to_dict()


@router.patch("/leads/{lead_id}/status", summary="Update lead pipeline status and counselor notes")
async def update_lead_pipeline_status(
    lead_id: int,
    payload: LeadStatusUpdate,
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update lead status ('contacted', 'enrolled', 'closed', 'do_not_contact') and attach follow-up notes (Admin session required)."""
    updated = update_lead_status(db=db, lead_id=lead_id, status_update=payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"success": True, "lead": updated}


@router.post("/waitlist", summary="Join waitlist for upcoming subject or cohort")
async def submit_waitlist(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Register a student waitlist interest for upcoming subjects (e.g. Next Batch in SQL, Excel, Power BI).
    Accepts JSON or Form data.
    """
    check_submission_rate_limit(request)
    client_ip = request.client.host if request.client else None
    content_type = request.headers.get("content-type", "")

    try:
        if "application/json" in content_type:
            raw_data = await request.json()
            if raw_data.get("website_url_hp"):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Spam submission detected.")
            if not raw_data.get("source_utm"):
                raw_data["source_utm"] = request.cookies.get("mythos_utm")
            if not raw_data.get("referrer_url"):
                raw_data["referrer_url"] = request.headers.get("referer")
            waitlist_obj = WaitlistCreate(**raw_data)
        else:
            form = await request.form()
            hp = form.get("website_url_hp")
            if hp and str(hp).strip():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Spam submission detected.")
            raw_consent = form.get("consent")
            consent_flag = raw_consent in ("on", "true", "1", "yes", True) if raw_consent is not None else False
            waitlist_obj = WaitlistCreate(
                full_name=str(form.get("full_name") or ""),
                phone=str(form.get("phone") or ""),
                email=str(form.get("email") or ""),
                subject_interest=str(form.get("subject_interest") or "Next Cohort"),
                message=str(form.get("message") or ""),
                consent=consent_flag,
                website_url_hp=str(hp or "") if hp else None,
                source_utm=str(form.get("source_utm") or "") or request.cookies.get("mythos_utm"),
                referrer_url=str(form.get("referrer_url") or "") or request.headers.get("referer")
            )
    except HTTPException:
        raise
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=_format_validation_errors(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

    result = create_waitlist_lead(db=db, waitlist_data=waitlist_obj, client_ip=client_ip)

    if "application/json" not in content_type:
        return RedirectResponse(
            url=f"/registration-success?type=waitlist&subject={waitlist_obj.subject_interest}",
            status_code=303
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)


@router.post("/batches", response_model=BatchOut, status_code=status.HTTP_201_CREATED, summary="Create a new batch")
async def add_new_batch(
    payload: BatchCreate,
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Admin endpoint to create a new batch schedule (Admin session required)."""
    batch = create_batch(db=db, batch_data=payload)
    return batch.to_dict()


@router.patch("/batches/{batch_id}", response_model=BatchOut, summary="Update batch details")
async def update_existing_batch(
    batch_id: int,
    payload: BatchUpdate,
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Admin endpoint to update batch parameters (Admin session required)."""
    batch = update_batch(db=db, batch_id=batch_id, update_dict=payload.model_dump(exclude_unset=True))
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch.to_dict()
