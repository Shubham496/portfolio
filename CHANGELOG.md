# Platform Changelog & Implementation History

All notable changes, updates, feature implementations, and bug fixes for the **MYTHOS Online Institute Platform** are documented in this file.
This serves as an audit trail and system log (similar to GitHub releases/commit logs) for developers, agents, and maintainers to immediately check what is already built, configured, and verified.

---

## [Latest Updates] - 2026-11-18 (Phase 1.5: Inter-Page Top Nav, Left In-Page Rails, Zero-Upfront Pricing & Icon Library Hub)

### Added, Updated & Refactored
- **Multi-Page Top Navigation with Hover Dropdowns (`app/templates/partials/navbar.html`)**:
  - Transformed the top navbar from intra-page section anchors into true multi-page navigation:
    - **Courses & Cohorts**: Hover dropdown with links to Track 1 (Performance Marketing), Track 2 (SEO & Growth), and Track 3 (Data Analytics & BI).
    - **Notes & Guides**: Hover dropdown for SQL, Python, Power BI, and Digital Marketing notes.
    - **Interview & Viva**: Direct dropdown for top viva banks and examiner trap banks.
    - **Datasets**: One-click link to clean real-world CSV portfolios (`/library?vertical=datasets`).
    - **Admissions**: Dedicated link to `/register`.
- **Universal Left-Side In-Page Section Navigator (`app/templates/partials/in_page_nav.html`)**:
  - Implemented glassmorphism docked left navigation rail with active scroll-spy and tooltip labels.
  - Allows 1-click jumping between page sections (`#hero`, `#engine`, `#programs`, `#methodology`, `#projects`, `#admission`, `#career`, `#syllabus`, `#about`).
  - Added responsive mobile in-page jump menu button.
- **Strict Zero-Upfront Pricing Rule Enforcement**:
  - Codified Rule 3 in `docs/AGENT_GUIDE.md`: Zero prices are displayed on browse surfaces, subject hubs, or reader sidebars.
  - Purged all upfront "₹10", "₹20", "₹99" badges across browse pages and replaced them with access status tags ("Free Access", "Student Account", "Viva Bank", "Complete Handbook").
  - Prices are only revealed when a student hits an access paywall or clicks to unlock a product.
- **Strictly Zero Code Execution Rule (Rule 7)**:
  - Codified immutable policy that the platform will never provide runtime code execution or interactive REPL consoles for students; all code remains static, copy-only syntax.
- **Minimalist Icon-First Library Hub (`app/templates/library/index.html`)**:
  - Completely decluttered `/library` by removing long text blocks and card clutter.
  - Replaced with a high-impact technology logo grid displaying big official symbols (MySQL, PostgreSQL, SQLite, Python, Pandas, NumPy, Power BI, Tableau, Excel, Google Ads/GA4, Meta Ads, Technical SEO) with clear names and quick-filter category pills.
- **Automated Verification**:
  - All 24 automated tests in `tests/test_courses.py`, `tests/test_library.py`, and `tests/test_main.py` passing cleanly (100%).

---

## [Latest Updates] - 2026-11-18 (Phase 1: Core Library Engine, Base Routing & Technical Docs UI Completed)

### Added, Configured & Implemented
- **Granular Task Decomposition in `docs/task_new.md`**:
  - Subdivided all 5 roadmap phases into granular, bite-sized tasks and subtasks for phased, deterministic execution.
- **Dependency Specification (Task 1.1)**:
  - Added `markdown>=3.6.0`, `python-frontmatter>=1.1.0`, and `pymdown-extensions>=10.7` to `requirements.txt`.
- **Content Engine & Caching Services (`app/apps/library/services.py`) (Task 1.2)**:
  - Built markdown file discovery and YAML frontmatter extraction (supporting `title`, `slug`, `subject`, `vertical`, `category`, `order`, `tier`, `price_inr`, `reading_time`, `description`, `tags`, `last_updated`).
  - Added PyMdown extensions integration (fenced code, highlight, tables, admonitions, and TOC tokens).
  - Added preprocessor converting GitHub-style alerts (`> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`, etc.) to standard admonitions.
  - Implemented automatic reading time calculation and in-memory TTL/LRU caching with on-disk mtime invalidation.
- **Library Web Routing & Application Mounting (`app/apps/library/router.py`) (Task 1.3)**:
  - Added `GET /library` (main resource hub with subject cards and micro-pricing badges).
  - Added `GET /library/{subject}` (subject portal with vertical tabs and category grouping).
  - Added `GET /library/{subject}/notes/{slug}` (3-column reader view).
  - Added JSON API endpoints: `GET /api/library/subjects` and `GET /api/library/{subject}/documents`.
  - Mounted `library_router` into `app/main.py`.
