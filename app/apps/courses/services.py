import os
import csv
import io
import math
import logging
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc

from app.apps.courses.database import engine, Base
from app.apps.courses.models import Batch, StudentLead, AdminUser
from app.apps.courses.schemas import (
    EnquiryCreate,
    BatchRegistrationCreate,
    BatchCreate,
    LeadStatusUpdate
)
from app.core.config import settings

logger = logging.getLogger("courses.services")


def init_courses_db():
    """Create courses tables if they don't exist and seed the default weekend batch."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Course platform tables verified / created.")
        
        # Seed default weekend Data Analysis batch if none exists
        from app.apps.courses.database import SessionLocal
        with SessionLocal() as db:
            existing_batch = db.query(Batch).filter(Batch.is_active == True).first()
            if not existing_batch:
                default_batch = Batch(
                    batch_code="DA-WKND-2026-B1",
                    title="Weekend Data Analysis Masterclass",
                    course_name="Data Analysis (Python, SQL, PowerBI, Excel, Tableau)",
                    technologies="Python, SQL, PowerBI, Excel, Tableau",
                    schedule_days="Saturday & Sunday",
                    schedule_time="6:00 PM – 8:00 PM IST",
                    start_date="Upcoming Weekend",
                    duration="8-10 Weeks Hands-On Mentorship",
                    status="enrolling",
                    max_seats=25,
                    description=(
                        "Live interactive weekend training designed for students and working professionals. "
                        "Complete practical curriculum covering Python programming, SQL databases, "
                        "Power BI dashboards, Excel data modeling, and Tableau visual storytelling."
                    ),
                    is_active=True
                )
                db.add(default_batch)
                db.commit()
                logger.info("Default Weekend Data Analysis batch seeded.")

            # Seed / ensure default 'admin' user exists with updated password from .env
            admin_user = db.query(AdminUser).filter(AdminUser.username == "admin").first()
            env_password = os.getenv("ADMIN_PASSWORD")
            env_hash = os.getenv("ADMIN_PASSWORD_HASH")

            from app.apps.courses.auth import hash_password

            if env_password:
                target_hash = hash_password(env_password)
            elif env_hash:
                target_hash = env_hash
            else:
                target_hash = "$2b$12$uSiwGr.E6jVYlVLLvQmj/exumDJRDsAT2rJH1H.YKjsRGO9YCfJ8e"

            if not admin_user:
                admin_user = AdminUser(
                    username="admin",
                    email="admin@mythostech.in",
                    hashed_password=target_hash,
                    is_active=True
                )
                db.add(admin_user)
                db.commit()
                logger.info("Admin user 'admin' seeded.")
            else:
                if env_password or env_hash:
                    admin_user.hashed_password = target_hash
                    db.commit()

            # Seed / ensure dedicated 'agent_admin' profile exists for agent operations and automated tests
            agent_user = db.query(AdminUser).filter(AdminUser.username == "agent_admin").first()
            agent_password = os.getenv("AGENT_PASSWORD", "hUrHD1qKvVPQqk_y1itG*ISU")
            agent_hash = hash_password(agent_password)

            if not agent_user:
                agent_user = AdminUser(
                    username="agent_admin",
                    email="agent@mythostech.in",
                    hashed_password=agent_hash,
                    is_active=True
                )
                db.add(agent_user)
                db.commit()
                logger.info("Dedicated agent user 'agent_admin' seeded.")
            else:
                agent_user.hashed_password = agent_hash
                db.commit()
    except Exception as e:
        logger.error(f"Error initializing course database: {e}", exc_info=True)


def get_default_active_batch(db: Session) -> Optional[Batch]:
    """Retrieve the primary currently enrolling weekend batch."""
    return db.query(Batch).filter(
        Batch.is_active == True,
        Batch.status == "enrolling"
    ).order_by(desc(Batch.id)).first() or db.query(Batch).filter(Batch.is_active == True).first()


def list_batches(db: Session, active_only: bool = True) -> List[Dict[str, Any]]:
    """List batches with registration stats."""
    query = db.query(Batch)
    if active_only:
        query = query.filter(Batch.is_active == True)
    batches = query.order_by(desc(Batch.id)).all()
    return [b.to_dict() for b in batches]


def create_batch(db: Session, batch_data: BatchCreate) -> Batch:
    """Create a new batch."""
    batch = Batch(**batch_data.model_dump())
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


def create_student_enquiry(
    db: Session,
    enquiry: EnquiryCreate,
    client_ip: Optional[str] = None
) -> Dict[str, Any]:
    """Record a general student enquiry or counseling request."""
    # Associate with default weekend batch if available
    default_batch = get_default_active_batch(db)
    
    lead = StudentLead(
        lead_type="enquiry",
        batch_id=default_batch.id if default_batch else None,
        full_name=enquiry.full_name.strip(),
        email=enquiry.email.strip().lower() if enquiry.email else "",
        phone=enquiry.phone.strip(),
        current_status=enquiry.current_status,
        prior_experience=None,
        preferred_schedule=enquiry.preferred_schedule or "Saturday & Sunday 6:00 PM – 8:00 PM IST",
        message=enquiry.message.strip() if enquiry.message else "",
        status="new",
        source_ip=client_ip
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    
    return {
        "success": True,
        "message": "Your enquiry has been received. Shubham will reach out shortly to discuss syllabus, schedule, and answer your questions.",
        "lead_id": lead.id,
        "lead_type": lead.lead_type,
        "schedule": lead.preferred_schedule,
        "data": lead.to_dict()
    }


def create_batch_registration(
    db: Session,
    reg: BatchRegistrationCreate,
    client_ip: Optional[str] = None
) -> Dict[str, Any]:
    """Record a direct batch registration for the Weekend Data Analysis class."""
    target_batch = None
    if reg.batch_id:
        target_batch = db.query(Batch).filter(Batch.id == reg.batch_id, Batch.is_active == True).first()
    
    if not target_batch:
        target_batch = get_default_active_batch(db)

    lead = StudentLead(
        lead_type="batch_registration",
        batch_id=target_batch.id if target_batch else None,
        full_name=reg.full_name.strip(),
        email=reg.email.strip().lower() if reg.email else "",
        phone=reg.phone.strip(),
        current_status=reg.current_status,
        prior_experience=reg.prior_experience,
        preferred_schedule=reg.preferred_schedule or "Saturday & Sunday 6:00 PM – 8:00 PM IST",
        message=reg.message.strip() if reg.message else "",
        status="new",
        source_ip=client_ip
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    batch_info = target_batch.to_dict() if target_batch else None

    return {
        "success": True,
        "message": f"Successfully registered for the Weekend Data Analysis batch! Classes run Saturday & Sunday from 6:00 PM to 8:00 PM.",
        "registration_id": lead.id,
        "lead_type": lead.lead_type,
        "batch": batch_info,
        "schedule": "Saturday & Sunday 6:00 PM – 8:00 PM IST",
        "data": lead.to_dict()
    }


def get_leads(
    db: Session,
    lead_type: Optional[str] = None,
    batch_id: Optional[int] = None,
    status: Optional[str] = None,
    search: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieve student leads with flexible filtering."""
    query = db.query(StudentLead)

    if lead_type and lead_type != "all":
        query = query.filter(StudentLead.lead_type == lead_type)

    if batch_id:
        query = query.filter(StudentLead.batch_id == batch_id)

    if status and status != "all":
        query = query.filter(StudentLead.status == status)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                StudentLead.full_name.ilike(search_term),
                StudentLead.email.ilike(search_term),
                StudentLead.phone.ilike(search_term)
            )
        )

    leads = query.order_by(desc(StudentLead.id)).all()
    return [l.to_dict() for l in leads]


