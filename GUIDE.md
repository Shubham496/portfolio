# MYTHOS Online Institute — Technical Guide & System Specification (GUIDE.md)

> **PRIMARY DIRECTIVE FOR DEVELOPERS & AI AGENTS**:
> This document is the **definitive single-source-of-truth manual** for the current state of the codebase.
> It describes current implementation, architecture, API contracts, schemas, and operational constraints.
> For historical records, refer to [`Changeslog.md`](file:///f:/Projects/coding/Changeslog.md). For operational directives, refer to [`AGENTS.md`](file:///f:/Projects/coding/AGENTS.md).

---

## 1. Project Purpose & Mission

**MYTHOS Online Institute** (`mythostech.in`) is a high-performance web platform built on **FastAPI** serving two primary missions:
1. **Live Online Academic Cohorts**: Delivers weekend cohort mentorship in **Digital Marketing** (Performance Marketing & SEO/Growth) and **Data Analytics** (Python, SQL, Power BI, Excel, Tableau).
2. **Resource Library & Knowledge Engine**: Provides university-rigorous documentation, W3Schools-style sequential study tracks, and interview viva preparation covering **34 major programming languages, databases, tools, and platforms**.

---

## 2. Technology Stack & Key Dependencies

### Core Stack
- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) `0.110+` running on Python `3.10.11`
- **ASGI Web Server**: [Uvicorn](https://www.uvicorn.org/) `0.28+`
- **Templating Engine**: [Jinja2](https://jinja.palletsprojects.com/) `3.1+` with modular component partials
- **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) `2.0+` with PostgreSQL driver (`psycopg2-binary`)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/) and `pydantic-settings`
- **Authentication & Security**: `bcrypt` (12 rounds) and `itsdangerous` (`URLSafeTimedSerializer`)
- **Documentation Engine**: `markdown>=3.6.0`, `python-frontmatter>=1.1.0`, `pymdown-extensions>=10.7`
- **PDF Generation**: `fpdf2>=2.7.0` for dynamic, publication-grade syllabus brochures
- **Styling & UI**: Tailwind CSS (via CDN), Lucide Icons, Devicons, Prism.js syntax styling

### Production Dependencies (`requirements.txt`)
```text
fastapi>=0.110.0,<1.0.0
uvicorn[standard]>=0.28.0,<1.0.0
jinja2>=3.1.3,<4.0.0
pydantic-settings>=2.2.1,<3.0.0
python-multipart>=0.0.9
aiofiles>=23.2.1
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.9
itsdangerous>=2.2.0
bcrypt>=4.0.0
fpdf2>=2.7.0
python-dotenv>=1.0.0
markdown>=3.6.0
python-frontmatter>=1.1.0
pymdown-extensions>=10.7
```

### Development & Testing Dependencies (`requirements-dev.txt`)
```text
pytest>=8.1.0
httpx>=0.27.0
flake8>=7.0.0
black>=24.2.0
python-docx>=1.1.0
```

---

## 3. Project Directory Map & File Responsibilities

