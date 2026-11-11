import os
from typing import Optional
from fastapi import Request, Depends, HTTPException, status
import bcrypt
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from sqlalchemy.orm import Session

from app.apps.courses.database import get_db
from app.apps.courses.models import AdminUser

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "shubham-data-analysis-secret-key-2026")
serializer = URLSafeTimedSerializer(SECRET_KEY, salt="admin-auth-salt")
SESSION_COOKIE_NAME = "admin_session"


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
