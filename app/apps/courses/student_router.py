"""
MYTHOS Student Portal & Authentication Router.
Handles student registration, login, session management, personal dashboard,
and engagement activity logging.
"""

import uuid
from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.config import settings
from app.apps.courses.database import get_db
from app.apps.courses.models import User
from app.apps.courses.schemas import (
    StudentRegister,
    StudentLogin,
    StudentOut,
    ActivityLogCreate,
)
from app.apps.courses.auth import (
    create_student_session_token,
    get_current_student,
    require_student,
    get_or_create_guest_id,
    STUDENT_COOKIE_NAME,
    GUEST_COOKIE_NAME,
)
from app.apps.courses.services import (
    register_student,
    authenticate_student,
    log_user_activity,
    link_guest_activities_to_user,
    get_student_activities,
)

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["settings"] = settings

router = APIRouter(tags=["Student Portal & Authentication"])


# -------------------------------------------------------------------------
# Web HTML Routes
# -------------------------------------------------------------------------

@router.get("/student/register", response_class=HTMLResponse)
async def student_register_page(
    request: Request,
    next: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Student registration view. Redirects to dashboard if already logged in."""
    current_user = get_current_student(request, db)
    if current_user:
        return RedirectResponse(url=next or "/student/dashboard", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        request=request,
        name="student/register.html",
        context={
            "settings": settings,
            "title": "Student Registration | MYTHOS",
            "next_url": next or "/student/dashboard",
            "error": None,
        }
    )


@router.post("/student/register")
async def student_register_submit(
    request: Request,
    full_name: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    email: Optional[str] = Form(None),
    user_type: Optional[str] = Form("student"),
    college_or_company: Optional[str] = Form(None),
    next: Optional[str] = Form("/student/dashboard"),
    db: Session = Depends(get_db)
):
    """Process student registration form submission."""
    guest_id = get_or_create_guest_id(request)
    try:
        student_data = StudentRegister(
            full_name=full_name,
            phone=phone,
            password=password,
            email=email or "",
            user_type=user_type or "student",
            college_or_company=college_or_company or "",
        )
        user = register_student(db, student_data)
        
        # Link previous anonymous reading activity
        link_guest_activities_to_user(db, guest_id, user.id)
        
        # Log registration event
        log_user_activity(
            db=db,
            session_id=guest_id,
            event_type="student_registered",
            user_id=user.id,
            resource_type="auth",
            resource_slug="register",
            ip_address=request.client.host if request.client else None,
        )

        token = create_student_session_token(user.id, user.phone)
        redirect_target = next if next and next.startswith("/") else "/student/dashboard"
        response = RedirectResponse(url=redirect_target, status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            key=STUDENT_COOKIE_NAME,
            value=token,
            max_age=60 * 60 * 24 * 30,  # 30 days
            httponly=True,
            samesite="lax",
        )
        response.set_cookie(
            key=GUEST_COOKIE_NAME,
            value=guest_id,
            max_age=60 * 60 * 24 * 365,
            httponly=True,
            samesite="lax",
        )
        return response

    except ValueError as e:
        return templates.TemplateResponse(
            request=request,
            name="student/register.html",
            context={
                "settings": settings,
                "title": "Student Registration | MYTHOS",
                "next_url": next,
                "error": str(e),
                "full_name": full_name,
                "phone": phone,
                "email": email,
                "user_type": user_type,
                "college_or_company": college_or_company,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/student/login", response_class=HTMLResponse)
async def student_login_page(
    request: Request,
    next: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Student sign-in view. Redirects to dashboard if already logged in."""
    current_user = get_current_student(request, db)
    if current_user:
        return RedirectResponse(url=next or "/student/dashboard", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        request=request,
        name="student/login.html",
        context={
            "settings": settings,
            "title": "Student Login | MYTHOS",
            "next_url": next or "/student/dashboard",
            "error": None,
        }
    )


@router.post("/student/login")
async def student_login_submit(
    request: Request,
    identifier: str = Form(...),
    password: str = Form(...),
    next: Optional[str] = Form("/student/dashboard"),
    db: Session = Depends(get_db)
):
    """Process student login form submission."""
    guest_id = get_or_create_guest_id(request)
    user = authenticate_student(db, identifier=identifier, password=password)
    
    if not user:
        return templates.TemplateResponse(
            request=request,
            name="student/login.html",
            context={
                "settings": settings,
                "title": "Student Login | MYTHOS",
                "next_url": next,
                "error": "Invalid phone/email or password. Please try again.",
                "identifier": identifier,
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # Link prior guest interactions
    link_guest_activities_to_user(db, guest_id, user.id)

    # Record login activity
    log_user_activity(
        db=db,
        session_id=guest_id,
        event_type="student_login",
        user_id=user.id,
        resource_type="auth",
        resource_slug="login",
        ip_address=request.client.host if request.client else None,
    )

    token = create_student_session_token(user.id, user.phone)
    redirect_target = next if next and next.startswith("/") else "/student/dashboard"
    response = RedirectResponse(url=redirect_target, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key=STUDENT_COOKIE_NAME,
        value=token,
        max_age=60 * 60 * 24 * 30,  # 30 days
        httponly=True,
        samesite="lax",
    )
    response.set_cookie(
        key=GUEST_COOKIE_NAME,
        value=guest_id,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="lax",
    )
    return response


@router.get("/student/logout")
async def student_logout():
    """Clear student session cookie and redirect to home."""
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key=STUDENT_COOKIE_NAME)
    return response


@router.get("/student/dashboard", response_class=HTMLResponse)
async def student_dashboard(
    request: Request,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Personal student dashboard showing active access, downloadable datasets, and reading history."""
    activities = get_student_activities(db, current_user.id, limit=15)
    
    # Available practice datasets
    datasets = [
        {
            "slug": "indian-ecommerce-orders",
            "title": "Indian E-Commerce 50,000 Transaction Orders",
            "format": "CSV & SQLite",
            "rows": "50,000 Rows",
            "category": "E-Commerce & SQL",
            "description": "Normalized transactional dataset with orders, customers, delivery statuses across Tier-1/2/3 Indian cities, and GST calculations.",
            "download_url": "/library/datasets/indian-ecommerce-orders/download",
        },
        {
            "slug": "delhi-metro-transit-ridership",
            "title": "Delhi Metro Rail Transit Ridership & Footfall Analysis",
            "format": "CSV",
            "rows": "24,000 Rows",
            "category": "Time-Series & Power BI",
            "description": "Hourly station-wise footfall, card vs token revenue, interchange congestion metrics, and peak weekend surge patterns.",
            "download_url": "/library/datasets/delhi-metro-transit-ridership/download",
        },
        {
            "slug": "digital-marketing-campaign-roas",
            "title": "Performance Marketing Multi-Channel ROAS & Funnel Audits",
            "format": "CSV & Excel",
            "rows": "15,000 Rows",
            "category": "Marketing Analytics",
            "description": "Meta Ads & Google Ads campaign logs: spend, CPC, CTR, conversion rates, customer acquisition cost (CAC), and ROAS calculations.",
            "download_url": "/library/datasets/digital-marketing-campaign-roas/download",
        },
    ]

    return templates.TemplateResponse(
        request=request,
        name="student/dashboard.html",
        context={
            "settings": settings,
            "title": f"Student Dashboard — {current_user.full_name} | MYTHOS",
            "student": current_user,
            "activities": activities,
            "datasets": datasets,
            "active_nav": "student_dashboard",
        }
    )


# -------------------------------------------------------------------------
# JSON API Endpoints
# -------------------------------------------------------------------------

@router.post("/api/student/register", response_model=StudentOut)
async def api_student_register(
    request: Request,
    data: StudentRegister,
    db: Session = Depends(get_db)
):
    """Register student via JSON API."""
    guest_id = get_or_create_guest_id(request)
    try:
        user = register_student(db, data)
        link_guest_activities_to_user(db, guest_id, user.id)
        log_user_activity(
            db=db,
            session_id=guest_id,
            event_type="student_registered",
            user_id=user.id,
            resource_type="auth",
            resource_slug="api_register",
            ip_address=request.client.host if request.client else None,
        )
        token = create_student_session_token(user.id, user.phone)
        response = JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "Student account registered successfully.",
                "student": user.to_dict(),
                "token": token,
            }
        )
        response.set_cookie(
            key=STUDENT_COOKIE_NAME,
            value=token,
            max_age=60 * 60 * 24 * 30,
            httponly=True,
            samesite="lax",
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/api/student/login")
async def api_student_login(
    request: Request,
    data: StudentLogin,
    db: Session = Depends(get_db)
):
    """Authenticate student via JSON API."""
    guest_id = get_or_create_guest_id(request)
    user = authenticate_student(db, identifier=data.identifier, password=data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials. Verify phone/email and password."
        )

    link_guest_activities_to_user(db, guest_id, user.id)
    log_user_activity(
        db=db,
        session_id=guest_id,
        event_type="student_login",
        user_id=user.id,
        resource_type="auth",
        resource_slug="api_login",
        ip_address=request.client.host if request.client else None,
    )

    token = create_student_session_token(user.id, user.phone)
    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Authenticated successfully.",
            "student": user.to_dict(),
            "token": token,
        }
    )
    response.set_cookie(
        key=STUDENT_COOKIE_NAME,
        value=token,
        max_age=60 * 60 * 24 * 30,
        httponly=True,
        samesite="lax",
    )
    return response


@router.get("/api/student/me")
async def api_student_me(current_user: User = Depends(require_student)):
    """Fetch current authenticated student profile."""
    return {
        "success": True,
        "student": current_user.to_dict()
    }


@router.post("/api/activity/log")
async def api_log_activity(
    request: Request,
    payload: ActivityLogCreate,
    db: Session = Depends(get_db)
):
    """Record an engagement interaction from client-side UI."""
    guest_id = get_or_create_guest_id(request)
    current_user = get_current_student(request, db)
    user_id = current_user.id if current_user else None

    activity = log_user_activity(
        db=db,
        session_id=guest_id,
        event_type=payload.event_type,
        user_id=user_id,
        resource_type=payload.resource_type,
        resource_slug=payload.resource_slug,
        referrer=payload.referrer,
        ip_address=request.client.host if request.client else None,
    )

    response = JSONResponse(
        content={
            "success": True,
            "logged": activity is not None,
            "session_id": guest_id
        }
    )
    # Ensure guest session cookie is persisted
    if not request.cookies.get(GUEST_COOKIE_NAME):
        response.set_cookie(
            key=GUEST_COOKIE_NAME,
            value=guest_id,
            max_age=60 * 60 * 24 * 365,
            httponly=True,
            samesite="lax",
        )
    return response
