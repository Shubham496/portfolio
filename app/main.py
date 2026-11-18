from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse
from fastapi.middleware.gzip import GZipMiddleware
from app.core.config import settings
from app.apps.todos.router import router as todos_router
from app.apps.courses.router import router as courses_router
from app.apps.courses.admin_router import router as admin_router
from app.apps.courses.student_router import router as student_router
from app.apps.library.router import router as library_router
from app.apps.courses.services import (
    get_instructor_curriculum_profile,
    generate_syllabus_html_brochure,
    list_batches,
    get_grouped_batches
)
from app.apps.courses.database import SessionLocal
from app.apps.library.services import SUBJECTS, list_documents_for_subject, list_practice_datasets
import os
import datetime

# Initialize application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="High-performance lightweight portfolio and multi-app engine.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable GZip middleware for optimal static and dynamic compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Register Sub-Apps / Mini-Apps
app.include_router(todos_router)
app.include_router(courses_router)
app.include_router(admin_router)
app.include_router(student_router)
app.include_router(library_router)


class CachedStaticFiles(StaticFiles):
    """Static file handler adding 1-year aggressive cache-control headers."""
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 200:
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        return response


# Mount static files with cache headers
app.mount("/static", CachedStaticFiles(directory="app/static"), name="static")

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
    """Render the primary educational institute homepage."""
    with SessionLocal() as db:
        active_batches = list_batches(db)
        grouped_batches = get_grouped_batches(db)
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
            "course_profile": get_instructor_curriculum_profile(),
            "batches": active_batches,
            "grouped_batches": grouped_batches,
        }
    )

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Dedicated registration page for prospective students."""
    with SessionLocal() as db:
        active_batches = list_batches(db)
        grouped_batches = get_grouped_batches(db)
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "settings": settings,
            "title": "Register for Weekend Batch",
            "course_profile": get_instructor_curriculum_profile(),
            "batches": active_batches,
            "grouped_batches": grouped_batches,
        }
    )

@app.get("/registration-success", response_class=HTMLResponse)
async def registration_success_page(request: Request):
    """Confirmation page informing student that we received registration and will contact them."""
    return templates.TemplateResponse(
        request=request,
        name="confirmation.html",
        context={
            "settings": settings,
            "title": "Registration Confirmed",
            "course_profile": get_instructor_curriculum_profile(),
        }
    )

@app.get("/privacy", response_class=HTMLResponse)
async def privacy_policy_page(request: Request):
    """Privacy Policy page explaining student data protection and communication standards."""
    return templates.TemplateResponse(
        request=request,
        name="legal/privacy.html",
        context={
            "settings": settings,
            "title": "Privacy Policy",
        }
    )

@app.get("/terms", response_class=HTMLResponse)
async def terms_of_service_page(request: Request):
    """Terms of Service covering educational use, academic integrity, and platform policies."""
    return templates.TemplateResponse(
        request=request,
        name="legal/terms.html",
        context={
            "settings": settings,
            "title": "Terms of Service",
        }
    )

@app.get("/refund-policy", response_class=HTMLResponse)
async def refund_policy_page(request: Request):
    """Refund & Rescheduling Policy detailing demo sessions and cohort transfer terms."""
    return templates.TemplateResponse(
        request=request,
        name="legal/refund_policy.html",
        context={
            "settings": settings,
            "title": "Refund & Rescheduling Policy",
        }
    )

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """Dedicated About page detailing institute history, faculty separation, and academic standards."""
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={
            "settings": settings,
            "title": "About MYTHOS Online Institute — Faculty, Mission & Architecture",
        }
    )

@app.get("/demo", response_class=HTMLResponse)
async def demo_page(request: Request):
    """Dedicated Free Live Demo Class reservation page."""
    with SessionLocal() as db:
        active_batches = list_batches(db)
        grouped_batches = get_grouped_batches(db)
    return templates.TemplateResponse(
        request=request,
        name="demo.html",
        context={
            "settings": settings,
            "title": "Free Live Weekend Demo Class | MYTHOS",
            "batches": active_batches,
            "grouped_batches": grouped_batches,
        }
    )

@app.get("/sitemap.xml", response_class=Response)
async def sitemap_xml():
    """Dynamic XML sitemap listing home, /about, /demo, active subject hubs, and published notes."""
    base_url = settings.BASE_URL.rstrip("/")
    today = datetime.date.today().isoformat()

    urls = [
        {"loc": f"{base_url}/", "changefreq": "daily", "priority": "1.0", "lastmod": today},
        {"loc": f"{base_url}/about", "changefreq": "monthly", "priority": "0.8", "lastmod": today},
        {"loc": f"{base_url}/demo", "changefreq": "weekly", "priority": "0.9", "lastmod": today},
        {"loc": f"{base_url}/register", "changefreq": "weekly", "priority": "0.9", "lastmod": today},
        {"loc": f"{base_url}/library", "changefreq": "daily", "priority": "0.9", "lastmod": today},
        {"loc": f"{base_url}/library/datasets", "changefreq": "weekly", "priority": "0.8", "lastmod": today},
        {"loc": f"{base_url}/privacy", "changefreq": "yearly", "priority": "0.3", "lastmod": today},
        {"loc": f"{base_url}/terms", "changefreq": "yearly", "priority": "0.3", "lastmod": today},
        {"loc": f"{base_url}/refund-policy", "changefreq": "yearly", "priority": "0.3", "lastmod": today},
    ]

    # Practice datasets
    for ds in list_practice_datasets():
        urls.append({
            "loc": f"{base_url}/library/datasets/{ds['slug']}",
            "changefreq": "monthly",
            "priority": "0.7",
            "lastmod": today,
        })

    # Active subject hubs
    for subj_slug in SUBJECTS:
        urls.append({
            "loc": f"{base_url}/library/{subj_slug}",
            "changefreq": "weekly",
            "priority": "0.8",
            "lastmod": today,
        })

        # Published technical notes only (drafts are excluded)
        published_docs = list_documents_for_subject(subj_slug, published_only=True)
        for doc in published_docs:
            lastmod = doc.last_updated if (doc.last_updated and len(doc.last_updated) == 10 and doc.last_updated[4] == '-') else today
            urls.append({
                "loc": f"{base_url}/library/{subj_slug}/notes/{doc.slug}",
                "changefreq": "monthly",
                "priority": "0.7",
                "lastmod": lastmod,
            })

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for u in urls:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{u['loc']}</loc>")
        xml_lines.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        xml_lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        xml_lines.append(f"    <priority>{u['priority']}</priority>")
        xml_lines.append("  </url>")
    xml_lines.append("</urlset>")

    xml_content = "\n".join(xml_lines)
    return Response(content=xml_content, media_type="application/xml")

@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt():
    """Robots.txt disallowing private administrative and API routes and directing to sitemap.xml."""
    base_url = settings.BASE_URL.rstrip("/")
    content = f"""User-agent: *
Disallow: /admin/
Disallow: /api/
Disallow: /student/

Sitemap: {base_url}/sitemap.xml
"""
    return PlainTextResponse(content=content)

@app.get("/course/syllabus/download", response_class=FileResponse)
async def download_full_course_syllabus():
    """Download complete Data Analysis syllabus PDF brochure."""
    pdf_path = "app/static/pdf/Data_Analysis_Syllabus.pdf"
    if os.path.exists(pdf_path):
        return FileResponse(
            path=pdf_path,
            filename="Data_Analysis_Full_Course_Syllabus.pdf",
            media_type="application/pdf",
        )
    return HTMLResponse("Syllabus PDF file not found", status_code=404)

@app.get("/course/syllabus", response_class=FileResponse)
async def view_course_syllabus():
    """View Data Analysis syllabus PDF directly in browser."""
    pdf_path = "app/static/pdf/Data_Analysis_Syllabus.pdf"
    if os.path.exists(pdf_path):
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
        )
    return HTMLResponse("Syllabus PDF file not found", status_code=404)

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
