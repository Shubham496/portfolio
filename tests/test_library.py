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
    assert "SQL Basics" in html
    assert "What is a Database" in html
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
    assert "SQL Joins" in html
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


def test_library_python_w3schools_panel_architecture():
    """Verify /library/python loads with the 4 panels and W3Schools left-topic hierarchy."""
    response = client.get("/library/python")
    assert response.status_code == 200
    html = response.text

    # 1. Four Primary Panels
    assert "All Topics" in html
    assert "Notes (" in html
    assert "Interview Questions (" in html
    assert "Video Lectures (" in html

    # 2. W3Schools-Style Left Sidebar Hierarchies
    assert "Python Basics" in html
    assert "Control Flow" in html
    assert "Data Structures" in html
    assert "Python Syntax &amp; Comments" in html or "Python Syntax & Comments" in html
    assert "Python Variables &amp; Dynamic Typing" in html or "Python Variables & Dynamic Typing" in html
    assert "Python Numbers &amp; Type Casting" in html or "Python Numbers & Type Casting" in html
    assert "Python Booleans &amp; Logical Operators" in html or "Python Booleans & Logical Operators" in html
    assert "Python While Loops, Break &amp; Continue" in html or "Python While Loops, Break & Continue" in html

    # 3. Next Topic Navigation Button on default topic
    assert "Next Topic" in html


def test_library_python_sequential_navigation():
    """Verify clicking a topic loads adjacent Previous and Next topic buttons."""
    response = client.get("/library/python?tab=all_topics&topic=python-variables-datatypes")
    assert response.status_code == 200
    html = response.text

    # Both previous and next should be present
    assert "Previous Topic" in html
    assert "python-syntax-comments" in html
    assert "Next Topic" in html
    assert "python-numbers-casting" in html


def test_library_panel_switching():
    """Verify switching across Notes, Interview Questions, and Video Lectures panels."""
    # 1. Notes Panel
    res_notes = client.get("/library/python?tab=notes")
    assert res_notes.status_code == 200
    assert "Curated Engineering Notes" in res_notes.text
    assert "Read Note" in res_notes.text

    # 2. Interview Questions Panel
    res_interview = client.get("/library/python?tab=interview_questions")
    assert res_interview.status_code == 200
    assert "Oral Viva &amp; Senior Interview Traps" in res_interview.text or "Oral Viva & Senior Interview Traps" in res_interview.text
    assert "Top 40 Python Viva" in res_interview.text

    # 3. Video Lectures Panel
    res_videos = client.get("/library/python?tab=video_lectures")
    assert res_videos.status_code == 200
    assert "Curated Video Masterclasses" in res_videos.text
    assert "CPython Execution Engine" in res_videos.text
    assert "Key Takeaways" in res_videos.text
    assert "Access Lecture" in res_videos.text


def test_adjacent_topics_service():
    """Verify get_adjacent_topics returns correct sequence."""
    from app.apps.library.services import get_adjacent_topics

    # First topic: prev is None, next is variables
    prev_doc, next_doc = get_adjacent_topics("python", "python-syntax-comments")
    assert prev_doc is None
    assert next_doc is not None
    assert next_doc.slug == "python-variables-datatypes"

    # Middle topic: prev is syntax, next is numbers
    prev_mid, next_mid = get_adjacent_topics("python", "python-variables-datatypes")
    assert prev_mid is not None
    assert prev_mid.slug == "python-syntax-comments"
    assert next_mid is not None
    assert next_mid.slug == "python-numbers-casting"


def test_library_sql_w3schools_study_track():
    """Verify /library/sql defaults to foundational Topic 1 (What is a Database & RDBMS?) without interview mixing."""
    response = client.get("/library/sql")
    assert response.status_code == 200
    html = response.text

    # 1. Default active topic must be What is a Database & RDBMS?
    assert "What is a Database &amp; RDBMS?" in html or "What is a Database & RDBMS?" in html
    assert "Relational Database Model" in html or "RELATIONAL DATABASE MODEL" in html

    # 2. Sequential Next Topic button must point to Topic 2 (SQL Introduction & Syntax)
    assert "Next Topic" in html
    assert "sql-intro-syntax" in html
    assert "Previous Topic" not in html  # First topic should not have a previous button

    # 3. Sidebar contains pure study categories in pedagogical sequence
    assert "1. SQL Basics" in html
    assert "2. Database &amp; Table Management" in html or "2. Database & Table Management" in html
    assert "3. Querying &amp; Filtering" in html or "3. Querying & Filtering" in html
    assert "4. Data Manipulation" in html

    # 4. Standalone viva interview traps category must not be in the All Topics study sidebar
    assert "11. Interview Prep" not in html


def test_library_sql_sequential_progression():
    """Verify sequential next/previous topic progression across SQL foundational curriculum."""
    # Step 1 -> Step 2
    res2 = client.get("/library/sql?tab=all_topics&topic=sql-intro-syntax")
    assert res2.status_code == 200
    html2 = res2.text
    assert "SQL Introduction &amp; Syntax" in html2 or "SQL Introduction & Syntax" in html2
    assert "Previous Topic" in html2
    assert "sql-what-is-database" in html2
    assert "Next Topic" in html2
    assert "sql-create-drop-database" in html2

    # Step 2 -> Step 3
    res3 = client.get("/library/sql?tab=all_topics&topic=sql-create-drop-database")
    assert res3.status_code == 200
    html3 = res3.text
    assert "SQL CREATE &amp; DROP DATABASE" in html3 or "SQL CREATE & DROP DATABASE" in html3
    assert "Previous Topic" in html3
    assert "sql-intro-syntax" in html3
    assert "Next Topic" in html3
    assert "sql-create-drop-table" in html3

    # Step 3 -> Step 4
    res4 = client.get("/library/sql?tab=all_topics&topic=sql-create-drop-table")
    assert res4.status_code == 200
    html4 = res4.text
    assert "SQL CREATE &amp; DROP TABLE" in html4 or "SQL CREATE & DROP TABLE" in html4
    assert "Previous Topic" in html4
    assert "sql-create-drop-database" in html4
    assert "Next Topic" in html4
    assert "sql-alter-truncate-table" in html4


def test_library_sql_interview_panel_isolation():
    """Verify viva interview traps remain in the dedicated Interview Questions panel."""
    response = client.get("/library/sql?tab=interview_questions")
    assert response.status_code == 200
    html = response.text
    assert "Top 45 SQL Viva" in html
    assert "Interview Questions (" in html


def test_library_sql_primary_foreign_key_published_note():
    """Verify published note for SQL Primary & Foreign Key rendering the skipped basics and composite key reality."""
    response = client.get("/library/sql/notes/sql-primary-foreign-key")
    assert response.status_code == 200
    html = response.text
    assert "SQL PRIMARY KEY &amp; FOREIGN KEY" in html or "SQL PRIMARY KEY & FOREIGN KEY" in html
    assert "Composite Primary Key" in html
    assert "Clustered Index" in html
    assert "Unindexed Foreign Key Lock Trap" in html
    assert "students" in html
    assert "student_enrollments" in html