def get_leads_paginated(
    db: Session,
    lead_type: Optional[str] = None,
    batch_id: Optional[int] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    per_page: int = 10
) -> Dict[str, Any]:
    """Retrieve paginated student leads with filtering and pagination metadata."""
    query = db.query(StudentLead)

    if lead_type and lead_type != "all":
        query = query.filter(StudentLead.lead_type == lead_type)

    if batch_id:
        query = query.filter(StudentLead.batch_id == batch_id)

    if status and status != "all":
        query = query.filter(StudentLead.status == status)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                StudentLead.full_name.ilike(search_term),
                StudentLead.email.ilike(search_term),
                StudentLead.phone.ilike(search_term)
            )
        )

    total_count = query.count()
    per_page = max(1, min(per_page, 100))
    total_pages = max(1, math.ceil(total_count / per_page)) if total_count > 0 else 1
    page = max(1, min(page, total_pages)) if total_count > 0 else 1
    offset = (page - 1) * per_page

    leads = query.order_by(desc(StudentLead.id)).offset(offset).limit(per_page).all()

    start_item = offset + 1 if total_count > 0 else 0
    end_item = min(offset + per_page, total_count)

    return {
        "items": [l.to_dict() for l in leads],
        "total": total_count,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "start_item": start_item,
        "end_item": end_item,
        "has_prev": page > 1,
        "has_next": page < total_pages,
        "prev_page": page - 1 if page > 1 else None,
        "next_page": page + 1 if page < total_pages else None,
    }


