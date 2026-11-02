from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from app.core.config import settings
from app.apps.todos.router import router as todos_router
import os

# Initialize application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="High-performance lightweight portfolio and multi-app engine.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Register Sub-Apps / Mini-Apps
app.include_router(todos_router)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Accurate skills with verified Devicons and exact official SVGs
SKILLS_CATEGORIES = [
    {
        "category": "Languages & Core",
        "skills": [
            {"name": "Python", "type": "devicon", "icon": "devicon-python-plain colored"},
            {"name": "SQL (Advanced)", "type": "devicon", "icon": "devicon-azuresqldatabase-plain colored"},
            {"name": "FastAPI", "type": "devicon", "icon": "devicon-fastapi-plain colored"},
            {"name": "Django", "type": "devicon", "icon": "devicon-django-plain colored"},
            {"name": "Pandas", "type": "devicon", "icon": "devicon-pandas-plain colored"},
            {"name": "NumPy", "type": "devicon", "icon": "devicon-numpy-plain colored"},
            {"name": "Bash", "type": "devicon", "icon": "devicon-bash-plain colored"},
        ]
    },
    {
        "category": "Databases & Storage",
        "skills": [
            {"name": "PostgreSQL", "type": "devicon", "icon": "devicon-postgresql-plain colored"},
            {"name": "MySQL", "type": "devicon", "icon": "devicon-mysql-plain colored"},
            {"name": "SQLite", "type": "devicon", "icon": "devicon-sqlite-plain colored"},
            {"name": "Snowflake", "type": "svg", "slug": "snowflake", "color": "#29B5E8"},
            {"name": "MS SQL Server", "type": "devicon", "icon": "devicon-microsoftsqlserver-plain colored"},
        ]
    },
    {
        "category": "BI & Analytics",
        "skills": [
            {"name": "Power BI", "type": "svg", "slug": "powerbi", "color": "#F2C811"},
            {"name": "Tableau", "type": "svg", "slug": "tableau", "color": "#E97627"},
            {"name": "Retool", "type": "devicon", "icon": "devicon-electron-original colored"},
            {"name": "Excel Modeling", "type": "devicon", "icon": "devicon-unifiedmodelinglanguage-plain colored"},
            {"name": "ETL Pipelines", "type": "devicon", "icon": "devicon-networkx-plain colored"},
        ]
    },
    {
        "category": "Workflow & Orchestration",
        "skills": [
            {"name": "Git", "type": "devicon", "icon": "devicon-git-plain colored"},
            {"name": "GitHub", "type": "devicon", "icon": "devicon-github-original"},
            {"name": "Docker", "type": "devicon", "icon": "devicon-docker-plain colored"},
            {"name": "n8n Automation", "type": "svg", "slug": "n8n", "color": "#EA4B71"},
            {"name": "Linux", "type": "devicon", "icon": "devicon-linux-plain colored"},
        ]
    }
]

# Experience history
EXPERIENCE_DATA = [
    {
        "role": "Lead Python & Data Architecture Consultant",
        "company": "Ducat",
        "period": "August 2025 – Present",
        "type": "Consulting & Engineering",
        "points": [
            "Architecting enterprise-scale Python data services, asynchronous processing engines, and high-throughput data extraction systems for enterprise clients.",
            "Spearheading end-to-end data pipeline redesigns, boosting processing throughput by 42% and eliminating manual reporting bottlenecks.",
            "Directing curriculum and mentoring 120+ senior developers and data engineers on modern Python architecture, distributed computing, and machine learning workflows.",
            "Consulting on cloud warehouse migration strategies (PostgreSQL/Snowflake) and instituting rigorous automated validation testing."
        ]
    },
    {
        "role": "Data Analyst & Automation Engineer",
        "company": "LNP Infotech",
        "period": "December 2025 – May 2026",
        "type": "Financial Systems & Compliance",
        "points": [
            "Processed and analyzed financial and operational transaction data for U.S.-based credit card and mortgage lending clients.",
            "Engineered automated n8n workflows for automated document verification, audits, and real-time compliance alerting.",
            "Designed relational schemas in PostgreSQL, optimizing complex multi-table queries for high-concurrency executive reporting.",
            "Developed responsive internal tools and dashboards with Retool, cutting resolution time for inter-departmental inquiries."
        ]
    },
    {
        "role": "Data Analyst & Technical Instructor",
        "company": "Netmax Technologies",
        "period": "December 2024 – November 2025",
        "type": "Analytics & Mentorship",
        "points": [
            "Processed enterprise datasets using Python, SQL, and Excel, producing actionable business insights and retention metrics.",
            "Engineered interactive Power BI & Tableau dashboards with automated refresh intervals for cross-functional stakeholders.",
            "Constructed automated ETL extraction scripts in Python to streamline cross-database synchronization."
        ]
    },
    {
        "role": "Software & Data Developer",
        "company": "JKM Amusements",
        "period": "July 2023 – December 2024",
        "type": "Full-Stack & Analytics",
        "points": [
            "Built internal operations dashboards and inventory tracking applications using Python and Django.",
            "Designed and implemented RESTful APIs integrating backend database operations with front-facing operational portals.",
            "Constructed centralized MySQL data warehouse consolidating disparate ticketing, retail sales, and visitor engagement streams."
        ]
    }
]

