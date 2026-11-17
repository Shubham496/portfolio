# Application Architecture Specification

## 1. Architectural Philosophy & Overview

**MYTHOS Online Institute** is engineered as a high-performance, low-footprint web application utilizing **FastAPI** on **Python 3.10+** running on the **Uvicorn** ASGI server. 

### Core Architectural Principles
1. **Low Memory Footprint**: Baseline runtime memory is held strictly between **40–60 MB RAM**, ensuring robust performance on constrained cloud tiers (such as Render.io free containers) without OOM restarts.
2. **Modular Sub-App Architecture**: Functionality is divided into decoupled application domains under `app/apps/`, each containing isolated models, schemas, routers, and business services.
3. **Component-Based Server-Side Rendering (SSR)**: Dynamic page generation is powered by Jinja2 templates decomposed into discrete section partials, achieving rapid initial page loads (<100ms) with zero client-side hydration overhead.
4. **Decoupled Heavy Asset Vault**: All large binary assets (datasets, high-resolution imagery, downloadable PDF bundles) are segregated into an external asset vault (`external_assets/`) served via CDN, keeping the deployment slug lightweight (<50 MB).

```
                      ┌────────────────────────────────────────┐
                      │            Incoming Request            │
                      └───────────────────┬────────────────────┘
                                          │
                                          ▼
                      ┌────────────────────────────────────────┐
                      │          FastAPI ASGI Server           │
                      │          (Uvicorn on $PORT)            │
                      └───────────────────┬────────────────────┘
                                          │
             ┌────────────────────────────┼────────────────────────────┐
             ▼                            ▼                            ▼
  ┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
  │ app/apps/courses    │      │ app/apps/library    │      │ app/apps/todos      │
  │ • Admissions & Leads│      │ • Knowledge Engine  │      │ • Internal Kanban   │
  │ • Admin Portal & Auth      │ • 34-Tech Catalog   │      │ • SQLite Task Store │
  │ • PDF Generation    │      │ • W3Schools Panels  │      └─────────────────────┘
  └──────────┬──────────┘      │ • Sequential Nav    │
             │                 │ • LRU/TTL Cache     │
             │                 └──────────┬──────────┘
             ▼                            ▼
  ┌─────────────────────┐      ┌─────────────────────┐
  │ Dual-Engine DB      │      │ On-Disk Markdown    │
  │ SQLite (Local) /    │      │ + PyMdown Parsing   │
  │ PostgreSQL (Cloud)  │      │ (app/content/)      │
  └─────────────────────┘      └─────────────────────┘
```

---

## 2. Directory Structure & Domain Boundary Mapping

```text
app/
├── main.py                     # Root FastAPI application, lifecycle, middleware, route mounting
├── content/                    # Canonical Markdown knowledge repository
│   └── sql/                    # SQL curriculum notes, blueprints, and viva banks
├── core/                       # Shared application configuration & environment abstraction
│   ├── base_config.py          # Pydantic BaseSettings (app metadata, contact, social links)
│   ├── config.py               # Settings dispatcher (toggles between LocalSettings & DeploymentSettings)
│   ├── local.py                # Local debug settings (SQLite default, relaxed debugging)
│   └── deployment.py           # Production settings (Cloud DB, $PORT binding, security flags)
├── apps/                       # Modular business domains
│   ├── courses/                # Core Admissions, Batch Management & Instructor Dashboard
│   ├── library/                # Knowledge Engine, W3Schools-Style Study Tracks & Documentation Reader
│   └── todos/                  # Supporting micro-app for internal task tracking
├── static/                     # Public web assets (compiled CSS, JavaScript, PDF brochures, icons)
└── templates/                  # Jinja2 template hierarchies & component partials
```

---

## 3. Modular Sub-Applications

### 3.1 Course & Admissions Engine (`app/apps/courses/`)
- **Domain Responsibilities**:
  - Processing student applications (`/register`) and general inquiries.
  - Cohort management (`batches` table) and seat tracking.
  - Secret administrative portal (`/admin/login`, `/admin/dashboard`).
  - Session security, bcrypt password hashing, and cookie signing.
  - Asynchronous generation of print-ready PDF syllabi using `fpdf2`.
  - Student lead pipeline filtering, search, pagination, and CSV data export.
- **Key Modules**:
  - `database.py`: Dual-engine database connection handling (SQLite local, PostgreSQL cloud).
  - `models.py`: SQLAlchemy entities (`Batch`, `StudentLead`, `AdminUser`).
  - `schemas.py`: Pydantic v2 schemas for payload validation and sanitization.
  - `services.py`: Database initialization, pagination math, CSV generation, and profile retrieval.
  - `auth.py`: Cryptographic signature validation via `itsdangerous.URLSafeTimedSerializer` and bcrypt verification.
  - `router.py`: Public JSON APIs and form submission endpoints (`/api/courses/*`).
  - `admin_router.py`: Protected administrative routes (`/admin/*`) guarded by `require_admin`.
  - `generate_syllabus_pdf.py`: Standalone publication-grade 2-page syllabus PDF builder.

### 3.2 Knowledge Engine & Library (`app/apps/library/`)
- **Domain Responsibilities**:
  - Dynamic discovery and rendering of Markdown study guides from `app/content/`.
  - Indexing 34 major programming languages, database systems, data science tools, and cloud platforms.
  - Organizing content into 5 verticals: Notes, Practice & Viva Banks, Datasets, Books, and Capstones.
  - Rendering W3Schools-style 4-panel interfaces (All Topics, Notes, Interview Questions, Video Lectures).
  - Managing sequential curriculum progression with `< Previous Topic` and `Next Topic >` traversal.
  - Generating dynamic Table of Contents (TOC) with active scroll-spy IDs.
