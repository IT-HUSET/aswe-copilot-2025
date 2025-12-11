"""Todo item routes."""

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.deps import get_current_user_id
from app.database import Todo, TodoList, get_db
from app.utils import format_date, format_date_input, is_due_today, is_overdue

router = APIRouter(prefix="/api/todos", tags=["todos"])
templates = Jinja2Templates(directory="src/app/templates")

# Add utility functions to template globals
templates.env.globals["is_overdue"] = is_overdue
templates.env.globals["is_due_today"] = is_due_today
templates.env.globals["format_date"] = format_date
templates.env.globals["format_date_input"] = format_date_input


def _verify_list_access(db: Session, list_id: str, user_id: str) -> TodoList | None:
    """Verify user owns the list and return it."""
    return db.query(TodoList).filter(
        TodoList.id == list_id, TodoList.user_id == user_id
    ).first()


def _get_list_todo_count(db: Session, list_id: str) -> int:
    """Get the count of incomplete todos in a list."""
    return db.query(func.count(Todo.id)).filter(
        Todo.list_id == list_id, Todo.is_completed == False
    ).scalar()


@router.get("/search", response_class=HTMLResponse)
async def search_todos(
    request: Request,
    user_id: Annotated[str, Depends(get_current_user_id)],
    list_id: str,
    q: str = "",
    db: Session = Depends(get_db),
):
    """Search todos by title in a specific list."""
    # Verify list access
    list_obj = _verify_list_access(db, list_id, user_id)
    if not list_obj:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "List not found"},
            status_code=404,
        )

    query = db.query(Todo).filter(Todo.list_id == list_id)

    if q.strip():
        query = query.filter(Todo.title.ilike(f"%{q.strip()}%"))

    todos = query.order_by(Todo.position).all()

    return templates.TemplateResponse(
        request=request,
        name="partials/todos_list.html",
        context={"todos": todos, "list": list_obj, "search_query": q},
    )


@router.post("", response_class=HTMLResponse)
async def create_todo(
    request: Request,
    user_id: Annotated[str, Depends(get_current_user_id)],
    list_id: Annotated[str, Form()],
    title: Annotated[str, Form()],
    db: Session = Depends(get_db),
):
    """Create a new todo (quick add with title only)."""
    # Verify list access
    list_obj = _verify_list_access(db, list_id, user_id)
    if not list_obj:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "List not found"},
            status_code=404,
        )

    # Validate title
    if not title.strip():
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Title is required"},
        )

    if len(title) > 200:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Title must be 200 characters or less"},
        )

    # Calculate next position
    max_pos = (
        db.query(func.max(Todo.position))
        .filter(Todo.list_id == list_id)
        .scalar()
    )
    new_pos = (max_pos or -1) + 1

    # Create todo - FIX: Added priority="low" as default
    todo = Todo(
        list_id=list_id,
        title=title.strip(),
        position=new_pos,
        priority="low",
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)

    # Get updated count for OOB swap
    count = _get_list_todo_count(db, list_id)

    return templates.TemplateResponse(
        request=request,
        name="partials/todo_item_with_oob.html",
        context={"todo": todo, "list": list_obj, "count": count},
    )


@router.get("/{todo_id}", response_class=HTMLResponse)
async def get_todo(
    request: Request,
    todo_id: str,
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Session = Depends(get_db),
):
    """Get a single todo item."""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Todo not found"},
            status_code=404,
        )

    # Verify access
    list_obj = _verify_list_access(db, todo.list_id, user_id)
    if not list_obj:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Not authorized"},
            status_code=403,
        )

    return templates.TemplateResponse(
        request=request,
        name="partials/todo_item.html",
        context={"todo": todo},
    )


