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

### Faculty Mentorship Model & Brand Credibility
- **Dual Specialized Mentors**: Strict separation of disciplines. The Data Analytics mentor is anonymous (*Mythos Data Analytics Mentor*, lead faculty, high-tech emblem, no photo), while the Digital Marketing mentor is featured with real credentials (`[DM_MENTOR_NAME]`, `[DM_MENTOR_PHOTO]`, `[DM_MENTOR_BIO]`, `[DM_MENTOR_LINKEDIN]`).
- **Standardized Trust Metric**: Grounded in `[TRUST_CLAIM]` (*"400+ learners taught by our mentors over 3+ years"*). The legacy "550+" metric is systematically expunged across all surfaces.
- **Dynamic Contact Information**: Support and admissions contacts load dynamically via `BUSINESS_EMAIL` and `BUSINESS_WHATSAPP`. Legacy personal contacts are completely expunged.
- **Dormant Testimonials Component**: `sections/testimonials.html` renders nothing (100% dormant) unless authentic student reviews are supplied in context. Zero fake quotes or corporate logos.
- **Compliance & Guarantee Standard**: Strictly zero placement guarantees or fabricated salary claims. All student outcomes are framed around verifiable proof of work and interview readiness.

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
├── GUIDE.md                            # Definitive single-source-of-truth system manual & AI Accelerator
├── AGENTS.md                           # 16 persistent golden rules, incremental slicing & operational directives
├── agent.md                            # Standard alias mirroring AGENTS.md (resolves naming ambiguity)
├── Changeslog.md                       # Latest 15 development history entries (active rolling log)
├── task_new.md                         # Quick pointer referencing active master roadmap in docs/task_new.md
├── CHANGELOG_ARCHIVE.md                # Quick pointer referencing historical archive in docs/
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
│       ├── sections/                   # 11 modular landing page section partials (includes dormant testimonials.html)
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
└── tests/                              # Automated test suite (77 tests passing cleanly)
    ├── test_courses.py                 # Admissions, registrations, auth, CSV export, PDF, funnels, security (27 tests)
    ├── test_library.py                 # W3Schools panels, sequential nav, reader, catalog (17 tests)
    ├── test_student_auth.py            # Student auth, session cookies, activity logging, datasets (14 tests)
    └── test_main.py                    # Health, SEO, sitemap, robots, Open Graph, schema, quality gate, analytics (19 tests)
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
| `GET` | `/about` | HTML (`about.html`) | Institute history, dual-mentor separation, and academic standards. |
| `GET` | `/demo` | HTML (`demo.html`) | Free 60-minute live weekend demo class reservation page. |
| `GET` | `/sitemap.xml` | XML (`application/xml`) | Dynamic sitemap listing active pages, hubs, datasets, and published notes. |
| `GET` | `/robots.txt` | PlainText (`text/plain`) | Crawl directives disallowing `/admin/`, `/api/`, `/student/`, pointing to sitemap. |
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
| `GET` | `/admin/dashboard` | **`require_admin`** | Protected dashboard with 6 KPI cards, multi-filter toolbar (Lead Type, Status, Traffic Source, Subject), and paginated leads table. |
| `POST` | `/admin/leads/{id}/status`| **`require_admin`** | Updates lead pipeline status (`new`, `contacted`, `demo_attended`, `enrolled`, `closed`, `do_not_contact`), follow-up date, and counselor notes. |
| `GET` | `/admin/logout` | No | Clears `admin_session` cookie and redirects to `/admin/login`. |

