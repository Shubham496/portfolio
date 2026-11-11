# AGENT PROJECT GUIDE & CONTEXT SPECIFICATION (DEFINITIVE REFERENCE)

> **PRIMARY DIRECTIVE FOR AI AGENTS**:
> This document is the **single-source-of-truth reference manual** for the entire codebase.
> It contains exhaustive architectural details, exact schemas, credentials, routes, business constraints, and implementation specifics so that you **do not have to inspect raw files** before making decisions or answering technical questions.

---

## 1. Project Mission & Identity

* **Platform Name**: Data Analysis Training & Student Admission Engine
* **Platform Owner & Instructor**: **Shubham Singh**
  * **Title**: Lead Python & Data Architecture Consultant & Instructor
  * **Experience**: 3+ years consulting & teaching across Ducat, Netmax Technologies, and LNP Infotech.
  * **Track Record**: Architected enterprise data services and trained 550+ students, senior developers & data engineers.
  * **Contact**: `shubhamsingh41100@gmail.com` | WhatsApp: `+91 8727864157`
  * **Profiles**: GitHub: `https://github.com/Shubham496` | LinkedIn: `https://linkedin.com/in/shubham469`

---

## 2. Immutable Business Rules (NON-NEGOTIABLE)

1. **Course Curriculum — Exactly 5 Pillars**:
   - **Python**: Pandas, NumPy, ETL pipelines, automated extraction, data wrangling.
   - **SQL**: Complex queries, Window functions, Common Table Expressions (CTEs), multi-table joins, relational modeling.
   - **Power BI**: Data modeling, DAX formulas, executive KPI dashboards, automated refreshes.
   - **Excel**: Advanced XLOOKUP, Index/Match, multi-table Pivot tables, financial modeling.
   - **Tableau**: Visual storytelling, parameters, calculated fields, dashboard actions.
2. **Batch Class Schedule**:
   - **Days**: **Saturday and Sunday ONLY**.
   - **Timings**: **6:00 PM to 8:00 PM IST** (2 hours/day = 4 hours/week).
   - **Duration**: **8 to 10 Weeks Hands-On Mentorship**.
   - **Batch Format**: Live interactive weekend cohort (Batch code: `DA-WKND-2026-B1`).
3. **Strict Zero-Fee Policy**:
   - **NO pricing or tuition fees appear anywhere on the public website**.
   - No prices, no discounts, no currency symbols, no payment gateways.
   - Financial arrangements are strictly discussed privately between Shubham and the student during counseling calls.
4. **Optional Student Email**:
   - Email is **strictly optional** across all student-facing enrollment and inquiry forms (`/register`, homepage modals, `/api/courses/*`).
   - Only **Full Name** and **Phone / WhatsApp Number** are mandatory.
5. **Admin Access Exclusivity**:
   - Secret hidden portal at `/admin/login` and `/admin/dashboard`.
   - **Zero public links** to the admin portal on the landing page or navbar.
   - Public signup is permanently disabled (`/admin/signup` redirects with 303 to `/admin/login`).
6. **Continuous Git Maintenance & Repository Hygiene (ALWAYS MANDATORY)**:
   - Developers and AI agents must proactively maintain git repository cleanliness at all times.
   - Every completed task, bug fix, feature, or refactoring must be staged and committed with clean, descriptive commit messages.
   - The working directory must always be kept clean (`git status` clean, no leftover untracked debug artifacts).
   - Remote synchronization: Changes must be pushed to remote repository (`origin/main`) to ensure code durability.
   - **Zero-Secret Leak Guard**: Never stage or commit `.env`, plaintext passwords, authentication tokens, or SQLite databases (`*.db`). Always ensure `.gitignore` remains active.

---

## 3. Environment Variables & Secret Configuration

Auto-loaded via `python-dotenv` from `.env` in `app/core/config.py`:

