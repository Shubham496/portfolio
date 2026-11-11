# Platform Changelog & Implementation History

All notable changes, updates, feature implementations, and bug fixes for the **Data Analysis Training & Student Admission Platform** are documented in this file.
This serves as an audit trail and system log (similar to GitHub releases/commit logs) for developers, agents, and maintainers to immediately check what is already built, configured, and verified.

---

## [Latest Updates] - 2026-11-12 (Frontend Architecture Modularization & Environment Template)

### Added & Refactored
- **Mandatory Git Maintenance Protocols in Agent Guide**:
  - Embedded Rule 6 in `docs/AGENT_GUIDE.md` mandating continuous repository cleanliness, commit verification, and zero-secret leaks.
  - Added Section 10 ("Mandatory Git Maintenance & Operational Protocols") detailing pre-commit verification, clean working tree management, strict exclusions, and upstream synchronization.
- **Header Navigation Streamlining**:
  - Removed "Data Systems" badge from next to the Mythos logo in the header.
  - Removed "Learning Engine" and "Admission" links from both desktop and mobile navigation menus for cleaner spacing and focused navigation flow.
- **Frontend Architecture Modularization (`app/templates/sections/`)**:
  - Decomposed monolithic `app/templates/index.html` (~1,300 lines) into 10 isolated, maintainable Jinja2 section partials:
    1. `sections/hero.html` (Hero headline, CTAs, trust metric bar, and floating photo card)
    2. `sections/engine.html` (Problem vs. Mythos Learning Engine 4-step pipeline)
    3. `sections/programs.html` (2 Core Tracks: Backend Engineering & BI Analytics, plus 5 tool badges)
    4. `sections/methodology.html` (How You Will Learn / "This is not passive learning")
    5. `sections/projects.html` (3 Production Capstones: Adidas, Data Warehouse, Event Analytics)
    6. `sections/admission.html` (Outcomes & 4-step admission process)
    7. `sections/career.html` (Job Readiness: GitHub, ATS Resume, LinkedIn, Mock Interviews)
    8. `sections/syllabus.html` (Expandable 6-module curriculum accordion & inline toggle JS)
    9. `sections/mentor.html` (Shubham Singh bio, experience timeline, WhatsApp link & bottom CTA banner)
    10. `sections/modals.html` (Enrollment modal, Enquiry modal, and toast notification)
  - Transformed `index.html` into a clean 15-line component orchestrator extending `base.html`.
  - Zero visual or UX changes — exact DOM hierarchy, Tailwind classes, scripts, and links preserved.
- **Environment Template (`.env.example`)**:
  - Created `.env.example` documenting all expected environment variables (`ADMIN_PASSWORD`, `AGENT_PASSWORD`, `SECRET_KEY`, `ENVIRONMENT`, `PORT`, `DATABASE_URL`) with safe dummy placeholders.
  - Verified `.env` remains completely git-ignored.
- **Verification & Integrity**:
  - All 15 automated pytest tests passing (100%).
  - Verified homepage status 200, WhatsApp link (`8727864157`), "Students Trained: 550+", and syllabus toggle functions.


---

## [Latest Updates] - 2026-11-12 (Security Hardening, Hero Card Redesign, WhatsApp Integration & Interactive Syllabus Fix)

### Added & Fixed
- **Hero Photo Card Refinement (Task 1)**:
  - Eliminated the clunky outer podium container and stage bar around the instructor photo.
  - Replaced with a borderless, floating portrait card (`rounded-3xl shadow-2xl`) featuring soft ambient gradient glow (`-inset-4 blur-2xl`) and overlapping status badges ("Students Trained: 550+", "Lead Mentor", "5 Core Pillars", "Sat & Sun 6–8 PM").
- **Security Hardening & Profile Isolation (Task 2)**:
  - Expunged the old plaintext admin password from all documentation (`docs/AGENT_GUIDE.md`, `docs/USER_GUIDE.md`, and history).
  - Generated a brand-new, high-entropy master password for Shubham's `admin` account and saved it securely in `.env`.
  - Created a dedicated, isolated admin profile: `agent_admin` (`agent@mythostech.in`) with its own password in `.env` (`AGENT_PASSWORD`) for automated testing and agent operations.
  - Updated `tests/test_courses.py` to authenticate with `agent_admin`, ensuring the instructor's personal account is never tested or exposed in test logs.
