from typing import Optional, List
from fastapi import APIRouter, Depends, Request, Query, HTTPException, status
from fastapi.responses import JSONResponse, Response, RedirectResponse
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.apps.courses.database import get_db
from app.apps.courses.schemas import (
    EnquiryCreate,
    BatchRegistrationCreate,
    BatchCreate,
    LeadStatusUpdate,
    LeadOut,
    BatchOut
)
from app.apps.courses.services import (
    init_courses_db,
    create_student_enquiry,
    create_batch_registration,
    list_batches,
    create_batch,
    get_leads,
    get_lead_summary,
    update_lead_status,
    export_leads_csv,
    get_instructor_curriculum_profile
)

router = APIRouter(prefix="/api/courses", tags=["Courses & Admissions"])

# Ensure database tables and initial weekend batch are created on module load
init_courses_db()


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
    Does NOT contain or reveal any course fees.
    """
    return get_instructor_curriculum_profile()


@router.get("/batches", response_model=List[BatchOut], summary="List all active batches")
async def get_active_batches(db: Session = Depends(get_db)):
    """Returns available batches with schedule (Saturday & Sunday 6:00 PM – 8:00 PM IST)."""
    return list_batches(db=db, active_only=True)


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
    No fees required or stored.
    """
    client_ip = request.client.host if request.client else None
    content_type = request.headers.get("content-type", "")

    try:
        if "application/json" in content_type:
            raw_data = await request.json()
            enquiry_obj = EnquiryCreate(**raw_data)
        else:
            form = await request.form()
            enquiry_obj = EnquiryCreate(
                full_name=str(form.get("full_name") or ""),
                email=str(form.get("email") or ""),
                phone=str(form.get("phone") or ""),
                current_status=str(form.get("current_status") or "Working Professional"),
                message=str(form.get("message") or ""),
                preferred_schedule=str(form.get("preferred_schedule") or "Saturday & Sunday 6:00 PM – 8:00 PM IST")
            )
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


@router.post("/register", summary="Register student for the Weekend Data Analysis batch")
async def register_for_batch(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Register student directly into the upcoming weekend Data Analysis batch.
    Classes: Saturday & Sunday only, 6:00 PM to 8:00 PM.
    No fees required on the page.
    """
    client_ip = request.client.host if request.client else None
    content_type = request.headers.get("content-type", "")

    try:
        if "application/json" in content_type:
            raw_data = await request.json()
            reg_obj = BatchRegistrationCreate(**raw_data)
        else:
            form = await request.form()
            batch_id_raw = form.get("batch_id")
            batch_id = int(batch_id_raw) if batch_id_raw and str(batch_id_raw).isdigit() else None
            
            reg_obj = BatchRegistrationCreate(
                full_name=str(form.get("full_name") or ""),
                email=str(form.get("email") or ""),
                phone=str(form.get("phone") or ""),
                batch_id=batch_id,
                current_status=str(form.get("current_status") or "Working Professional"),
                prior_experience=str(form.get("prior_experience") or "Beginner"),
                message=str(form.get("message") or ""),
                preferred_schedule=str(form.get("preferred_schedule") or "Saturday & Sunday 6:00 PM – 8:00 PM IST")
            )
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
        return RedirectResponse(url="/#registration-success", status_code=303)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)


# -------------------------------------------------------------
# Admin & Lead Management Endpoints
# -------------------------------------------------------------

@router.get("/leads", response_model=List[LeadOut], summary="List all student leads and registrations")
async def list_student_leads(
    lead_type: Optional[str] = Query(None, description="'enquiry' or 'batch_registration'"),
    batch_id: Optional[int] = Query(None, description="Filter by batch ID"),
    lead_status: Optional[str] = Query(None, alias="status", description="'new', 'contacted', 'enrolled', 'closed'"),
    search: Optional[str] = Query(None, description="Search by student name, email, or phone"),
    db: Session = Depends(get_db)
):
    """View student leads with filtering for enquiries and batch admissions."""
    return get_leads(
        db=db,
        lead_type=lead_type,
        batch_id=batch_id,
        status=lead_status,
        search=search
    )


@router.get("/leads/summary", summary="Lead pipeline metrics and admission counts")
async def get_leads_summary_stats(db: Session = Depends(get_db)):
    """Retrieve statistical breakdown of enquiries vs registrations."""
    return get_lead_summary(db=db)


@router.get("/leads/export.csv", summary="Export student leads to CSV")
async def export_leads(db: Session = Depends(get_db)):
    """
    Download CSV file of all student registrations and enquiries for spreadsheet analysis.
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
async def get_lead_detail(lead_id: int, db: Session = Depends(get_db)):
    """Retrieve specific student details."""
    from app.apps.courses.models import StudentLead
    lead = db.query(StudentLead).filter(StudentLead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead.to_dict()


@router.patch("/leads/{lead_id}/status", summary="Update lead pipeline status and counselor notes")
async def update_lead_pipeline_status(
    lead_id: int,
    payload: LeadStatusUpdate,
    db: Session = Depends(get_db)
):
    """Update lead status ('contacted', 'enrolled', 'closed') and attach follow-up notes."""
    updated = update_lead_status(db=db, lead_id=lead_id, status_update=payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"success": True, "lead": updated}


@router.post("/batches", response_model=BatchOut, status_code=status.HTTP_201_CREATED, summary="Create a new batch")
async def add_new_batch(payload: BatchCreate, db: Session = Depends(get_db)):
    """Admin endpoint to create a new batch schedule."""
    batch = create_batch(db=db, batch_data=payload)
    return batch.to_dict()