| Variable | Default Fallback | Purpose |
| :--- | :--- | :--- |
| `ADMIN_PASSWORD` | Loaded from `.env` | Master instructor password for the `admin` account (never hardcoded in docs). |
| `AGENT_PASSWORD` | Loaded from `.env` | Dedicated credentials for the exclusive `agent_admin` AI/test execution profile. |
| `SECRET_KEY` | `shubham-data-analysis-secret-key-2026` | Cryptographic secret for signing session cookies via `itsdangerous`. |
| `DATABASE_URL` | `""` (falls back to `sqlite:///./course_platform.db`) | External cloud PostgreSQL URI for Render.io deployments. |
| `ENVIRONMENT` | `development` | Switch between `LocalSettings` and `DeploymentSettings`. |
| `PORT` | `8000` | Port binding on cloud platforms. |

### Verified Admin Credentials Architecture
- **Instructor Profile**: `admin` (email: `admin@mythostech.in`)
  - Password configured securely in `.env` as `ADMIN_PASSWORD`.
  - Never exposed in plain text in documentation or public commit history.
- **Exclusive AI Agent & Automation Profile**: `agent_admin` (email: `agent@mythostech.in`)
  - Password configured securely in `.env` as `AGENT_PASSWORD`.
  - Dedicated for automated test suites, health verification, and background administration.
- **Session Cookie Name**: `admin_session` (HTTP-only, Lax, 7 days max age)
- **Password Hash**: Modern bcrypt with 12 rounds of salt.

---

## 4. Complete Codebase File Map