```text
coding/
│
├── GUIDE.md                            # This document (Current system knowledge manual)
├── Changeslog.md                       # Latest 15 development history entries
├── CHANGELOG_ARCHIVE.md                # Historical changelog records
├── AGENTS.md                           # 15 persistent golden rules for AI agents
├── README.md                           # Top-level repository overview
├── render.yaml                         # Cloud deployment blueprint for Render.io
├── Procfile                            # Cloud process launcher (uvicorn app.main:app)
├── requirements.txt                    # Production dependencies
├── requirements-dev.txt                # Development dependencies
├── .env                                # Local secrets (ADMIN_PASSWORD, SECRET_KEY) [git-ignored]
├── .env.example                        # Template documenting expected environment variables
├── .gitignore                          # Exclusions (.env, *.db, external_assets/, venv)
├── course_platform.db                  # Local SQLite database for admissions & admin
├── portfolio.db                        # Local SQLite database for todos micro-app
│
├── app/
│   ├── main.py                         # FastAPI application entrypoint, router mounts, root routes
│   │
│   ├── core/                           # Configuration layer
│   │   ├── base_config.py              # Pydantic BaseSettings (metadata, contact, links)
│   │   ├── config.py                   # Environment loader (switches LocalSettings / DeploymentSettings)
│   │   ├── local.py                    # Local development configuration (debug=True, SQLite fallback)
│   │   └── deployment.py               # Production configuration (Render cloud $PORT, security)
│   │
│   ├── apps/                           # Modular application domains
│   │   ├── courses/                    # Admissions & Cohort Management
│   │   │   ├── models.py               # Entities: Batch, StudentLead, AdminUser, User, UserActivityLog
│   │   │   ├── schemas.py              # Pydantic v2 schemas: EnquiryCreate, BatchRegistrationCreate, StudentRegister
│   │   │   ├── database.py             # Dual-engine connection pool (SQLite local, PostgreSQL cloud)
│   │   │   ├── services.py             # CRUD, pagination math, CSV export, db seeding, user & activity services
│   │   │   ├── auth.py                 # Bcrypt hashing, session cookies (admin & student), auth dependencies
│   │   │   ├── router.py               # Public API routes (/api/courses/*)
│   │   │   ├── admin_router.py         # Protected admin portal (/admin/*)
│   │   │   ├── student_router.py       # Student portal & auth routes (/student/*, /api/student/*, /api/activity/log)
│   │   │   └── generate_syllabus_pdf.py# Dynamic 2-page syllabus PDF generator (fpdf2)
│   │   │
│   │   ├── library/                    # 34-Technology Knowledge & Documentation Engine
│   │   │   ├── services.py             # PyMdown markdown parsing, LRU cache, topic trees, practice datasets catalog
│   │   │   ├── router.py               # Web routes (/library/*), datasets vault & JSON APIs (/api/library/*)
│   │   │   └── models.py               # Re-exports User & UserActivityLog; future digital products
│   │   │
│   │   └── todos/                      # Supporting internal task tracking micro-app
│   │       ├── models.py               # SQLite helpers for project_todos in portfolio.db
│   │       ├── router.py               # Routes for /apps/todos
│   │       └── templates/todos.html    # Kanban task board template
│   │
│   ├── content/                        # Markdown study guides and notes repository
│   │   └── sql/                        # SQL notes, viva sets, and W3Schools study track blueprints
│   │
│   ├── static/                         # Static web assets
│   │   ├── css/style.css               # Custom theme styles & typography
│   │   ├── js/main.js                  # Modals, toasts, syllabus accordion, theme toggle
│   │   ├── pdf/                        # Generated PDF syllabus & resume
│   │   └── Images/                     # Visual assets and instructor photos
│   │
│   └── templates/                      # Component-decomposed Jinja2 templates
│       ├── base.html                   # HTML5 layout shell (Poppins font, Lucide icons)
│       ├── index.html                  # Landing page orchestrator (15 lines composing sections/)
│       ├── register.html               # Dedicated full-page weekend cohort registration
│       ├── confirmation.html           # Post-registration student confirmation page
│       ├── partials/                   # Global components (navbar.html, in_page_nav.html, footer.html)
│       ├── sections/                   # 10 modular landing page section partials
│       ├── admin/                      # Instructor portal views (login.html, dashboard.html)
│       ├── student/                    # Student portal views (login.html, register.html, dashboard.html)
│       └── library/                    # Docs & dataset views (index.html, subject_hub.html, reader.html, datasets.html, dataset_detail.html)
│
├── design/                             # Design system & brand asset repository
│   ├── GUIDELINES.md                   # Brand identity, color tokens, typography, certificate specs
│   ├── tokens.json                     # Machine-readable design tokens
│   ├── certificate_generator_template.py# Automation script for student completion certificates
│   └── assets/                         # Vector SVGs and transparent brand marks
│
├── docs/                               # Architectural deep-dives & operations
│   ├── architecture.md                 # Detailed application architecture & component decomposition
│   ├── database.md                     # Database schemas, relationships, dual-engine strategy
│   ├── deployment.md                   # Complete Render cloud deployment & rollback guide
│   ├── USER_GUIDE.md                   # Plain-English guide for the platform owner
│   └── task_new.md                     # Knowledge Engine phased implementation roadmap
│
├── external_assets/                    # [DECOUPLED VAULT] Git-ignored submodule (mythos-assets)
│                                       # Houses datasets, downloads, and large images via CDN
│
└── tests/                              # Automated test suite (46 tests passing cleanly)
    ├── test_courses.py                 # Admissions, registrations, auth, CSV export, PDF (13 tests)
    ├── test_library.py                 # W3Schools panels, sequential nav, reader, catalog (17 tests)
    ├── test_student_auth.py            # Student auth, session cookies, activity logging, datasets (14 tests)
    └── test_main.py                    # Root health check and homepage integration (2 tests)
```

