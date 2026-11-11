import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.apps.courses.database import Base, engine, SessionLocal
from app.apps.courses.models import Batch, StudentLead

client = TestClient(app)


def setup_function():
    """Ensure clean test state before tests."""
    Base.metadata.create_all(bind=engine)


def test_instructor_endpoint():
    """Instructor profile endpoint must accurately describe who Shubham is, the curriculum, and the schedule."""
    response = client.get("/api/courses/instructor")
    assert response.status_code == 200
    data = response.json()
    
    # Verify instructor credentials
    instructor = data["instructor"]
    assert "Shubham" in instructor["name"]
    assert len(instructor["experience_highlights"]) > 0

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
        "message": "Looking for syllabus details"
    }
    response = client.post("/api/courses/enquiry", data=form_data)
    assert response.status_code == 201
    assert response.json()["success"] is True


def test_lead_pipeline_and_summary():
    """Admin can view lead summaries and update lead counseling statuses."""
    # Fetch summary stats
    summary_resp = client.get("/api/courses/leads/summary")
    assert summary_resp.status_code == 200
    summary = summary_resp.json()
    assert summary["total_leads"] >= 2
    assert summary["enquiries"] >= 1
    assert summary["batch_registrations"] >= 1

    # Fetch leads list filtered by type
    leads_resp = client.get("/api/courses/leads?lead_type=batch_registration")
    assert leads_resp.status_code == 200
    reg_leads = leads_resp.json()
    assert len(reg_leads) >= 1
    reg_id = reg_leads[0]["id"]

    # Update pipeline status
    patch_resp = client.patch(
        f"/api/courses/leads/{reg_id}/status",
        json={"status": "contacted", "admin_notes": "Spoke on call; confirmed weekend schedule."}
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["lead"]["status"] == "contacted"
    assert "confirmed weekend schedule" in patch_resp.json()["lead"]["admin_notes"]


def test_csv_export():
    """Admin can download leads as CSV."""
    response = client.get("/api/courses/leads/export.csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "attachment; filename=student_leads_and_registrations.csv" in response.headers["content-disposition"]
    csv_text = response.text
    assert "Full Name" in csv_text
    assert "Email" in csv_text
    assert "Phone" in csv_text
    assert "Batch Title" in csv_text



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


def test_syllabus_download_and_view():
    """Verify course syllabus download button and printable view."""
    # Download attachment
    dl_resp = client.get("/course/syllabus/download")
    assert dl_resp.status_code == 200
    assert "attachment; filename=Data_Analysis_Full_Course_Syllabus.html" in dl_resp.headers["content-disposition"]
    assert "Complete Data Analysis Masterclass" in dl_resp.text
    assert "Python" in dl_resp.text
    assert "SQL" in dl_resp.text
    assert "Power BI" in dl_resp.text

    # Inline view
    view_resp = client.get("/course/syllabus")
    assert view_resp.status_code == 200
    assert "Complete Data Analysis Masterclass" in view_resp.text


def test_admin_auth_and_dashboard_flow():
    """Verify admin signup, login, protected dashboard, and lead status update."""
    # Unauthenticated access to dashboard must redirect to login
    unauth_resp = client.get("/admin/dashboard", follow_redirects=False)
    assert unauth_resp.status_code == 303
    assert "/admin/login" in unauth_resp.headers["location"]

    # Signup new admin with unique credentials
    import uuid
    uid = uuid.uuid4().hex[:6]
    test_user = f"admin_{uid}"
    test_email = f"admin_{uid}@example.com"
    signup_data = {
        "username": test_user,
        "email": test_email,
        "password": "securepassword123",
        "confirm_password": "securepassword123"
    }
    signup_resp = client.post("/admin/signup", data=signup_data, follow_redirects=False)
    assert signup_resp.status_code == 303
    assert "/admin/dashboard" in signup_resp.headers["location"]
    session_cookie = signup_resp.cookies.get("admin_session")
    assert session_cookie is not None

    # Access dashboard with session cookie
    dash_resp = client.get("/admin/dashboard", cookies={"admin_session": session_cookie})
    assert dash_resp.status_code == 200
    assert "Student Leads &amp; Batch Admissions" in dash_resp.text or "Student Leads & Batch Admissions" in dash_resp.text
    assert test_user in dash_resp.text

    # Test login with valid credentials
    login_data = {
        "username_or_email": test_user,
        "password": "securepassword123"
    }
    login_resp = client.post("/admin/login", data=login_data, follow_redirects=False)
    assert login_resp.status_code == 303
    assert "/admin/dashboard" in login_resp.headers["location"]

    # Test login with invalid password
    bad_login = client.post("/admin/login", data={"username_or_email": test_user, "password": "wrong"})
    assert bad_login.status_code == 401
    assert "Invalid username or password" in bad_login.text

    # Test logout
    logout_resp = client.get("/admin/logout", follow_redirects=False)
    assert logout_resp.status_code == 303
    assert "/admin/login" in logout_resp.headers["location"]