- **Interactive Syllabus Accordion Fix (Task 3)**:
  - Resolved browser caching issue by embedding the toggle logic directly inside `app/templates/index.html` and adding version cache-busting to `main.js?v=2.2`.
  - Enhanced `toggleSyllabus(index)` to explicitly control `display: block / none` and force immediate Lucide icon initialization (`lucide.createIcons()`) upon opening.
- **WhatsApp Integration & Phone Update (Task 4)**:
  - Updated phone number across all files and templates to `8727864157`.
  - Replaced phone icon with official WhatsApp SVG icon with direct `https://wa.me/918727864157` links in the profile section, footer, and confirmation page.
  - Updated brochure PDF footer to state `WhatsApp: +91 8727864157`.

---

### Added & Updated
- **Instructor Hero Showcase & Credibility Metric (Task 3)**:
  - Replaced the hero floating emblem with **Shubham Singh's instructor photo** in an illuminated podium stage with gradient glow borders.
  - Added floating verification badge: **"Students Trained: 550+"** with an active emerald pulsing indicator.
  - Added floating status pills: **"Shubham Singh · Lead Mentor"**, **"5 Core Pillars"**, and **"Sat & Sun · 6–8 PM"**.
  - Added 4-card trust metric strip directly beneath the hero:
    - 550+ Students Trained
    - 3+ Years Enterprise Consulting
    - Sat & Sun (6:00 – 8:00 PM IST)
    - 100% Live Hands-On Builds
  - Updated instructor profile section, register page, and PDF brochure to uniformly reflect **550+ Students Trained**.

- **Interactive Expandable Syllabus Architecture (Task 2)**:
  - Transformed the static curriculum map into an interactive deep-dive explorer with **"Show More Details"** and master **"Expand All / Collapse All"** controls.
  - In **Excel**: Explicitly detailed **Power Query Editor** (multi-file ingestion, unpivoting, custom M columns, automated refresh), **VBA & Macro Automation** (subroutines, loops, custom UDFs, one-click reports), **Advanced Formulas** (XLOOKUP, Dynamic Arrays, LET, LAMBDA), and **What-If Analysis** (Goal Seek, Scenarios).
  - In **SQL**: Deep-dive into analytical window functions (`LEAD`, `LAG`, `NTILE`, frame specs), nested/recursive CTEs, 3NF schema normalization, indexing, and `EXPLAIN ANALYZE`.
  - In **Python**: Vectorized NumPy arrays, Pandas wrangling masterclass, missing value imputation, regex extraction, and scheduled SQLAlchemy ETL ingestion.
  - In **Power BI**: Fact/Dimension star schemas, advanced DAX measures (`CALCULATE`, `FILTER`, `ALL`, virtual tables), time intelligence (`SAMEPERIODLASTYEAR`, YTD), custom tooltips, and drill-throughs.
  - In **Tableau**: Level of Detail (LOD) calculations (`FIXED`, `INCLUDE`, `EXCLUDE`), table calculations, parameter actions, multi-story dashboards, and Tableau Public deployment.

- **Career Acceleration & Job Readiness Ecosystem (Task 1)**:
  - Added a dedicated 4-pillar placement system to the homepage and curriculum:
    1. **GitHub Portfolio Architecture**: Clean commit hygiene, branch workflows, architecture schemas, and production READMEs.
    2. **ATS-Compliant Resume Engineering**: 1-on-1 resume overhaul converting projects into quantifiable impact metrics (Action + Tool + Metric).
    3. **LinkedIn Brand Optimization**: Inbound magnet profile headline, featured project media, public dashboard demos, and high-response outreach scripts.
    4. **1-on-1 Mock Technical Interviews**: Live timed SQL query solving on CoderPad/HackerRank, Python wrangling challenges, and dashboard defense.

- **UI Polish & Navigation Enhancements (Task 4)**:
  - Added "Career Prep" quick anchor in desktop and mobile navigation bars and footer.
  - Added GitHub link directly to instructor contact row in profile section.
  - Animated syllabus drawer expansion with smooth cubic-bezier transitions.
  - Regenerated `app/static/pdf/Data_Analysis_Syllabus.pdf` with the updated 6 modules and 550+ students credential.

---

