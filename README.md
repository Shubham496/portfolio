# MYTHOS Online Institute — Educational Institute Platform

A modern, high-performance web platform built with **FastAPI** powering **MYTHOS Online Institute**, an online educational institute delivering intensive live cohorts across **Digital Marketing** and **Data Analytics**.

---

## 📌 Quick Navigation & Documentation

- 📖 **[Documentation README](docs/README.md)**: Secondary in-depth site guide covering student workflows, architecture, and deployment.
- 👤 **[User & Instructor Guide](docs/USER_GUIDE.md)**: Simple guide explaining how to run locally, manage student leads, export CSVs, and configure cloud databases.
- 🤖 **[Comprehensive Agent Guide](docs/AGENT_GUIDE.md)**: Exhaustive technical specification and single-source-of-truth reference for AI coding agents.
- 📋 **[Changelog & Updates Log](CHANGELOG.md)**: Audit trail of all implementations, fixes, and GitHub-style release logs.

---

## 🚀 Current Platform Features & Live Programs

### 1. Multi-Course Academic Curriculum
MYTHOS operates as a 100% live online cohort institute offering structured programs across two high-demand faculties:
* **Digital Marketing Track 1**: *Performance Marketing & Paid Advertising* (Meta Ads, Google Ads, GA4, Funnel Optimization, ROAS Scaling).
* **Digital Marketing Track 2**: *SEO, Content Strategy & Social Media Growth* (Technical SEO, Semrush, Content Marketing Frameworks, LinkedIn Growth, Multi-channel Automation).
* **Data Analysis Track 3**: *Data Analysis & Business Intelligence Masterclass* (Python, SQL, Power BI, Advanced Excel, Tableau).
* **Weekend Cohort Schedule**: Saturday & Sunday, 6:00 PM – 8:00 PM IST (4 hours/weekend, 8–10 weeks hands-on live cohorts).
* **Zero Public Pricing**: Pure educational admissions model where enrollment readiness and tracks are reviewed during orientation without online checkout or payment gateways.

### 2. Student Conversion & Admission Funnel
* **Dedicated Batch Registration**: [`/register`](http://localhost:8000/register) — Clean, full-page application form with course selection and optional email (only Name and WhatsApp/Phone are mandatory).
* **Registration Success Confirmation**: [`/registration-success`](http://localhost:8000/registration-success) — Confirms application receipt and informs applicants that admissions will verify their orientation schedule.
* **Homepage Interactive Modals**: Asynchronous pop-up forms for **Enroll in Batch** (`/#enroll`) and **Ask a Question** (`/#enquiry`) with course track selector and instant toast alerts.
* **Syllabus PDF Delivery**:
  * Direct brochure download: [`/course/syllabus/download`](http://localhost:8000/course/syllabus/download)
  * Inline browser PDF preview: [`/course/syllabus`](http://localhost:8000/course/syllabus)
  * Printable syllabus brochure generated dynamically with `fpdf2`.

### 3. Protected Academic Admin Portal (`/admin`)
* **Secret Login**: [`/admin/login`](http://localhost:8000/admin/login)
  * Pre-configured administrative user (`admin` / `admin@mythostech.in`) with modern bcrypt password verification.
  * Public registration disabled (`/admin/signup` redirects to login).
  * Signed HTTP-only session cookies with 7-day expiration (`URLSafeTimedSerializer`).
* **Live Dashboard & Lead Pipeline**: [`/admin/dashboard`](http://localhost:8000/admin/dashboard)
  * **Interactive Pagination**: Seamless page navigation with configurable items per page (10, 25, 50).
  * **Separated Status & Date Columns**: Clear timestamp/date records and status badge dropdowns.
  * **Real-time Pipeline Filtering**: Filter by lead type (*Registrations* vs *Enquiries*), pipeline status (*New*, *Contacted*, *Enrolled*, *Closed*), or search by student details.
  * **One-Click CSV Export**: Download all leads anytime via [`/api/courses/leads/export.csv`](http://localhost:8000/api/courses/leads/export.csv).
  * **Direct WhatsApp Integration**: Click-to-chat links for instantaneous student follow-up.

### 4. Supporting Micro-Apps
* **Project Task & Sprint Tracker**: [`/apps/todos`](http://localhost:8000/apps/todos) — Built-in Kanban/task management interface.
* **Health Check & Cloud Probes**: [`/health`](http://localhost:8000/health) — Zero-dependency JSON status check for cloud hosts.

---

## 🛠️ Architecture & Tech Stack

* **Backend**: FastAPI 0.110+ on Python 3.10+ with Uvicorn ASGI server (~40–60 MB RAM baseline).
* **Database Architecture**:
  * **Local Development**: SQLite (`course_platform.db`) with zero external service requirements.
  * **Production (Render.io)**: External PostgreSQL via `DATABASE_URL` (Neon.tech / Supabase / Render Postgres) with connection pooling (`pool_pre_ping=True`, `pool_recycle=300`).
* **Environment Configuration**: `python-dotenv` autoloads `.env` for `ADMIN_PASSWORD`, `SECRET_KEY`, and `DATABASE_URL`.
* **Templating & UI**: Jinja2 templates, Tailwind CSS (via CDN), Lucide Icons, Devicons, and custom animations.
* **PDF Engine**: `fpdf2` automated PDF brochure builder.

---

## 💻 Quickstart (Running Locally)

### 1. Prerequisites
Ensure Python 3.10+ is installed on your machine.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Development Server
```bash
uvicorn app.main:app --reload --port 8000
```
Navigate to [http://localhost:8000](http://localhost:8000) in your browser.

### 4. Run the Automated Test Suite
```bash
python -m pytest -v
```
All tests should pass cleanly.
