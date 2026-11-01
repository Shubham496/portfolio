import sqlite3
import os
from contextlib import contextmanager

DB_FILE = os.getenv("DATABASE_FILE", "portfolio.db")

def init_todos_db():
    """Create the todos table if it doesn't already exist and seed default tasks."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT DEFAULT 'General',
                priority TEXT DEFAULT 'Medium',
                status TEXT DEFAULT 'pending',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)
        
        # Check if empty, seed our initial project milestones
        cursor.execute("SELECT COUNT(*) FROM project_todos")
        count = cursor.fetchone()[0]
        if count == 0:
            initial_todos = [
                ("Initialize FastAPI platform & Jinja2 templates", "Phase 1: Setup", "High", "completed", "Clean responsive dark theme with Tailwind CSS"),
                ("Set up GitHub repo & branch tracking", "Phase 1: Setup", "High", "completed", "Connected to Shubham496/portfolio"),
                ("Two-tier configuration (local.py & deployment.py)", "Phase 1: Setup", "High", "completed", "Auto-detects dev vs prod environment"),
                ("Deploy to Render & configure mythostech.in DNS", "Phase 1: Setup", "High", "completed", "A & CNAME records set in BigRock"),
                ("Build Project Action Tracker & To-Do Micro-App", "Phase 2: Apps", "High", "in-progress", "Self-hosting live interactive roadmap"),
                ("Build URL Shortener & Analytics micro-app", "Phase 2: Apps", "Medium", "pending", "Link redirection and click analytics"),
                ("Build JSON & API Schema inspector tool", "Phase 2: Apps", "Medium", "pending", "Formatting, validation, diff tools"),
                ("Integrate SQLite cloud persistence (Turso/Neon)", "Phase 3: Scale", "Medium", "pending", "Serverless cloud database connection"),
            ]
            cursor.executemany("""
                INSERT INTO project_todos (title, category, priority, status, notes)
                VALUES (?, ?, ?, ?, ?)
            """, initial_todos)
        conn.commit()

def get_todos(status_filter: str = "all", category_filter: str = "all"):
    """Fetch todos filtered by status or category."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM project_todos WHERE 1=1"
        params = []
        
        if status_filter != "all":
            query += " AND status = ?"
            params.append(status_filter)
            
        if category_filter != "all":
            query += " AND category = ?"
            params.append(category_filter)
            
        query += " ORDER BY CASE status WHEN 'in-progress' THEN 1 WHEN 'pending' THEN 2 WHEN 'completed' THEN 3 END, id DESC"
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def add_todo(title: str, category: str, priority: str, notes: str = ""):
    """Add a new task."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO project_todos (title, category, priority, status, notes)
            VALUES (?, ?, ?, 'pending', ?)
        """, (title.strip(), category.strip(), priority.strip(), notes.strip()))
        conn.commit()
        return cursor.lastrowid

def update_todo_status(todo_id: int, new_status: str):
    """Toggle or update status between pending, in-progress, completed."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        if new_status == "completed":
            cursor.execute("""
                UPDATE project_todos 
                SET status = ?, completed_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (new_status, todo_id))
        else:
            cursor.execute("""
                UPDATE project_todos 
                SET status = ?, completed_at = NULL 
                WHERE id = ?
            """, (new_status, todo_id))
        conn.commit()

def delete_todo(todo_id: int):
    """Delete a task."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM project_todos WHERE id = ?", (todo_id,))
        conn.commit()
