from typing import Optional
from fastapi import APIRouter, Depends, Request, Form, Query, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.apps.courses.database import get_db
from app.apps.courses.models import AdminUser, StudentLead, Batch
from app.apps.courses.auth import (
    verify_password,
    create_session_token,
    get_current_admin,
    require_admin,
    SESSION_COOKIE_NAME
)
from app.apps.courses.services import (
    get_leads,
    get_leads_paginated,
    get_lead_summary,
    update_lead_status,
    list_batches,
    create_batch,
    update_batch,
    toggle_batch_active
)
from app.apps.courses.schemas import LeadStatusUpdate, BatchCreate, BatchUpdate
from app.core.config import settings

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/admin", tags=["Instructor Admin & Monitoring"])


@router.get("", response_class=HTMLResponse)
async def admin_root():
    """Redirect /admin directly to /admin/dashboard."""
    return RedirectResponse(url="/admin/dashboard", status_code=303)


# -------------------------------------------------------------
# Sign In (Only Login Permitted - Registration Disabled)
# -------------------------------------------------------------

@router.get("/login", response_class=HTMLResponse)
async def admin_login_page(request: Request, db: Session = Depends(get_db)):
    """Render instructor sign in page."""
    admin = get_current_admin(request=request, db=db)
    if admin:
        return RedirectResponse(url="/admin/dashboard", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="admin/login.html",
        context={"settings": settings, "error": None}
    )


@router.post("/login", response_class=HTMLResponse)
async def admin_login_submit(
    request: Request,
    username: Optional[str] = Form(None),
    username_or_email: Optional[str] = Form(None),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Authenticate instructor and create signed session cookie."""
    raw_user = (username or username_or_email or "").strip().lower()
    
    admin = db.query(AdminUser).filter(
        or_(
            AdminUser.username.ilike(raw_user),
            AdminUser.email.ilike(raw_user)
        )
    ).first()

    if not admin or not verify_password(password, admin.hashed_password):
        return templates.TemplateResponse(
            request=request,
            name="admin/login.html",
            context={
                "settings": settings,
                "error": "Invalid username or password. Please try again."
            },
            status_code=401
        )

    response = RedirectResponse(url="/admin/dashboard", status_code=303)
    token = create_session_token(admin_id=admin.id, username=admin.username)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=60 * 60 * 24 * 7,  # 7 days
        samesite="lax",
        secure=False
    )
    return response


# Public registration is strictly disabled
@router.get("/signup")
@router.post("/signup")
async def admin_signup_disabled():
    """Sign up is disabled for security. Only pre-configured admin login is permitted."""
    return RedirectResponse(url="/admin/login", status_code=303)


# -------------------------------------------------------------
# Protected Dashboard & Monitoring
# -------------------------------------------------------------

@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    lead_type: str = Query("all"),
    status: str = Query("all"),
    search: Optional[str] = Query(None),
    traffic_source: str = Query("all"),
    subject_interest: str = Query("all"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Protected monitoring dashboard displaying student admissions, demo requests & enquiries with multi-filters & pagination."""
    pagination = get_leads_paginated(
        db=db,
        lead_type=lead_type if lead_type != "all" else None,
        status=status if status != "all" else None,
        search=search,
        traffic_source=traffic_source if traffic_source != "all" else None,
        subject_interest=subject_interest if subject_interest != "all" else None,
        page=page,
        per_page=per_page
    )
    summary = get_lead_summary(db=db)

    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={
            "settings": settings,
            "admin": admin,
            "leads": pagination["items"],
            "pagination": pagination,
            "summary": summary,
            "current_lead_type": lead_type,
            "current_status": status,
            "current_search": search,
            "current_traffic_source": traffic_source,
            "current_subject_interest": subject_interest,
            "current_page": page,
            "per_page": per_page
        }
    )


