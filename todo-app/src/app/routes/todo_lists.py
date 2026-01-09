"""Todo list routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.deps import get_current_user_id
from app.database import Todo, TodoList, get_db
from app.utils import format_date, format_date_input, is_due_today, is_overdue

router = APIRouter(prefix="/api/lists", tags=["lists"])
templates = Jinja2Templates(directory="src/app/templates")

# Add utility functions to template globals
templates.env.globals["is_overdue"] = is_overdue
templates.env.globals["is_due_today"] = is_due_today
templates.env.globals["format_date"] = format_date
templates.env.globals["format_date_input"] = format_date_input


@router.get("", response_class=HTMLResponse)
async def get_lists(
    request: Request,
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Session = Depends(get_db),
):
    """Get all lists for sidebar."""
    lists = (
        db.query(TodoList)
        .filter(TodoList.user_id == user_id)
        .order_by(TodoList.position)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="partials/sidebar_lists.html",
        context={"lists": lists, "active_list": None},
    )


@router.post("", response_class=HTMLResponse)
async def create_list(
    request: Request,
    user_id: Annotated[str, Depends(get_current_user_id)],
    name: Annotated[str, Form()],
    description: Annotated[str | None, Form()] = None,
    color: Annotated[str, Form()] = "#3b82f6",
    db: Session = Depends(get_db),
):
    """Create a new todo list."""
    # Validate name
    if not name.strip():
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Name is required"},
        )

    if len(name) > 100:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Name must be 100 characters or less"},
        )

    # Calculate next position
    max_pos = (
        db.query(func.max(TodoList.position))
        .filter(TodoList.user_id == user_id)
        .scalar()
    )
    new_pos = (max_pos or -1) + 1

    # Create list
    new_list = TodoList(
        user_id=user_id,
        name=name.strip(),
        description=description.strip() if description else None,
        color=color,
        position=new_pos,
    )
    db.add(new_list)
    db.commit()
    db.refresh(new_list)

    # Return list item for sidebar and redirect to the new list
    response = templates.TemplateResponse(
        request=request,
        name="partials/todo_list_item.html",
        context={"list": new_list, "active_list": None},
    )
    response.headers["HX-Redirect"] = f"/app/lists/{new_list.id}"
    return response


@router.get("/{list_id}", response_class=HTMLResponse)
async def get_list(
    request: Request,
    list_id: str,
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Session = Depends(get_db),
):
    """Get a specific list and its todos."""
    list_obj = db.query(TodoList).filter(
        TodoList.id == list_id, TodoList.user_id == user_id
    ).first()

    if not list_obj:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "List not found"},
            status_code=404,
        )

    todos = (
        db.query(Todo)
        .filter(Todo.list_id == list_id)
        .order_by(Todo.position)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="partials/todo_list_content.html",
        context={"list": list_obj, "todos": todos},
    )


@router.put("/{list_id}", response_class=HTMLResponse)
async def update_list(
    request: Request,
    list_id: str,
    user_id: Annotated[str, Depends(get_current_user_id)],
    name: Annotated[str, Form()],
    description: Annotated[str | None, Form()] = None,
    color: Annotated[str, Form()] = "#3b82f6",
    db: Session = Depends(get_db),
):
    """Update a todo list."""
    list_obj = db.query(TodoList).filter(
        TodoList.id == list_id, TodoList.user_id == user_id
    ).first()

    if not list_obj:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "List not found"},
            status_code=404,
        )

    # Validate name
    if not name.strip():
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Name is required"},
        )

    if len(name) > 100:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Name must be 100 characters or less"},
        )

    list_obj.name = name.strip()
    list_obj.description = description.strip() if description else None
    list_obj.color = color
    db.commit()
    db.refresh(list_obj)

    # Get updated sidebar
    lists = (
        db.query(TodoList)
        .filter(TodoList.user_id == user_id)
        .order_by(TodoList.position)
        .all()
    )

    response = templates.TemplateResponse(
        request=request,
        name="partials/todo_list_item.html",
        context={"list": list_obj, "active_list": list_obj},
    )
    return response


@router.delete("/{list_id}")
async def delete_list(
    request: Request,
    list_id: str,
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Session = Depends(get_db),
):
    """Delete a todo list (CASCADE deletes todos)."""
    list_obj = db.query(TodoList).filter(
        TodoList.id == list_id, TodoList.user_id == user_id
    ).first()

    if not list_obj:
        return Response(status_code=404)

    db.delete(list_obj)
    db.commit()

    response = Response(status_code=200)
    response.headers["HX-Redirect"] = "/app"
    return response


@router.post("/reorder", response_class=HTMLResponse)
async def reorder_lists(
    request: Request,
    user_id: Annotated[str, Depends(get_current_user_id)],
    list_id: Annotated[list[str], Form()],
    db: Session = Depends(get_db),
):
    """Reorder lists based on drag-and-drop. list_id contains IDs in new order."""
    # Update positions based on order received
    for position, lid in enumerate(list_id):
        list_obj = db.query(TodoList).filter(
            TodoList.id == lid, TodoList.user_id == user_id
        ).first()
        if list_obj:
            list_obj.position = position

    db.commit()

    # Return updated sidebar lists
    lists = (
        db.query(TodoList)
        .filter(TodoList.user_id == user_id)
        .order_by(TodoList.position)
        .all()
    )

    # Determine active list from referer URL
    referer = request.headers.get("referer", "")
    active_list_id = None
    if "/app/lists/" in referer:
        active_list_id = referer.split("/app/lists/")[-1].split("?")[0]

    active_list = None
    if active_list_id:
        active_list = db.query(TodoList).filter(TodoList.id == active_list_id).first()

    return templates.TemplateResponse(
        request=request,
        name="partials/sidebar_lists.html",
        context={"lists": lists, "active_list": active_list},
    )