### Added & Updated
- **Mythos Brand Theme Transformation (Based on Brand Manual & Landing Reference)**:
  - Transformed design system across all pages to **Mythos** ("BUILD SKILLS. BUILD SYSTEMS. BUILD THE FUTURE."):
    - **Typography**: Integrated Google Fonts **Poppins** (`wght@300;400;500;600;700;800;900`).
    - **Color Palette**: Primary Deep Navy (`#070B14`, `#0B1120`), Electric Blue (`#2563EB`), Royal Blue (`#1E3A8A`), Cyan (`#06B6D4`), and Mythos Accent Spectrum (Violet `#7C3AED`, Magenta `#EC4899`, Orange `#F97316`).
    - **Visual Assets**: Embedded official Mythos icon, transparent vector emblem, and 3D illuminated podium stage showcase.
    - **Logo & Wordmark**: Custom MYTHOS wordmark with split-colored blue and orange 'O' circle and tagline.
  - **Rebuilt Landing Page (`app/templates/index.html`)**:
    1. **Hero Section**: "Become Industry-Ready Through Structured Execution" with vibrant gradient typography, CTA buttons, and 3D illuminated emblem podium with floating feature badges.
    2. **The Problem vs. Our Solution**: "Why Most Students Fail in Tech" vs "The Mythos Learning Engine" with 4-stage pipeline (Foundation &rarr; Controlled Builds &rarr; Independent Execution &rarr; Industry Simulation).
    3. **Programs Designed for Real Capability**: Deep-dive tracks for Backend &amp; Data Engineering (Python + SQL) and Business Intelligence &amp; Analytics (Power BI + Excel + Tableau), with 5 tool cards.
    4. **How You Will Learn**: "This is Not Passive Learning" with weekend live coding, mandatory builds, and vibrant gradient slogan banner (`You will write code every session. No exceptions.`).
    5. **Real Projects**: Showcase of 3 production capstones (Adidas Retail Intelligence Dashboard, Automated Multi-Source Data Warehouse, Event Analytics &amp; Ticketing Hub).
    6. **Outcomes & Admission Process**: "Not certificates. Capability." and "Not everyone is accepted."
    7. **Full Syllabus & Instructor Profile**: 5-pillar curriculum breakdown and Shubham Singh consultant background.
    8. **Bottom CTA**: Wide gradient banner ("If You're Serious About Tech, This Is Your System.").
  - **Modernized Navigation & Footer**:
    - Navbar with Mythos icon, split 'O' wordmark, quick anchors, and direct "Apply Now" button.
    - 5-column footer with Mythos brand statement, social links, program links, schedule, and FastAPI Minimal Core badge.
  - **Aligned Cohort & Admin Views**:
    - Updated `/register`, `/registration-success`, `/admin/login`, and `/admin/dashboard` to inherit the Mythos visual system while preserving all schemas and functional constraints.
  - **Non-Negotiable Constraints Strictly Maintained**:
    - Course: Exactly Data Analysis (Python, SQL, Power BI, Excel, Tableau).
    - Schedule: Saturday &amp; Sunday ONLY, 6:00 PM – 8:00 PM IST.
    - Pricing: STRICTLY zero fees or prices anywhere on the public platform.
    - Student Email: Strictly optional (Name and Phone/WhatsApp mandatory).
    - Admin credentials: Intact with modern bcrypt hashing. All 15 automated test cases passing.

---

## [2026-11-11]

### Added
- **Admin Dashboard Pagination (`/admin/dashboard`)**:
  - Implemented `get_leads_paginated()` in `app/apps/courses/services.py` with SQLAlchemy `count()`, `offset()`, and `limit()`.
  - Added query parameters: `page` (default 1) and `per_page` (default 10, options for 10, 25, 50).
  - Added pagination toolbar in `app/templates/admin/dashboard.html` showing `"Showing X to Y of Z leads"`.
  - Added page number navigation with previous/next controls, preserving active filters (`lead_type`, `status`, `search`).
  - Added form redirect preservation: updating lead status or notes returns to the current active page and filter set.
- **Separated Status and Date Columns**:
  - Restructured the leads table into 7 distinct columns:
    1. **Type**: Visual badge for `Batch Registration` vs `Course Enquiry`.
    2. **Submitted Date**: Dedicated column displaying formatted calendar date (`created_date`, e.g. `Nov 11, 2026`) and submission timestamp (`created_time`, e.g. `10:45 PM`).
    3. **Student**: Full Name and career status (`College Student`, `Working Professional`, `Fresher`).
    4. **Contact**: WhatsApp direct message link and email address with fallback for optional email.
    5. **Message / Goals**: Prior experience badge and student inquiry message.
    6. **Status**: Dedicated column with status badge (`New`, `Contacted`, `Enrolled`, `Closed`) and quick inline status selector dropdown.
    7. **Admin Notes & Action**: Dedicated column with notes text input and inline save button using HTML5 `form` association.
- **Date Formatting Attributes in Model**:
  - Added `created_date` and `created_time` to `StudentLead.to_dict()` in `app/apps/courses/models.py`.