---

## 4. Application Architecture Summary

For the exhaustive architectural specification, see [`docs/architecture.md`](file:///f:/Projects/coding/docs/architecture.md).

### 4.1 Sub-App Modularization
- `app/apps/courses`: Manages student admissions funnels, live cohort registrations, syllabus PDF generation, and protected instructor operations.
- `app/apps/library`: Manages documentation rendering, YAML frontmatter extraction, in-memory LRU/TTL caching, W3Schools-style panel navigation, and sequential curricula.
- `app/apps/todos`: Lightweight Kanban micro-app for internal milestone tracking.

### 4.2 Presentation & Template Decomposition
The landing page (`app/templates/index.html`) is modularized into 10 isolated partials in `app/templates/sections/`:
`hero.html`, `engine.html`, `programs.html`, `methodology.html`, `projects.html`, `admission.html`, `career.html`, `syllabus.html`, `mentor.html`, `modals.html`.
Navigation features a top inter-page bar (`navbar.html`) and a left in-page docking rail (`in_page_nav.html`) with scroll-spy tracking.

---

## 5. Complete API Endpoints Catalog

### 5.1 Public Web Routes (`app/main.py`)
| Method | Path | Response Type | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | HTML (`index.html`) | Primary landing page orchestrating all section partials. |
| `GET` | `/register` | HTML (`register.html`) | Dedicated weekend cohort registration form. |
| `GET` | `/registration-success` | HTML (`confirmation.html`) | Post-enrollment confirmation page. |
| `GET` | `/privacy` | HTML (`legal/privacy.html`) | Data protection, WhatsApp outreach terms, and zero data-selling policy. |
| `GET` | `/terms` | HTML (`legal/terms.html`) | Academic guidelines, static code execution invariant, and IP protections. |
| `GET` | `/refund-policy` | HTML (`legal/refund_policy.html`) | Free demo guarantee, cohort rescheduling, and refund terms. |
| `GET` | `/course/syllabus/download` | File (`Data_Analysis_Syllabus.pdf`) | Direct attachment download of syllabus brochure. |
| `GET` | `/course/syllabus` | File (Inline PDF) | Inline browser preview of syllabus brochure. |
| `GET` | `/resume` | File (Inline PDF) | Serves the instructor's technical resume PDF. |
| `GET` | `/health` | JSON (`{"status": "healthy", ...}`) | Cloud uptime and health probe endpoint. |

### 5.2 Admin Portal Routes (`app/apps/courses/admin_router.py`)
| Method | Path | Auth Guard | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/admin` | No | 303 Redirect to `/admin/dashboard`. |
| `GET` | `/admin/login` | No | Secret instructor sign-in view. |
| `POST` | `/admin/login` | No | Authenticates credentials and sets signed session cookie. |
| `GET` | `/admin/signup` | No | **Disabled**: returns 303 redirect to `/admin/login`. |
| `POST` | `/admin/signup` | No | **Disabled**: returns 303 redirect to `/admin/login`. |
| `GET` | `/admin/dashboard` | **`require_admin`** | Protected dashboard with KPI cards and paginated leads table. |
| `POST` | `/admin/leads/{id}/status`| **`require_admin`** | Updates lead status & counseling notes; preserves active page. |
| `GET` | `/admin/logout` | No | Clears `admin_session` cookie and redirects to `/admin/login`. |

### 5.3 Course Admissions API (`app/apps/courses/router.py`)
| Method | Path | Auth Guard | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/courses/instructor` | Public | Instructor profile, tools, credentials, and highlights. |
| `GET` | `/api/courses/batches` | Public | Returns active cohorts with available seat metrics. |
| `GET` | `/api/courses/batches/{id}` | Public | Detailed information for a single batch. |
| `POST` | `/api/courses/enquiry` | Public | Submits a general inquiry or callback request (mandatory consent). |
| `POST` | `/api/courses/register` | Public | Enrolls a student in a cohort. Email is optional (mandatory consent). |
| `GET` | `/api/courses/leads` | **`require_admin`** | Filtered lead records (returns 401 for anonymous access). |
| `GET` | `/api/courses/leads/summary`| **`require_admin`** | KPI metrics (`total_leads`, `registrations`, `enquiries`, `do_not_contact`). |
| `GET` | `/api/courses/leads/export.csv`| **`require_admin`** | Downloads student lead database with consent timestamps as clean CSV. |
| `GET` | `/api/courses/leads/{id}` | **`require_admin`** | Single lead detail lookup. |
| `PATCH`| `/api/courses/leads/{id}/status`| **`require_admin`** | Updates pipeline status (`contacted`, `enrolled`, `closed`, `do_not_contact`). |
| `POST` | `/api/courses/batches` | **`require_admin`** | Creates new cohort batch. |

### 5.4 Knowledge Engine & Library API (`app/apps/library/router.py`)
| Method | Path | Response Type | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/library` | HTML (`library/index.html`) | 34-Technology directory and category filter tabs. |
| `GET` | `/library/datasets` | HTML (`library/datasets.html`) | Practice datasets vault listing clean datasets for SQL & BI. |
| `GET` | `/library/datasets/{slug}` | HTML (`library/dataset_detail.html`) | Dataset inspection, data dictionary schema, and sample preview. |
| `GET` | `/library/datasets/{slug}/download` | File (CSV) | **Protected Gate**: Download full RFC 4180 CSV (requires student login). |
| `GET` | `/library/{subject}` | HTML (`library/subject_hub.html`) | W3Schools-style hub with 4-tab panels & topic sidebar. |
| `GET` | `/library/{subject}/notes/{slug}`| HTML (`library/reader.html`) | 3-Column docs reader with TOC and Prism.js styling. |
| `GET` | `/api/library/subjects` | JSON | List of all 34 supported subjects with topic counts. |
| `GET` | `/api/library/{subject}/documents`| JSON | List of all markdown articles indexed for a subject. |

### 5.5 Student Portal & Authentication API (`app/apps/courses/student_router.py`)
| Method | Path | Auth Guard | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/student/login` | No | Student sign-in page. Redirects to `/student/dashboard` if already authenticated. |
| `POST` | `/student/login` | No | Authenticates student via phone or email + password; sets 30-day `student_session` cookie. |
| `GET` | `/student/register` | No | Student registration form (Phone/WhatsApp mandatory, email strictly optional). |
| `POST` | `/student/register` | No | Creates student record, links prior guest activities, sets session cookie. |
| `GET` | `/student/logout` | No | Clears `student_session` cookie and redirects to `/`. |
| `GET` | `/student/dashboard` | **`require_student`** | Personal student portal showing verified status, unlocked datasets, and activity history. |
| `POST` | `/api/student/register` | No | JSON API: Registers student and returns safe `StudentOut` profile + session token. |
| `POST` | `/api/student/login` | No | JSON API: Authenticates student and returns `StudentOut` profile + session token. |
| `GET` | `/api/student/me` | **`require_student`** | JSON API: Returns current authenticated student profile. |
| `POST` | `/api/activity/log` | No | JSON API: Records client interactions (`note_read`, `page_view`, etc.) for guests or students. |

---

## 6. Database Structure & Dual-Engine Strategy

For the exhaustive database specification, see [`docs/database.md`](file:///f:/Projects/coding/docs/database.md).

### Dual-Engine Strategy
- **Local Development**: Connects to `sqlite:///./course_platform.db` with `check_same_thread=False`.
- **Cloud Production (Render.io)**: Connects to PostgreSQL via `DATABASE_URL` with:
  - Protocol rewrite: `postgres://` &rarr; `postgresql://`
  - `pool_pre_ping=True` (verifies socket health before checkout)
  - `pool_recycle=300` (recycles idle sockets every 5 minutes)
  - `pool_size=5`, `max_overflow=10`

### Tables Summary
1. `batches`: Scheduled live cohorts (`batch_code`, `course_name`, `schedule_days`, `schedule_time`, `max_seats`, `is_active`).
2. `student_leads`: Prospective student records (`full_name`, `email` [optional], `phone` [mandatory], `current_status`, `prior_experience`, `status`, `admin_notes`, foreign key to `batches.id`).
3. `admin_users`: Administrative accounts (`username`, `email`, `hashed_password` [bcrypt 12 rounds], `is_active`).
4. `users`: Registered student & professional platform accounts (`full_name`, `phone` [unique/mandatory], `email` [optional], `hashed_password` [bcrypt 12 rounds], `user_type`, `college_or_company`, `is_active`).
5. `user_activity_logs`: High-resolution engagement logs (`user_id`, `session_id`, `event_type`, `resource_type`, `resource_slug`, `referrer`, `ip_address`).
6. `project_todos`: Internal task tracker items stored inside `portfolio.db`.

---

## 7. Environment Variables Reference

Auto-loaded via `python-dotenv` from `.env` in [`app/core/config.py`](file:///f:/Projects/coding/app/core/config.py):

| Variable Name | Required | Default Fallback | Purpose & Guidelines |
| :--- | :--- | :--- | :--- |
| `ADMIN_PASSWORD` | Recommended | Loaded from `.env` | Master instructor password for `admin` account (`admin@mythostech.in`). |
| `AGENT_PASSWORD` | Recommended | Loaded from `.env` | Isolated password for automated test runs (`agent@mythostech.in`). |
| `SECRET_KEY` | Mandatory in Prod | Dev fallback only | Cryptographic 256-bit secret for signing cookies; app refuses to start in production if absent or default. Generate via: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `ENVIRONMENT` | Yes | `development` | Toggles between `LocalSettings` and `DeploymentSettings`. |
| `PORT` | Auto | `8000` (dev) / `10000` (cloud)| Injected by cloud host; bound dynamically by Uvicorn. |
| `DATABASE_URL` | Cloud Prod | `""` (falls back to SQLite)| External PostgreSQL connection URI (Neon / Supabase / Render Postgres). |
| `PYTHON_VERSION`| Cloud Prod | `3.10.11` | Runtime version specified for Render build environments. |

---

## 8. Local Development Instructions

### 8.1 Setup & Dependency Installation
```powershell
# 1. Open terminal in workspace root (f:\Projects\coding)
# 2. Activate virtual environment (if using one) or ensure Python 3.10+ is active:
python --version

# 3. Install production and development dependencies:
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 8.2 Run Local Server
```powershell
uvicorn app.main:app --reload --port 8000
```
- Web Application: [http://localhost:8000](http://localhost:8000)
- Weekend Batch Registration: [http://localhost:8000/register](http://localhost:8000/register)
- Secret Admin Sign-in: [http://localhost:8000/admin/login](http://localhost:8000/admin/login)
- Interactive API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Resource Library: [http://localhost:8000/library](http://localhost:8000/library)

### 8.3 Run Automated Test Suite
```powershell
python -m pytest -v
```
**Verification Requirement**: All **32 automated tests** must pass with zero failures.

---

## 9. Non-Negotiable Business & Architectural Constraints

1. **Cohort Admissions & Zero-Upfront Pricing Rule**:
   - **No tuition fees, prices, discounts, or payment gateways appear on the public website for cohorts**.
   - Browse surfaces (subject hubs, reader sidebars, catalog cards) never display prices.
   - Live cohort admissions counseling and seat allocations are handled privately during orientation.
2. **Optional Student Email**:
   - Student email is **strictly optional** across all student-facing enrollment forms (`/register`, modal popups).
   - Only **Full Name** and **WhatsApp/Phone Number** are mandatory.
3. **Strictly Zero Code Execution on Platform**:
   - The platform never provides options for students to execute code online. All code snippets are static, copy-only Prism.js styled blocks with copy buttons.
4. **Strict Push Authority — Platform Owner ONLY**:
   - **Only the human platform owner ("I") can execute `git push` or deploy to production.**
   - AI agents maintain local git hygiene (test, stage, commit locally) and must never push to remote.
5. **Decoupled Heavy Asset Vault (`external_assets/`)**:
   - High-resolution imagery, large datasets (`.csv`, `.sqlite`), and downloadable bundles are isolated in `external_assets/` and served via CDN/GitHub Raw to keep the Render container lightweight.