- **Documentation UI Templates & Styles (`app/templates/library/`) (Task 1.4)**:
  - `app/templates/library/index.html`: Responsive resource hub with subject cards, 5 vertical breakdowns, and live cohort CTA.
  - `app/templates/library/subject_hub.html`: Subject portal with vertical filter tabs, resource counter badges, and curriculum cards.
  - `app/templates/library/reader.html`: 3-column technical docs reader layout (collapsible left tree, center canvas with Prism.js & copy buttons, sticky TOC with scroll-spy, and WhatsApp/Telegram 1-click sharing).
  - Added complete typography, admonition styles, and responsive table styling in `app/static/css/style.css`.
- **Navigation & Footer Integration (Task 1.5)**:
  - Added Library link with active indicator in `app/templates/partials/navbar.html` (desktop & mobile menus).
  - Added Resource Library links in `app/templates/partials/footer.html` under Academics.
- **Flagship Seed Note & Comprehensive Test Suite (Task 1.6)**:
  - Authored starter flagship note `app/content/sql/sql-joins-textbook-vs-reality.md` following the 5-part content blueprint.
  - Created `tests/test_library.py` with 9 automated tests verifying routes, 404 boundaries, TOC extraction, caching, and JSON APIs.
  - Total automated tests expanded to 24 tests. All 24/24 passing (100%).

---

## [Latest Updates] - 2026-11-18 (Knowledge Engine Blueprint, Decoupled Assets Vault & Micro-Monetization Architecture)

### Added, Configured & Documented
- **Architectural Roadmap & Task Guide (`docs/task_new.md`)**:
  - Outlined comprehensive 5-phase blueprint to transform `mythostech.in` into an authoritative educational repository and dataset vault for Indian college students and junior developers.
  - Defined 5 distinct content verticals under a unified **Resource Library** (`/library`): Notes, Practice & Viva Banks, Datasets, Books & Handbooks, and Capstone Projects.
  - Formalized 5-part standard content blueprint for future technical guides: (1) Formal Exam Definition, (2) Interactive Query Examples, (3) Production Reality ("What Textbooks Skip"), (4) Exam & Interview Gotchas, and (5) Mythos Mentorship Bridge.
- **Micro-Monetization & Admissions Dual Strategy**:
  - Preserved the immutable rule that live weekend cohort tuition fees remain 100% unadvertised online (admissions and orientation counseling model via `/register`).
  - Introduced friction-free micro-pricing for student digital study assets:
    - Full solved viva & interview question banks: **₹10** (instant UPI unlock).
    - Complete semester exam notes bundles: **₹20 – ₹29**.
    - Full books & handbooks: **₹99 – ₹199**.
    - Production capstone project bundles: **₹149 – ₹249**.
    - Free student account tier for dataset downloads, reading progress tracking, and bookmarking.
- **Decoupled Secondary Assets Vault (`https://github.com/Shubham496/mythos-assets`)**:
  - Connected separate GitHub repository `mythos-assets` at `external_assets/` to shield Render.io free-tier deployment from image and dataset bloat.
  - Added `external_assets/` to `.gitignore` in the core application repository.
  - Initialized standardized directory structure (`images/sql`, `images/python`, `images/bi`, `datasets/`, `downloads/viva`, `downloads/books`).
  - Standardized asset serving: jsDelivr CDN for notes imagery (`https://cdn.jsdelivr.net/gh/Shubham496/mythos-assets@main/...`) and GitHub Raw for direct dataset downloads.
- **Synchronized System Documentation (`docs/AGENT_GUIDE.md`)**:
  - Updated Section 2 to define the dual pricing architecture.
  - Updated Section 4 Codebase File Map with `external_assets/`, `app/content/`, `app/apps/library/`, and `app/templates/library/`.
  - Added Section 12 detailing the Resource Library architecture, 3-column technical docs reader UI, and activity logging specification.
- **Automated Verification**:
  - Full test suite verified: 15/15 tests passing cleanly with zero failures.

---

## [2026-11-15] (Transition to Multi-Course Online Educational Institute & Complete Removal of Payment Mentions)

### Added, Updated & Refactored
- **Full Transformation to MYTHOS Online Institute**:
  - Re-architected platform identity from a single-subject data analytics site into a **comprehensive 100% online educational institute** offering structured cohort programs across multiple disciplines.
  - Multi-faculty positioning introduced: **Digital Marketing & Growth** and **Data Analysis & Business Intelligence**.
