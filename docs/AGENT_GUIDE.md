# AGENT PROJECT GUIDE & CONTEXT SPECIFICATION

> **Read this file first** when starting any new session or executing commands on this repository.
> It contains the complete architectural context, business constraints, data schemas, API specifications, and operational directives.

---

## 1. Project Mission & Objective

Transform this application from a personal developer resume portfolio into an **Education, Mentorship & Student Admission Platform** for **Shubham Singh**.

* **Instructor Identity**: Shubham Singh (Lead Python & Data Architecture Consultant & Instructor with 3+ years experience across Ducat, Netmax, and LNP Infotech; trained 120+ senior developers and students).
* **Target Audience**: Prospective students, freshers, and working professionals seeking hands-on Data Analysis skills.
* **Core Conversion Funnel**:
  1. Student lands on the site and sees **who the instructor is** (industry experience, proven mentorship track record, technical mastery).
  2. Student reviews the course curriculum and schedule.
  3. Student takes one of two primary actions:
     - **General Enquiry**: Asks questions, requests a counseling callback, or asks for syllabus guidance.
     - **Batch Registration**: Directly enrolls into the upcoming weekend training batch.

---

## 2. Immutable Business Constraints (DO NOT VIOLATE)

1. **Course Subject**: **Data Analysis** covering exactly 5 core pillars:
   - **Python** (Pandas, NumPy, automation, data wrangling)
   - **SQL** (Complex queries, Window functions, CTEs, Joins, relational modeling)
   - **Power BI** (Data modeling, DAX, executive KPI dashboards)
   - **Excel** (Advanced formulas, XLOOKUP, Pivot tables, modeling)
   - **Tableau** (Visual storytelling, parameters, calculated fields)
2. **Class Schedule**:
   - **Saturday and Sunday ONLY**.
   - **Timings: 6:00 PM to 8:00 PM IST** (2 hours/day = 4 hours/week).
   - No weekday classes.
3. **Pricing Policy**:
   - **STRICTLY NO FEES ON THE PAGE**.
   - No public price tags, tuition numbers, discount badges, or fee input fields.
   - Financial discussions happen privately during student counseling.
4. **Current Phase & Scope Focus**:
   - **Phase 1 (Completed)**: Backend admission engine, database models, REST API, Pydantic validation, CSV lead export, automated pytest suite.
   - **Phase 2 (Current / Next)**: Frontend UI transformation (landing hero, instructor credentials showcase, weekend schedule banner, interactive enquiry & batch registration forms/modals).

---

## 3. Deployment & Database Architecture (Render.io Strategy)

### The Render.io Ephemeral Storage Constraint
* Standard web services on Render.io run in **ephemeral containers**.
* Local SQLite files (`portfolio.db` or `course_platform.db`) are wiped on every redeploy, git push, or idle container sleep/wake cycle.
* Storing student leads in local SQLite in production will lead to lost data.

### The Solution: Universal Dual-Engine in `app/apps/courses/database.py`
The database connection dynamically adapts based on environment configuration:

* **Production (Render.io)**:
  - Connects to an external/managed PostgreSQL database via `DATABASE_URL` (e.g. Neon.tech, Supabase, or Render PostgreSQL).
  - Automatically converts legacy `postgres://` prefixes to `postgresql://` (required by SQLAlchemy 1.4/2.0+).
  - Uses connection pooling with `pool_pre_ping=True` and `pool_recycle=300` to prevent dropped sockets.
* **Local Development**:
  - If `DATABASE_URL` is unset or starts with `sqlite`, it automatically defaults to `sqlite:///./course_platform.db` with `check_same_thread=False`.
  - Developers can run and test offline immediately with zero external services.

---

## 4. Codebase Directory Structure

