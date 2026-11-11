from typing import Optional
from fastapi import APIRouter, Depends, Request, Form, Query, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.apps.courses.database import get_db
from app.apps.courses.models import AdminUser, StudentLead
from app.apps.courses.auth import (
    hash_password,
    verify_password,
    create_session_token,
    get_current_admin,
    require_admin,
    SESSION_COOKIE_NAME
)
from app.apps.courses.services import get_leads, get_lead_summary, update_lead_status
from app.apps.courses.schemas import LeadStatusUpdate
from app.core.config import settings

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/admin", tags=["Instructor Admin & Monitoring"])


@router.get("", response_class=HTMLResponse)
async def admin_root():
    """Redirect /admin directly to /admin/dashboard."""
    return RedirectResponse(url="/admin/dashboard", status_code=303)


# -------------------------------------------------------------
# Sign In
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
    username_or_email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Authenticate instructor and create signed session cookie."""
    query_val = username_or_email.strip().lower()
    admin = db.query(AdminUser).filter(
        or_(
            AdminUser.username.ilike(query_val),
            AdminUser.email.ilike(query_val)
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
        secure=False  # True in strict HTTPS production if desired
    )
    return response


# -------------------------------------------------------------
# Sign Up
# -------------------------------------------------------------

@router.get("/signup", response_class=HTMLResponse)
async def admin_signup_page(request: Request, db: Session = Depends(get_db)):
    """Render instructor sign up page."""
    admin = get_current_admin(request=request, db=db)
    if admin:
        return RedirectResponse(url="/admin/dashboard", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="admin/signup.html",
        context={"settings": settings, "error": None}
    )


@router.post("/signup", response_class=HTMLResponse)
async def admin_signup_submit(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Register a new instructor account."""
    clean_username = username.strip().lower()
    clean_email = email.strip().lower()

    if password != confirm_password:
        return templates.TemplateResponse(
            request=request,
            name="admin/signup.html",
            context={"settings": settings, "error": "Passwords do not match."}
        )

    if len(password) < 6:
        return templates.TemplateResponse(
            request=request,
            name="admin/signup.html",
            context={"settings": settings, "error": "Password must be at least 6 characters."}
        )

    # Check for existing user
    existing = db.query(AdminUser).filter(
        or_(
            AdminUser.username == clean_username,
            AdminUser.email == clean_email
        )
    ).first()

    if existing:
        return templates.TemplateResponse(
            request=request,
            name="admin/signup.html",
            context={
                "settings": settings,
                "error": "An account with that username or email already exists. Please sign in."
            }
        )

    new_admin = AdminUser(
        username=clean_username,
        email=clean_email,
        hashed_password=hash_password(password),
        is_active=True
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    response = RedirectResponse(url="/admin/dashboard", status_code=303)
    token = create_session_token(admin_id=new_admin.id, username=new_admin.username)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=60 * 60 * 24 * 7,
        samesite="lax",
        secure=False
    )
    return response


# -------------------------------------------------------------
# Protected Dashboard & Monitoring
# -------------------------------------------------------------

@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    lead_type: str = Query("all"),
    status: str = Query("all"),
    search: Optional[str] = Query(None),
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Protected monitoring dashboard displaying student admissions & enquiries."""
    leads = get_leads(
        db=db,
        lead_type=lead_type if lead_type != "all" else None,
        status=status if status != "all" else None,
        search=search
    )
    summary = get_lead_summary(db=db)

    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={
            "settings": settings,
            "admin": admin,
            "leads": leads,
            "summary": summary,
            "current_lead_type": lead_type,
            "current_status": status,
            "current_search": search
        }
    )


@router.post("/leads/{lead_id}/status")
async def admin_update_lead(
    lead_id: int,
    status: str = Form(...),
    admin_notes: Optional[str] = Form(""),
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update lead pipeline stage and notes directly from the dashboard."""
    update_lead_status(
        db=db,
        lead_id=lead_id,
        status_update=LeadStatusUpdate(status=status, admin_notes=admin_notes or "")
    )
    return RedirectResponse(url="/admin/dashboard", status_code=303)


@router.get("/logout")
async def admin_logout():
    """Clear session cookie and redirect to sign in."""
    response = RedirectResponse(url="/admin/login", status_code=303)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response