### 5.3 Course Admissions API (`app/apps/courses/router.py`)
| Method | Path | Auth Guard | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/courses/instructor` | Public | Instructor profile, tools, credentials, and highlights. |
| `GET` | `/api/courses/batches` | Public | Returns active cohorts with available seat metrics. |
| `GET` | `/api/courses/batches/grouped` | Public | Cohorts grouped by Track (`data_analytics`, `digital_marketing`) and lifecycle. |
| `GET` | `/api/courses/batches/{id}` | Public | Detailed information for a single batch. |
| `POST` | `/api/courses/enquiry` | Public | Submits general inquiry or callback request (mandatory consent, honeypot & rate limited). |
| `POST` | `/api/courses/register` | Public | Enrolls a student in a cohort. Email is optional (mandatory consent, honeypot & rate limited). |
| `POST` | `/api/courses/demo` | Public | Reserves seat for upcoming live demo class (`[DEMO_CLASS_DATETIME]`, honeypot & rate limited). |
| `POST` | `/api/courses/lead-magnet` | Public | Requests free cheat sheet or clean dataset with instant download reveal (honeypot & rate limited). |
| `POST` | `/api/courses/waitlist` | Public | Adds student to priority waitlist for upcoming subject or next batch (honeypot & rate limited). |
| `GET` | `/api/courses/leads` | **`require_admin`** | Filtered lead records by type, status, traffic source, subject interest (returns 401 for anonymous). |
| `GET` | `/api/courses/leads/summary`| **`require_admin`** | KPI metrics (`total_leads`, `batch_registrations`, `enquiries`, `demo_classes`, `lead_magnets`, `new`, `contacted`, `demo_attended`, `enrolled`, `do_not_contact`). |
| `GET` | `/api/courses/leads/export.csv`| **`require_admin`** | Downloads lead database with UTM attribution, subject interest, follow-up date, and consent timestamps as clean CSV. |
| `GET` | `/api/courses/leads/{id}` | **`require_admin`** | Single lead detail lookup. |
| `PATCH`| `/api/courses/leads/{id}/status`| **`require_admin`** | Updates pipeline status (`contacted`, `demo_attended`, `enrolled`, `closed`, `do_not_contact`) and follow-up date. |
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
1. `batches`: Scheduled live cohorts (`batch_code`, `title`, `course_name`, `track` ['data_analytics', 'digital_marketing'], `technologies`, `schedule_days`, `schedule_time`, `max_seats`, `status` ['enrolling', 'running', 'next', 'past'], `is_active`).
2. `student_leads`: Prospective student records across funnels (`lead_type` ['demo_class', 'waitlist', 'lead_magnet', 'enquiry', 'batch_registration'], `full_name`, `email` [optional], `phone` [mandatory], `subject_interest`, `source_utm`, `referrer_url`, `preferred_schedule`, `message`, `status` ['new', 'contacted', 'demo_attended', 'enrolled', 'closed', 'do_not_contact'], `admin_notes`, `follow_up_date`, `consent_given`, `consent_at`, foreign key to `batches.id`).
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
| `BASE_URL` | No | `https://mythostech.in` | Canonical base domain used for sitemap.xml, canonical URLs, and schema metadata. |
| `GOOGLE_SITE_VERIFICATION` | Optional | `""` | Google Search Console site verification HTML tag content. |
| `ANALYTICS_SCRIPT` | Optional | `""` | Privacy-friendly tracking snippet injection (Plausible, Umami, Cloudflare Web Analytics). |
| `GA4_MEASUREMENT_ID` | Optional | `""` | Google Analytics 4 measurement ID (e.g., `G-XXXXXXXXXX`) with automated `gtag` setup. |
| `BUSINESS_EMAIL` | Recommended | `admissions@mythostech.in` | Official institute contact email rendered across templates and PDF brochures. |
| `BUSINESS_WHATSAPP` | Recommended | `[BUSINESS_WHATSAPP]` | Official institute WhatsApp/phone contact number; purged of legacy personal numbers. |
| `DM_MENTOR_NAME` | Optional | `[DM_MENTOR_NAME]` | Full name for the Digital Marketing Mentor. |
| `DM_MENTOR_PHOTO` | Optional | `[DM_MENTOR_PHOTO]` | Professional photo path or URL for the Digital Marketing Mentor. |
| `DM_MENTOR_BIO` | Optional | `[DM_MENTOR_BIO]` | Professional track record and background for the Digital Marketing Mentor. |
| `DM_MENTOR_LINKEDIN`| Optional | `[DM_MENTOR_LINKEDIN]` | Verified LinkedIn profile URL for the Digital Marketing Mentor. |
| `DM_SCHEDULE` | Optional | `[DM_SCHEDULE]` | Live cohort schedule for Digital Marketing batches. |
| `TRUST_CLAIM` | Optional | `400+ learners taught by our mentors over 3+ years` | Standardized institutional credibility statement replacing legacy 550+ metrics. |
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
**Verification Requirement**: All **77 automated tests** must pass with zero failures.

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