@router.put("/{todo_id}", response_class=HTMLResponse)
async def update_todo(
    request: Request,
    todo_id: str,
    user_id: Annotated[str, Depends(get_current_user_id)],
    title: Annotated[str, Form()],
    note: Annotated[str | None, Form()] = None,
    due_date: Annotated[str | None, Form()] = None,
    priority: Annotated[str, Form()] = "low",
    db: Session = Depends(get_db),
):
    """Update a todo item."""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Todo not found"},
            status_code=404,
        )

    # Verify access
    list_obj = _verify_list_access(db, todo.list_id, user_id)
    if not list_obj:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Not authorized"},
            status_code=403,
        )

    # Validate title
    if not title.strip():
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Title is required"},
        )

    if len(title) > 200:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Title must be 200 characters or less"},
        )

    # Validate priority
    if priority not in ("low", "medium", "high"):
        priority = "low"

    # Update fields
    todo.title = title.strip()
    todo.note = note.strip() if note else None

    # Parse due date - FIX: Correct format for HTML date inputs
    if due_date and due_date.strip():
        try:
            todo.due_date = datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            pass  # Keep existing
    else:
        todo.due_date = None

    todo.priority = priority
    db.commit()
    db.refresh(todo)

    return templates.TemplateResponse(
        request=request,
        name="partials/todo_item.html",
        context={"todo": todo},
    )


@router.patch("/{todo_id}/toggle", response_class=HTMLResponse)
async def toggle_todo(
    request: Request,
    todo_id: str,
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Session = Depends(get_db),
):
    """Toggle todo completion status."""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Todo not found"},
            status_code=404,
        )

    # Verify access
    list_obj = _verify_list_access(db, todo.list_id, user_id)
    if not list_obj:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Not authorized"},
            status_code=403,
        )

    # Toggle completion
    todo.is_completed = not todo.is_completed
    todo.completed_at = datetime.now(timezone.utc) if todo.is_completed else None
    db.commit()
    db.refresh(todo)

    # Get updated count for OOB swap
    count = _get_list_todo_count(db, todo.list_id)

    return templates.TemplateResponse(
        request=request,
        name="partials/todo_item_with_oob.html",
        context={"todo": todo, "list": list_obj, "count": count},
    )


# FIX: Added response_class=HTMLResponse for proper HTMX OOB swap
@router.delete("/{todo_id}", response_class=HTMLResponse)
async def delete_todo(
    request: Request,
    todo_id: str,
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Session = Depends(get_db),
):
    """Delete a todo item."""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return Response(status_code=404)

    # Verify access
    list_obj = _verify_list_access(db, todo.list_id, user_id)
    if not list_obj:
        return Response(status_code=403)

    list_id = todo.list_id
    db.delete(todo)
    db.commit()

    # Get updated count for OOB swap
    count = _get_list_todo_count(db, list_id)

    return templates.TemplateResponse(
        request=request,
        name="partials/todo_deleted_oob.html",
        context={"list_id": list_id, "count": count},
    )


@router.post("/{todo_id}/reorder")
async def reorder_todo(
    request: Request,
    todo_id: str,
    user_id: Annotated[str, Depends(get_current_user_id)],
    position: Annotated[int, Form()],
    db: Session = Depends(get_db),
):
    """Reorder a todo to a new position (drag-drop)."""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return Response(status_code=404)

    # Verify access
    list_obj = _verify_list_access(db, todo.list_id, user_id)
    if not list_obj:
        return Response(status_code=403)

    old_position = todo.position
    new_position = position

    if old_position == new_position:
        return Response(status_code=200)

    # Get all todos in the list ordered by position
    todos = (
        db.query(Todo)
        .filter(Todo.list_id == todo.list_id)
        .order_by(Todo.position)
        .all()
    )

    # Reorder: shift items between old and new positions
    if old_position < new_position:
        # Moving down: shift items up
        for t in todos:
            if old_position < t.position <= new_position:
                t.position -= 1
    else:
        # Moving up: shift items down
        for t in todos:
            if new_position <= t.position < old_position:
                t.position += 1

    todo.position = new_position
    db.commit()

    return Response(status_code=200)
