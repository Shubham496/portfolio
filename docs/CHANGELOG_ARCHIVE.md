# Historical Changelog Archive (CHANGELOG_ARCHIVE.md)

This file stores **historical changelog entries** transferred from [`Changeslog.md`](file:///f:/Projects/coding/Changeslog.md) as development progresses.
Entries are organized chronologically by **Year** and **Month**, preserving original dates, descriptions, affected files, technical decisions, database schemas, and API changes.

---

## Archiving Policy & Maintenance Protocol
1. **15-Entry Retention Limit**: [`Changeslog.md`](file:///f:/Projects/coding/Changeslog.md) holds strictly the latest 15 development entries.
2. **Transfer on Overflow**: When a new meaningful task is completed and added to `Changeslog.md` (pushing the count to 16), the oldest entry is transferred completely to this archive under the appropriate Year & Month section.
3. **Information Preservation**: Never delete, shorten, or discard technical details during archiving. Original dates, filenames, schemas, and rationale must be preserved intact.
4. **Duplicate Prevention**: Verify that entries exist in either `Changeslog.md` or `CHANGELOG_ARCHIVE.md`, never duplicated across both.

---

## 2026

### November 2026

- **[Archived from Changeslog.md Entry 17] (2026-11-19)**:
  - **Feature**: Phase 0: Security Hardening, Lead API Access Control, Legal Policies & Consent Enforcement: Hardened platform security and student data privacy before scaling traffic; locked all `/api/courses/leads*` and `/api/courses/batches` endpoints behind `require_admin` dependency (returning HTTP 401 for unauthorized access while leaving public registration and inquiry endpoints open); eliminated hardcoded fallback secrets across code and documentation; configured production startup assertion in `DeploymentSettings` refusing boot if `SECRET_KEY` is missing or default; authored comprehensive legal policy views (`/privacy`, `/terms`, `/refund-policy`); updated global footer with direct legal policy navigation; implemented mandatory consent capture ("I agree to be contacted by phone or WhatsApp about this course") across dedicated registration view (`register.html`), enrollment modal, enquiry modal, and student portal account creation; extended `student_leads` table with `consent_given` and `consent_at` columns along with idempotent startup database migrations; added `do_not_contact` lead pipeline status in schemas, services, dashboard filters, and export routines; implemented logging PII masking utilities (`mask_phone`, `mask_email`) preventing raw contact disclosure in application logs; expanded test suite with 5 new automated security tests (51 tests passing cleanly).
  - **Files**: `app/core/base_config.py`, `app/core/deployment.py`, `app/core/local.py`, `app/apps/courses/auth.py`, `app/apps/courses/router.py`, `app/apps/courses/models.py`, `app/apps/courses/schemas.py`, `app/apps/courses/services.py`, `app/main.py`, `app/templates/legal/privacy.html`, `app/templates/legal/terms.html`, `app/templates/legal/refund_policy.html`, `app/templates/partials/footer.html`, `app/templates/register.html`, `app/templates/sections/modals.html`, `app/templates/student/register.html`, `app/templates/admin/dashboard.html`, `tests/test_courses.py`, `docs/task_new.md`, `docs/AGENT_GUIDE.md`, `GUIDE.md`, `Changeslog.md`, `CHANGELOG_ARCHIVE.md`.
  - **API Changes**: Secured `GET /api/courses/leads`, `GET /api/courses/leads/summary`, `GET /api/courses/leads/export.csv`, `GET /api/courses/leads/{id}`, `PATCH /api/courses/leads/{id}/status`, `POST /api/courses/batches` with `require_admin`; mounted public web routes `GET /privacy`, `GET /terms`, `GET /refund-policy`; updated `POST /api/courses/enquiry` and `POST /api/courses/register` with mandatory `consent` validation.
  - **Database Changes**: Added `consent_given` (Boolean, default True) and `consent_at` (DateTime) columns to `student_leads` table; added `do_not_contact` to `status` choices in `LeadStatusUpdate`; updated `export_leads_csv` with Consent Given and Consent At columns.
  - **Bugs Fixed**: Resolved unauthenticated access loophole on leads pipeline endpoints; purged legacy fallback secret key strings.
  - **Breaking Changes**: None for public students; automated lead scrapers without admin credentials now receive HTTP 401 Unauthorized.

- **[Archived from Changeslog.md Entry 16] (2026-11-19)**:
  - **Feature**: Phase 2: Student Authentication, Access Control & Activity Logging: Implemented complete student authentication system and activity logging engine; added `users` and `user_activity_logs` tables; created student registration view (`/student/register`) respecting the mandatory phone & optional email invariant; created student sign-in (`/student/login`) supporting phone or email login; implemented 30-day signed HTTP-only cookie session management (`student_session`); created student portal dashboard (`/student/dashboard`) displaying verified badge, activity history, and downloadable datasets; established Practice Datasets Vault (`/library/datasets`) and dataset detail view (`/library/datasets/{slug}`) with schema data dictionaries and preview rows; implemented protected dataset download gate (`/library/datasets/{slug}/download`) providing 1-click RFC 4180 CSV downloads for authenticated students while redirecting guests; created activity logging service linking anonymous guest reading trails to student accounts upon registration/login; added JSON APIs (`POST /api/student/register`, `POST /api/student/login`, `GET /api/student/me`, `POST /api/activity/log`); created comprehensive automated test suite with 14 test cases (`tests/test_student_auth.py`).
  - **Files**: `app/apps/courses/models.py`, `app/apps/courses/schemas.py`, `app/apps/courses/auth.py`, `app/apps/courses/services.py`, `app/apps/courses/student_router.py`, `app/apps/library/models.py`, `app/apps/library/services.py`, `app/apps/library/router.py`, `app/main.py`, `app/templates/partials/navbar.html`, `app/templates/student/login.html`, `app/templates/student/register.html`, `app/templates/student/dashboard.html`, `app/templates/library/datasets.html`, `app/templates/library/dataset_detail.html`, `tests/test_student_auth.py`, `docs/task_new.md`, `GUIDE.md`, `Changeslog.md`, `CHANGELOG_ARCHIVE.md`.
  - **API Changes**: Mounted `/student/login`, `/student/register`, `/student/logout`, `/student/dashboard`, `/library/datasets`, `/library/datasets/{slug}`, `/library/datasets/{slug}/download`, `/api/student/register`, `/api/student/login`, `/api/student/me`, `/api/activity/log`.
  - **Database Changes**: Added `users` table (`id`, `full_name`, `phone` [unique], `email`, `hashed_password`, `user_type`, `college_or_company`, `is_active`, `created_at`, `updated_at`); added `user_activity_logs` table (`id`, `user_id` [FK users.id], `session_id`, `event_type`, `resource_type`, `resource_slug`, `referrer`, `ip_address`, `created_at`).
  - **Bugs Fixed**: Resolved TestClient cookie persistence across session boundary tests in test fixtures.
  - **Breaking Changes**: None.

- **[Archived from Changeslog.md Entry 15] (2026-11-18)**:
  - **Feature**: Phase 1.7: W3Schools Sequential SQL Study Track & Topic Progression: Re-architected `/library/sql` into a 38-topic sequential study track across 11 categories mirroring W3Schools MySQL/SQL standards; added `< Previous Topic` and `Next Topic >` sequential navigation; isolated viva interview question banks into the dedicated Interview Questions tab (`?tab=interview_questions`).
  - **Files**: `app/apps/library/router.py`, `app/apps/library/services.py`, `app/content/sql/sql-joins-textbook-vs-reality.md`, `tests/test_library.py`.
  - **API Changes**: Added `get_adjacent_topics_from_list()` in `app/apps/library/services.py`; updated `/library/{subject}` route handling.
  - **Database Changes**: None.
  - **Bugs Fixed**: Prevented standalone viva question banks from polluting the step-by-step SQL tutorial progression.
  - **Breaking Changes**: None.

- **[Archived from Changeslog.md Entry 14] (2026-11-18)**:
  - **Feature**: Phase 1.6: W3Schools Panel Architecture, Hierarchical Topic Sidebar & Sequential Navigation: Transformed `/library/{subject}` into a 4-panel workspace (All Topics, Notes, Interview Questions, Video Lectures); implemented a left hierarchical topic sidebar with instant topic switching; authored Python foundational blueprints.
  - **Files**: `app/apps/library/router.py`, `app/apps/library/services.py`, `app/templates/library/reader.html`, `app/templates/library/subject_hub.html`, `tests/test_library.py`.
  - **API Changes**: Implemented `get_adjacent_topics(subject, slug)`; added `?tab=` query parameter routing on subject hubs.
  - **Database Changes**: None.
  - **Bugs Fixed**: None.
  - **Breaking Changes**: None.

- **[Archived from Changeslog.md Entry 13] (2026-11-18)**:
  - **Feature**: Phase 1.5: 34 Major Languages & Tools Catalog, Topic Curricula & Navigation Polish: Expanded resource catalog to index 34 major programming languages, databases, data tools, frameworks, and cloud platforms; dynamically synthesized 5-part blueprint guides with Table of Contents; added minimalist icon grid with category filter tabs; added universal left in-page navigator rail (`in_page_nav.html`).
  - **Files**: `app/apps/library/services.py`, `app/templates/library/index.html`, `app/templates/library/reader.html`, `app/templates/library/subject_hub.html`, `app/templates/partials/navbar.html`, `app/templates/partials/in_page_nav.html`, `tests/test_library.py`.
  - **API Changes**: Synthesized 5-part curriculum generator in `app/apps/library/services.py`.
  - **Database Changes**: None.
  - **Bugs Fixed**: Eliminated 404 errors for topics under active curation.
  - **Breaking Changes**: None.

- **[Archived from Changeslog.md Entry 12] (2026-11-18)**:
  - **Feature**: Phase 1: Core Library Engine, Base Routing & Technical Docs UI Completed: Implemented core Knowledge Engine; Markdown parser with PyMdown extensions (admonitions, code highlight, tables); in-memory LRU/TTL caching with file mtime invalidation; 3-column docs reader layout (`reader.html`).
  - **Files**: `requirements.txt`, `app/apps/library/__init__.py`, `app/apps/library/router.py`, `app/apps/library/services.py`, `app/content/sql/sql-joins-textbook-vs-reality.md`, `app/main.py`, `app/static/css/style.css`, `app/templates/base.html`, `app/templates/library/index.html`, `app/templates/library/reader.html`, `app/templates/library/subject_hub.html`, `app/templates/partials/footer.html`, `app/templates/partials/navbar.html`, `tests/test_library.py`.
  - **API Changes**: Mounted `GET /library`, `GET /library/{subject}`, `GET /library/{subject}/notes/{slug}`, `GET /api/library/subjects`, `GET /api/library/{subject}/documents`.
  - **Database Changes**: Established YAML frontmatter schema (`title`, `slug`, `subject`, `vertical`, `tier`, `price_inr`, `tags`).
  - **Bugs Fixed**: None.
  - **Breaking Changes**: None.

- **[Archived from Changeslog.md Entry 11] (2026-11-18)**:
  - **Feature**: Knowledge Engine Blueprint, Decoupled Assets Vault & Micro-Monetization Architecture: Designed 5-phase educational platform roadmap (`docs/task_new.md`); established decoupled secondary asset vault (`external_assets/` linked to `https://github.com/Shubham496/mythos-assets`); formulated 4-tier micro-monetization ladder (free core notes, free student datasets, ₹10–₹49 micro-assets, unadvertised live cohorts).
  - **Files**: `external_assets/`, `.gitignore`, `docs/task_new.md`, `docs/AGENT_GUIDE.md`.
  - **API Changes**: None.
  - **Database Changes**: None.
  - **Bugs Fixed**: Prevented Render.io container slug size and RAM bloat by isolating media/datasets from Git tracking.
  - **Breaking Changes**: None.

- **[Archived from Changeslog.md Entry 10] (2026-11-15)**:
  - **Feature**: Re-architected platform identity into MYTHOS Online Institute with multiple cohort offerings (Performance Marketing Track 1, SEO & Growth Track 2, Data Analysis & BI Track 3); completely removed defensive payment and fee disclaimers across all pages; added dynamic course track selection in enrollment forms and modals.
  - **Files**: `app/templates/sections/mentor.html`, `app/templates/sections/modals.html`, `app/templates/sections/syllabus.html`, `app/templates/register.html`, `app/templates/confirmation.html`, `app/static/js/main.js`, `app/apps/courses/generate_syllabus_pdf.py`, `app/apps/courses/schemas.py`, `app/apps/courses/router.py`.
  - **API Changes**: Updated `POST /api/courses/register` and `POST /api/courses/enquiry` to accept `course_name` and `course_interest`.
  - **Database Changes**: Pydantic schemas updated for course selection.
  - **Bugs Fixed**: Eliminated awkward defensive payment disclaimers across templates.
  - **Breaking Changes**: None.

- **[Archived from Changeslog.md Entry 9] (2026-11-12)**:
  - **Feature**: Replaced pixelated assets with 1376x768 3D studio renders (illuminated circular neon podium, gradient 'M' ribbon sculpture); created zero-halo transparent icons (`mythos_icon_transparent.png`, `mythos_icon_2048.png`); built precision vector SVG emblem (`mythos_emblem.svg`); updated certificate generator to modern FPDF2 coordinates.
  - **Files**: `design/assets/`, `app/static/Images/mythos/`, `design/certificate_generator_template.py`, `design/GUIDELINES.md`.
  - **API Changes**: Modernized `fpdf2` coordinate calls (`new_x`, `new_y`).
  - **Database Changes**: None.
  - **Bugs Fixed**: Eliminated alpha halo fringing; resolved FPDF2 deprecation warnings.
  - **Breaking Changes**: None.

- **[Archived from Changeslog.md Entry 8] (2026-11-12)**:
  - **Feature**: Codified immutable policy that ONLY the human platform owner can execute `git push`; replaced personal instructor photos with high-tech Mythos Data Systems Pipeline card; redesigned `#about` into Direct Admissions & Mentorship Desk; implemented paired laptop accordion expansion for curriculum modules ([1,2], [3,4], [5,6]); established `design/` repository; rebuilt 2-page syllabus PDF.
  - **Files**: `docs/AGENT_GUIDE.md`, `app/templates/sections/syllabus.html`, `app/templates/sections/mentor.html`, `app/core/base_config.py`, `app/apps/courses/services.py`, `app/apps/courses/generate_syllabus_pdf.py`, `design/`.
  - **API Changes**: Updated `toggleSyllabus(index)` paired logic.
  - **Database Changes**: None.
  - **Bugs Fixed**: Mobile vs laptop syllabus expansion ergonomics.
  - **Breaking Changes**: None.

- **[Archived from Changeslog.md Entry 7] (2026-11-12)**:
  - **Feature**: Decomposed monolithic 1,300-line `app/templates/index.html` into 10 maintainable Jinja2 section partials in `app/templates/sections/`; streamlined header navigation by removing redundant badges; created `.env.example` documenting all expected environment variables with safe dummy placeholders.
  - **Files**: `app/templates/index.html`, `app/templates/sections/*.html`, `app/templates/partials/navbar.html`, `.env.example`, `docs/AGENT_GUIDE.md`.
  - **API Changes**: None.
  - **Database Changes**: None.
  - **Bugs Fixed**: Eliminated monolithic HTML maintenance issues with zero visual or UX regression.
  - **Breaking Changes**: None.

- **[Archived from Changeslog.md Entry 6] (2026-11-12)**:
  - **Feature**: Expunged plaintext passwords from all documentation and git history; provisioned high-entropy master password for `admin` in `.env`; created isolated `agent_admin` test profile (`agent@mythostech.in`) with `AGENT_PASSWORD` in `.env`; redesigned floating hero portrait card; integrated direct WhatsApp click-to-chat links (`wa.me/918727864157`).
  - **Files**: `docs/AGENT_GUIDE.md`, `docs/USER_GUIDE.md`, `tests/test_courses.py`, `.env`, `app/templates/index.html`, `app/templates/partials/footer.html`, `app/templates/confirmation.html`, `app/static/js/main.js`, `app/static/pdf/Data_Analysis_Syllabus.pdf`.
  - **API Changes**: None.
  - **Database Changes**: Added `agent_admin` profile seeding in `app/apps/courses/services.py`.
  - **Bugs Fixed**: Resolved browser caching bug with syllabus accordion by inlining toggle logic and cache-busting `main.js?v=2.2`.
  - **Breaking Changes**: None.

#### [Historical Foundation: Commits 1c231b6 through c3eb35f] - 2026-11-02 to 2026-11-11

- **Commit c3eb35f (2026-11-11) [Archived from Changeslog.md Entry 2]**:
  - **Feature**: Dynamic generation of 2-page Data Analysis syllabus brochure via `fpdf2`; added routes for PDF download and inline browser preview; made student email optional across registration and inquiry forms; disabled public admin registration with 303 redirect to `/admin/login`; implemented signed HTTP-only cookie-based session management (`admin_session`) with 7-day expiration.
  - **Files**: `app/apps/courses/generate_syllabus_pdf.py`, `app/apps/courses/schemas.py`, `app/apps/courses/models.py`, `app/apps/courses/admin_router.py`, `app/main.py`.
  - **API Changes**: Added `GET /course/syllabus/download`, `GET /course/syllabus`, `GET /admin/logout`.
  - **Database Changes**: `StudentLead.email` set to `nullable=True`; Pydantic schemas updated with `email: Optional[str] = None`.
  - **Bugs Fixed**: Fixed security loophole allowing public account creation on admin routes.
  - **Breaking Changes**: None.

- **Commit 05e052c (2026-11-11) [Archived from Changeslog.md Entry 3]**:
  - **Feature**: Implemented SQL-level pagination in `get_leads_paginated()` with configurable `per_page` (10, 25, 50); restructured leads table into 7 distinct columns (Type, Submitted Date, Student, Contact, Message, Status, Admin Notes & Action); integrated `python-dotenv` for auto-loading `.env` variables (`ADMIN_PASSWORD`, `SECRET_KEY`, `DATABASE_URL`); purged 17 obsolete standalone attendance analysis scripts.
  - **Files**: `app/apps/courses/services.py`, `app/apps/courses/models.py`, `app/templates/admin/dashboard.html`, `app/core/config.py`, `requirements.txt`, `tests/test_courses.py`.
  - **API Changes**: Added query parameters (`page`, `per_page`, `lead_type`, `status`, `search`) to `/admin/dashboard`.
  - **Database Changes**: Added `created_date` and `created_time` IST formatting attributes to `StudentLead.to_dict()`.
  - **Bugs Fixed**: Resolved critical test bug where test runner overwrote production admin password hash when run without environment variables.
  - **Breaking Changes**: None.

- **[Archived from Changeslog.md Entry 4] (2026-11-12)**:
  - **Feature**: Overhauled design system across all pages to Mythos brand ("BUILD SKILLS. BUILD SYSTEMS. BUILD THE FUTURE.") using Google Fonts Poppins, Deep Navy (`#070B14`), Electric Blue (`#2563EB`), Cyan (`#06B6D4`), and Split Orange (`#F97316`); rebuilt landing page with hero, problem vs solution, capability programs, methodology, capstones, and admission desk; updated cohort views.
  - **Files**: `app/templates/base.html`, `app/templates/index.html`, `app/templates/register.html`, `app/templates/confirmation.html`, `app/templates/admin/login.html`, `app/templates/admin/dashboard.html`, `app/static/css/style.css`.
  - **API Changes**: None.
  - **Database Changes**: None.
  - **Bugs Fixed**: None.
  - **Breaking Changes**: None.

- **[Archived from Changeslog.md Entry 5] (2026-11-12)**:
  - **Feature**: Embedded instructor photo in illuminated podium stage with floating "Students Trained: 550+" pulsing badge; added 4-card trust metric strip; converted static syllabus into interactive explorer with "Show More Details" and "Expand All / Collapse All"; detailed deep-dive competencies across Excel, SQL, Python, Power BI, and Tableau; introduced 4-pillar placement system (GitHub, ATS Resume, LinkedIn, Mock Interviews).
  - **Files**: `app/templates/sections/hero.html`, `app/templates/sections/syllabus.html`, `app/templates/sections/career.html`, `app/apps/courses/generate_syllabus_pdf.py`.
  - **API Changes**: None.
  - **Database Changes**: None.
  - **Bugs Fixed**: None.
  - **Breaking Changes**: None.

- **Commit 4347a5e (2026-11-11)**:
  - **Feature**: Hardened admin authentication integration test to be strictly idempotent across test runner environments.
  - **Files**: `tests/test_courses.py`.
  - **Technical Decision**: Prevented test environment runs from mutating production password hashes when executed without explicit environment credentials.

- **Commit b1d7df3 (2026-11-11)**:
  - **Feature**: Added dedicated full-page batch registration view (`/register`), post-registration confirmation view (`/registration-success`), direct syllabus PDF download endpoints (`/course/syllabus/download` and `/course/syllabus`), and secret instructor monitoring portal (`/admin`).
  - **Files**: `app/main.py`, `app/templates/register.html`, `app/templates/confirmation.html`, `app/apps/courses/admin_router.py`, `app/templates/admin/login.html`, `app/templates/admin/dashboard.html`.
  - **API Changes**: Introduced `/admin/login`, `/admin/dashboard`, `/admin/leads/{id}/status`.
  - **Security Decision**: Implemented HTTP-only session cookies and permanently disabled public signup routes.

- **Commit b0da854 (2026-11-11)**:
  - **Feature**: Added temporary batch attendance analysis scripts and historical enrollment spreadsheets for initial batch audits (later cleaned in commit `05e052c`).
  - **Files**: `analyze_attendance.py`, `check_att.py`, `Repeated_Batches_Analysis.xlsx`.

- **Commit 0e6e320 (2026-11-11)**:
  - **Feature**: Transformed developer portfolio landing page into an interactive Data Analysis teaching and student enrollment platform.
  - **Files**: `app/templates/index.html`, `app/static/css/style.css`, `app/static/js/main.js`.
  - **UI Additions**: Added interactive batch enrollment modal (`#modal-enroll`), curriculum inquiry modal (`#modal-enquiry`), expandable 6-module curriculum accordion, and weekend schedule highlights (Saturday & Sunday, 6:00 PM – 8:00 PM IST).

- **Commit af37f5a (2026-11-11)**:
  - **Feature**: Established initial comprehensive documentation hub.
  - **Files**: `docs/AGENT_GUIDE.md`, `docs/USER_GUIDE.md`, `docs/README.md`.
  - **Technical Decision**: Formulated the AI agent technical specification to provide context without requiring manual file inspection.

- **Commit 705109c (2026-11-10)**:
  - **Feature**: Implemented core backend models and REST endpoints for weekend Data Analysis batch registration and prospective student inquiries.
  - **Files**: `app/apps/courses/models.py`, `app/apps/courses/database.py`, `app/apps/courses/router.py`, `app/apps/courses/schemas.py`.
  - **Database Changes**: Provisioned initial `batches` and `student_leads` tables with SQLite fallback.

- **Commit 9b8f2a1 (2026-11-11) [Archived from Changeslog.md Entry 1]**:
  - **Feature**: Initialized Course & Student Admission Engine (`app/apps/courses/`); established SQLAlchemy models (`Batch`, `StudentLead`, `AdminUser`); dual-database architecture (SQLite local, PostgreSQL cloud); dedicated registration page (`/register`), success page (`/registration-success`), and homepage inquiry modals; created 15 automated test cases in `tests/test_courses.py` and `tests/test_main.py`.
  - **Files**: `app/apps/courses/models.py`, `app/apps/courses/database.py`, `app/apps/courses/router.py`, `app/apps/courses/services.py`, `app/templates/index.html`, `app/templates/register.html`, `app/templates/confirmation.html`, `tests/test_courses.py`, `tests/test_main.py`.
  - **API Changes**: Created `GET /api/courses/instructor`, `GET /api/courses/batches`, `GET /api/courses/batches/{id}`, `POST /api/courses/enquiry`, `POST /api/courses/register`, `GET /api/courses/leads`, `GET /api/courses/leads/summary`, `GET /api/courses/leads/export.csv`, `PATCH /api/courses/leads/{id}/status`.
  - **Database Changes**: Created `batches`, `student_leads`, and `admin_users` tables.
  - **Bugs Fixed**: Initial core admissions implementation.
  - **Breaking Changes**: None.

- **Commit e9047fc & 433f02d (2026-11-02)**:
  - **Feature**: Added inset margins and custom webkit scrollbar styling for floating scrollbars across light and dark themes; fixed theme toggle icon inversion bug.
  - **Files**: `app/static/css/style.css`, `app/static/js/main.js`.

- **Commit b739938 & d3d21e1 (2026-11-02)**:
  - **Feature**: Implemented client-side dark/light theme switcher with persistent localStorage; increased sun/moon toggle icon size; boosted light theme contrast; integrated verified SVGs and Devicons for Power BI, Tableau, Snowflake, and n8n; added phone contact details.
  - **Files**: `app/templates/base.html`, `app/static/css/style.css`, `app/static/js/main.js`.

- **Commit 485356a & 1f1e482 (2026-11-02)**:
  - **Feature**: Toned down ambient neon glow; refined minimalist developer UI; converted skill badges to interactive button-style tech icons; added compact hero spacing and inline career experience timeline strip.
  - **Files**: `app/templates/index.html`, `app/static/css/style.css`.

- **Commit 997b5a5 (2026-11-02)**:
  - **Feature**: Restructured landing page hierarchy to feature prominent "Try My Apps" showcase directly below skills.
  - **Files**: `app/templates/index.html`.

- **Commit baf41d3 (2026-11-02)**:
  - **Feature**: Implemented interactive SQLite-backed Project Task and Sprint Tracker mini-app mounted at `/apps/todos`.
  - **Files**: `app/apps/todos/__init__.py`, `app/apps/todos/models.py`, `app/apps/todos/router.py`, `app/apps/todos/templates/todos.html`, `portfolio.db`.
  - **Database Changes**: Provisioned `project_todos` table in `portfolio.db`.

- **Commit 1c231b6 (2026-11-02)**:
  - **Feature**: Initial platform repository setup; established FastAPI ASGI application; configured settings separation between `LocalSettings` and `DeploymentSettings`.
  - **Files**: `app/main.py`, `app/core/base_config.py`, `app/core/config.py`, `app/core/local.py`, `app/core/deployment.py`, `Procfile`, `render.yaml`, `requirements.txt`.
  - **Architectural Decision**: Bound dynamic cloud `$PORT` for Render compatibility while maintaining zero-setup SQLite execution locally.
