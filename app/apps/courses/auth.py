import os
import uuid
from typing import Optional
from fastapi import Request, Depends, HTTPException, status
import bcrypt
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from sqlalchemy.orm import Session

from app.apps.courses.database import get_db
from app.apps.courses.models import AdminUser, User

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "shubham-data-analysis-secret-key-2026")
serializer = URLSafeTimedSerializer(SECRET_KEY, salt="admin-auth-salt")
student_serializer = URLSafeTimedSerializer(SECRET_KEY, salt="student-auth-salt")

SESSION_COOKIE_NAME = "admin_session"
STUDENT_COOKIE_NAME = "student_session"
GUEST_COOKIE_NAME = "mythos_guest_id"


def hash_password(password: str) -> str:
    """Hash password using modern bcrypt directly."""
    pwd_bytes = password.encode("utf-8")[:72]  # bcrypt standard limit
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password."""
    try:
        pwd_bytes = plain_password.encode("utf-8")[:72]
        hashed_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(pwd_bytes, hashed_bytes)
    except Exception:
        return False


def create_session_token(admin_id: int, username: str) -> str:
    """Generate signed session token for cookie."""
    return serializer.dumps({"admin_id": admin_id, "username": username})


def decode_session_token(token: str, max_age_seconds: int = 60 * 60 * 24 * 7) -> Optional[dict]:
    """Decode and verify signed session token (default 7 days validity)."""
    try:
        return serializer.loads(token, max_age=max_age_seconds)
    except (BadSignature, SignatureExpired):
        return None
    except Exception:
        return None


def get_current_admin(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[AdminUser]:
    """Return currently authenticated AdminUser if session cookie is valid, else None."""
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        return None
    
    payload = decode_session_token(token)
    if not payload or "admin_id" not in payload:
        return None

    admin = db.query(AdminUser).filter(
        AdminUser.id == payload["admin_id"],
        AdminUser.is_active == True
    ).first()
    return admin


def require_admin(
    request: Request,
    db: Session = Depends(get_db)
) -> AdminUser:
    """
    Dependency that enforces admin authentication.
    Redirects browser requests to /admin/login.
    """
    admin = get_current_admin(request=request, db=db)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/admin/login"},
            detail="Authentication required"
        )
    return admin


# -------------------------------------------------------------------------
# Student Authentication & Session Management
# -------------------------------------------------------------------------

def create_student_session_token(user_id: int, phone: str) -> str:
    """Generate signed 30-day session token for student cookie."""
    return student_serializer.dumps({"user_id": user_id, "phone": phone})


def decode_student_session_token(token: str, max_age_seconds: int = 60 * 60 * 24 * 30) -> Optional[dict]:
    """Decode and verify signed student session token (default 30 days validity)."""
    try:
        return student_serializer.loads(token, max_age=max_age_seconds)
    except (BadSignature, SignatureExpired):
        return None
    except Exception:
        return None


def get_current_student(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Return currently authenticated User (student) if session cookie or
    Authorization bearer header is valid and user is active, else None.
    """
    token = request.cookies.get(STUDENT_COOKIE_NAME)
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "").strip()

    if not token:
        return None

    payload = decode_student_session_token(token)
    if not payload or "user_id" not in payload:
        return None

    user = db.query(User).filter(
        User.id == payload["user_id"],
        User.is_active == True
    ).first()
    return user


def require_student(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency that enforces student authentication.
    Redirects browser requests to /student/login with next destination;
    returns HTTP 401 for JSON/API clients.
    """
    student = get_current_student(request=request, db=db)
    if not student:
        # Check if API request
        is_api = (
            request.url.path.startswith("/api/")
            or "application/json" in request.headers.get("Accept", "")
        )
        if is_api:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Student authentication required. Please register or log in.",
            )
        next_url = str(request.url.path)
        if request.url.query:
            next_url += f"?{request.url.query}"
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": f"/student/login?next={next_url}"},
            detail="Student authentication required"
        )
    return student


def get_or_create_guest_id(request: Request) -> str:
    """Extract existing guest session UUID or generate a new unique identifier."""
    guest_id = request.cookies.get(GUEST_COOKIE_NAME)
    if not guest_id:
        guest_id = uuid.uuid4().hex
    return guest_id