def get_lead_summary(db: Session) -> Dict[str, Any]:
    """Provide dashboard analytics for leads and batch admissions."""
    all_leads = db.query(StudentLead).all()
    total = len(all_leads)
    enquiries = len([l for l in all_leads if l.lead_type == "enquiry"])
    registrations = len([l for l in all_leads if l.lead_type == "batch_registration"])
    new_count = len([l for l in all_leads if l.status == "new"])
    contacted_count = len([l for l in all_leads if l.status == "contacted"])
    enrolled_count = len([l for l in all_leads if l.status == "enrolled"])

    return {
        "total_leads": total,
        "enquiries": enquiries,
        "batch_registrations": registrations,
        "new": new_count,
        "contacted": contacted_count,
        "enrolled": enrolled_count,
    }


def update_lead_status(
    db: Session,
    lead_id: int,
    status_update: LeadStatusUpdate
) -> Optional[Dict[str, Any]]:
    """Update pipeline status and internal notes for a lead."""
    lead = db.query(StudentLead).filter(StudentLead.id == lead_id).first()
    if not lead:
        return None

    lead.status = status_update.status
    if status_update.admin_notes is not None:
        lead.admin_notes = status_update.admin_notes

    db.commit()
    db.refresh(lead)
    return lead.to_dict()


def export_leads_csv(db: Session) -> str:
    """Generate a clean CSV string containing all enquiries and batch registrations."""
    leads = db.query(StudentLead).order_by(desc(StudentLead.id)).all()

    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "ID",
        "Type",
        "Batch Title",
        "Batch Code",
        "Full Name",
        "Email",
        "Phone",
        "Current Status",
        "Prior Experience",
        "Schedule",
        "Message / Questions",
        "Status",
        "Admin Notes",
        "Submitted At"
    ])

    for l in leads:
        writer.writerow([
            l.id,
            l.lead_type,
            l.batch.title if l.batch else "General",
            l.batch.batch_code if l.batch else "-",
            l.full_name,
            l.email,
            l.phone,
            l.current_status or "",
            l.prior_experience or "",
            l.preferred_schedule or "",
            l.message or "",
            l.status,
            l.admin_notes or "",
            l.created_at.strftime("%Y-%m-%d %H:%M:%S") if l.created_at else ""
        ])

    return output.getvalue()


