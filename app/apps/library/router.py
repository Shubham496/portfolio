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
    get_adjacent_topics,
    get_subject_videos,
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
    tab: Optional[str] = Query("all_topics", description="Panels: all_topics, notes, interview_questions, video_lectures"),
    topic: Optional[str] = Query(None, description="Topic slug to display in all_topics panel"),
    vertical: Optional[str] = Query(None, description="Legacy filter parameter for backwards compatibility"),
):
    """
    Unified Subject Portal (e.g. /library/sql, /library/python).
    4 Panels:
      1. All Topics (Default: W3Schools style left curriculum sidebar, center reading canvas, prev/next buttons)
      2. Notes (Deep-dive study guides & architectural breakdowns)
      3. Interview Questions (Top viva & interview traps)
      4. Video Lectures (Curated workshop video masterclasses)
    """
    subject_lower = subject.lower().strip()
    if subject_lower not in SUBJECTS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject '{subject}' not found in the Mythos Resource Library.",
        )

    # Backward compatibility with legacy vertical param
    if vertical:
        if vertical in ("notes", "handbooks"):
            tab = "notes"
        elif vertical in ("viva", "interview"):
            tab = "interview_questions"
        elif vertical in ("videos", "video_lectures"):
            tab = "video_lectures"
        else:
            tab = "all_topics"

    valid_tabs = {"all_topics", "notes", "interview_questions", "video_lectures"}
    active_tab = tab if tab in valid_tabs else "all_topics"

    summary = get_subject_summary(subject_lower)
    all_docs = list_documents_for_subject(subject_lower)
    grouped_docs = get_subject_grouped_by_category(subject_lower)

    # Determine active topic for "all_topics" panel
    active_slug = topic
    if not active_slug and all_docs:
        active_slug = all_docs[0].slug

    active_doc = get_document(subject_lower, active_slug) if active_slug else None
    prev_topic, next_topic = get_adjacent_topics(subject_lower, active_slug) if active_slug else (None, None)

    # Segment documents for dedicated panels
    notes_docs = [d for d in all_docs if d.vertical == "notes"]
    interview_docs = [d for d in all_docs if d.vertical in ("viva", "interview")]
    video_lectures = get_subject_videos(subject_lower)

    page_title = (
        f"{active_doc.metadata.title} | {summary['short_title']} Topics | MYTHOS"
        if (active_doc and active_tab == "all_topics")
        else f"{summary['title']} — Study Guides & Resources | MYTHOS"
    )

    return templates.TemplateResponse(
        request=request,
        name="library/subject_hub.html",
        context={
            "settings": settings,
            "subject": summary,
            "active_tab": active_tab,
            "active_topic_slug": active_slug,
            "active_doc": active_doc,
            "prev_topic": prev_topic,
            "next_topic": next_topic,
            "grouped_docs": grouped_docs,
            "all_docs": all_docs,
            "notes_docs": notes_docs,
            "interview_docs": interview_docs,
            "video_lectures": video_lectures,
            "verticals": VERTICALS,
            "page_title": page_title,
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
    sidebar_grouped = get_subject_grouped_by_category(subject_lower)
    prev_topic, next_topic = get_adjacent_topics(subject_lower, slug)

    return templates.TemplateResponse(
        request=request,
        name="library/reader.html",
        context={
            "settings": settings,
            "doc": parsed_doc,
            "meta": parsed_doc.metadata,
            "subject": subject_info,
            "sidebar_grouped": sidebar_grouped,
            "prev_topic": prev_topic,
            "next_topic": next_topic,
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