```text
coding/
│
├── app/
│   ├── main.py                      # FastAPI app entrypoint, router mounts, home route context
│   ├── core/
│   │   ├── base_config.py           # Personal details, contact, bio, socials
│   │   ├── config.py                # Environment-aware settings switcher
│   │   ├── deployment.py            # Production settings & cloud port binding
│   │   └── local.py                 # Local debug settings
│   │
│   ├── apps/
│   │   ├── courses/                 # [NEW] Course & Student Admission Engine
│   │   │   ├── __init__.py
│   │   │   ├── database.py          # Dual-engine SQLAlchemy setup (Postgres/SQLite)
│   │   │   ├── models.py            # Batch & StudentLead ORM entities
│   │   │   ├── schemas.py           # Pydantic v2 schemas with custom email validator
│   │   │   ├── services.py          # Seeding, CRUD, filters, CSV exporter, instructor profile
│   │   │   └── router.py            # API routes (JSON + HTML Form compatible)
│   │   │
│   │   └── todos/                   # Existing Project Roadmap / Action tracker app
│   │       ├── models.py
│   │       ├── router.py
│   │       └── templates/
│   │
│   ├── static/
│   │   ├── css/style.css            # Dark/light theme styles & scrollbar rules
│   │   ├── js/main.js               # Theme toggle & UI scripts
│   │   ├── Images/Profile/          # profilePhoto.jpeg
│   │   └── pdf/resume.pdf           # Downloadable resume
│   │
│   └── templates/
│       ├── base.html                # Main layout (Tailwind CDN, Lucide, fonts)
│       ├── index.html               # Portfolio / Course Landing page
│       └── partials/
│           ├── navbar.html          # Sticky navigation bar
│           └── footer.html          # Footer
│
├── docs/
│   ├── AGENT_GUIDE.md               # [THIS FILE] Technical agent handoff & system spec
│   └── USER_GUIDE.md                # Simple, non-complex guide for Shubham
│
├── tests/
│   ├── test_courses.py              # 10 integration tests for admissions engine
│   └── test_main.py                 # Health and baseline route checks
│
├── requirements.txt                 # FastAPI, uvicorn, jinja2, sqlalchemy, psycopg2-binary
├── requirements-dev.txt             # pytest, httpx, black, flake8
├── render.yaml                      # Render Blueprint with DATABASE_URL
└── Procfile                         # web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## 5. Relational Database Schema (`app/apps/courses/models.py`)

### Table: `batches`
Stores scheduled course cohorts.
* `id`: Integer (PK, Autoincrement)
* `batch_code`: String(50), Unique, Indexed (e.g., `DA-WKND-2026-B1`)
* `title`: String(150) (e.g., "Weekend Data Analysis Masterclass")
* `course_name`: String(150) (Default: "Data Analysis")
* `technologies`: String(255) (Default: "Python, SQL, PowerBI, Excel, Tableau")
* `schedule_days`: String(100) (Default: "Saturday & Sunday")
* `schedule_time`: String(100) (Default: "6:00 PM – 8:00 PM IST")
* `start_date`: String(50) (e.g., "Upcoming Weekend")
* `duration`: String(50) (Default: "8-10 Weeks Hands-On")
* `status`: String(50) ("enrolling", "upcoming", "in_progress", "completed")
* `max_seats`: Integer (Default: 25)
* `description`: Text
* `is_active`: Boolean (Default: True)
* `created_at`: DateTime (UTC)

### Table: `student_leads`
Stores both general inquiries and direct batch enrollments.
* `id`: Integer (PK, Autoincrement)
* `lead_type`: String(30), Indexed (`"enquiry"` vs `"batch_registration"`)
* `batch_id`: Integer, FK -> `batches.id` (Nullable, ondelete="SET NULL")
* `full_name`: String(120), Not Null
* `email`: String(150), Indexed, Not Null
* `phone`: String(30), Indexed, Not Null (Mobile / WhatsApp)
* `current_status`: String(80) ("College Student", "Working Professional", "Fresher", "Career Changer")
* `prior_experience`: String(80) ("Beginner", "Basic Python", "Excel User", etc.)
* `preferred_schedule`: String(100) (Default: "Saturday & Sunday 6:00 PM – 8:00 PM IST")
* `message`: Text (Student questions, goals, counseling requirements)
* `status`: String(30), Indexed (Default: `"new"`; transitions to `"contacted"`, `"enrolled"`, `"closed"`)
* `admin_notes`: Text (Instructor follow-up notes)
* `source_ip`: String(50) (Optional client IP for spam analysis)
* `created_at`: DateTime (UTC)
* `updated_at`: DateTime (UTC)

---

## 6. REST API Endpoint Catalog (`/api/courses`)

| Method | Endpoint | Description | Request Body / Params |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/courses/instructor` | Instructor bio, tools, schedule, verified experience (No fees). | None |
| `GET` | `/api/courses/batches` | List all active enrolling cohorts. | None |
| `GET` | `/api/courses/batches/{id}` | Single batch details and seat registration count. | `id` in path |
| `POST` | `/api/courses/enquiry` | Submit enquiry (Supports JSON & standard HTML form). | `full_name`, `email`, `phone`, `current_status`, `message` |
| `POST` | `/api/courses/register` | Register for batch (JSON & HTML form compatible). | `full_name`, `email`, `phone`, `batch_id` (optional), `current_status`, `prior_experience`, `message` |
| `GET` | `/api/courses/leads` | Admin lead list with filters. | Query: `lead_type`, `batch_id`, `status`, `search` |
| `GET` | `/api/courses/leads/summary` | Admission conversion counts & pipeline stats. | None |
| `GET` | `/api/courses/leads/export.csv` | Download complete lead list as CSV attachment. | Defined **before** `/leads/{id}` to avoid 422 routing clashes |
| `GET` | `/api/courses/leads/{id}` | Detailed single lead inspection. | `id` in path |
| `PATCH` | `/api/courses/leads/{id}/status`| Update lead stage & counseling notes. | `status`, `admin_notes` |
| `POST` | `/api/courses/batches` | Create a new cohort batch. | `BatchCreate` payload |