```text
coding/
│
├── .env                                # Local secret environment variables (ADMIN_PASSWORD, SECRET_KEY)
├── .env.example                        # Template documenting expected environment variables
├── .gitignore                          # Git exclusions (venv, pycache, sqlite dbs)
├── CHANGELOG.md                        # Reverse-chronological implementation and release log
├── course_platform.db                  # Local SQLite database for courses, batches, leads, and admin
├── portfolio.db                        # Local SQLite database for the todos micro-app
├── Procfile                            # Cloud process launcher: web: uvicorn app.main:app ...
├── README.md                           # Main developer and repository README
├── render.yaml                         # Render.io blueprint for one-click web service deployment
├── requirements.txt                    # Production dependencies (FastAPI, Uvicorn, SQLAlchemy, etc.)
├── requirements-dev.txt                # Testing & dev dependencies (pytest, httpx)
│
├── app/
│   ├── main.py                         # Primary application entrypoint; mounts routers, static files, home routes
│   │
│   ├── core/
│   │   ├── base_config.py              # Pydantic BaseSettings containing personal info, social links, bio
│   │   ├── config.py                   # Calls load_dotenv() and switches between Local/Deployment settings
│   │   ├── deployment.py               # Production settings & Render cloud port binding
│   │   └── local.py                    # Local debug settings
│   │
│   ├── apps/
│   │   ├── courses/                    # [CORE MODULE] Course & Student Admission Engine
│   │   │   ├── __init__.py             # Exposes courses module
│   │   │   ├── database.py             # Dual-engine SQLAlchemy connection (PostgreSQL/SQLite)
│   │   │   ├── models.py               # ORM Entities: Batch, StudentLead, AdminUser
│   │   │   ├── schemas.py              # Pydantic v2 schemas: EnquiryCreate, BatchRegistrationCreate, etc.
│   │   │   ├── services.py             # Seeding, CRUD, filters, pagination, CSV exporter, instructor profile
│   │   │   ├── auth.py                 # Bcrypt hashing, verification, session tokens, require_admin guard
│   │   │   ├── router.py               # Public API routes (/api/courses/*) for JSON & HTML form posts
│   │   │   ├── admin_router.py         # Protected instructor portal routes (/admin/login, /admin/dashboard)
│   │   │   └── generate_syllabus_pdf.py# Standalone script building Data_Analysis_Syllabus.pdf via fpdf2
│   │   │
│   │   └── todos/                      # [SUPPORTING MODULE] Micro-app for internal task tracking
│   │       ├── models.py               # SQLite helpers for project_todos table in portfolio.db
│   │       ├── router.py               # APIRouter for /apps/todos
│   │       └── templates/todos.html    # Kanban task board template
│   │
│   ├── static/
│   │   ├── css/style.css               # Custom theme styles & subtle animations
│   │   ├── js/main.js                  # Client modal handling, theme toggle, toast notifications
│   │   ├── Images/Profile/profilePhoto.jpeg # Shubham's instructor photo
│   │   └── pdf/
│   │       ├── Data_Analysis_Syllabus.pdf   # 2-Page Data Analysis course brochure
│   │       └── resume.pdf                   # Shubham's formal technical resume
│   │
│   └── templates/
│       ├── base.html                   # Global layout (HTML skeleton, dark mode script, Lucide icons)
│       ├── index.html                  # Landing page orchestrator (includes sections/* partials)
│       ├── register.html               # Dedicated full-page weekend batch enrollment form
│       ├── confirmation.html           # Post-registration student confirmation page
│       ├── sections/                   # Modular landing page section partials
│       │   ├── hero.html               # Hero headline, CTAs, trust metric bar & floating photo card
│       │   ├── engine.html             # The Problem vs. Mythos Learning Engine 4-step pipeline
│       │   ├── programs.html           # 2 Core System Tracks (Backend Engineering & BI Analytics)
│       │   ├── methodology.html        # How You Will Learn / "This is not passive learning"
│       │   ├── projects.html           # 3 Production Capstone project cards
│       │   ├── admission.html          # Outcomes & 4-step admission process
│       │   ├── career.html             # Career acceleration (GitHub, ATS Resume, LinkedIn, Mocks)
│       │   ├── syllabus.html           # Expandable 6-module curriculum accordion & inline toggle JS
│       │   ├── mentor.html             # Shubham Singh bio, experience timeline & WhatsApp link
│       │   └── modals.html             # Enrollment & Enquiry modals with toast notifications
│       ├── partials/
│       │   ├── navbar.html             # Top navigation with syllabus download CTA & theme toggle
│       │   └── footer.html             # Footer with copyright, disclaimer, and social links
│       └── admin/
│           ├── login.html              # Instructor secret sign-in page
│           └── dashboard.html          # Protected live monitoring dashboard with pagination
│
├── docs/
│   ├── README.md                       # Documentation hub & platform manual (Secondary README)
│   ├── USER_GUIDE.md                   # Plain-English guide for Shubham explaining admin & leads
│   ├── AGENT_GUIDE.md                  # This file (Definitive agent technical specification)
│   ├── generate_doc.py                 # Python script to build Word document action tracker
│   └── Project_Action_Plan_and_Tracker.docx # Formal Word document roadmap
│
└── tests/
    ├── test_main.py                    # Health check (/health) and homepage (/) tests
    └── test_courses.py                 # 13 comprehensive tests for admissions, PDF, auth, and pagination
```

---

## 5. Database Architecture & Complete Schemas

### Dual-Engine Strategy (`app/apps/courses/database.py`)
- **Local Dev**: When `DATABASE_URL` is empty, connects to `sqlite:///./course_platform.db` with `check_same_thread=False`.
- **Cloud Prod (Render.io)**: Automatically converts `postgres://` to `postgresql://` and sets:
  - `pool_pre_ping=True` (verifies socket liveness before checkout)
  - `pool_recycle=300` (recycles connections every 5 minutes to avoid idle drops)
  - `pool_size=5`, `max_overflow=10`

