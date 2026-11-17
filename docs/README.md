# Documentation Hub & Platform Manual

Welcome to the central documentation index for **MYTHOS Online Institute**.

---

## 📚 Central Documentation System

| Document | Primary Audience | Purpose |
| :--- | :--- | :--- |
| **[`../GUIDE.md`](file:///f:/Projects/coding/GUIDE.md)** | Developers & AI Agents | **Single-source-of-truth manual** describing current system state, tech stack, APIs, and business rules. |
| **[`../Changeslog.md`](file:///f:/Projects/coding/Changeslog.md)** | Developers & AI Agents | **Recent development history** containing strictly the latest 15 meaningful entries. |
| **[`../CHANGELOG_ARCHIVE.md`](file:///f:/Projects/coding/CHANGELOG_ARCHIVE.md)** | Developers & Maintainers | **Historical changelog archive** organized chronologically by Year and Month. |
| **[`../AGENTS.md`](file:///f:/Projects/coding/AGENTS.md)** | AI Coding Assistants | **The 15 Golden Rules & operational directives** for AI agents working in this repository. |
| **[`architecture.md`](file:///f:/Projects/coding/docs/architecture.md)** | Architects & Engineers | Modular sub-app layout (`courses`, `library`, `todos`), request lifecycle, and UI component decomposition. |
| **[`database.md`](file:///f:/Projects/coding/docs/database.md)** | Engineers & DBA | Dual-engine strategy (SQLite local / PostgreSQL cloud), connection pooling, ER model, and schemas. |
| **[`deployment.md`](file:///f:/Projects/coding/docs/deployment.md)** | DevOps & Maintainers | Render.io deployment pipeline, build/start commands, environment variables, health checks, and rollback. |
| **[`USER_GUIDE.md`](file:///f:/Projects/coding/docs/USER_GUIDE.md)** | Platform Owner (Shubham) | Plain-English non-technical guide explaining how to run locally, manage student leads, and export CSVs. |
| **[`task_new.md`](file:///f:/Projects/coding/docs/task_new.md)** | Product & Engineering | Architectural roadmap and task tracker for the Knowledge & Resource Engine. |
| **[`../README.md`](file:///f:/Projects/coding/README.md)** | Public & Developers | Top-level repository overview and quickstart instructions. |

---

## 🌐 Current Site Features & User Journey

### 1. Prospective Student Journey
1. **Homepage Engagement (`/`)**:
   - High-impact hero section presenting Mythos Data Systems & Learning Engine.
   - Verified credentials showcase: 3+ years enterprise consulting, 550+ students & developers trained.
   - Visual display of the **5 Data Analysis Pillars**: Python, SQL, Power BI, Excel, Tableau.
   - Prominent weekend schedule badges: **Saturday & Sunday only, 6:00 PM – 8:00 PM IST**.
   - Immediate CTAs: **Apply for Batch** and **Direct Admissions Desk**.
2. **Syllabus PDF Access**:
   - Students can view the comprehensive PDF brochure in their browser (`/course/syllabus`) or download it directly (`/course/syllabus/download`).
3. **Application & Admission**:
   - Students can enroll via homepage modals or dedicated page (`/register`).
   - **Student-friendly form**: Email is optional; only Full Name and WhatsApp/Phone are required.
   - Upon submission, students are redirected to `/registration-success` reassuring them of a prompt orientation callback.

### 2. Instructor Administration Journey (`/admin`)
1. **Secret Sign In (`/admin/login`)**:
   - Clean, dark-mode-ready login form with zero public links on the website.
   - Pre-configured `admin` account with bcrypt password hashing.
   - Signed session cookie with 7-day validity.
2. **Protected Monitoring Dashboard (`/admin/dashboard`)**:
   - **4 KPI Metric Cards**: Total Leads, Batch Registrations, Course Inquiries, and Pending (New).
   - **7-Column Leads Table**: Type, Submitted Date, Student, Contact, Message, Status, Admin Notes & Action.
   - **Interactive Pagination**: Configurable items per page (10, 25, 50), page numbers, and persistent filters.
   - **One-Click CSV Export**: Download student database as a clean spreadsheet (`/api/courses/leads/export.csv`).

---

## ⚙️ Data & Infrastructure Architecture Summary

- **Dual-Engine SQLAlchemy**:
  - `sqlite:///./course_platform.db` for zero-setup local offline execution.
  - PostgreSQL via `DATABASE_URL` for persistent cloud deployments on Render.io (with connection pooling: `pool_pre_ping=True`, `pool_recycle=300`).
- **Security & Integrity**:
  - `.env` auto-loaded via `python-dotenv`.
  - Secret key sessions with `itsdangerous` signed tokens.
  - Registration disabled on admin routes to prevent unauthorized account creation.
  - Strict push authority: only the human platform owner may execute `git push` or deploy to production.
