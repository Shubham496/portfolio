# Data Analysis Training & Admission Platform

A high-performance, modular web application built with **FastAPI**. It showcases instructor background and credentials, and provides an end-to-end student admission engine for weekend Data Analysis batches (Python, SQL, Power BI, Excel, Tableau).

---

## Quick Navigation & Guides

- 🤖 **[Agent Technical Guide](docs/AGENT_GUIDE.md)**: Comprehensive technical specs, data schemas, business rules, Render.io database setup, and API specifications for AI coding assistants.
- 👤 **[User & Beginner Guide](docs/USER_GUIDE.md)**: Simple, non-complex guide for Shubham explaining how the system works, how to run locally, how to connect Render to free cloud PostgreSQL, and how to export student leads to CSV.

---

## Architecture Overview

- **Core Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+) with Uvicorn ASGI server (~40–60 MB RAM baseline)
- **Templating & UI**: Jinja2 templates + Tailwind CSS (via CDN) + Lucide Icons
- **Database Architecture**: SQLite locally (`portfolio.db`) with zero external service requirements; ready for Turso / Neon serverless DB for persistent free-tier cloud deployments
- **Application Structure**: Modular routers (`app/apps/<mini_app_name>/`) mounted dynamically onto the main application
- **Production / CI/CD**: Cloud-agnostic (Render, Fly.io, Railway, Koyeb) with automatic GitHub Actions / Git Push deployments and custom domain support

---

## Directory Structure

```text
coding/
│
├── app/
│   ├── main.py                     # Primary FastAPI application entrypoint & routing
│   ├── core/
│   │   ├── config.py               # Application settings and environment variables
│   │   └── database.py             # SQLite / Database engine connection helper
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css           # Custom styles & animations
│   │   ├── js/
│   │   │   └── main.js             # Client interactivity scripts
│   │   └── images/                 # Favicons, project screenshots, avatar
│   ├── templates/
│   │   ├── base.html               # Shared layout (Navbar, Footer, SEO meta tags)
│   │   ├── index.html              # Portfolio landing page (Bio, Skills, Projects, Contact)
│   │   └── partials/
│   │       ├── navbar.html         # Header navigation
│   │       └── footer.html         # Footer with links & status badge
│   └── apps/                       # Sub-applications directory
│       └── __init__.py
│
├── docs/                           # Planning, tracking, and architecture documentation
│   ├── Project_Action_Plan_and_Tracker.docx  # Word document for tasks & roadmap
│   └── ARCHITECTURE.md             # Detailed engineering specifications
│
├── tests/
│   └── test_main.py                # Health check and basic route testing
│
├── .gitignore                      # Git exclusion rules
├── requirements.txt                # Production Python dependencies
├── requirements-dev.txt            # Development / Linting / Testing dependencies
├── Dockerfile                      # Container definition for portable deployment
└── README.md                       # Project documentation (this file)
```

---

## Quickstart

### 1. Clone & Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Locally

```bash
uvicorn app.main:app --reload --port 8000
```

Open your browser at:
- **Portfolio Homepage**: [http://localhost:8000](http://localhost:8000)
- **Interactive API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative Docs (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Adding a New Mini-App

Every mini-app follows an isolated module pattern under `app/apps/<app_name>/`:
1. Create `app/apps/<app_name>/router.py` with an `APIRouter(prefix="/apps/<app_name>", tags=["<app_name>"])`.
2. Include templates inside `app/apps/<app_name>/templates/` or route directly to views.
3. Register the router in `app/main.py`:
   ```python
   from app.apps.<app_name>.router import router as app_router
   app.include_router(app_router)
   ```
4. Add the app entry in `app/main.py`'s project catalog so it automatically renders onto the homepage.

---

## Project Tracker & Action Plan

A full project tracker, task list, and milestone roadmap is maintained in:
- `docs/Project_Action_Plan_and_Tracker.docx`
- `docs/ARCHITECTURE.md`
