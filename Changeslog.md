# Recent Development History (Changeslog.md)

This file contains the **latest 15 meaningful development entries** for the **MYTHOS Online Institute** platform.
Historical records prior to these entries are archived in [`docs/CHANGELOG_ARCHIVE.md`](file:///f:/Projects/coding/docs/CHANGELOG_ARCHIVE.md).

---

## [Entry 20] - 2026-11-19 (Phase 3: Modular Cohort & Subject Display — Track Groups, Curriculum Roadmap Strip, Next-Batch Waitlist, Honest Scarcity & Admin Batch CRUD)
- **Feature Added / Modified**: Implemented comprehensive modular cohort and subject display architecture; restructured cohort presentation on the homepage (`app/templates/sections/programs.html`) and registration page (`app/templates/register.html`) with dual-track grouping (**Data Analytics & BI Track** vs **Digital Marketing Track**) and lifecycle classification (**Now Enrolling**, **Running**, **Next in Queue**, and **Archived/Past** in collapsed historical drawer); embedded horizontal curriculum roadmap strip for Data Analytics rendering `[SUBJECT_ORDER]` (`SQL`, `Excel`, `Power BI`, `Python`, `Tableau`, `Git & GitHub`) with live enrolling badge ("One subject per batch so you go deep") and one-click "Notify Me for Next Batch" waitlist capture; added priority waitlist modal (`app/templates/sections/modals.html`) and waitlist lead capture endpoint (`POST /api/courses/waitlist`) storing `lead_type="waitlist"` and `subject_interest`; aligned Digital Marketing cohorts with `[DM_SCHEDULE]` and mentor attribution linking to `[DM_MENTOR_NAME]` (`/about#dm-mentor`), while isolating Data Analytics cohorts to the anonymous *Mythos Data Analytics Mentor* (Sat & Sun 6–8 PM IST); integrated real-time seat scarcity calculation (`remaining_seats = max_seats - total_registrations`) with strictly zero public tuition fee or pricing mentions; engineered complete Admin Cohort & Batch Manager (`/admin/batches`, `app/templates/admin/batches.html`) enabling the platform owner to create, edit, update schedules, toggle active states, and archive cohorts without modifying application code; added `track` (`data_analytics`, `digital_marketing`) column to `batches` table and `subject_interest` column to `student_leads` with idempotent database migrations; added 4 new automated test cases in `tests/test_courses.py` (70 tests passing cleanly).
- **Files Affected**: `app/core/base_config.py`, `app/apps/courses/models.py`, `app/apps/courses/schemas.py`, `app/apps/courses/services.py`, `app/apps/courses/router.py`, `app/apps/courses/admin_router.py`, `app/main.py`, `app/static/js/main.js`, `app/templates/sections/programs.html`, `app/templates/sections/modals.html`, `app/templates/register.html`, `app/templates/admin/batches.html`, `app/templates/admin/dashboard.html`, `tests/test_courses.py`, `docs/task_new.md`, `GUIDE.md`, `Changeslog.md`, `docs/CHANGELOG_ARCHIVE.md`.
- **Important API Changes**: Added `GET /api/courses/batches/grouped`, `POST /api/courses/waitlist`, `PATCH /api/courses/batches/{id}`; added web routes `GET /admin/batches`, `POST /admin/batches/create`, `POST /admin/batches/{id}/update`, `POST /admin/batches/{id}/toggle-active`.
- **Database / Schema Changes**: Added `track` (VARCHAR(50), default 'data_analytics') column to `batches` table; added `subject_interest` (VARCHAR(100)) column to `student_leads` table; added `BatchUpdate` and `WaitlistCreate` Pydantic schemas.
- **Bugs Fixed**: Resolved route collision where `/batches/{batch_id}` intercepted `/batches/grouped`; eliminated keyword leakage on homepage causing test assertion conflicts; sanitized test database teardown.
- **Breaking Changes**: None.

---

## [Entry 19] - 2026-11-19 (Phase 2: Trust & People — Dual Mentorship, Contact Sanitization & Brand Credibility)
- **Feature Added / Modified**: Implemented comprehensive platform human credibility and brand transparency overhaul; rebuilt the Mentorship section on the landing page (`app/templates/sections/mentor.html`) and modernized faculty showcase (`app/templates/about.html`) featuring strict discipline isolation between specialized mentors; established grounded profile for the anonymous *Mythos Data Analytics Mentor* (lead Python & data architecture faculty, no photo, high-tech terminal emblem, 3+ years teaching, 400+ learners taught, covering SQL, Python, Excel, Power BI, Tableau, Git/GitHub, Sat & Sun 6–8 PM IST); established verified showcase for the Digital Marketing Mentor (`[DM_MENTOR_NAME]`, professional photo container `[DM_MENTOR_PHOTO]`, verified bio `[DM_MENTOR_BIO]`, verified LinkedIn link `[DM_MENTOR_LINKEDIN]`, schedule `[DM_SCHEDULE]`); systematically purged the legacy "550+" metric across all templates, services, brochure PDF generator, and test assertions, standardizing on `[TRUST_CLAIM]` (default: "400+ learners taught by our mentors over 3+ years"); completely removed hardcoded personal email (`shubhamsinghh057@gmail.com`) and phone (`8727864157`) across templates, footer, confirmation, syllabus brochure, and config, migrating all admissions and counseling channels to dynamic environment variables `BUSINESS_EMAIL` and `BUSINESS_WHATSAPP`; re-rendered `app/static/pdf/Data_Analysis_Syllabus.pdf` with updated mentor credentials and dynamic contact channels; implemented clean, dormant testimonials partial (`app/templates/sections/testimonials.html`) that remains completely hidden when no verified testimonials exist; audited copy across platform to eliminate job guarantee or placement claims, framing all outcomes around verifiable proof of work and interview preparation; added 5 automated test cases in `tests/test_main.py` (66 tests passing cleanly).
- **Files Affected**: `app/core/base_config.py`, `.env`, `.env.example`, `app/apps/courses/services.py`, `app/apps/courses/generate_syllabus_pdf.py`, `app/static/pdf/Data_Analysis_Syllabus.pdf`, `app/templates/sections/mentor.html`, `app/templates/sections/hero.html`, `app/templates/sections/testimonials.html`, `app/templates/sections/engine.html`, `app/templates/sections/career.html`, `app/templates/index.html`, `app/templates/about.html`, `app/templates/register.html`, `app/templates/student/register.html`, `app/templates/confirmation.html`, `app/templates/library/index.html`, `app/templates/library/reader.html`, `app/templates/partials/footer.html`, `design/GUIDELINES.md`, `docs/README.md`, `docs/AGENT_GUIDE.md`, `docs/USER_GUIDE.md`, `docs/task_new.md`, `tests/test_courses.py`, `tests/test_main.py`, `Changeslog.md`, `CHANGELOG_ARCHIVE.md`, `GUIDE.md`.
- **Important API Changes**: Updated `/api/courses/instructor` to output dynamic `BUSINESS_EMAIL`, `BUSINESS_WHATSAPP`, and `TRUST_CLAIM` without legacy contact strings.
- **Database / Schema Changes**: None.
- **Bugs Fixed**: Eliminated hardcoded personal contact leakage on public pages; removed legacy 550+ metric across templates and PDF; resolved HTML entity escaping in dual-mentor test assertions.
- **Breaking Changes**: None.

---

## [Entry 18] - 2026-11-19 (Phase 1: Findability, SEO Directives, Content Quality Gate & Performance Caching)
- **Feature Added / Modified**: Implemented comprehensive search engine findability and content quality gate architecture; created dynamic `GET /sitemap.xml` mapping core pages (`/`, `/about`, `/demo`, `/register`, `/privacy`, `/terms`, `/refund-policy`), active subject hubs (`/library/{subject}`), practice datasets (`/library/datasets/{slug}`), and hand-authored published notes while strictly excluding draft blueprints; implemented dynamic `GET /robots.txt` disallowing `/admin/`, `/api/`, `/student/` and referencing `sitemap.xml`; authored dedicated faculty showcase view (`/about`) and free demo class reservation view (`/demo`); modernized `<head>` meta architecture across all templates with unique `<title>`, `<meta name="description">`, `<link rel="canonical">`, Open Graph (`og:title`, `og:description`, `og:image`, `og:url`), and Twitter Cards derived from `BASE_URL`; implemented Google Search Console verification support (`GOOGLE_SITE_VERIFICATION`); embedded Schema.org JSON-LD structured data (`EducationalOrganization` and `Course` schemas on homepage, `TechArticle` and `BreadcrumbList` on published notes, `Dataset` on dataset detail views); established Content Quality Gate with `status: "published" | "draft"` frontmatter attribute (marking hand-authored articles `published` and treating blueprint topics as `draft` with `noindex, nofollow` and "Coming Soon" sidebar badges); updated library resource counters to count exclusively published articles; configured HTTP static asset caching (`Cache-Control: public, max-age=31536000, immutable`), enabled `GZipMiddleware`, and added `loading="lazy"` across template images; added contextual Free Live Demo Class CTA cards on all study track hubs and note reading layouts; created 10 new automated test cases (61 tests passing cleanly).
- **Files Affected**: `app/core/base_config.py`, `.env.example`, `app/content/sql/sql-joins-textbook-vs-reality.md`, `app/apps/library/services.py`, `app/main.py`, `app/templates/base.html`, `app/templates/index.html`, `app/templates/register.html`, `app/templates/confirmation.html`, `app/templates/about.html`, `app/templates/demo.html`, `app/templates/library/index.html`, `app/templates/library/datasets.html`, `app/templates/library/dataset_detail.html`, `app/templates/library/subject_hub.html`, `app/templates/library/reader.html`, `app/templates/legal/privacy.html`, `app/templates/legal/terms.html`, `app/templates/legal/refund_policy.html`, `app/templates/admin/login.html`, `app/templates/admin/dashboard.html`, `app/templates/student/login.html`, `app/templates/student/register.html`, `app/templates/student/dashboard.html`, `app/templates/partials/navbar.html`, `app/templates/partials/footer.html`, `app/templates/sections/hero.html`, `tests/test_main.py`, `docs/task_new.md`, `GUIDE.md`, `Changeslog.md`, `CHANGELOG_ARCHIVE.md`.
- **Important API Changes**: Added `GET /sitemap.xml`, `GET /robots.txt`, `GET /about`, `GET /demo`; added `published_only` filtering support in `list_documents_for_subject`.
- **Database / Schema Changes**: Added `status` (`published` | `draft`) and `is_published` property to `DocumentMetadata` and markdown parsing engine.
- **Bugs Fixed**: Purged hardcoded legacy mentor string from `base.html` meta description; resolved missing robots directives on private and draft surfaces.
- **Breaking Changes**: None.

---

## [Entry 17] - 2026-11-19 (Phase 0: Security Hardening, Lead API Access Control, Legal Policies & Consent Enforcement)
- **Feature Added / Modified**: Hardened platform security and student data privacy before scaling traffic; locked all `/api/courses/leads*` and `/api/courses/batches` endpoints behind `require_admin` dependency (returning HTTP 401 for unauthorized access while leaving public registration and inquiry endpoints open); eliminated hardcoded fallback secrets across code and documentation; configured production startup assertion in `DeploymentSettings` refusing boot if `SECRET_KEY` is missing or default; authored comprehensive legal policy views (`/privacy`, `/terms`, `/refund-policy`); updated global footer with direct legal policy navigation; implemented mandatory consent capture ("I agree to be contacted by phone or WhatsApp about this course") across dedicated registration view (`register.html`), enrollment modal, enquiry modal, and student portal account creation; extended `student_leads` table with `consent_given` and `consent_at` columns along with idempotent startup database migrations; added `do_not_contact` lead pipeline status in schemas, services, dashboard filters, and export routines; implemented logging PII masking utilities (`mask_phone`, `mask_email`) preventing raw contact disclosure in application logs; expanded test suite with 5 new automated security tests (51 tests passing cleanly).
- **Files Affected**: `app/core/base_config.py`, `app/core/deployment.py`, `app/core/local.py`, `app/apps/courses/auth.py`, `app/apps/courses/router.py`, `app/apps/courses/models.py`, `app/apps/courses/schemas.py`, `app/apps/courses/services.py`, `app/main.py`, `app/templates/legal/privacy.html`, `app/templates/legal/terms.html`, `app/templates/legal/refund_policy.html`, `app/templates/partials/footer.html`, `app/templates/register.html`, `app/templates/sections/modals.html`, `app/templates/student/register.html`, `app/templates/admin/dashboard.html`, `tests/test_courses.py`, `docs/task_new.md`, `docs/AGENT_GUIDE.md`, `GUIDE.md`, `Changeslog.md`, `CHANGELOG_ARCHIVE.md`.
- **Important API Changes**: Secured `GET /api/courses/leads`, `GET /api/courses/leads/summary`, `GET /api/courses/leads/export.csv`, `GET /api/courses/leads/{id}`, `PATCH /api/courses/leads/{id}/status`, `POST /api/courses/batches` with `require_admin`; mounted public web routes `GET /privacy`, `GET /terms`, `GET /refund-policy`; updated `POST /api/courses/enquiry` and `POST /api/courses/register` with mandatory `consent` validation.
- **Database / Schema Changes**: Added `consent_given` (Boolean, default True) and `consent_at` (DateTime) columns to `student_leads` table; added `do_not_contact` to `status` choices in `LeadStatusUpdate`; updated `export_leads_csv` with Consent Given and Consent At columns.
- **Bugs Fixed**: Resolved unauthenticated access loophole on leads pipeline endpoints; purged legacy fallback secret key strings.
- **Breaking Changes**: None for public students; automated lead scrapers without admin credentials now receive HTTP 401 Unauthorized.

---

## [Entry 16] - 2026-11-19 (Phase 2: Student Authentication, Access Control & Activity Logging)
- **Feature Added / Modified**: Implemented complete student authentication system and activity logging engine; added `users` and `user_activity_logs` tables; created student registration view (`/student/register`) respecting the mandatory phone & optional email invariant; created student sign-in (`/student/login`) supporting phone or email login; implemented 30-day signed HTTP-only cookie session management (`student_session`); created student portal dashboard (`/student/dashboard`) displaying verified badge, activity history, and downloadable datasets; established Practice Datasets Vault (`/library/datasets`) and dataset detail view (`/library/datasets/{slug}`) with schema data dictionaries and preview rows; implemented protected dataset download gate (`/library/datasets/{slug}/download`) providing 1-click RFC 4180 CSV downloads for authenticated students while redirecting guests; created activity logging service linking anonymous guest reading trails to student accounts upon registration/login; added JSON APIs (`POST /api/student/register`, `POST /api/student/login`, `GET /api/student/me`, `POST /api/activity/log`); created comprehensive automated test suite with 14 test cases (`tests/test_student_auth.py`).
- **Files Affected**: `app/apps/courses/models.py`, `app/apps/courses/schemas.py`, `app/apps/courses/auth.py`, `app/apps/courses/services.py`, `app/apps/courses/student_router.py`, `app/apps/library/models.py`, `app/apps/library/services.py`, `app/apps/library/router.py`, `app/main.py`, `app/templates/partials/navbar.html`, `app/templates/student/login.html`, `app/templates/student/register.html`, `app/templates/student/dashboard.html`, `app/templates/library/datasets.html`, `app/templates/library/dataset_detail.html`, `tests/test_student_auth.py`, `docs/task_new.md`, `GUIDE.md`, `Changeslog.md`, `CHANGELOG_ARCHIVE.md`.
- **Important API Changes**: Mounted `/student/login`, `/student/register`, `/student/logout`, `/student/dashboard`, `/library/datasets`, `/library/datasets/{slug}`, `/library/datasets/{slug}/download`, `/api/student/register`, `/api/student/login`, `/api/student/me`, `/api/activity/log`.
- **Database / Schema Changes**: Added `users` table (`id`, `full_name`, `phone` [unique], `email`, `hashed_password`, `user_type`, `college_or_company`, `is_active`, `created_at`, `updated_at`); added `user_activity_logs` table (`id`, `user_id` [FK users.id], `session_id`, `event_type`, `resource_type`, `resource_slug`, `referrer`, `ip_address`, `created_at`).
- **Bugs Fixed**: Resolved TestClient cookie persistence across session boundary tests in test fixtures.
- **Breaking Changes**: None.

---

## [Entry 15] - 2026-11-18 (Phase 1.7: W3Schools Sequential SQL Study Track & Topic Progression)
- **Feature Added / Modified**: Re-architected `/library/sql` into a 38-topic sequential study track across 11 categories mirroring W3Schools MySQL/SQL standards; added `< Previous Topic` and `Next Topic >` sequential navigation; isolated viva interview question banks into the dedicated Interview Questions tab (`?tab=interview_questions`).
- **Files Affected**: `app/apps/library/router.py`, `app/apps/library/services.py`, `app/content/sql/sql-joins-textbook-vs-reality.md`, `tests/test_library.py`.
- **Important API Changes**: Added `get_adjacent_topics_from_list()` in `app/apps/library/services.py`; updated `/library/{subject}` route handling.
- **Database / Schema Changes**: None.
- **Bugs Fixed**: Prevented standalone viva question banks from polluting the step-by-step SQL tutorial progression.
- **Breaking Changes**: None.

---

## [Entry 14] - 2026-11-18 (Phase 1.6: W3Schools Panel Architecture, Hierarchical Topic Sidebar & Sequential Navigation)
- **Feature Added / Modified**: Transformed `/library/{subject}` into a 4-panel workspace (All Topics, Notes, Interview Questions, Video Lectures); implemented a left hierarchical topic sidebar with instant topic switching; authored Python foundational blueprints.
- **Files Affected**: `app/apps/library/router.py`, `app/apps/library/services.py`, `app/templates/library/reader.html`, `app/templates/library/subject_hub.html`, `tests/test_library.py`.
- **Important API Changes**: Implemented `get_adjacent_topics(subject, slug)`; added `?tab=` query parameter routing on subject hubs.
- **Database / Schema Changes**: None.
- **Bugs Fixed**: None.
- **Breaking Changes**: None.

---

## [Entry 13] - 2026-11-18 (Phase 1.5: 34 Major Languages & Tools Catalog, Topic Curricula & Navigation Polish)
- **Feature Added / Modified**: Expanded resource catalog to index 34 major programming languages, databases, data tools, frameworks, and cloud platforms; dynamically synthesized 5-part blueprint guides with Table of Contents; added minimalist icon grid with category filter tabs; added universal left in-page navigator rail (`in_page_nav.html`).
- **Files Affected**: `app/apps/library/services.py`, `app/templates/library/index.html`, `app/templates/library/reader.html`, `app/templates/library/subject_hub.html`, `app/templates/partials/navbar.html`, `app/templates/partials/in_page_nav.html`, `tests/test_library.py`.
- **Important API Changes**: Synthesized 5-part curriculum generator in `app/apps/library/services.py`.
- **Database / Schema Changes**: None.
- **Bugs Fixed**: Eliminated 404 errors for topics under active curation.
- **Breaking Changes**: None.

---

## [Entry 12] - 2026-11-18 (Phase 1: Core Library Engine, Base Routing & Technical Docs UI Completed)
- **Feature Added / Modified**: Implemented core Knowledge Engine; Markdown parser with PyMdown extensions (admonitions, code highlight, tables); in-memory LRU/TTL caching with file mtime invalidation; 3-column docs reader layout (`reader.html`).
- **Files Affected**: `requirements.txt`, `app/apps/library/__init__.py`, `app/apps/library/router.py`, `app/apps/library/services.py`, `app/content/sql/sql-joins-textbook-vs-reality.md`, `app/main.py`, `app/static/css/style.css`, `app/templates/base.html`, `app/templates/library/index.html`, `app/templates/library/reader.html`, `app/templates/library/subject_hub.html`, `app/templates/partials/footer.html`, `app/templates/partials/navbar.html`, `tests/test_library.py`.
- **Important API Changes**: Mounted `GET /library`, `GET /library/{subject}`, `GET /library/{subject}/notes/{slug}`, `GET /api/library/subjects`, `GET /api/library/{subject}/documents`.
- **Database / Schema Changes**: Established YAML frontmatter schema (`title`, `slug`, `subject`, `vertical`, `tier`, `price_inr`, `tags`).
- **Bugs Fixed**: None.
- **Breaking Changes**: None.

---

## [Entry 11] - 2026-11-18 (Knowledge Engine Blueprint, Decoupled Assets Vault & Micro-Monetization Architecture)
- **Feature Added / Modified**: Designed 5-phase educational platform roadmap (`docs/task_new.md`); established decoupled secondary asset vault (`external_assets/` linked to `https://github.com/Shubham496/mythos-assets`); formulated 4-tier micro-monetization ladder (free core notes, free student datasets, ₹10–₹49 micro-assets, unadvertised live cohorts).
- **Files Affected**: `external_assets/`, `.gitignore`, `docs/task_new.md`, `docs/AGENT_GUIDE.md`.
- **Important API Changes**: None.
- **Database / Schema Changes**: None.
- **Bugs Fixed**: Prevented Render.io container slug size and RAM bloat by isolating media/datasets from Git tracking.
- **Breaking Changes**: None.

---

## [Entry 10] - 2026-11-15 (Transition to Multi-Course Online Educational Institute & Complete Removal of Payment Mentions)
- **Feature Added / Modified**: Re-architected platform identity into MYTHOS Online Institute with multiple cohort offerings (Performance Marketing Track 1, SEO & Growth Track 2, Data Analysis & BI Track 3); completely removed defensive payment and fee disclaimers across all pages; added dynamic course track selection in enrollment forms and modals.
- **Files Affected**: `app/templates/sections/mentor.html`, `app/templates/sections/modals.html`, `app/templates/sections/syllabus.html`, `app/templates/register.html`, `app/templates/confirmation.html`, `app/static/js/main.js`, `app/apps/courses/generate_syllabus_pdf.py`, `app/apps/courses/schemas.py`, `app/apps/courses/router.py`.
- **Important API Changes**: Updated `POST /api/courses/register` and `POST /api/courses/enquiry` to accept `course_name` and `course_interest`.
- **Database / Schema Changes**: Pydantic schemas updated for course selection.
- **Bugs Fixed**: Eliminated awkward defensive payment disclaimers across templates.
- **Breaking Changes**: None.

---

## [Entry 9] - 2026-11-12 (High-Definition Design Assets & Brand Master Overhaul)
- **Feature Added / Modified**: Replaced pixelated assets with 1376x768 3D studio renders (illuminated circular neon podium, gradient 'M' ribbon sculpture); created zero-halo transparent icons (`mythos_icon_transparent.png`, `mythos_icon_2048.png`); built precision vector SVG emblem (`mythos_emblem.svg`); updated certificate generator to modern FPDF2 coordinates.
- **Files Affected**: `design/assets/`, `app/static/Images/mythos/`, `design/certificate_generator_template.py`, `design/GUIDELINES.md`.
- **Important API Changes**: Modernized `fpdf2` coordinate calls (`new_x`, `new_y`).
- **Database / Schema Changes**: None.
- **Bugs Fixed**: Eliminated alpha halo fringing; resolved FPDF2 deprecation warnings.
- **Breaking Changes**: None.

---

## [Entry 8] - 2026-11-12 (Production Push Authority, Brand Anonymization, Paired Syllabus, Design System & Styled Brochure)
- **Feature Added / Modified**: Codified immutable policy that ONLY the human platform owner can execute `git push`; replaced personal instructor photos with high-tech Mythos Data Systems Pipeline card; redesigned `#about` into Direct Admissions & Mentorship Desk; implemented paired laptop accordion expansion for curriculum modules ([1,2], [3,4], [5,6]); established `design/` repository; rebuilt 2-page syllabus PDF.
- **Files Affected**: `docs/AGENT_GUIDE.md`, `app/templates/sections/syllabus.html`, `app/templates/sections/mentor.html`, `app/core/base_config.py`, `app/apps/courses/services.py`, `app/apps/courses/generate_syllabus_pdf.py`, `design/`.
- **Important API Changes**: Updated `toggleSyllabus(index)` paired logic.
- **Database / Schema Changes**: None.
- **Bugs Fixed**: Mobile vs laptop syllabus expansion ergonomics.
- **Breaking Changes**: None.

---

## [Entry 7] - 2026-11-12 (Frontend Architecture Modularization & Environment Template)
- **Feature Added / Modified**: Decomposed monolithic 1,300-line `app/templates/index.html` into 10 maintainable Jinja2 section partials in `app/templates/sections/`; streamlined header navigation by removing redundant badges; created `.env.example` documenting all expected environment variables with safe dummy placeholders.
- **Files Affected**: `app/templates/index.html`, `app/templates/sections/*.html`, `app/templates/partials/navbar.html`, `.env.example`, `docs/AGENT_GUIDE.md`.
- **Important API Changes**: None.
- **Database / Schema Changes**: None.
- **Bugs Fixed**: Eliminated monolithic HTML maintenance issues with zero visual or UX regression.
- **Breaking Changes**: None.

---

## [Entry 6] - 2026-11-12 (Security Hardening, Hero Card Redesign, WhatsApp Integration & Interactive Syllabus Fix)
- **Feature Added / Modified**: Expunged plaintext passwords from all documentation and git history; provisioned high-entropy master password for `admin` in `.env`; created isolated `agent_admin` test profile (`agent@mythostech.in`) with `AGENT_PASSWORD` in `.env`; redesigned floating hero portrait card; integrated direct WhatsApp click-to-chat links (`wa.me/918727864157`).
- **Files Affected**: `docs/AGENT_GUIDE.md`, `docs/USER_GUIDE.md`, `tests/test_courses.py`, `.env`, `app/templates/index.html`, `app/templates/partials/footer.html`, `app/templates/confirmation.html`, `app/static/js/main.js`, `app/static/pdf/Data_Analysis_Syllabus.pdf`.
- **Important API Changes**: None.
- **Database / Schema Changes**: Added `agent_admin` profile seeding in `app/apps/courses/services.py`.
- **Bugs Fixed**: Resolved browser caching bug with syllabus accordion by inlining toggle logic and cache-busting `main.js?v=2.2`.
- **Breaking Changes**: None.

---

## Historical Changelog Archive Reference

For the complete archive of development history and foundations prior to these 15 entries, see:  
**[`docs/CHANGELOG_ARCHIVE.md`](file:///f:/Projects/coding/docs/CHANGELOG_ARCHIVE.md)**