def get_instructor_curriculum_profile() -> Dict[str, Any]:
    """
    Returns structured data about the instructor, curriculum, and schedule.
    Explicitly enforces NO fee mention.
    """
    return {
        "instructor": {
            "name": settings.OWNER_NAME,
            "title": "Lead Python & Data Architecture Consultant | Technical Instructor",
            "bio": (
                "Lead Consultant and Instructor with deep production experience across enterprise data pipelines, "
                "relational databases, and executive BI dashboards. Trained and mentored 550+ students and developers in "
                "practical, hands-on Python, SQL, Power BI, Excel modeling, and Tableau."
            ),
            "experience_highlights": [
                "Lead Python & Data Architecture Consultant at Ducat (Trained 550+ students & developers across enterprise batches)",
                "Data Analyst & Automation Engineer at LNP Infotech (U.S. financial & compliance transaction analysis)",
                "Data Analyst & Technical Instructor at Netmax Technologies (Enterprise ETL, SQL, and Power BI dashboards)"
            ],
            "phone": settings.OWNER_PHONE,
            "email": settings.EMAIL,
            "linkedin": settings.LINKEDIN_URL,
            "github": settings.GITHUB_URL
        },
        "course": {
            "name": "Complete Data Analysis Masterclass",
            "tools": ["Python", "SQL", "PowerBI", "Excel", "Tableau"],
            "schedule": {
                "days": "Saturday & Sunday only",
                "timings": "6:00 PM – 8:00 PM IST",
                "frequency": "Weekend only (2 hours/day, 4 hours/week)"
            },
            "syllabus_modules": [
                {
                    "module": "Excel Advanced Modeling, Power Query & VBA",
                    "badge": "Spreadsheets & Automation",
                    "icon": "excel",
                    "topics": [
                        "Advanced Formulas: XLOOKUP, INDEX/MATCH, Dynamic Arrays",
                        "Pivot Tables, Slicers & Executive Pivot Charts",
                        "Power Query Editor: Multi-file Ingestion & ETL Cleansing",
                        "VBA & Macro Automation for Routine Reporting"
                    ],
                    "detailed_sections": [
                        {
                            "title": "Power Query Editor & ETL",
                            "bullets": [
                                "Connecting to multiple CSVs, Excels, and folder directories",
                                "Unpivoting cross-tabulated data into normalized rows",
                                "Custom & conditional columns, data type casting, error handling",
                                "Merging queries (VLOOKUP replacement) & Append queries (stacking datasets)",
                                "Automated data refreshes without manual copy-pasting"
                            ]
                        },
                        {
                            "title": "VBA & Macro Automation",
                            "bullets": [
                                "Recording and editing macros for repetitive weekly tasks",
                                "VBA core syntax: Subroutines, Variables, For/While Loops, If-Then logic",
                                "Building User Defined Functions (UDFs) for proprietary business formulas",
                                "Automating one-click workbook report generation and formatting"
                            ]
                        },
                        {
                            "title": "Advanced Formula Engineering & What-If",
                            "bullets": [
                                "Dynamic Arrays: FILTER, UNIQUE, SORT, XLOOKUP, XMATCH",
                                "Modern formulas: LET (named variables) & LAMBDA custom reusable logic",
                                "Nested conditionals: SUMIFS, COUNTIFS, AVERAGEIFS, IFS, SWITCH",
                                "What-If Analysis: Goal Seek, Data Tables, Scenario Manager, Sensitivity modeling"
                            ]
                        },
                        {
                            "title": "Data Cleansing & Executive Dashboards",
                            "bullets": [
                                "Text wrangling: TEXTSPLIT, SUBSTITUTE, TRIM, Flash Fill",
                                "Data validation rules, custom dropdown lists, IFERROR sanitization",
                                "Multi-slicer linked dashboards with dynamic KPI cards & sparklines"
                            ]
                        }
                    ]
                },
                {
                    "module": "SQL for Data Analysis & Relational Databases",
                    "badge": "Database Architecture",
                    "icon": "sql",
                    "topics": [
                        "Relational Database Architecture & 3NF Normalization",
                        "Complex Multi-Table JOINs & Nested Subqueries",
                        "Analytical Window Functions (RANK, DENSE_RANK, ROW_NUMBER)",
                        "Common Table Expressions (CTEs) & Query Optimization"
                    ],
                    "detailed_sections": [
                        {
                            "title": "Analytical Window Functions Deep-Dive",
                            "bullets": [
                                "Ranking metrics: ROW_NUMBER, RANK, DENSE_RANK, NTILE",
                                "Lead & Lag analysis: Comparing period-over-period sales without self-joins",
                                "Cumulative statistics: Running totals, moving averages with window frames",
                                "Frame specifications: ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW"
                            ]
                        },
                        {
                            "title": "CTEs & Advanced Query Structuring",
                            "bullets": [
                                "Common Table Expressions (WITH clauses) for modular SQL architecture",
                                "Correlated subqueries vs Non-correlated subqueries",
                                "Recursive CTEs for hierarchical organizational trees & bill-of-materials",
                                "Complex aggregations: GROUP BY, HAVING, GROUPING SETS, ROLLUP, CUBE"
                            ]
                        },
                        {
                            "title": "Relational Modeling & Schema Design",
                            "bullets": [
                                "Primary keys, Foreign keys, Composite keys, Unique constraints, Cascading",
                                "Database normalization principles: 1NF, 2NF, 3NF design",
                                "Entity Relationship Diagrams (ERD) & schema mapping"
                            ]
                        },
                        {
                            "title": "Performance Tuning & Business Analytics Queries",
                            "bullets": [
                                "B-Tree indexing strategies, composite indexes, avoiding table scans",
                                "Query execution analysis using EXPLAIN and EXPLAIN ANALYZE",
                                "Real business queries: Cohort retention analysis, customer churn velocity, active users"
                            ]
                        }
                    ]
                },
                {
                    "module": "Python for Data Analysis & Automation",
                    "badge": "Core Programming & ETL",
                    "icon": "python",
                    "topics": [
                        "Python Foundations, Control Flow & Data Structures",
                        "High-Performance NumPy Array Matrix Computing",
                        "Pandas DataFrames Manipulation & Multi-Source Cleansing",
                        "Automated Data Extraction & Production Scripting"
                    ],
                    "detailed_sections": [
                        {
                            "title": "Pandas Data Wrangling Masterclass",
                            "bullets": [
                                "DataFrame indexing, slicing, boolean filtering, query() method",
                                "High-performance vector operations: apply(), map(), transform()",
                                "Reshaping datasets: pivot_table(), melt(), stack(), unstack()",
                                "Multi-level GroupBy aggregations and statistical summarization",
                                "Merging, joining, and concatenating heterogeneous sources"
                            ]
                        },
                        {
                            "title": "Data Sanitization & Missing Value Handling",
                            "bullets": [
                                "Detecting, imputing, and dropping null values (isna, fillna, dropna)",
                                "Vectorized string manipulation (.str methods) and Regex extraction",
                                "Datetime parsing, time-series resampling, and business calendars"
                            ]
                        },
                        {
                            "title": "NumPy Matrix Operations & Mathematics",
                            "bullets": [
                                "Creating and reshaping 1D, 2D, and 3D ndarrays",
                                "Broadcasting rules, boolean masking, fast numerical filtering",
                                "Vectorized mathematical computations & statistical arrays"
                            ]
                        },
                        {
                            "title": "Data Visualization & Scripted Automation",
                            "bullets": [
                                "Visualizing distributions, correlations & outliers with Matplotlib & Seaborn",
                                "Connecting Python to SQL databases via SQLAlchemy & psycopg2",
                                "Automating batch CSV/Excel processing and scheduling pipeline execution"
                            ]
                        }
                    ]
                },
                {
                    "module": "Power BI Interactive Business Intelligence",
                    "badge": "Enterprise BI & Modeling",
                    "icon": "powerbi",
                    "topics": [
                        "Power Query ETL Ingestion & Data Transformation",
                        "Star Schema Relational Data Modeling & Cardinality",
                        "Advanced DAX Measures & Time Intelligence Calculations",
                        "Executive KPI Dashboards, Bookmarks & Drill-Throughs"
                    ],
                    "detailed_sections": [
                        {
                            "title": "Data Modeling & Power Query ETL",
                            "bullets": [
                                "Power Query data shaping, unpivoting, merging queries, column profiling",
                                "Star Schema vs Snowflake Schema: Fact tables vs Dimension tables",
                                "Managing 1-to-Many and Many-to-Many relationships, active vs inactive (USERELATIONSHIP)",
                                "Designing robust calendar tables for enterprise time-series"
                            ]
                        },
                        {
                            "title": "Advanced DAX Measures & Virtual Tables",
                            "bullets": [
                                "Evaluation contexts: Row context, Filter context, Context transition",
                                "Core DAX functions: CALCULATE, FILTER, ALL, ALLEXCEPT, VALUES, RELATED, RELATEDTABLE",
                                "Virtual table manipulation: SUMMARIZE, ADDCOLUMNS, GENERATE",
                                "Safe numerical calculations using DIVIDE, COALESCE, SELECTEDVALUE"
                            ]
                        },
                        {
                            "title": "Time Intelligence Calculations",
                            "bullets": [
                                "Year-to-Date (YTD), Quarter-to-Date (QTD), Month-to-Date (MTD)",
                                "Period-over-period comparisons: SAMEPERIODLASTYEAR, DATEADD, PARALLELPERIOD",
                                "Rolling metrics: 30-day moving averages and trailing 12-month metrics"
                            ]
                        },
                        {
                            "title": "Executive Visual Storytelling & UX",
                            "bullets": [
                                "Building interactive drill-through pages and custom tooltip report pages",
                                "Interactive UI bookmarks, buttons, slicer panels, dynamic measure selectors",
                                "Designing responsive executive dashboard layouts optimized for leadership"
                            ]
                        }
                    ]
                },
                {
                    "module": "Tableau Visual Storytelling & Dashboards",
                    "badge": "Visual Analytics",
                    "icon": "tableau",
                    "topics": [
                        "Connecting to Files, Cloud Databases & Live Extracts",
                        "Visual Dimensions vs Measures & Granularity Controls",
                        "Level of Detail (LOD) Calculations (FIXED, INCLUDE, EXCLUDE)",
                        "Interactive Storyboards, Dynamic Actions & Cloud Publishing"
                    ],
                    "detailed_sections": [
                        {
                            "title": "LOD Expressions & Advanced Calculations",
                            "bullets": [
                                "Level of Detail (LOD) calculations: FIXED, INCLUDE, EXCLUDE syntax",
                                "Calculating customer lifetime value and first-purchase cohorts with LODs",
                                "Table calculations: Percent of total, running total, rank, difference from previous",
                                "Dynamic parameters, parameter actions, and calculated field logic"
                            ]
                        },
                        {
                            "title": "Interactive Actions & Dashboard Architecture",
                            "bullets": [
                                "Filter actions, highlight actions, set actions, and URL external actions",
                                "Creating collapsible containers, custom navigation buttons, dynamic icons",
                                "Geographic mapping with latitude/longitude, spatial data, and regional layers"
                            ]
                        },
                        {
                            "title": "Advanced Chart Types & Visual Best Practices",
                            "bullets": [
                                "Dual-axis combination charts, Pareto charts, waterfall charts, donut charts",
                                "Cognitive design: Color theory, visual hierarchy, avoiding chart clutter",
                                "Formatting guidelines for C-level executive consumption"
                            ]
                        },
                        {
                            "title": "Storyboarding & Tableau Public Portfolio",
                            "bullets": [
                                "Building multi-chapter story points presenting narrative business insights",
                                "Extract performance tuning, dashboard latency optimization",
                                "Publishing interactive web portfolios on Tableau Public"
                            ]
                        }
                    ]
                },
                {
                    "module": "Career Acceleration: GitHub, Resume & LinkedIn Setup",
                    "badge": "Job Readiness & Portfolio",
                    "icon": "career",
                    "topics": [
                        "GitHub Portfolio Setup & Open-Source Code Architecture",
                        "ATS-Compliant Data Analyst Resume Engineering",
                        "LinkedIn Profile Optimization & Inbound Recruiter Strategy",
                        "1-on-1 Mock Technical Interviews & Live SQL Screenings"
                    ],
                    "detailed_sections": [
                        {
                            "title": "GitHub Portfolio Architecture",
                            "bullets": [
                                "Setting up a clean, professional GitHub developer profile with profile README",
                                "Git version control fundamentals: commits, branching, pushing repository updates",
                                "Writing production-grade README.md files: Problem statements, architecture schemas, key insights, screenshots",
                                "Hosting 3+ complete capstone portfolios with downloadable data dictionaries"
                            ]
                        },
                        {
                            "title": "ATS-Optimized Tech Resume Building",
                            "bullets": [
                                "Line-by-line resume engineering specifically for Data Analyst & BI roles",
                                "Quantifiable business impact formula: Action + Tool + Business Result (e.g., 'Reduced query latency by 45%')",
                                "Strategic technical keyword placement to pass automated ATS recruiter screeners",
                                "Removing rookie formatting flaws and organizing technical skills hierarchy"
                            ]
                        },
                        {
                            "title": "LinkedIn Personal Branding & Inbound Networking",
                            "bullets": [
                                "High-converting profile headline, about section, and featured portfolio media",
                                "Documenting learning in public: Sharing live dashboard demos and SQL insights",
                                "High-response direct messaging templates for reaching hiring managers and team leads",
                                "Leveraging alumni networks and technical community groups for interview referrals"
                            ]
                        },
                        {
                            "title": "Mock Technical Interviews & Capstone Deployment",
                            "bullets": [
                                "Live timed SQL query solving on CoderPad & HackerRank under interview pressure",
                                "Python data wrangling live screening challenges using Pandas & NumPy",
                                "Dashboard defense: Answering business stakeholder questions on DAX logic and metrics",
                                "Publishing live web-accessible dashboards on Power BI Service and Tableau Public"
                            ]
                        }
                    ]
                }
            ],
            "fees": None  # Explicitly None - NO fees on page
        }
    }