---

## 10. AI Agent Accelerator & Rapid Discovery Index

> [!TIP]
> **Use this index on every task to bypass redundant file searches, directory scans, and route guessing.**

### 10.1 Master Document Locator
| Purpose | Primary Workspace Path | Secondary / Alias Path | Notes |
| :--- | :--- | :--- | :--- |
| **Master Task Roadmap** | [`docs/task_new.md`](file:///f:/Projects/coding/docs/task_new.md) | [`task_new.md`](file:///f:/Projects/coding/task_new.md) (root pointer) | Active Phases 0–6 task checklist & owner directives. |
| **AI Operational Rules** | [`AGENTS.md`](file:///f:/Projects/coding/AGENTS.md) | [`agent.md`](file:///f:/Projects/coding/agent.md) (root alias) | 16 golden rules, incremental slicing protocol & push restrictions. Auto-loaded by Antigravity. |
| **System Technical Guide** | [`GUIDE.md`](file:///f:/Projects/coding/GUIDE.md) | — | Definitive single-source-of-truth manual (current file). |
| **Recent Changelog** | [`Changeslog.md`](file:///f:/Projects/coding/Changeslog.md) | — | Strictly latest 15 development entries (rolling log). |
| **Changelog Archive** | [`docs/CHANGELOG_ARCHIVE.md`](file:///f:/Projects/coding/docs/CHANGELOG_ARCHIVE.md) | [`CHANGELOG_ARCHIVE.md`](file:///f:/Projects/coding/CHANGELOG_ARCHIVE.md) (root pointer) | Permanent historical archive (Entry 4 and older). |
| **Deep-Dive Architecture** | [`docs/architecture.md`](file:///f:/Projects/coding/docs/architecture.md) | — | Detailed sub-app modular layout & request lifecycle. |
| **Database Blueprint** | [`docs/database.md`](file:///f:/Projects/coding/docs/database.md) | — | Schemas, connection pools, and dual-engine strategy. |
| **Deployment Blueprint** | [`docs/deployment.md`](file:///f:/Projects/coding/docs/deployment.md) | — | Cloud hosting, Render build commands, and health pingers. |
| **User Operations Manual** | [`docs/USER_GUIDE.md`](file:///f:/Projects/coding/docs/USER_GUIDE.md) | — | Human owner's operations & leads management manual. |
| **Legacy Archives** | `docs/archive/` | — | Archived monolithic guides, original brief, and older changelogs. |

---

### 10.2 Template & Route Registry
Never guess route names or template locations:

| Template Path | HTTP Route | Handler File & Function | Jinja Context Variables Passed |
| :--- | :--- | :--- | :--- |
| `app/templates/index.html` | `GET /` | `app/main.py:read_root()` | `settings`, `batches`, `course_profile`, `testimonials` |
| `app/templates/about.html` | `GET /about` | `app/main.py:about_page()` | `settings`, `course_profile` |
| `app/templates/demo.html` | `GET /demo` | `app/main.py:demo_class_page()`| `settings`, `course_profile` |
| `app/templates/register.html` | `GET /register` | `app/main.py:register_page()` | `settings`, `batches` |
| `app/templates/confirmation.html` | `GET /registration-success` | `app/main.py:registration_success_page()` | `settings`, `title`, `course_profile` *(Note: route is `/registration-success`, NOT `/confirmation`)* |
| `app/templates/legal/privacy.html` | `GET /privacy` | `app/main.py:privacy_policy_page()` | `settings` |
| `app/templates/legal/terms.html` | `GET /terms` | `app/main.py:terms_page()` | `settings` |
| `app/templates/legal/refund_policy.html` | `GET /refund-policy` | `app/main.py:refund_policy_page()` | `settings` |
| `app/templates/library/index.html` | `GET /library` | `app/apps/library/router.py:library_home()` | `settings`, `subjects`, `summary`, `verticals` |
| `app/templates/library/subject_hub.html` | `GET /library/{subject}` | `app/apps/library/router.py:subject_hub()` | `settings`, `subject`, `documents`, `adjacent` |
| `app/templates/library/reader.html` | `GET /library/{subject}/notes/{slug}` | `app/apps/library/router.py:reader()` | `settings`, `subject`, `meta`, `html_content`, `toc` |
| `app/templates/library/datasets.html` | `GET /library/datasets` | `app/apps/library/router.py:practice_datasets()` | `settings`, `datasets`, `current_user` |
| `app/templates/library/dataset_detail.html` | `GET /library/datasets/{slug}`| `app/apps/library/router.py:practice_dataset_detail()` | `settings`, `dataset`, `current_user` |
| `app/templates/admin/login.html` | `GET /admin/login` | `app/apps/courses/admin_router.py:admin_login_page()` | `settings`, `error` |
| `app/templates/admin/dashboard.html` | `GET /admin/dashboard` | `app/apps/courses/admin_router.py:admin_dashboard()` | `settings`, `leads`, `summary`, `batches`, `current_admin` |
| `app/templates/admin/batches.html` | `GET /admin/batches` | `app/apps/courses/admin_router.py:admin_batches_page()` | `settings`, `admin`, `batches`, `summary` |
| `app/templates/student/login.html` | `GET /student/login` | `app/apps/courses/student_router.py:student_login_page()` | `settings`, `error`, `next` |
| `app/templates/student/register.html` | `GET /student/register` | `app/apps/courses/student_router.py:student_register_page()` | `settings`, `error`, `next` |
| `app/templates/student/dashboard.html` | `GET /student/dashboard` | `app/apps/courses/student_router.py:student_dashboard()` | `settings`, `current_user`, `activity_logs`, `datasets` |

#### Homepage (`index.html`) Section Partials (Render Order):
1. `partials/in_page_nav.html`: Sticky left in-page navigator rail
2. `sections/hero.html`: Hero banner, 3D animated terminal, trust pill
3. `sections/engine.html`: Problem vs Solution & 4-step institute model
4. `sections/programs.html`: Dual cohort tracks (Data Analytics & Digital Marketing)
5. `sections/methodology.html`: 5-part engineering pedagogy
6. `sections/projects.html`: Real-world enterprise capstones
7. `sections/admission.html`: Step-by-step admissions counseling path
8. `sections/career.html`: 4-pillar interview readiness & proof of work
9. `sections/syllabus.html`: Paired interactive 6-module curriculum accordion
10. `sections/testimonials.html`: **Dormant partial** (renders 0 bytes unless authentic reviews are provided)
11. `sections/mentor.html`: Dual-mentor showcase (anonymous DA mentor + verified DM mentor) & admissions contact desk
12. `sections/modals.html`: Quick-apply enrollment & enquiry modal dialogs

---

### 10.3 Canonical Institutional Constants & Placeholders
Always use these exact attributes and tokens; **never hardcode strings**:

| Token / Attribute | Source / Config Property | Default Fallback Value | Usage Context |
| :--- | :--- | :--- | :--- |
| `BUSINESS_EMAIL` | `settings.BUSINESS_EMAIL` | `admissions@mythostech.in` | All public email links (`mailto:{{ settings.BUSINESS_EMAIL }}`) |
| `BUSINESS_WHATSAPP` | `settings.BUSINESS_WHATSAPP` | `[BUSINESS_WHATSAPP]` | Formatted WhatsApp display number |
| WhatsApp URL | `settings.whatsapp_url` | `https://wa.me/{digits}` or `#about` | Direct click-to-chat links |
| `TRUST_CLAIM` | `settings.TRUST_CLAIM` | `400+ learners taught by our mentors over 3+ years` | Credibility metric (*NEVER use 550+*) |
| `DM_MENTOR_NAME` | `settings.DM_MENTOR_NAME` | `[DM_MENTOR_NAME]` | Digital Marketing Mentor Name |
| `DM_MENTOR_PHOTO` | `settings.DM_MENTOR_PHOTO` | `[DM_MENTOR_PHOTO]` | DM Mentor image path/URL |
| `DM_MENTOR_BIO` | `settings.DM_MENTOR_BIO` | `[DM_MENTOR_BIO]` | DM Mentor background |
| `DM_MENTOR_LINKEDIN` | `settings.DM_MENTOR_LINKEDIN` | `[DM_MENTOR_LINKEDIN]` | DM Mentor LinkedIn profile URL |
| `DM_SCHEDULE` | `settings.DM_SCHEDULE` | `[DM_SCHEDULE]` | DM cohort days & timing |
| DA Mentor Profile | Code / Template constant | *Mythos Data Analytics Mentor* | Anonymous DA Mentor (no photo, terminal emblem, 3+ yrs, 400+ taught, Sat & Sun 6–8 PM) |
| `[SUBJECT_ORDER]` | `settings.SUBJECT_ORDER` | `SQL, Excel, Power BI, Python, Tableau, Git & GitHub` | Data Analytics curriculum sequence & roadmap strip |
| `DEMO_CLASS_DATETIME`| Token | `[DEMO_CLASS_DATETIME]` | Free demo session schedule |

> [!WARNING]
> **Strictly Prohibited Legacy Strings**:
> - Never use `"550+"` or `"550+ Students"` (replaced by `settings.TRUST_CLAIM`).
> - Never use `"shubhamsinghh057@gmail.com"` (replaced by `settings.BUSINESS_EMAIL`).
> - Never use `"8727864157"` (replaced by `settings.BUSINESS_WHATSAPP`).
> - Never use `"100% placement"`, `"placement guarantee"`, or specific salary packages.

---

### 10.4 Subsystem Test Suite Map & Fast Verification Commands

Instead of running all 70 tests during rapid iterations, run targeted sub-suites:

```powershell
# 1. Frontend & Core Routing (SEO, sitemap, meta, mentors, contact, quality gate, 550+ purge)
python -m pytest tests/test_main.py -v

# 2. Admissions, Cohorts, Leads, Auth & Admin Security
python -m pytest tests/test_courses.py -v

# 3. Knowledge Engine, 34-Tech Catalog, W3Schools Tracks & Parsing
python -m pytest tests/test_library.py -v

# 4. Student Authentication, Sessions, Datasets Vault & Activity Logs
python -m pytest tests/test_student_auth.py -v

# 5. Full Final Verification Suite (Mandatory before committing)
python -m pytest -v
```

---

### 10.5 Phase Development Protocol (Rapid Checklist)
Follow this exact 8-step sequence for every upcoming phase:

```text
1. INGEST    ──> Read current phase in docs/task_new.md.
2. LOCATE    ──> Lookup affected routes & templates in Section 10.2 above.
3. BASELINE  ──> Run: git status && python -m pytest tests/test_<module>.py -v
4. IMPLEMENT ──> Write clean code adhering to Section 10.3 placeholders.
5. PDF CHECK ──> If syllabus/contact changed, run: python -m app.apps.courses.generate_syllabus_pdf
6. TEST      ──> Run: python -m pytest -v (must pass with 0 failures).
7. CHANGELOG ──> Add [Entry N] to Changeslog.md. If 16 entries exist, move oldest to CHANGELOG_ARCHIVE.md.
8. COMMIT    ──> Update docs/task_new.md & GUIDE.md. Stage files and run:
                 git commit -m "feat(scope): concise description" (NEVER RUN git push).
```

