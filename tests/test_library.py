"""
Automated Test Suite for MYTHOS Resource Library & Knowledge Engine.
Verifies routing, frontmatter parsing, markdown rendering, TOC generation,
caching, and 404 error boundaries.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.apps.library.services import (
    SUBJECTS,
    get_document,
    list_documents_for_subject,
    get_all_subjects_summary,
)

client = TestClient(app)


def test_library_home_page():
    """Verify the /library main hub renders successfully with technology logo grid."""
    response = client.get("/library")
    assert response.status_code == 200
    html = response.text
    assert "Resource Library" in html
    assert "MySQL" in html
    assert "PostgreSQL" in html
    assert "Python" in html
    assert "Power BI" in html


def test_library_subject_hub():
    """Verify /library/{subject} renders category groups, tabs, and resources."""
    response = client.get("/library/sql")
    assert response.status_code == 200
    html = response.text
    assert "SQL &amp; Relational Databases" in html or "SQL & Relational Databases" in html
    assert "Relational Database Internals" in html
    assert "SQL Joins" in html
    assert "Weekend Live Cohort" in html


def test_library_subject_hub_vertical_filter():
    """Verify vertical filter tab (e.g. ?vertical=notes)."""
    response = client.get("/library/sql?vertical=notes")
    assert response.status_code == 200
    html = response.text
    assert "SQL Joins" in html


def test_library_subject_hub_not_found():
    """Unknown subject should return 404."""
    response = client.get("/library/nonexistent-subject-xyz")
    assert response.status_code == 404


def test_library_reader_page():
    """Verify /library/{subject}/notes/{slug} renders full 3-column reader view."""
    response = client.get("/library/sql/notes/sql-joins-textbook-vs-reality")
    assert response.status_code == 200
    html = response.text
    
    # 1. Header & Metadata
    assert "SQL Joins: What Textbooks Teach vs. How Production Databases Actually Work" in html
    assert "Relational Database Internals" in html
    assert "100% Free Public Note" in html
    
    # 2. Content Sections
    assert "Academic Definition &amp; Core Concept" in html or "Academic Definition & Core Concept" in html
    assert "The Production Reality" in html
    assert "Nested Loop Join" in html
    assert "Hash Join" in html
    assert "Sort-Merge Join" in html
    
    # 3. Code & Admonitions
    assert "departments" in html
    assert "employees" in html
    assert "admonition" in html
    
    # 4. Table of Contents & Social sharing
    assert "On This Page" in html
    assert "WhatsApp Class Group" in html
    assert "MYTHOS Production Mentorship Bridge" in html


def test_library_reader_not_found():
    """Invalid article slug should return 404."""
    response = client.get("/library/sql/notes/nonexistent-article-xyz")
    assert response.status_code == 404


def test_library_json_api_subjects():
    """Verify /api/library/subjects endpoint."""
    response = client.get("/api/library/subjects")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    subjects = [s["slug"] for s in data["subjects"]]
    assert "sql" in subjects
    assert "python" in subjects


def test_library_json_api_documents():
    """Verify /api/library/{subject}/documents endpoint."""
    response = client.get("/api/library/sql/documents")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["subject"] == "sql"
    assert data["total"] >= 1
    slugs = [d["slug"] for d in data["documents"]]
    assert "sql-joins-textbook-vs-reality" in slugs


def test_service_caching_and_parsing():
    """Verify services parse frontmatter, extract TOC, and cache effectively."""
    doc1 = get_document("sql", "sql-joins-textbook-vs-reality")
    assert doc1 is not None
    assert doc1.metadata.title.startswith("SQL Joins")
    assert doc1.metadata.is_free is True
    assert len(doc1.toc_tokens) >= 3

    # Subsequent call should return cached instance
    doc2 = get_document("sql", "sql-joins-textbook-vs-reality")
    assert doc2 is doc1


def test_expanded_technology_hub_and_topics():
    """Verify expanded technologies (Python, JavaScript, Docker) show full topic curricula."""
    response = client.get("/library/python")
    assert response.status_code == 200
    html = response.text
    assert "Python &amp; Data Engineering" in html or "Python" in html
    assert "CPython Memory Architecture" in html
    assert "Mutable Default Argument" in html

    # JavaScript hub
    res_js = client.get("/library/javascript")
    assert res_js.status_code == 200
    assert "JavaScript" in res_js.text
    assert "Event Loop" in res_js.text

    # Docker hub
    res_docker = client.get("/library/docker")
    assert res_docker.status_code == 200
    assert "Docker" in res_docker.text
    assert "Namespaces" in res_docker.text


def test_topic_outline_reader_page():
    """Verify that clicking any curriculum topic loads a full, structured 5-part guide."""
    response = client.get("/library/python/notes/python-mutable-default-argument-trap")
    assert response.status_code == 200
    html = response.text
    assert "Mutable Default Argument" in html
    assert "Academic Definition &amp; Objectives" in html or "Academic Definition & Objectives" in html
    assert "The Production Reality" in html
    assert "Exam &amp; Technical Interview Gotchas" in html or "Exam & Technical Interview Gotchas" in html
    assert "Mythos Mentorship Bridge" in html
    assert "On This Page" in html