- **Key Modules**:
  - `services.py`: Frontmatter parsing, PyMdown markdown rendering, reading-time estimation, in-memory LRU/TTL caching, topic curricula definitions, and sequential navigation resolution.
  - `router.py`: Web routes (`/library`, `/library/{subject}`, `/library/{subject}/notes/{slug}`) and JSON data APIs (`/api/library/*`).

### 3.3 Task Tracker Micro-App (`app/apps/todos/`)
- **Domain Responsibilities**:
  - Internal sprint task tracking Kanban interface (`/apps/todos`).
  - Isolated persistence via `portfolio.db` (SQLite).
- **Key Modules**:
  - `models.py`: Direct SQLite helper operations for the `project_todos` table.
  - `router.py`: HTML endpoint rendering `app/apps/todos/templates/todos.html`.

---

## 4. Frontend Architecture & Jinja2 Template Decomposition

To prevent monolithic template bloat and facilitate rapid updates, the presentation layer follows a strict decomposition hierarchy:

```text
app/templates/
├── base.html                   # HTML5 skeleton, meta tags, Google Fonts (Poppins), Lucide icons
├── index.html                  # Landing page orchestrator (15-line component composition)
├── register.html               # Dedicated full-page weekend cohort registration form
├── confirmation.html           # Post-registration acknowledgment screen
├── partials/                   # Global layout partials
│   ├── navbar.html             # Inter-page top navbar with hover dropdowns & mobile drawer
│   ├── in_page_nav.html        # Left-docked in-page section navigator rail with scroll-spy
│   └── footer.html             # Multi-column footer, contact details, social links, legal
├── sections/                   # Modular landing page section components
│   ├── hero.html               # Hero headline, trust metric badges, animated status card
│   ├── engine.html             # The Problem vs. Mythos Learning Engine 4-step pipeline
│   ├── programs.html           # 2 Core System Tracks (Backend & Data BI) + tool cards
│   ├── methodology.html        # "This is Not Passive Learning" manifesto
│   ├── projects.html           # 3 Enterprise capstone project cards
│   ├── admission.html          # Admissions counseling flow & selection criteria
│   ├── career.html             # 4-Pillar placement preparation system
│   ├── syllabus.html           # 6-Module expandable curriculum accordion with paired laptop expansion
│   ├── mentor.html             # Direct Admissions Desk & WhatsApp contact
│   └── modals.html             # Modal popups for instant cohort enrollment and inquiry
├── admin/                      # Instructor portal templates
│   ├── login.html              # Dark-mode styled sign-in form
│   └── dashboard.html          # Protected monitor with KPI cards, 7-column lead table, pagination bar
└── library/                    # Technical documentation engine templates
    ├── index.html              # 34-Technology directory with category filter pills
    ├── subject_hub.html        # W3Schools-style subject portal with 4-tab panel architecture
    └── reader.html             # 3-Column docs reader (sidebar tree, reading canvas, sticky TOC)
```

### Key Frontend Patterns:
1. **Paired Laptop Accordion**: In `sections/syllabus.html`, modules expand in pairs on desktop screens (`>= 768px`) for optimal visual balance, while expanding individually on mobile screens.
2. **Docked Left In-Page Navigation**: `partials/in_page_nav.html` provides a persistent, glassmorphic rail on the left side of complex pages, updating active pill highlights based on viewport scroll position.
3. **Pure Static Syntax Highlighting**: All code blocks utilize Prism.js styling with static copy buttons. Interactive consoles and client-side code execution engines are strictly prohibited.

---

## 5. Security & Authentication Flow

```
User visits /admin/login
        │
        ▼
Submits credentials (username, password)
        │
        ▼
Fetch AdminUser from database
        │
        ├─► Hash check fails ──► Re-render login with "Invalid credentials" error
        │
        ▼
Hash check succeeds (bcrypt.checkpw)
        │
        ▼
Generate signed session token using itsdangerous.URLSafeTimedSerializer
Token payload: {"user_id": admin.id, "username": admin.username}
        │
        ▼
Set HTTP-Only cookie: admin_session (Max-Age: 7 days, SameSite: Lax)
        │
        ▼
Redirect 303 to /admin/dashboard
        │
        ▼
Subsequent requests verified via require_admin FastAPI dependency
```

### Critical Security Constraints:
- Master instructor credentials (`ADMIN_PASSWORD`) are loaded strictly from `.env` and never hardcoded in templates or docs.
- Dedicated `agent_admin` profile (`AGENT_PASSWORD`) is isolated for automated testing and test-suite execution.
- Public admin registration is permanently disabled (`GET /admin/signup` and `POST /admin/signup` return HTTP 303 redirecting to `/admin/login`).

---

## 6. External Decoupled Assets Vault Architecture

To protect Render.io deployments from ephemeral slug limits (500 MB limit on free web services) and RAM bloat:

- **Secondary Repository**: Hosted at `https://github.com/Shubham496/mythos-assets`.
- **Local Clone**: Stored in `external_assets/` (strictly excluded from Git tracking via root `.gitignore`).
- **Delivery Strategy**:
  - Documentation Images: Delivered via global CDN:
    `https://cdn.jsdelivr.net/gh/Shubham496/mythos-assets@main/images/<category>/<filename>`
  - Student Project Datasets: Delivered directly via raw GitHub links:
    `https://github.com/Shubham496/mythos-assets/raw/main/datasets/<filename>`
- **Separation of Concerns**: The main application repository contains code, templates, and markdown text only. Large binary blobs remain isolated.