### Table: `batches` (Mapped to `Batch`)
Represents scheduled cohorts.
* `id`: `Integer`, Primary Key, Autoincrement.
* `batch_code`: `String(50)`, Unique, Indexed, Not Null (e.g. `"DA-WKND-2026-B1"`).
* `title`: `String(150)`, Not Null (e.g. `"Weekend Data Analysis Masterclass"`).
* `course_name`: `String(150)`, Default `"Data Analysis"`.
* `technologies`: `String(255)`, Default `"Python, SQL, PowerBI, Excel, Tableau"`.
* `schedule_days`: `String(100)`, Default `"Saturday & Sunday"`.
* `schedule_time`: `String(100)`, Default `"6:00 PM – 8:00 PM IST"`.
* `start_date`: `String(50)`, Default `"Upcoming Weekend"`.
* `duration`: `String(50)`, Default `"8-10 Weeks Hands-On"`.
* `status`: `String(50)`, Default `"enrolling"` (options: `enrolling`, `upcoming`, `ongoing`, `completed`).
* `max_seats`: `Integer`, Default `25`.
* `description`: `Text`, Nullable.
* `is_active`: `Boolean`, Default `True`, Indexed.
* `created_at`: `DateTime`, Default `utcnow`.
* **Relationship**: `registrations` -> `StudentLead.batch` (`cascade="all, delete-orphan"`).

### Table: `student_leads` (Mapped to `StudentLead`)
Stores all student applications and callback inquiries.
* `id`: `Integer`, Primary Key, Autoincrement.
* `lead_type`: `String(30)`, Indexed, Not Null (`"batch_registration"` or `"enquiry"`).
* `batch_id`: `Integer`, FK -> `batches.id`, Nullable, Indexed (`ondelete="SET NULL"`).
* `full_name`: `String(120)`, Not Null.
* `email`: `String(150)`, Nullable, Indexed (Optional).
* `phone`: `String(30)`, Not Null, Indexed (WhatsApp/Mobile).
* `current_status`: `String(80)`, Nullable (`"Working Professional"`, `"College Student"`, `"Fresher"`).
* `prior_experience`: `String(80)`, Nullable (`"Beginner"`, `"Basic Python"`, `"Excel User"`).
* `preferred_schedule`: `String(100)`, Default `"Saturday & Sunday 6:00 PM – 8:00 PM IST"`.
* `message`: `Text`, Nullable (Student goals or questions).
* `status`: `String(30)`, Default `"new"`, Indexed (`"new"`, `"contacted"`, `"enrolled"`, `"closed"`).
* `admin_notes`: `Text`, Nullable (Counseling notes added by Shubham).
* `source_ip`: `String(50)`, Nullable.
* `created_at`: `DateTime`, Default `utcnow`.
* `updated_at`: `DateTime`, Default `utcnow`, onupdate.
* **Special Properties in `to_dict()`**:
  - `created_date`: Formatted calendar date (e.g. `"Nov 11, 2026"`).
  - `created_time`: Formatted 12-hour timestamp (e.g. `"10:45 PM"`).

### Table: `admin_users` (Mapped to `AdminUser`)
Stores instructor accounts.
* `id`: `Integer`, Primary Key, Autoincrement.
* `username`: `String(80)`, Unique, Indexed, Not Null (Default: `"admin"`).
* `email`: `String(150)`, Unique, Indexed, Not Null (Default: `"admin@mythostech.in"`).
* `hashed_password`: `String(255)`, Not Null (Bcrypt hash).
* `is_active`: `Boolean`, Default `True`.
* `created_at`: `DateTime`, Default `utcnow`.

### Table: `project_todos` (SQLite inside `portfolio.db`)
* `id`: `Integer`, Primary Key.
* `title`: `Text`, Not Null.
* `category`: `Text`, Default `"General"`.
* `priority`: `Text`, Default `"Medium"`.
* `status`: `Text`, Default `"pending"`.
* `notes`: `Text`.
* `created_at`: `Timestamp`.
* `completed_at`: `Timestamp`.

---

## 6. Complete REST & Web Route Catalog

