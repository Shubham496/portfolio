import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.apps.courses.database import Base, engine, SessionLocal
from app.apps.courses.models import Batch, StudentLead, AdminUser
from app.apps.courses.auth import create_session_token, SESSION_COOKIE_NAME
from app.apps.courses.services import init_courses_db
from app.core.config import settings
import os

client = TestClient(app)


def setup_function():
    """Ensure clean test state before tests."""
    Base.metadata.create_all(bind=engine)
    init_courses_db()


def get_admin_cookies():
    """Helper to generate signed admin session cookies for protected test operations."""
    with SessionLocal() as db:
        admin = db.query(AdminUser).filter(AdminUser.username == "agent_admin").first()
        if not admin:
            admin = db.query(AdminUser).first()
        token = create_session_token(admin_id=admin.id, username=admin.username)
        return {SESSION_COOKIE_NAME: token}



def test_instructor_endpoint():
    """Instructor profile endpoint must accurately describe the mentorship desk, curriculum, and schedule."""
    response = client.get("/api/courses/instructor")
    assert response.status_code == 200
    data = response.json()
    
    # Verify instructor credentials & dynamic contact
    instructor = data["instructor"]
    assert "Mythos" in instructor["name"] or "Mentor" in instructor["name"]
    assert instructor["email"] == settings.BUSINESS_EMAIL or "@" in instructor["email"]
    assert "shubhamsinghh057@gmail.com" not in instructor["email"]
    assert "8727864157" not in instructor["phone"]
    assert instructor["phone"] == settings.BUSINESS_WHATSAPP
    assert len(instructor["experience_highlights"]) > 0
    assert "550+" not in str(data)

    # Verify course & syllabus
    course = data["course"]
    assert course["name"] == "Complete Data Analysis Masterclass"
    tools = [t.lower() for t in course["tools"]]
    assert "python" in tools
    assert "sql" in tools
    assert "powerbi" in tools
    assert "excel" in tools
    assert "tableau" in tools

    # Verify schedule constraints: Saturday and Sunday only, 6 to 8 pm
    schedule = course["schedule"]
    assert "Saturday & Sunday" in schedule["days"]
    assert "6:00 PM – 8:00 PM" in schedule["timings"]

    # Verify strictly NO fees displayed
    assert course.get("fees") is None


def test_batches_endpoint():
    """Batches list endpoint must return active enrolling batches."""
    response = client.get("/api/courses/batches")
    assert response.status_code == 200
    batches = response.json()
    assert len(batches) >= 1
    
    default_batch = batches[0]
    assert "Saturday & Sunday" in default_batch["schedule_days"]
    assert "6:00 PM – 8:00 PM" in default_batch["schedule_time"]
    assert "Python" in default_batch["technologies"]
    assert "SQL" in default_batch["technologies"]


