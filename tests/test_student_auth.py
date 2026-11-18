"""
Automated Test Suite for Student Authentication, Session Management,
Activity Logging, and Dataset Access Control Gating (Phase 2).
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.apps.courses.database import SessionLocal
from app.apps.courses.services import init_courses_db
from app.apps.courses.models import User, UserActivityLog
from app.apps.courses.auth import create_student_session_token, STUDENT_COOKIE_NAME, GUEST_COOKIE_NAME

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    """Ensure database tables exist and clean test users before each test."""
    client.cookies.clear()
    init_courses_db()
    with SessionLocal() as db:
        # Clean up test users and activities created during tests
        test_phones = [
            "9876543210", "9998887776", "9123456789", "9988776655",
            "9000000001", "9000000002", "9000000003", "9000000004", "9000000005"
        ]
        users = db.query(User).filter(User.phone.in_(test_phones)).all()
        for u in users:
            db.delete(u)
        db.query(UserActivityLog).filter(UserActivityLog.session_id.like("test_%")).delete()
        db.commit()
    yield
    client.cookies.clear()


# -------------------------------------------------------------------------
# 1. Student Registration Tests
# -------------------------------------------------------------------------

def test_student_registration_form_success():
    """Verify HTML form student registration with mandatory phone and optional email."""
    response = client.post(
        "/student/register",
        data={
            "full_name": "Rohan Gupta",
            "phone": "9876543210",
            "password": "securepassword123",
            "email": "rohan.gupta@example.com",
            "user_type": "student",
            "college_or_company": "Delhi Technical Campus",
            "next": "/student/dashboard",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/student/dashboard"
    assert STUDENT_COOKIE_NAME in response.cookies

    # Verify user exists in database and password is encrypted
    with SessionLocal() as db:
        user = db.query(User).filter(User.phone == "9876543210").first()
        assert user is not None
        assert user.full_name == "Rohan Gupta"
        assert user.email == "rohan.gupta@example.com"
        assert user.hashed_password != "securepassword123"
        assert user.hashed_password.startswith("$2b$")


def test_student_registration_without_email():
    """Verify student registration strictly respects optional email invariant."""
    response = client.post(
        "/student/register",
        data={
            "full_name": "Pooja Verma",
            "phone": "9998887776",
            "password": "mypassword456",
            "email": "",
            "user_type": "fresher",
            "college_or_company": "",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303

    with SessionLocal() as db:
        user = db.query(User).filter(User.phone == "9998887776").first()
        assert user is not None
        assert user.full_name == "Pooja Verma"
        assert user.email is None or user.email == ""


def test_student_registration_duplicate_phone():
    """Verify duplicate phone registration is rejected with 400 Bad Request."""
    # First registration
    client.post(
        "/student/register",
        data={
            "full_name": "First User",
            "phone": "9123456789",
            "password": "password123",
            "email": "user1@example.com",
        },
    )

    # Second registration with identical phone
    response = client.post(
        "/student/register",
        data={
            "full_name": "Second User",
            "phone": "9123456789",
            "password": "password456",
            "email": "user2@example.com",
        },
    )
    assert response.status_code == 400
    assert "already registered" in response.text


# -------------------------------------------------------------------------
# 2. Student Login & Session Tests
# -------------------------------------------------------------------------

def test_student_login_with_phone_and_email():
    """Verify student can log in via either Phone or Email."""
    # Register student
    client.post(
        "/student/register",
        data={
            "full_name": "Amit Kumar",
            "phone": "9988776655",
            "password": "mypassword123",
            "email": "amit.kumar@example.com",
        },
    )

    # 1. Login with Phone
    res_phone = client.post(
        "/student/login",
        data={"identifier": "9988776655", "password": "mypassword123"},
        follow_redirects=False,
    )
    assert res_phone.status_code == 303
    assert STUDENT_COOKIE_NAME in res_phone.cookies

    # 2. Login with Email
    res_email = client.post(
        "/student/login",
        data={"identifier": "amit.kumar@example.com", "password": "mypassword123"},
        follow_redirects=False,
    )
    assert res_email.status_code == 303
    assert STUDENT_COOKIE_NAME in res_email.cookies


def test_student_login_invalid_password():
    """Verify incorrect credentials return 401 Unauthorized."""
    client.post(
        "/student/register",
        data={
            "full_name": "Test User",
            "phone": "9000000001",
            "password": "correctpassword",
        },
    )

    response = client.post(
        "/student/login",
        data={"identifier": "9000000001", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "Invalid phone/email or password" in response.text


def test_student_logout():
    """Verify logout removes the student_session cookie."""
    client.cookies.set(STUDENT_COOKIE_NAME, "mock_token")
    response = client.get("/student/logout", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/"


# -------------------------------------------------------------------------
# 3. Student Dashboard & Protected Route Access
# -------------------------------------------------------------------------

def test_student_dashboard_requires_auth():
    """Unauthenticated guest accessing /student/dashboard is redirected to login."""
    client.cookies.clear()
    response = client.get("/student/dashboard", follow_redirects=False)
    assert response.status_code == 303
    assert "/student/login" in response.headers["location"]


def test_student_dashboard_authenticated():
    """Authenticated student can view personal dashboard with datasets and activity."""
    # Register and get user
    client.post(
        "/student/register",
        data={
            "full_name": "Vikram Malhotra",
            "phone": "9000000002",
            "password": "vikrampassword",
            "email": "vikram@example.com",
            "college_or_company": "IIT Roorkee",
        },
    )

    with SessionLocal() as db:
        user = db.query(User).filter(User.phone == "9000000002").first()
        token = create_student_session_token(user.id, user.phone)

    client.cookies.set(STUDENT_COOKIE_NAME, token)
    response = client.get("/student/dashboard")
    assert response.status_code == 200
    assert "Vikram Malhotra" in response.text
    assert "Verified Student" in response.text
    assert "Practice Datasets Vault" in response.text


# -------------------------------------------------------------------------
# 4. Activity Logging & Guest Linking Tests
# -------------------------------------------------------------------------

def test_activity_logging_api_and_guest_linking():
    """Verify /api/activity/log records events and links guest activities upon login."""
    test_session = "test_guest_uuid_12345"
    client.cookies.set(GUEST_COOKIE_NAME, test_session)

    # 1. Log guest activity before registration
    res_log = client.post(
        "/api/activity/log",
        json={
            "event_type": "note_read",
            "resource_type": "note",
            "resource_slug": "sql-joins-textbook-vs-reality",
            "referrer": "telegram",
        },
    )
    assert res_log.status_code == 200
    assert res_log.json()["success"] is True

    # 2. Register user with this guest session
    reg_res = client.post(
        "/student/register",
        data={
            "full_name": "Activity Tester",
            "phone": "9000000003",
            "password": "testerpassword",
        },
        follow_redirects=False,
    )
    assert reg_res.status_code == 303

    # 3. Verify the previous guest activity is linked to the new user ID
    with SessionLocal() as db:
        user = db.query(User).filter(User.phone == "9000000003").first()
        activities = db.query(UserActivityLog).filter(
            UserActivityLog.session_id == test_session,
            UserActivityLog.user_id == user.id,
        ).all()
        assert len(activities) >= 1
        assert any(a.event_type == "note_read" for a in activities)
        assert activities[0].event_type in ("note_read", "student_registered")


# -------------------------------------------------------------------------
# 5. Dataset Access Control & Download Gating (Task 2.4)
# -------------------------------------------------------------------------

def test_practice_datasets_catalog():
    """Verify /library/datasets displays available datasets."""
    response = client.get("/library/datasets")
    assert response.status_code == 200
    assert "Practice Datasets Vault" in response.text
    assert "Indian E-Commerce" in response.text
    assert "Delhi Metro Rail" in response.text


def test_practice_dataset_detail_preview():
    """Verify /library/datasets/{slug} renders schema dictionary and sample rows."""
    response = client.get("/library/datasets/indian-ecommerce-orders")
    assert response.status_code == 200
    assert "Data Dictionary &amp; Column Specifications" in response.text or "Data Dictionary & Column Specifications" in response.text
    assert "order_id" in response.text
    assert "customer_id" in response.text
    assert "Sample Data Preview" in response.text


def test_dataset_download_guest_redirect():
    """Guest attempting to download dataset is redirected to /student/login."""
    client.cookies.clear()
    response = client.get(
        "/library/datasets/indian-ecommerce-orders/download",
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert "/student/login?next=/library/datasets/indian-ecommerce-orders/download" in response.headers["location"]


def test_dataset_download_authenticated_student():
    """Authenticated student receives CSV file download and activity is logged."""
    # Register and get student token
    client.post(
        "/student/register",
        data={
            "full_name": "Download Tester",
            "phone": "9000000004",
            "password": "password999",
        },
    )
    with SessionLocal() as db:
        user = db.query(User).filter(User.phone == "9000000004").first()
        token = create_student_session_token(user.id, user.phone)

    client.cookies.set(STUDENT_COOKIE_NAME, token)
    response = client.get("/library/datasets/indian-ecommerce-orders/download")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert 'attachment; filename="indian-ecommerce-orders.csv"' in response.headers["content-disposition"]
    assert "order_id,customer_id,order_date" in response.text

    # Verify download activity logged
    with SessionLocal() as db:
        activity = db.query(UserActivityLog).filter(
            UserActivityLog.user_id == user.id,
            UserActivityLog.event_type == "dataset_download",
            UserActivityLog.resource_slug == "indian-ecommerce-orders",
        ).first()
        assert activity is not None


# -------------------------------------------------------------------------
# 6. JSON API Endpoints Tests
# -------------------------------------------------------------------------

def test_api_student_register_and_me():
    """Verify JSON API registration and /api/student/me profile endpoint."""
    client.cookies.clear()
    reg_response = client.post(
        "/api/student/register",
        json={
            "full_name": "API Student",
            "phone": "9000000005",
            "password": "api_password_123",
            "email": "apistudent@example.com",
            "user_type": "working_professional",
            "college_or_company": "Infosys",
        },
    )
    assert reg_response.status_code == 201
    data = reg_response.json()
    assert data["success"] is True
    assert data["student"]["phone"] == "9000000005"
    token = data["token"]

    # Call /api/student/me with Bearer token
    me_response = client.get(
        "/api/student/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["success"] is True
    assert me_data["student"]["full_name"] == "API Student"
    assert me_data["student"]["college_or_company"] == "Infosys"
