# Documentation Hub & Platform Manual

Welcome to the central documentation index for the **Data Analysis Training & Student Admission Platform**.

---

## 📚 Documentation Index

| Document | Primary Audience | Purpose |
| :--- | :--- | :--- |
| **[Repository README](../README.md)** | Developers & Public | Top-level project overview, quickstart, and tech stack. |
| **[Documentation README](README.md)** *(This file)* | Developers & Reviewers | Detailed overview of current site capabilities, user journeys, and feature modules. |
| **[User & Instructor Guide](USER_GUIDE.md)** | Shubham (Site Owner) | Plain-English non-technical guide explaining how to run the site, use the admin portal, and handle leads. |
| **[Comprehensive Agent Guide](AGENT_GUIDE.md)** | AI Coding Assistants | Deep, exhaustive technical specification with data models, credentials, schemas, and guardrails. |
| **[Platform Changelog](../CHANGELOG.md)** | All | Reverse-chronological GitHub-style log of all completed implementations, fixes, and updates. |

---

## 🌐 Current Site Features & User Journey

### 1. Prospective Student Journey
1. **Homepage Engagement (`/`)**:
   - High-impact hero section presenting **Shubham Singh** as a seasoned Lead Python & Data Architecture Consultant.
   - Verified credentials showcase: 3+ years experience across Ducat, Netmax, and LNP Infotech; 120+ senior developers mentored.
   - Visual display of the **5 Data Analysis Pillars**: Python, SQL, Power BI, Excel, Tableau.
   - Prominent weekend schedule badges: **Saturday & Sunday only, 6:00 PM – 8:00 PM IST**.
   - Immediate CTAs: **Enroll in Batch** and **Ask a Question / Counseling**.
2. **Syllabus PDF Access**:
   - Students can view the comprehensive PDF brochure in their browser (`/course/syllabus`) or download it directly (`/course/syllabus/download`).
3. **Application & Admission**:
   - Students can enroll via the homepage modal (`/#enroll`) or the dedicated landing page (`/register`).
   - **Student-friendly form**: Email is optional; only Full Name and WhatsApp/Phone are required.
   - Upon submission, students are redirected to `/registration-success` which reassures them of a prompt callback.

### 2. Instructor Administration Journey (`/admin`)
1. **Secret Sign In (`/admin/login`)**:
   - Clean, dark-mode-ready login form with zero public links.
   - Pre-configured `admin` account with bcrypt password hashing.
   - Signed session cookie with 7-day validity.
2. **Protected Monitoring Dashboard (`/admin/dashboard`)**:
   - **4 KPI Metric Cards**: Total Leads, Batch Registrations, Course Inquiries, and Pending (New).
   - **Lead Table with Separated Columns**:
     - *Type*: Registration vs Enquiry visual tags.
     - *Submitted Date*: Clear calendar date and clock timestamp in IST.
     - *Student Info*: Full Name and career status.
     - *Contact*: Direct one-click WhatsApp chat link and email address.
     - *Goals / Message*: Student goals and prior tool experience.
     - *Status*: Colored status pill (`New`, `Contacted`, `Enrolled`, `Closed`) with quick inline change selector.
     - *Admin Notes*: In-place counseling notes input with one-click save.
   - **Interactive Pagination**:
     - Configurable items per page (10, 25, 50).
     - Page selector bar (`Prev`, page numbers `1, 2, 3...`, `Next`).
     - Persistent search terms and filters across page transitions.
   - **One-Click CSV Export**:
     - Download full student database as a clean spreadsheet (`/api/courses/leads/export.csv`) for Excel or Google Sheets.

---

## ⚙️ Data Architecture

- **Dual-Engine SQLAlchemy**:
  - `sqlite:///./course_platform.db` for zero-setup local offline execution.
  - PostgreSQL via `DATABASE_URL` for persistent cloud deployments on Render.io (works with Neon.tech, Supabase, or Render Postgres).
- **Security & Integrity**:
  - `.env` auto-loaded via `python-dotenv`.
  - Secret key sessions with itsdangerous signed tokens.
  - Registration disabled on admin routes to prevent unauthorized account creation.