---

## 7. Operational & Verification Commands

### Run Local Development Server
```powershell
uvicorn app.main:app --reload --port 8000
```
* Homepage: `http://localhost:8000`
* Swagger API Docs: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`

### Run Pytest Test Suite
```powershell
python -m pytest -v
```
All 10 tests in `tests/test_courses.py` and `tests/test_main.py` must pass.

### Git Conventions
All commits follow Conventional Commits:
```bash
git commit -m "feat(courses): description"
git commit -m "fix(courses): description"
git commit -m "style(ui): description"
```

---

## 8. Next Immediate Steps (Phase 2 - Frontend)

1. **Transform `app/templates/index.html`**:
   - Reposition hero banner: Focus on Data Analysis Mentorship by Shubham Singh.
   - Highlight the 5 tools: Python, SQL, Power BI, Excel, Tableau with Devicons/SVGs.
   - Schedule badge: "Saturday & Sunday | 6:00 PM – 8:00 PM IST".
   - Prominent CTA buttons: "Enroll in Weekend Batch" (opens registration modal) & "Ask a Question / Enquiry" (opens enquiry modal).
2. **Interactive Modals / Forms**:
   - Build client-side asynchronous modal forms submitting to `/api/courses/register` and `/api/courses/enquiry` via Fetch API with immediate feedback and toast notifications.
3. **Admin Dashboard & Monitoring**:
   - Hidden admin portal at `/admin/login` and `/admin/dashboard`.
   - Registration strictly disabled on `/admin` (`/admin/signup` redirects to `/admin/login`).
   - Default instructor user: `admin`, seeded automatically with bcrypt password hash via `ADMIN_PASSWORD` or fallback hash (no plaintext in repository).
   - Real-time lead management, pipeline stage updates, notes, search, filtering, and one-click CSV export.
4. **Syllabus PDF Delivery**:
   - Course syllabus is served as a dedicated PDF file from `app/static/pdf/Data_Analysis_Syllabus.pdf` at `/course/syllabus/download` (attachment) and `/course/syllabus` (inline view).
5. **Optional Student Email**:
   - Email is strictly optional on all enquiry and batch registration forms (`register.html`, `index.html` modals, and `/api/courses/*`). Only full name and phone/WhatsApp are mandatory.