def test_student_enquiry_submission():
    """Prospective student can submit an enquiry/question or callback request."""
    payload = {
        "full_name": "Rohan Sharma",
        "email": "rohan.sharma@example.com",
        "phone": "+91 9876543210",
        "current_status": "College Student",
        "message": "Interested in Weekend batch for Power BI and Python. Do we work on live projects?",
        "preferred_schedule": "Saturday & Sunday 6:00 PM – 8:00 PM IST"
    }
    response = client.post("/api/courses/enquiry", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["lead_type"] == "enquiry"
    assert data["data"]["full_name"] == "Rohan Sharma"
    assert data["data"]["email"] == "rohan.sharma@example.com"
    assert data["data"]["status"] == "new"


def test_student_batch_registration():
    """Prospective student can register directly for the weekend batch."""
    payload = {
        "full_name": "Priya Verma",
        "email": "priya.verma@example.com",
        "phone": "+91 9123456789",
        "current_status": "Working Professional",
        "prior_experience": "Basic Excel and SQL",
        "message": "Looking to transition into a full-time Data Analyst role.",
        "preferred_schedule": "Saturday & Sunday 6:00 PM – 8:00 PM IST"
    }
    response = client.post("/api/courses/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["lead_type"] == "batch_registration"
    assert data["data"]["full_name"] == "Priya Verma"
    assert "Saturday & Sunday 6:00 PM – 8:00 PM" in data["schedule"]


def test_lead_validation_errors():
    """Incomplete enquiry or registration should return 422 Unprocessable Entity."""
    # Missing email & phone
    response = client.post("/api/courses/enquiry", json={"full_name": "Incomplete"})
    assert response.status_code == 422

    # Invalid email format
    response = client.post("/api/courses/enquiry", json={
        "full_name": "Test User",
        "email": "not-an-email",
        "phone": "9999999999"
    })
    assert response.status_code == 422


def test_form_data_enquiry_submission():
    """Supports standard HTML form submission as well."""
    form_data = {
        "full_name": "Amit Patel",
        "email": "amit.patel@example.com",
        "phone": "+91 9988776655",
        "current_status": "Fresher",
        "message": "Looking for syllabus details",
        "consent": "on"
    }
    response = client.post("/api/courses/enquiry", data=form_data)
    assert response.status_code == 201
    assert response.json()["success"] is True


def test_lead_pipeline_and_summary():
    """Admin can view lead summaries and update lead counseling statuses when authenticated."""
    cookies = get_admin_cookies()
    # Fetch summary stats
    summary_resp = client.get("/api/courses/leads/summary", cookies=cookies)
    assert summary_resp.status_code == 200
    summary = summary_resp.json()
    assert summary["total_leads"] >= 2
    assert summary["enquiries"] >= 1
    assert summary["batch_registrations"] >= 1

    # Fetch leads list filtered by type
    leads_resp = client.get("/api/courses/leads?lead_type=batch_registration", cookies=cookies)
    assert leads_resp.status_code == 200
    reg_leads = leads_resp.json()
    assert len(reg_leads) >= 1
    reg_id = reg_leads[0]["id"]

    # Update pipeline status
    patch_resp = client.patch(
        f"/api/courses/leads/{reg_id}/status",
        json={"status": "contacted", "admin_notes": "Spoke on call; confirmed weekend schedule."},
        cookies=cookies
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["lead"]["status"] == "contacted"
    assert "confirmed weekend schedule" in patch_resp.json()["lead"]["admin_notes"]


def test_csv_export():
    """Admin can download leads as CSV when authenticated."""
    cookies = get_admin_cookies()
    response = client.get("/api/courses/leads/export.csv", cookies=cookies)
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "attachment; filename=student_leads_and_registrations.csv" in response.headers["content-disposition"]
    csv_text = response.text
    assert "Full Name" in csv_text
    assert "Email" in csv_text
    assert "Phone" in csv_text
    assert "Batch Title" in csv_text
    assert "Consent Given" in csv_text



def test_register_page():
    """Verify dedicated registration page renders correctly."""
    response = client.get("/register")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Weekend Batch Registration" in response.text
    assert "Saturday &amp; Sunday" in response.text or "Saturday & Sunday" in response.text


def test_registration_success_page():
    """Verify confirmation page informs student that we will contact them."""
    response = client.get("/registration-success")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Thank You for Registering" in response.text
    assert "Saturday & Sunday" in response.text


def test_registration_without_email():
    """Verify student can register without providing an email address."""
    payload = {
        "full_name": "Suresh Kumar",
        "email": "",
        "phone": "+91 9999888877",
        "current_status": "Fresher",
        "message": "Prefer WhatsApp contact only."
    }
    response = client.post("/api/courses/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] in (None, "")
    assert data["data"]["full_name"] == "Suresh Kumar"


def test_syllabus_download_and_view():
    """Verify course syllabus download button and printable view serve PDF file."""
    # Download attachment
    dl_resp = client.get("/course/syllabus/download")
    assert dl_resp.status_code == 200
    assert "application/pdf" in dl_resp.headers["content-type"]
    assert "Data_Analysis_Full_Course_Syllabus.pdf" in dl_resp.headers["content-disposition"]
    assert dl_resp.content.startswith(b"%PDF")

    # Inline view
    view_resp = client.get("/course/syllabus")
    assert view_resp.status_code == 200
    assert "application/pdf" in view_resp.headers["content-type"]
    assert view_resp.content.startswith(b"%PDF")


def test_admin_auth_and_dashboard_flow():
    """Verify admin login only (signup disabled), protected dashboard, and lead status update."""
    # Unauthenticated access to dashboard must redirect to login
    unauth_resp = client.get("/admin/dashboard", follow_redirects=False)
    assert unauth_resp.status_code == 303
    assert "/admin/login" in unauth_resp.headers["location"]

    # Registration / Signup is strictly disabled - must redirect to login
    signup_resp = client.get("/admin/signup", follow_redirects=False)
    assert signup_resp.status_code == 303
    assert "/admin/login" in signup_resp.headers["location"]

    signup_post_resp = client.post("/admin/signup", data={"username": "hacker"}, follow_redirects=False)
    assert signup_post_resp.status_code == 303
    assert "/admin/login" in signup_post_resp.headers["location"]

    # Test login with invalid password
    bad_login = client.post("/admin/login", data={"username": "agent_admin", "password": "wrongpassword"})
    assert bad_login.status_code == 401
    assert "Invalid username or password" in bad_login.text

    # Test login with dedicated agent admin credentials
    agent_password = os.getenv("AGENT_PASSWORD", "hUrHD1qKvVPQqk_y1itG*ISU")
    login_data = {
        "username": "agent_admin",
        "password": agent_password
    }
    login_resp = client.post("/admin/login", data=login_data, follow_redirects=False)
    assert login_resp.status_code == 303
    assert "/admin/dashboard" in login_resp.headers["location"]
    session_cookie = login_resp.cookies.get("admin_session")
    assert session_cookie is not None

    # Access dashboard with session cookie
    dash_resp = client.get("/admin/dashboard", cookies={"admin_session": session_cookie})
    assert dash_resp.status_code == 200
    assert "Student Leads &amp; Batch Admissions" in dash_resp.text or "Student Leads & Batch Admissions" in dash_resp.text
    assert "agent_admin" in dash_resp.text

    # Test logout
    logout_resp = client.get("/admin/logout", follow_redirects=False)
    assert logout_resp.status_code == 303
    assert "/admin/login" in logout_resp.headers["location"]


def test_anonymous_lead_endpoints_rejected():
    """Anonymous/unauthenticated requests to lead and batch admin endpoints must be rejected with 401."""
    # Lead list
    resp = client.get("/api/courses/leads")
    assert resp.status_code == 401
    assert "Admin authentication required" in resp.json()["detail"]

    # Lead summary
    resp = client.get("/api/courses/leads/summary")
    assert resp.status_code == 401

    # CSV export
    resp = client.get("/api/courses/leads/export.csv")
    assert resp.status_code == 401

    # Single lead detail
    resp = client.get("/api/courses/leads/1")
    assert resp.status_code == 401

    # Patch lead status
    resp = client.patch("/api/courses/leads/1/status", json={"status": "contacted"})
    assert resp.status_code == 401

    # Create batch
    resp = client.post("/api/courses/batches", json={
        "batch_code": "TEST-BATCH-2026",
        "title": "Test Batch",
    })
    assert resp.status_code == 401


def test_consent_enforcement_on_forms_and_api():
    """Submissions without consent must fail validation (HTTP 422), while valid consent persists timestamp."""
    # 1. API submission with explicit consent=False must fail
    resp_false = client.post("/api/courses/enquiry", json={
        "full_name": "No Consent Student",
        "email": "noconsent@example.com",
        "phone": "+91 9111122222",
        "consent": False
    })
    assert resp_false.status_code == 422
    assert "agree to be contacted" in resp_false.text

    reg_false = client.post("/api/courses/register", json={
        "full_name": "No Consent Enrollee",
        "phone": "+91 9111122222",
        "consent": False
    })
    assert reg_false.status_code == 422
    assert "agree to be contacted" in reg_false.text

    # 2. Form submission without consent (unchecked checkbox) must fail
    form_resp_fail = client.post("/api/courses/enquiry", data={
        "full_name": "Unchecked Consent",
        "phone": "+91 9333344444"
        # consent omitted
    })
    assert form_resp_fail.status_code == 422

    # 3. Valid consent persists consent_given=True and consent_at timestamp
    resp_success = client.post("/api/courses/enquiry", json={
        "full_name": "Consenting Student",
        "email": "consent@example.com",
        "phone": "+91 9444455555",
        "consent": True
    })
    assert resp_success.status_code == 201
    lead_data = resp_success.json()["data"]
    assert lead_data["consent_given"] is True
    assert lead_data["consent_at"] is not None


def test_do_not_contact_lead_status():
    """Admins can update a student lead to 'do_not_contact' to suppress outreach."""
    cookies = get_admin_cookies()
    # Create a test lead
    create_resp = client.post("/api/courses/enquiry", json={
        "full_name": "Opt Out Learner",
        "phone": "+91 9555566666",
        "consent": True
    })
    assert create_resp.status_code == 201
    lead_id = create_resp.json()["data"]["id"]

    # Update status to do_not_contact
    patch_resp = client.patch(
        f"/api/courses/leads/{lead_id}/status",
        json={"status": "do_not_contact", "admin_notes": "Student requested no further WhatsApp messages."},
        cookies=cookies
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["lead"]["status"] == "do_not_contact"

    # Verify summary reflects do_not_contact
    summary_resp = client.get("/api/courses/leads/summary", cookies=cookies)
    assert summary_resp.status_code == 200
    assert summary_resp.json()["do_not_contact"] >= 1


def test_secret_key_production_enforcement(monkeypatch):
    """DeploymentSettings in production mode must refuse to start without a valid, secure SECRET_KEY."""
    from app.core.deployment import DeploymentSettings

    # Empty SECRET_KEY
    monkeypatch.setenv("SECRET_KEY", "")
    with pytest.raises(RuntimeError) as exc_info:
        DeploymentSettings()
    assert "SECRET_KEY environment variable is required in production" in str(exc_info.value)

    # Insecure default placeholder
    monkeypatch.setenv("SECRET_KEY", "shubham-data-analysis-secret-key-2026")
    with pytest.raises(RuntimeError) as exc_info:
        DeploymentSettings()
    assert "SECRET_KEY environment variable is required in production" in str(exc_info.value)

    # Valid cryptographically secure key
    monkeypatch.setenv("SECRET_KEY", "b47c093a8126e0388d75cf82813123b34e2ab9030612c3f813c01287e07a3dfc")
    settings = DeploymentSettings()
    assert settings.SECRET_KEY == "b47c093a8126e0388d75cf82813123b34e2ab9030612c3f813c01287e07a3dfc"


def test_legal_policy_pages():
    """Verify that /privacy, /terms, and /refund-policy pages render with correct HTTP 200 responses."""
    # Privacy Policy
    priv_resp = client.get("/privacy")
    assert priv_resp.status_code == 200
    assert "Privacy Policy" in priv_resp.text
    assert "WhatsApp" in priv_resp.text
    assert "do_not_contact" in priv_resp.text

    # Terms of Service
    terms_resp = client.get("/terms")
    assert terms_resp.status_code == 200
    assert "Terms of Service" in terms_resp.text
    assert "Zero Code Execution" in terms_resp.text

    # Refund Policy
    ref_resp = client.get("/refund-policy")
    assert ref_resp.status_code == 200
    assert "Refund &amp; Rescheduling Policy" in ref_resp.text or "Refund & Rescheduling Policy" in ref_resp.text
    assert "Demo" in ref_resp.text