### Frontend HTML Routes
| Method | Path | Template | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | `index.html` | Primary landing page (Bio, 5 pillars, curriculum, modals). |
| `GET` | `/register` | `register.html` | Dedicated full-page weekend batch enrollment form. |
| `GET` | `/registration-success` | `confirmation.html` | Post-enrollment confirmation page. |
| `GET` | `/course/syllabus/download` | N/A (PDF attachment) | Download `Data_Analysis_Syllabus.pdf`. |
| `GET` | `/course/syllabus` | N/A (Inline PDF) | View syllabus PDF directly in browser. |
| `GET` | `/resume` | N/A (Inline PDF) | Serve Shubham's resume PDF. |
| `GET` | `/health` | JSON response | Health probe for Render uptime monitors. |

### Admin Portal Routes (`app/apps/courses/admin_router.py`)
| Method | Path | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/admin` | No | 303 Redirect to `/admin/dashboard`. |
| `GET` | `/admin/login` | No | Instructor sign-in page. If already authenticated, redirects to dashboard. |
| `POST` | `/admin/login` | No | Authenticates `username` and `password`. Sets signed `admin_session` cookie. |
| `GET` | `/admin/signup` | No | Strictly disabled; returns 303 redirect to `/admin/login`. |
| `POST` | `/admin/signup` | No | Strictly disabled; returns 303 redirect to `/admin/login`. |
| `GET` | `/admin/dashboard` | **Yes** (`require_admin`) | Protected live leads monitor with pagination, filters, and KPI cards. |
| `POST` | `/admin/leads/{id}/status` | **Yes** (`require_admin`) | Updates lead status & counseling notes; redirects preserving page & filters. |
| `GET` | `/admin/logout` | No | Clears `admin_session` cookie and redirects to `/admin/login`. |

### Public Admissions API (`app/apps/courses/router.py`)
| Method | Path | Request Body | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/courses/instructor` | None | Instructor profile, tools, verified highlights, no fees. |
| `GET` | `/api/courses/batches` | None | List active cohorts with seat enrollment counts. |
| `GET` | `/api/courses/batches/{id}` | Path param `id` | Single batch inspection. |
| `POST` | `/api/courses/enquiry` | JSON or Form (`EnquiryCreate`) | Submit student inquiry. Accepts JSON or standard HTML form. |
| `POST` | `/api/courses/register` | JSON or Form (`BatchRegistrationCreate`)| Enroll student into batch. Email is optional. |
| `GET` | `/api/courses/leads` | Query params | JSON list of leads (filtered by `lead_type`, `status`, `search`). |
| `GET` | `/api/courses/leads/summary`| None | KPI metrics: `total_leads`, `batch_registrations`, `enquiries`, `new`. |
| `GET` | `/api/courses/leads/export.csv`| None | Attachment download of all leads as CSV. |
| `GET` | `/api/courses/leads/{id}` | Path param `id` | Single lead detail lookup. |
| `PATCH`| `/api/courses/leads/{id}/status`| JSON (`LeadStatusUpdate`) | Update status & notes via JSON API. |

---

## 7. Admin Dashboard Pagination & Table Columns

### Pagination Architecture (`app/apps/courses/services.py:get_leads_paginated`)
```python
def get_leads_paginated(
    db: Session,
    lead_type: Optional[str] = None,
    batch_id: Optional[int] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    per_page: int = 10
) -> Dict[str, Any]:
    ...
```
* **Query Parameters**:
  - `page`: Integer (1-based, default `1`).
  - `per_page`: Integer (default `10`; options: `10`, `25`, `50`; max capped at `100`).
* **Return Structure**:
  ```json
  {
    "items": [...],
    "total": 42,
    "page": 1,
    "per_page": 10,
    "total_pages": 5,
    "start_item": 1,
    "end_item": 10,
    "has_prev": false,
    "has_next": true,
    "prev_page": null,
    "next_page": 2
  }
  ```

