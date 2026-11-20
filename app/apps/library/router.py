"""
MYTHOS Resource Library Web & API Router.
Handles public routes for /library, /library/{subject}, /library/{subject}/notes/{slug},
and JSON API endpoints.
"""

from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Query, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.config import settings
from app.apps.courses.database import get_db
from app.apps.courses.auth import (
    get_current_student,
    get_or_create_guest_id,
)
from app.apps.courses.services import log_user_activity
from app.apps.library.services import (
    SUBJECTS,
    VERTICALS,
    get_document,
    list_documents_for_subject,
    get_subject_grouped_by_category,
    get_subject_summary,
    get_all_subjects_summary,
    get_adjacent_topics,
    get_adjacent_topics_from_list,
    get_subject_videos,
    list_practice_datasets,
    get_practice_dataset,
    generate_dataset_csv,
)

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["settings"] = settings

router = APIRouter(tags=["Resource Library & Knowledge Engine"])


# -------------------------------------------------------------------------
# Web HTML Routes
# -------------------------------------------------------------------------

@router.get("/library", response_class=HTMLResponse)
async def library_home(
    request: Request,
    vertical: Optional[str] = Query(None),
):
    """
    Primary Resource Library Landing Hub.
    Displays subject cards, vertical offerings, and featured learning materials.
    """
    if vertical == "datasets":
        return RedirectResponse(url="/library/datasets", status_code=status.HTTP_303_SEE_OTHER)

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


# -------------------------------------------------------------------------
# Practice Datasets Vault & Access Control Gating
# -------------------------------------------------------------------------

@router.get("/library/datasets", response_class=HTMLResponse)
async def library_datasets_catalog(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Public Practice Datasets Vault.
    Lists portfolio-ready real-world datasets with schemas and sample data previews.
    """
    current_student = get_current_student(request, db)
    datasets = list_practice_datasets()
    return templates.TemplateResponse(
        request=request,
        name="library/datasets.html",
        context={
            "settings": settings,
            "datasets": datasets,
            "current_student": current_student,
            "page_title": "Practice Datasets Vault — Clean Real-World Data | MYTHOS",
            "active_nav": "datasets",
        },
    )


@router.get("/library/datasets/{slug}", response_class=HTMLResponse)
async def library_dataset_detail(
    request: Request,
    slug: str,
    db: Session = Depends(get_db),
):
    """
    Dataset Inspection & Data Dictionary Preview.
    Shows column specifications and first sample rows.
    Authenticated students see instant 1-click download; guests see login prompt.
    """
    dataset = get_practice_dataset(slug)
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset '{slug}' not found in the Mythos vault.",
        )

    current_student = get_current_student(request, db)
    guest_id = get_or_create_guest_id(request)

    # Log dataset preview view
    log_user_activity(
        db=db,
        session_id=guest_id,
        event_type="dataset_preview_view",
        user_id=current_student.id if current_student else None,
        resource_type="dataset",
        resource_slug=slug,
        ip_address=request.client.host if request.client else None,
    )

    return templates.TemplateResponse(
        request=request,
        name="library/dataset_detail.html",
        context={
            "settings": settings,
            "dataset": dataset,
            "current_student": current_student,
            "page_title": f"{dataset['title']} — Data Dictionary & Preview | MYTHOS",
            "active_nav": "datasets",
        },
    )


@router.get("/library/datasets/{slug}/download")
async def download_practice_dataset(
    request: Request,
    slug: str,
    db: Session = Depends(get_db),
):
    """
    Direct Dataset Download Endpoint (Protected Gate).
    Authenticated students receive instant RFC 4180 CSV download.
    Guests are redirected to /student/login with return URL.
    """
    current_student = get_current_student(request, db)
    if not current_student:
        return RedirectResponse(
            url=f"/student/login?next=/library/datasets/{slug}/download",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    dataset = get_practice_dataset(slug)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    guest_id = get_or_create_guest_id(request)
    csv_data = generate_dataset_csv(slug)
    if not csv_data:
        raise HTTPException(status_code=500, detail="Failed to synthesize dataset file")

    # Record download activity
    log_user_activity(
        db=db,
        session_id=guest_id,
        event_type="dataset_download",
        user_id=current_student.id,
        resource_type="dataset",
        resource_slug=slug,
        ip_address=request.client.host if request.client else None,
    )

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{slug}.csv"',
            "Cache-Control": "no-cache",
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

    # Segment documents for dedicated panels
    notes_docs = [d for d in all_docs if d.vertical == "notes"]
    interview_docs = [d for d in all_docs if d.vertical in ("viva", "interview")]
    video_lectures = get_subject_videos(subject_lower)

    # For the All Topics study workspace: study track only (excluding standalone viva interview banks)
    study_docs = [d for d in all_docs if d.vertical not in ("viva", "interview")]
    study_grouped_docs: dict = {}
    for doc in study_docs:
        study_grouped_docs.setdefault(doc.category, []).append(doc)

    full_grouped_docs = get_subject_grouped_by_category(subject_lower)

    # In "all_topics" panel, use the pure study curriculum
    active_docs_list = study_docs if active_tab == "all_topics" else all_docs
    grouped_docs = study_grouped_docs if active_tab == "all_topics" else full_grouped_docs

    # Determine active topic for "all_topics" panel
    active_slug = topic
    if not active_slug and active_docs_list:
        active_slug = active_docs_list[0].slug

    active_doc = get_document(subject_lower, active_slug) if active_slug else None
    prev_topic, next_topic = get_adjacent_topics_from_list(active_docs_list, active_slug) if active_slug else (None, None)

    if topic and active_doc:
        page_title = f"{active_doc.metadata.title} | {summary['short_title']} | MYTHOS"
    else:
        page_title = f"{summary['title']} Curriculum & Notes | MYTHOS Online Institute"

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