- **Environment Auto-Loading (`python-dotenv`)**:
  - Added `python-dotenv>=1.0.0` to `requirements.txt`.
  - Initialized `load_dotenv()` in `app/core/config.py` to ensure `os.environ` reliably receives `.env` values (`ADMIN_PASSWORD`, `SECRET_KEY`, `DATABASE_URL`) on server boot and in test harnesses.

### Fixed
- **Admin Password Reset & Test Mutation Bug**:
  - Identified root cause where `tests/test_courses.py` overwrote the admin password in `course_platform.db` with a dummy password whenever tests ran without `os.environ["ADMIN_PASSWORD"]`.
  - Updated `tests/test_courses.py` to use environment credentials without mutating existing admin records.
  - Updated `app/apps/courses/services.py:init_courses_db()` to only update password if explicitly provided in environment, preventing unintentional hash overwrites.
  - Recreated `admin` user account with username `admin`, email `admin@mythostech.in`, and verified password hash using modern bcrypt.

### Cleaned
- **Unused Scripts & Artifact Cleanup**:
  - Removed 17 obsolete standalone attendance analysis scripts and Excel files from project root:
    `analyze_attendance.py`, `check_att.py`, `check_col3.py`, `check_exact_same_batch.py`, `check_missing_sids.py`, `check_notes.py`, `check_rishab.py`, `detailed_analysis.py`, `final_categorized.py`, `final_repeats.py`, `find_repeats.py`, `generate_excel.py`, `print_cat1.py`, `print_remaining.py`, `print_remaining2.py`, `Repeated_Batches_Analysis.xlsx`, `unified_analysis.py`.
  - Removed unrelated incident document `MalwareIncidentReport.md`.
  - Removed Word temporary lock file `docs/~$oject_Action_Plan_and_Tracker.docx`.

---

## [Commit c3eb35f] - 2026-11-11

### Added
- **Syllabus PDF Generation & Delivery**:
  - Created `app/apps/courses/generate_syllabus_pdf.py` using `fpdf2` generating comprehensive 2-page Data Analysis brochure (`app/static/pdf/Data_Analysis_Syllabus.pdf`).
  - Added route `GET /course/syllabus/download` (attachment download).
  - Added route `GET /course/syllabus` (browser inline preview).
  - Added syllabus view and download buttons in homepage navbar and hero section.
- **Optional Student Email**:
  - Changed `email` field in `EnquiryCreate`, `BatchRegistrationCreate`, and `StudentLead` ORM model to be optional.
  - Only `full_name` and `phone` are strictly mandatory across all registration and inquiry forms.
- **Admin Portal Security Hardening**:
  - Disabled public admin registration (`/admin/signup` redirects to `/admin/login`).
  - Implemented signed cookie-based session management (`URLSafeTimedSerializer`, 7 days validity).
  - Added CSRF-safe HTTP-only session cookie `admin_session`.
  - Added `GET /admin/logout` clearing session cookie.

---

## [Commit 9b8f2a1] - 2026-11-11

### Added
- **Course & Student Admission Engine (`app/apps/courses/`)**:
  - Models: `Batch`, `StudentLead`, `AdminUser` with SQLAlchemy ORM.
  - Dual database architecture supporting local SQLite (`course_platform.db`) and Cloud PostgreSQL (`DATABASE_URL`).
  - REST API routes:
    - `GET /api/courses/instructor`
    - `GET /api/courses/batches`
    - `GET /api/courses/batches/{id}`
    - `POST /api/courses/enquiry`
    - `POST /api/courses/register`
    - `GET /api/courses/leads`
    - `GET /api/courses/leads/summary`
    - `GET /api/courses/leads/export.csv`
    - `PATCH /api/courses/leads/{id}/status`
- **Frontend Pages & Interactive Modals**:
  - Transformed `app/templates/index.html` to highlight Shubham Singh as Lead Python & Data Architecture Consultant.
  - Highlighted 5 core course pillars: Python, SQL, Power BI, Excel, Tableau.
  - Set fixed weekend schedule: Saturday & Sunday only, 6:00 PM – 8:00 PM IST.
  - Enforced strict business rule: No pricing or fee figures anywhere on the public website.
  - Dedicated full-page registration at `/register`.
  - Registration confirmation page at `/registration-success`.
  - Interactive enrollment and inquiry modals in homepage with toast alerts.
- **Automated Test Suite**:
  - Added 15 comprehensive automated test cases in `tests/test_courses.py` and `tests/test_main.py`.