@router.post("/leads/{lead_id}/status")
async def admin_update_lead(
    lead_id: int,
    status: str = Form(...),
    admin_notes: Optional[str] = Form(""),
    follow_up_date: Optional[str] = Form(None),
    page: int = Form(1),
    lead_type: str = Form("all"),
    filter_status: str = Form("all"),
    traffic_source: str = Form("all"),
    subject_interest: str = Form("all"),
    search: Optional[str] = Form(None),
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update lead pipeline stage, counselor notes, and follow-up date directly from the dashboard."""
    update_lead_status(
        db=db,
        lead_id=lead_id,
        status_update=LeadStatusUpdate(
            status=status,
            admin_notes=admin_notes or "",
            follow_up_date=follow_up_date
        )
    )
    # Redirect preserving current filters and page
    redirect_url = f"/admin/dashboard?page={page}&lead_type={lead_type}&status={filter_status}&traffic_source={traffic_source}&subject_interest={subject_interest}"
    if search:
        redirect_url += f"&search={search}"
    return RedirectResponse(url=redirect_url, status_code=303)


# -------------------------------------------------------------
# Batch & Cohort Management
# -------------------------------------------------------------

@router.get("/batches", response_class=HTMLResponse)
async def admin_batches_page(
    request: Request,
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Protected cohort & batch management panel for creating, editing, and closing batches."""
    batches = db.query(Batch).order_by(Batch.id.asc()).all()
    batch_dicts = [b.to_dict() for b in batches]
    
    total_batches = len(batch_dicts)
    active_batches = sum(1 for b in batch_dicts if b["is_active"])
    enrolling_batches = sum(1 for b in batch_dicts if b["status"] == "enrolling" and b["is_active"])
    total_registrations = sum(b["total_registrations"] for b in batch_dicts)

    return templates.TemplateResponse(
        request=request,
        name="admin/batches.html",
        context={
            "settings": settings,
            "admin": admin,
            "batches": batch_dicts,
            "summary": {
                "total_batches": total_batches,
                "active_batches": active_batches,
                "enrolling_batches": enrolling_batches,
                "total_registrations": total_registrations
            }
        }
    )


@router.post("/batches/create")
async def admin_create_batch(
    batch_code: str = Form(...),
    title: str = Form(...),
    course_name: str = Form("Data Analysis"),
    track: str = Form("data_analytics"),
    technologies: str = Form("Python, SQL, PowerBI, Excel, Tableau"),
    schedule_days: str = Form("Saturday & Sunday"),
    schedule_time: str = Form("6:00 PM – 8:00 PM IST"),
    start_date: str = Form("Upcoming Weekend"),
    duration: str = Form("8-10 Weeks Hands-On"),
    status: str = Form("enrolling"),
    max_seats: int = Form(25),
    description: Optional[str] = Form(""),
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new training batch schedule directly from the admin panel."""
    payload = BatchCreate(
        batch_code=batch_code.strip(),
        title=title.strip(),
        course_name=course_name.strip(),
        track=track.strip(),
        technologies=technologies.strip(),
        schedule_days=schedule_days.strip(),
        schedule_time=schedule_time.strip(),
        start_date=start_date.strip(),
        duration=duration.strip(),
        status=status.strip(),
        max_seats=max_seats,
        description=(description or "").strip(),
        is_active=True
    )
    create_batch(db=db, batch_data=payload)
    return RedirectResponse(url="/admin/batches", status_code=303)


@router.post("/batches/{batch_id}/update")
async def admin_update_batch(
    batch_id: int,
    title: Optional[str] = Form(None),
    course_name: Optional[str] = Form(None),
    track: Optional[str] = Form(None),
    technologies: Optional[str] = Form(None),
    schedule_days: Optional[str] = Form(None),
    schedule_time: Optional[str] = Form(None),
    start_date: Optional[str] = Form(None),
    duration: Optional[str] = Form(None),
    status: Optional[str] = Form(None),
    max_seats: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update batch parameters, schedule, or lifecycle status."""
    update_dict = {}
    if title is not None:
        update_dict["title"] = title.strip()
    if course_name is not None:
        update_dict["course_name"] = course_name.strip()
    if track is not None:
        update_dict["track"] = track.strip()
    if technologies is not None:
        update_dict["technologies"] = technologies.strip()
    if schedule_days is not None:
        update_dict["schedule_days"] = schedule_days.strip()
    if schedule_time is not None:
        update_dict["schedule_time"] = schedule_time.strip()
    if start_date is not None:
        update_dict["start_date"] = start_date.strip()
    if duration is not None:
        update_dict["duration"] = duration.strip()
    if status is not None:
        update_dict["status"] = status.strip()
    if max_seats is not None:
        update_dict["max_seats"] = max_seats
    if description is not None:
        update_dict["description"] = description.strip()

    update_batch(db=db, batch_id=batch_id, update_dict=update_dict)
    return RedirectResponse(url="/admin/batches", status_code=303)


@router.post("/batches/{batch_id}/toggle-active")
async def admin_toggle_batch_active(
    batch_id: int,
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Toggle active state or archive batch without deleting registrations."""
    toggle_batch_active(db=db, batch_id=batch_id)
    return RedirectResponse(url="/admin/batches", status_code=303)


@router.get("/logout")
async def admin_logout():
    """Clear session cookie and redirect to sign in."""
    response = RedirectResponse(url="/admin/login", status_code=303)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response
