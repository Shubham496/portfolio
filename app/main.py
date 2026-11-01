from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from app.core.config import settings
import os

# Initialize application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="High-performance lightweight portfolio and multi-app engine.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Detailed skills extracted from Shubham's Resume
SKILLS_DATA = [
    {
        "category": "Languages & Core",
        "icon": "code-2",
        "skills_list": ["Python (NumPy, Pandas)", "SQL (Advanced)", "Bash", "RESTful APIs", "FastAPI", "Django"]
    },
    {
        "category": "Data Engineering & DBs",
        "icon": "database",
        "skills_list": ["PostgreSQL", "MS SQL Server", "MySQL", "Snowflake", "ETL Pipelines", "Data Warehousing"]
    },
    {
        "category": "BI & Analytics Tools",
        "icon": "bar-chart-3",
        "skills_list": ["Power BI (DAX, Modeling)", "Tableau", "Retool", "Excel Modeling", "KPI Frameworks"]
    },
    {
        "category": "Workflow & Orchestration",
        "icon": "cpu",
        "skills_list": ["n8n Workflow Automation", "Data Cleansing", "Git / GitHub", "Docker", "Process Automation"]
    }
]

# Experience history with the latest role amplified as requested
EXPERIENCE_DATA = [
    {
        "role": "Lead Python & Data Architecture Consultant",
        "company": "Ducat",
        "period": "August 2025 – Present",
        "type": "Consulting & Engineering",
        "highlight": "Elevated Current Role",
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
        "highlight": "Fintech / Lending",
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
        "highlight": "BI & Pipelines",
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
        "highlight": "Applications & Warehousing",
        "points": [
            "Built internal operations dashboards and inventory tracking applications using Python and Django.",
            "Designed and implemented RESTful APIs integrating backend database operations with front-facing operational portals.",
            "Constructed centralized MySQL data warehouse consolidating disparate ticketing, retail sales, and visitor engagement streams."
        ]
    }
]

# Featured Projects & Interactive Apps
MINI_APPS_DATA = [
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
        "title": "URL Shortener & Analytics Micro-App",
        "tag": "FastAPI Sub-App",
        "description": "High-speed URL routing engine with custom aliases, click attribution tracking, and SQLite persistence running on this portfolio.",
        "status": "In Development",
        "tech": ["FastAPI", "SQLite", "Tailwind", "REST API"],
        "url": "/apps/url-shortener",
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
            "skills": SKILLS_DATA,
            "experiences": EXPERIENCE_DATA,
            "mini_apps": MINI_APPS_DATA,
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