def generate_syllabus_html_brochure() -> str:
    """Generate a clean, standalone, printable syllabus brochure HTML document."""
    profile = get_instructor_curriculum_profile()
    instructor = profile["instructor"]
    course = profile["course"]
    modules = course["syllabus_modules"]

    modules_html = ""
    for i, m in enumerate(modules, start=1):
        topics_li = "".join([f"<li style='margin-bottom:6px;'>• {t}</li>" for t in m["topics"]])
        modules_html += f"""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:18px; margin-bottom:14px; page-break-inside:avoid;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
                <span style="background:#2563eb; color:#ffffff; font-weight:bold; font-size:12px; width:24px; height:24px; border-radius:6px; display:inline-flex; align-items:center; justify-content:center;">{i}</span>
                <h3 style="margin:0; font-size:15px; font-weight:700; color:#0f172a;">{m['module']}</h3>
            </div>
            <ul style="margin:0; padding-left:18px; font-size:13px; color:#475569; line-height:1.6;">
                {topics_li}
            </ul>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Complete Data Analysis Masterclass Syllabus | {instructor['name']}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 40px 20px;
            background-color: #ffffff;
            color: #0f172a;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .header {{
            border-bottom: 2px solid #2563eb;
            padding-bottom: 20px;
            margin-bottom: 25px;
        }}
        .badge {{
            display: inline-block;
            background: #dbeafe;
            color: #1e40af;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 9999px;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .schedule-box {{
            background: #0f172a;
            color: #ffffff;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .footer {{
            border-top: 1px solid #e2e8f0;
            margin-top: 30px;
            padding-top: 15px;
            font-size: 12px;
            color: #64748b;
            text-align: center;
        }}
        @media print {{
            body {{ padding: 0; }}
            .no-print {{ display: none; }}
            .schedule-box {{ background: #1e293b !important; -webkit-print-color-adjust: exact; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="no-print" style="margin-bottom:20px; text-align:right;">
            <button onclick="window.print()" style="background:#2563eb; color:#fff; border:none; padding:8px 16px; border-radius:8px; font-weight:600; cursor:pointer;">
                🖨️ Print / Save as PDF
            </button>
        </div>

        <div class="header">
            <span class="badge">Official Course Curriculum</span>
            <h1 style="margin:0 0 6px 0; font-size:28px; font-weight:800; color:#0f172a;">Complete Data Analysis Masterclass</h1>
            <p style="margin:0; font-size:14px; color:#475569;">
                Comprehensive Hands-On Mentorship: <strong>Python, SQL, Power BI, Excel & Tableau</strong>
            </p>
            <p style="margin:4px 0 0 0; font-size:13px; color:#64748b;">
                Instructor: <strong>{instructor['name']}</strong> · {instructor['title']}
            </p>
        </div>

        <div class="schedule-box">
            <div>
                <div style="font-size:11px; text-transform:uppercase; color:#94a3b8; font-weight:600;">Fixed Batch Schedule</div>
                <div style="font-size:16px; font-weight:bold; color:#ffffff; margin-top:2px;">Saturday & Sunday Only</div>
            </div>
            <div>
                <div style="font-size:11px; text-transform:uppercase; color:#94a3b8; font-weight:600;">Timings</div>
                <div style="font-size:16px; font-weight:bold; color:#60a5fa; margin-top:2px;">6:00 PM – 8:00 PM IST</div>
            </div>
            <div>
                <div style="font-size:11px; text-transform:uppercase; color:#94a3b8; font-weight:600;">Duration</div>
                <div style="font-size:16px; font-weight:bold; color:#ffffff; margin-top:2px;">8–10 Weeks (Live Online)</div>
            </div>
        </div>

        <h2 style="font-size:18px; font-weight:700; margin-bottom:14px; color:#0f172a;">Course Syllabus by Module</h2>
        {modules_html}

        <div style="background:#f1f5f9; border-radius:12px; padding:18px; margin-top:20px;">
            <h3 style="margin:0 0 8px 0; font-size:14px; font-weight:700;">Mentorship & Hands-On Projects</h3>
            <p style="margin:0; font-size:13px; color:#475569; line-height:1.6;">
                Every module includes hands-on industry datasets (E-commerce retail, financial transactions, marketing analytics). 
                Students graduate with end-to-end portfolio projects ready for resume and LinkedIn showcase.
            </p>
        </div>

        <div class="footer">
            <p style="margin:0 0 4px 0;">Instructor Contact: Phone: {instructor['phone']} · Email: {instructor['email']}</p>
            <p style="margin:0;">© {instructor['name']}. Weekend Data Analysis Mentorship Program.</p>
        </div>
    </div>
</body>
</html>"""
    return html
