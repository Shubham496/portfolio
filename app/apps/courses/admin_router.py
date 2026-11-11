from typing import Optional
from fastapi import APIRouter, Depends, Request, Form, Query, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.apps.courses.database import get_db
from app.apps.courses.models import AdminUser, StudentLead
from app.apps.courses.auth import (
    verify_password,
    create_session_token,
    get_current_admin,
    require_admin,
    SESSION_COOKIE_NAME
)
from app.apps.courses.services import get_leads, get_leads_paginated, get_lead_summary, update_lead_status
from app.apps.courses.schemas import LeadStatusUpdate
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
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Protected monitoring dashboard displaying student admissions & enquiries with pagination."""
    pagination = get_leads_paginated(
        db=db,
        lead_type=lead_type if lead_type != "all" else None,
        status=status if status != "all" else None,
        search=search,
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
            "current_page": page,
            "per_page": per_page
        }
    )


@router.post("/leads/{lead_id}/status")
async def admin_update_lead(
    lead_id: int,
    status: str = Form(...),
    admin_notes: Optional[str] = Form(""),
    page: int = Form(1),
    lead_type: str = Form("all"),
    filter_status: str = Form("all"),
    search: Optional[str] = Form(None),
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update lead pipeline stage and notes directly from the dashboard."""
    update_lead_status(
        db=db,
        lead_id=lead_id,
        status_update=LeadStatusUpdate(status=status, admin_notes=admin_notes or "")
    )
    # Redirect preserving current filters and page
    redirect_url = f"/admin/dashboard?page={page}&lead_type={lead_type}&status={filter_status}"
    if search:
        redirect_url += f"&search={search}"
    return RedirectResponse(url=redirect_url, status_code=303)


@router.get("/logout")
async def admin_logout():
    """Clear session cookie and redirect to sign in."""
    response = RedirectResponse(url="/admin/login", status_code=303)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response