- **Expansion to Multiple Live Cohort Programs (3 Launch Tracks)**:
  1. **Performance Marketing & Paid Advertising (Digital Marketing Track 1)**:
     - 6 comprehensive modules: Meta Ads Manager architecture, Google Search & Performance Max campaigns, Conversion Tracking & GA4, High-converting Landing Pages & CRO, Budget Scaling & ROAS frameworks, Live Multi-Platform Capstone.
     - Tools: Meta Ads Manager, Google Ads, GA4, GTM, Looker Studio, Triple Whale.
  2. **SEO, Content Strategy & Social Media Growth (Digital Marketing Track 2)**:
     - 6 comprehensive modules: Technical SEO & Website Audits, Keyword Research & Search Intent Architecture, High-Converting Content Funnels, LinkedIn B2B Personal Branding, Multi-Channel Email & CRM Automation, Live 0-to-50K Organic Traffic Capstone.
     - Tools: Semrush, Ahrefs, Screaming Frog, Google Search Console, HubSpot, LinkedIn Sales Navigator.
  3. **Data Analysis & Business Intelligence Masterclass (Data Analysis Track 3)**:
     - 6 comprehensive modules: Advanced Excel & Financial Modeling, SQL Relational Database Mastery, Power BI Executive Dashboards & DAX, Python for Data Extraction & ETL, Tableau Storytelling & Spatial Analytics, Full-Stack BI Capstone & Career Strategy.
     - Tools: Python, SQL, Power BI, Advanced Excel, Tableau.
- **Complete Removal of Defensive Payment / Fee Mentions**:
  - Completely purged defensive disclaimers and awkward mentions stating "payments will not be shown online", "Zero-Fee Public Policy: No prices or payments are taken online", "Submitting this form does not charge any fees", and "Zero fees on this portal" across:
    - `app/templates/sections/mentor.html` (Replaced with Academic Admissions Desk callouts).
    - `app/templates/sections/modals.html` (Replaced with admissions review message).
    - `app/templates/register.html` (Replaced with Admissions Verification card).
    - `app/templates/confirmation.html` (Clean online cohort confirmation).
    - `app/apps/courses/generate_syllabus_pdf.py` (Purged from generated syllabus PDF and regenerated PDF).
    - `docs/AGENT_GUIDE.md` and codebase docstrings.
- **Dynamic Course Track Selection Across Forms & Modals**:
  - Updated `/register`, enrollment modal (`#modal-enroll`), and inquiry modal (`#modal-enquiry`) with course selection dropdowns allowing applicants to choose their target track.
  - Added `openModalWithCourse(which, courseName)` in `app/static/js/main.js` for instant preselection from course cards.
  - Updated backend schemas (`EnquiryCreate`, `BatchRegistrationCreate`) and router endpoints (`/api/courses/register`, `/api/courses/enquiry`) to capture `course_name` and `course_interest` and dynamically map them to the proper batch.
- **Interactive Multi-Course Syllabus Interface**:
  - Added responsive course tabs in `app/templates/sections/syllabus.html` enabling instant switching between Digital Marketing and Data Analytics tracks.
  - Retained paired desktop drawer accordion expansion (modules [1, 2], [3, 4], [5, 6] expand together on viewports >= 768px).
- **Automated Verification**:
  - All 15 automated pytest tests passing cleanly (100%).

---

## [2026-11-12] (High-Definition Design Assets & Brand Master Overhaul)

### Added, Updated & Enhanced
- **High-Resolution Master Brand Assets (`design/assets/` & `app/static/Images/mythos/`)**:
  - **3D Hero Art & Podium Replacement**:
    - Replaced low-res pixelated 345x185 (`hero_art.jpg`) and 380x205 (`hero_podium.jpg`) with studio-grade 1376x768 3D renders featuring the illuminated circular neon podium, continuous gradient 'M' ribbon sculpture, glowing wireframe globe, and floating digital pixel voxels.
  - **Zero-Halo Transparent Brand Icon (`mythos_icon_transparent.png`)**:
    - Eliminated dirty boundary alpha fringing; re-rendered crisp 1024x1024 master and 2048x2048 (`mythos_icon_2048.png`) unmultiplied transparent icons with anti-aliased edges that render cleanly on both light surfaces and deep dark navy (`#070B14`).
  - **Master Full Brand Lockup (`mythos_full_logo.jpg` & `mythos_full_transparent.png`)**:
    - Upgraded full corporate brand lockup to 1376x768 master resolution featuring the 3D 'M' emblem, geometric Poppins 'MYTHOS' wordmark with split cyan/orange 'O', vibrant tagline, and 5 technology capability pillars (CODE, BUILD, ANALYZE, INNOVATE, GROW).
  - **Dark-Mode Glowing Brand Lockup (`mythos_logo_dark.jpg`)**:
    - Added 1376x768 executive dark navy (`#070B14`) presentation asset with luminous neon glow highlights for dark themes and marketing collateral.
  - **Scalable Vector Emblem (`mythos_emblem.svg`)**:
    - Engineered precision vector SVG representation of the official Mythos 'M' ribbon with `< / >` code symbol and floating digital voxel cubes for infinite-resolution vector scalability.