# Featured Enterprise Projects
ENTERPRISE_PROJECTS = [
    {
        "title": "Adidas Retail Intelligence Dashboard",
        "tag": "Business Intelligence",
        "description": "Comprehensive Power BI analytics platform tracking retail performance, inventory turnover velocity, and multi-region sales forecasts.",
        "status": "Production Project",
        "tech": ["Power BI", "DAX", "Data Modeling", "SQL"],
        "url": settings.GITHUB_URL,
        "github": settings.GITHUB_URL
    },
    {
        "title": "Automated Multi-Source Data Warehouse",
        "tag": "ETL & Architecture",
        "description": "Centralized warehousing architecture consolidating disparate sales, operations, and finance APIs into optimized relational analytical schemas.",
        "status": "Production Project",
        "tech": ["Python", "MySQL", "ETL Pipelines", "APIs"],
        "url": settings.GITHUB_URL,
        "github": settings.GITHUB_URL
    },
    {
        "title": "Event Analytics & Ticketing Hub",
        "tag": "BI & Demographics",
        "description": "Interactive event intelligence suite combining ticket sales velocity, attendee demographic segmentation, and ROI attribution.",
        "status": "Production Project",
        "tech": ["Power BI", "Data Cleansing", "Analytics"],
        "url": settings.GITHUB_URL,
        "github": settings.GITHUB_URL
    }
]

# Education & Certifications
EDUCATION_DATA = {
    "degree": "Bachelor of Technology (B.Tech)",
    "major": "Electronics & Communication Engineering",
    "institution": "Rustamji Institute of Technology",
    "period": "2019 – 2023",
    "certifications": [
        {"name": "Power BI Masterclass", "issuer": "Udemy", "year": "2024"},
        {"name": "Full Stack Django Development", "issuer": "Coursera", "year": "2023"},
        {"name": "Python for Data Science & Engineering", "issuer": "Coursera", "year": "2022"}
    ]
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the primary portfolio homepage."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "settings": settings,
            "title": "Home",
            "skill_categories": SKILLS_CATEGORIES,
            "experiences": EXPERIENCE_DATA,
            "enterprise_projects": ENTERPRISE_PROJECTS,
            "education": EDUCATION_DATA,
        }
    )

@app.get("/resume", response_class=FileResponse)
async def download_resume():
    """Serve the latest resume PDF for viewing/downloading."""
    resume_file = "app/static/pdf/resume.pdf"
    if os.path.exists(resume_file):
        return FileResponse(
            path=resume_file,
            filename="Shubham_Singh_Resume.pdf",
            media_type="application/pdf"
        )
    return HTMLResponse("Resume file not found", status_code=404)

@app.get("/health", tags=["System"])
async def health_check():
    """Lightweight health check endpoint for cloud hosting probes."""
    return {
        "status": "healthy",
        "owner": settings.OWNER_NAME,
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "memory_friendly": True
    }