### Table Column Layout (`app/templates/admin/dashboard.html`)
The table is separated into 7 distinct columns:
1. **Type**: Visual pill badge (`Registration` in blue, `Enquiry` in purple).
2. **Submitted Date**: Calendar date (`created_date`, e.g. `Nov 11, 2026`) and time (`created_time`, e.g. `10:45 PM`).
3. **Student**: Full name in bold text + career stage (`Working Professional`, `Student`).
4. **Contact**: WhatsApp direct link (`https://wa.me/<cleaned_phone>`) + clickable `mailto:` link.
5. **Message / Goals**: Prior experience tag + inquiry notes (line-clamped to 3 lines).
6. **Status**: Dedicated column with colored status indicator (`New` amber, `Contacted` blue, `Enrolled` emerald, `Closed` slate) + inline select dropdown.
7. **Admin Notes & Action**: Dedicated column with text input for counselor notes + Save button linked via HTML5 `form="lead-form-{{ lead.id }}"`.

---

## 8. Critical Guardrails & Common Pitfalls

1. **Account Isolation & Secret Protection**:
   - `tests/test_courses.py:test_admin_auth_and_dashboard_flow` uses the dedicated `agent_admin` profile and `AGENT_PASSWORD`.
   - The instructor's personal `admin` account password (`ADMIN_PASSWORD`) is stored in `.env` and is strictly never mutated, exposed, or used in automated test runs.
2. **Database Seeding Safeguard (`app/apps/courses/services.py:init_courses_db`)**:
   - Only updates the admin password hash if `ADMIN_PASSWORD` or `ADMIN_PASSWORD_HASH` is explicitly present in `os.environ`.
   - Never overwrites an existing user hash with fallback values if neither variable is set.
3. **Form Route Precedence**:
   - Route `GET /api/courses/leads/export.csv` must remain defined **before** `GET /api/courses/leads/{id}` to prevent FastAPI from matching `export.csv` as an integer ID (which causes 422 errors).
4. **Email Formatting**:
   - Empty email strings (`""`) are converted to `None` in Pydantic schemas and database rows so they don't trigger invalid email format validation.

---

## 9. Verification & Operational Directives

### Run Development Server
```powershell
uvicorn app.main:app --reload --port 8000
```

### Run Full Test Suite
```powershell
python -m pytest -v
```
All 15 tests must pass with zero failures.

---

## 10. Mandatory Git Maintenance & Operational Protocols

To preserve repository durability, auditability, and team collaboration integrity, developers and AI agents must follow this standardized Git lifecycle:

### Core Git Rules & Workflows
1. **Pre-Commit Verification**:
   - Always run the full automated test suite (`python -m pytest -v`) before staging commits. Never commit broken builds or failing tests.
2. **Review Working Tree State (`git status`)**:
   - Inspect all unstaged and untracked files before running `git add`.
   - Ensure no temporary scratch scripts, scratch directories, or transient test artifacts remain untracked.
3. **Strict Secrets & Artifact Exclusions**:
   - **NEVER** stage or commit `.env`, `.env.local`, or any files containing private credentials or plaintext passwords.
   - **NEVER** commit SQLite databases (`course_platform.db`, `portfolio.db`, `*.sqlite`, `*.db`).
   - If an environment variable is introduced or changed, document it with safe dummy placeholders in `.env.example`.
4. **Synchronized Documentation Updates**:
   - Whenever functional code, templates, or database models change, immediately document the change in `CHANGELOG.md` and keep `docs/AGENT_GUIDE.md` updated.
5. **Conventional Commit Messages**:
   - Write clear, present-tense, descriptive commit messages summarizing the changes:
     - `feat:` for new capabilities or pages.
     - `refactor:` for architectural restructuring without UX changes.
     - `fix:` for bug fixes or test repairs.
     - `docs:` for documentation updates.
     - `chore:` for dependency and configuration updates.
6. **Remote Synchronization (`git push`)**:
   - Once changes are verified and committed locally, push to the upstream tracking branch (`git push origin <branch>`) to maintain alignment with remote GitHub repositories.
