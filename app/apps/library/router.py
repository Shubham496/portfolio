"""
MYTHOS Resource Library Web & API Router.
Handles public routes for /library, /library/{subject}, /library/{subject}/notes/{slug},
and JSON API endpoints.
"""

from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Query, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.apps.library.services import (
    SUBJECTS,
    VERTICALS,
    get_document,
    list_documents_for_subject,
    get_subject_grouped_by_category,
    get_subject_summary,
    get_all_subjects_summary,
)

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["settings"] = settings

router = APIRouter(tags=["Resource Library & Knowledge Engine"])


# -------------------------------------------------------------------------
# Web HTML Routes
# -------------------------------------------------------------------------

@router.get("/library", response_class=HTMLResponse)
async def library_home(request: Request):
    """
    Primary Resource Library Landing Hub.
    Displays subject cards, vertical offerings, and featured learning materials.
    """
    subjects_summary = get_all_subjects_summary()
    return templates.TemplateResponse(
        request=request,
        name="library/index.html",
        context={
            "settings": settings,
            "subjects": subjects_summary,
            "verticals": VERTICALS,
            "page_title": "Resource Library & Knowledge Engine | MYTHOS",
            "active_nav": "library",
        },
    )


@router.get("/library/{subject}", response_class=HTMLResponse)
async def library_subject_hub(
    request: Request,
    subject: str,
    vertical: Optional[str] = Query(None, description="Filter by vertical: notes, viva, datasets, books, projects"),
):
    """
    Unified Subject Portal (e.g. /library/sql, /library/python).
    Shows resource counts, tabbed navigation, and grouped curriculum cards.
    """
    subject_lower = subject.lower().strip()
    if subject_lower not in SUBJECTS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject '{subject}' not found in the Mythos Resource Library.",
        )

    summary = get_subject_summary(subject_lower)
    grouped_docs = get_subject_grouped_by_category(subject_lower, vertical)

    return templates.TemplateResponse(
        request=request,
        name="library/subject_hub.html",
        context={
            "settings": settings,
            "subject": summary,
            "active_vertical": vertical or "all",
            "grouped_docs": grouped_docs,
            "verticals": VERTICALS,
            "page_title": f"{summary['title']} — Study Guides & Resources | MYTHOS",
            "active_nav": "library",
        },
    )


@router.get("/library/{subject}/notes/{slug}", response_class=HTMLResponse)
async def library_reader(request: Request, subject: str, slug: str):
    """
    Distraction-Free 3-Column Technical Documentation Reader.
    Left: Subject tree
    Center: Markdown rendered article with Prism syntax and callouts
    Right: Sticky Table of Contents & Cohort Counseling card
    """
    subject_lower = subject.lower().strip()
    if subject_lower not in SUBJECTS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject '{subject}' not found.",
        )

    parsed_doc = get_document(subject_lower, slug)
    if not parsed_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article '{slug}' not found in subject '{subject}'.",
        )

    subject_info = SUBJECTS[subject_lower]
    # Fetch grouped docs for the left navigation tree (same vertical)
    sidebar_grouped = get_subject_grouped_by_category(subject_lower, parsed_doc.metadata.vertical)

    return templates.TemplateResponse(
        request=request,
        name="library/reader.html",
        context={
            "settings": settings,
            "doc": parsed_doc,
            "meta": parsed_doc.metadata,
            "subject": subject_info,
            "sidebar_grouped": sidebar_grouped,
            "verticals": VERTICALS,
            "page_title": f"{parsed_doc.metadata.title} | {subject_info['short_title']} | MYTHOS Library",
            "active_nav": "library",
        },
    )


# -------------------------------------------------------------------------
# JSON API Endpoints
# -------------------------------------------------------------------------

@router.get("/api/library/subjects", response_class=JSONResponse)
async def api_library_subjects():
    """Returns overview JSON of all library subjects and vertical counts."""
    return {
        "success": True,
        "subjects": get_all_subjects_summary(),
        "verticals": VERTICALS,
    }


@router.get("/api/library/{subject}/documents", response_class=JSONResponse)
async def api_library_documents(
    subject: str,
    vertical: Optional[str] = Query(None),
):
    """Returns JSON list of documents for a given subject."""
    subject_lower = subject.lower().strip()
    if subject_lower not in SUBJECTS:
        raise HTTPException(status_code=404, detail="Subject not found")

    docs = list_documents_for_subject(subject_lower, vertical)
    return {
        "success": True,
        "subject": subject_lower,
        "total": len(docs),
        "documents": [d.to_dict() for d in docs],
    }
