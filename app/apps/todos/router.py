from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.apps.todos.models import (
    init_todos_db,
    get_todos,
    add_todo,
    update_todo_status,
    delete_todo
)
from app.core.config import settings

# Initialize router
router = APIRouter(prefix="/apps/todos", tags=["To-Do Tracker App"])

# Point templates to include both app/apps/todos/templates and global app/templates
templates = Jinja2Templates(directory=["app/apps/todos/templates", "app/templates"])

# Ensure DB is created on load
init_todos_db()

@router.get("", response_class=HTMLResponse)
async def list_todos_page(request: Request, status: str = "all", category: str = "all"):
    """Render the interactive To-Do and Sprint Tracker app."""
    all_todos = get_todos(status_filter="all")
    filtered_todos = get_todos(status_filter=status, category_filter=category)
    
    # Calculate stats
    stats = {
        "total": len(all_todos),
        "completed": len([t for t in all_todos if t["status"] == "completed"]),
        "in_progress": len([t for t in all_todos if t["status"] == "in-progress"]),
        "pending": len([t for t in all_todos if t["status"] == "pending"])
    }
    
    return templates.TemplateResponse(
        request=request,
        name="todos.html",
        context={
            "settings": settings,
            "title": "Project Task & Sprint Tracker",
            "todos": filtered_todos,
            "stats": stats,
            "current_filter": status,
        }
    )

@router.post("/add")
async def add_new_todo(
    title: str = Form(...),
    category: str = Form("Phase 2: Apps"),
    priority: str = Form("Medium"),
    notes: str = Form("")
):
    """Add a new task to the database."""
    add_todo(title=title, category=category, priority=priority, notes=notes)
    return RedirectResponse(url="/apps/todos", status_code=303)

@router.post("/status/{todo_id}")
async def change_status(todo_id: int, status: str = Form(...)):
    """Update status of a task."""
    update_todo_status(todo_id=todo_id, new_status=status)
    return RedirectResponse(url="/apps/todos", status_code=303)

@router.post("/delete/{todo_id}")
async def remove_todo(todo_id: int):
    """Delete a task from the database."""
    delete_todo(todo_id=todo_id)
    return RedirectResponse(url="/apps/todos", status_code=303)