- **Certificate Generator Deprecation & Quality Polish**:
  - Updated `design/certificate_generator_template.py` to modern FPDF2 positioning (`new_x`, `new_y`) eliminating deprecation warnings.
  - Embedded high-res Mythos brand emblem directly into official certificate generation.
- **Design Guidelines Documentation**:
  - Expanded `design/GUIDELINES.md` with complete asset resolution tables, color token mapping, and geometry construction guidelines.
- **Automated Verification**:
  - All 15 automated pytest tests passing cleanly (100%).

---

## [2026-11-12] (Production Push Authority, Brand Anonymization, Paired Syllabus, Design System & Styled Brochure)

### Added, Updated & Hardened
- **Agent Guide Git Maintenance & Strict Push Authority (Task 1)**:
  - Updated `docs/AGENT_GUIDE.md` (Rule 6 in Section 2 and Section 10): Git repository hygiene is strictly maintained on every single task with automated test verification and atomic local commits.
  - **Strict Production Push Restriction**: Codified immutable policy that **ONLY the platform owner ("I") can push things to production** (`git push origin main` or deploy). AI agents and automated scripts are strictly prohibited from pushing to production.
- **Brand Anonymization & Contact Update (Task 2)**:
  - Removed all personal identity, instructor photos, personal biography, and past employment history from the website, hero section, mentor section, footer, and documentation.
  - Replaced the hero photo card with a high-tech **Mythos Data Systems Pipeline Showcase Card** with animated status pills, live execution stage tags, and 5-pillar highlights.
  - Redesigned `#about` into the **Direct Admissions & Mentorship Desk** highlighting WhatsApp (`8727864157`) and Email (`shubhamsinghh057@gmail.com`).
  - Updated official contact email across all files, templates, services, and footer to `shubhamsinghh057@gmail.com`.
  - Updated `app/core/base_config.py` and `app/apps/courses/services.py` with generic platform mentorship metadata.
- **Laptop Paired Syllabus Expansion (Task 3)**:
  - Updated `toggleSyllabus(index)` in `app/templates/sections/syllabus.html`:
    - On laptops/desktops (`window.matchMedia('(min-width: 768px)').matches`), modules expand in pairs: **[1, 2]**, **[3, 4]**, or **[5, 6]**.
    - If either module in the pair is clicked, both modules expand/collapse in unison with matching button labels ("Show More Details" / "Show Less Details") and synchronized chevron rotations.
    - On mobile / handheld screens (`< 768px`), modules continue expanding individually for optimal mobile scroll ergonomics.
- **Design System & Certificate Guidelines Folder (`design/`) (Task 4)**:
  - Created root-level design repository `design/`:
    - `design/GUIDELINES.md`: Comprehensive brand manual detailing Poppins typography hierarchy, exact Mythos color tokens (Deep Navy, Electric Blue, Cyan, Violet, Split Orange, Emerald), vector logo rules, and formal A4 landscape graduation certificate specifications.
    - `design/tokens.json`: Machine-readable design tokens for programmatic consumption.
    - `design/assets/`: Scalable SVG vectors (`mythos_icon.svg`, `mythos_logo.svg`) and transparent PNG logos (`mythos_icon_transparent.png`, `mythos_full_transparent.png`).
    - `design/certificate_generator_template.py`: Working Python automation template generating official student completion certificates using `fpdf2` and design tokens.
- **Styled 2-Page Downloadable Syllabus Brochure (Task 5)**:
  - Rebuilt `app/apps/courses/generate_syllabus_pdf.py` using `fpdf2`:
    - Executive Mythos navy header banner with split Electric Blue / Vivid Orange accent bar.
    - Fixed weekend schedule grid (Saturday & Sunday, 6:00 – 8:00 PM IST, 8–10 weeks hands-on).
    - Color-coded module cards for all 6 pillars (Excel, SQL, Python, Power BI, Tableau, Career Prep) with Core Competencies and Deep-Dive Labs.
    - 3 Production Capstone project showcases (Adidas Retail, Data Warehouse, Event Analytics Hub).
    - Admissions & Counseling Desk strip with `shubhamsinghh057@gmail.com` and `+91 8727864157`.
    - Exactly 2 print-ready publication-grade pages saved to `app/static/pdf/Data_Analysis_Syllabus.pdf`.
  - Updated inline HTML printable brochure in `app/apps/courses/services.py`.
- **Automated Verification**:
  - Full pytest test suite passing with 15/15 tests (100%).

---

## [2026-11-12] (Frontend Architecture Modularization & Environment Template)

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
