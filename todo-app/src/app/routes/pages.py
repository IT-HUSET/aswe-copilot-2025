"""Page routes - HTML page rendering."""

from typing import Annotated, Optional

from fastapi import APIRouter, Cookie, Depends, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.deps import get_optional_user_id, get_session
from app.database import Todo, TodoList, User, get_db
from app.utils import format_date, format_date_input, is_due_today, is_overdue

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="src/app/templates")

# Add utility functions to template globals
templates.env.globals["is_overdue"] = is_overdue
templates.env.globals["is_due_today"] = is_due_today
templates.env.globals["format_date"] = format_date
templates.env.globals["format_date_input"] = format_date_input


@router.get("/", response_class=HTMLResponse)
async def root(
    session_id: Annotated[Optional[str], Cookie()] = None,
):
    """Root route - redirect based on auth status."""
    session = get_session(session_id)
    if session:
        return RedirectResponse(url="/app", status_code=302)
    return RedirectResponse(url="/login", status_code=302)


@router.get("/login", response_class=HTMLResponse)
async def login_page(
    request: Request,
    next: Annotated[str, Query()] = "/app",
    session_id: Annotated[Optional[str], Cookie()] = None,
):
    """Login page."""
    session = get_session(session_id)
    if session:
        return RedirectResponse(url="/app", status_code=302)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"next": next},
    )


@router.get("/register", response_class=HTMLResponse)
async def register_page(
    request: Request,
    session_id: Annotated[Optional[str], Cookie()] = None,
):
    """Registration page."""
    session = get_session(session_id)
    if session:
        return RedirectResponse(url="/app", status_code=302)

    return templates.TemplateResponse(
        request=request,
        name="register.html",
    )


@router.get("/app", response_class=HTMLResponse)
async def app_page(
    request: Request,
    session_id: Annotated[Optional[str], Cookie()] = None,
    db: Session = Depends(get_db),
):
    """Main application page."""
    session = get_session(session_id)
    if not session:
        return RedirectResponse(url="/login?next=/app", status_code=302)

    user_id = session["user_id"]
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    # Get user's lists with todo counts
    lists = (
        db.query(TodoList)
        .filter(TodoList.user_id == user_id)
        .order_by(TodoList.position)
        .all()
    )

    # Auto-select first list if available
    if lists:
        return RedirectResponse(url=f"/app/lists/{lists[0].id}", status_code=302)

    return templates.TemplateResponse(
        request=request,
        name="app.html",
        context={
            "user": user,
            "lists": lists,
            "active_list": None,
            "todos": [],
        },
    )


@router.get("/app/lists/{list_id}", response_class=HTMLResponse)
async def app_list_page(
    request: Request,
    list_id: str,
    session_id: Annotated[Optional[str], Cookie()] = None,
    db: Session = Depends(get_db),
):
    """Main app page with a specific list selected."""
    session = get_session(session_id)
    if not session:
        return RedirectResponse(url=f"/login?next=/app/lists/{list_id}", status_code=302)

    user_id = session["user_id"]
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    # Get all lists
    lists = (
        db.query(TodoList)
        .filter(TodoList.user_id == user_id)
        .order_by(TodoList.position)
        .all()
    )

    # Get the active list
    active_list = db.query(TodoList).filter(
        TodoList.id == list_id, TodoList.user_id == user_id
    ).first()

    if not active_list:
        return RedirectResponse(url="/app", status_code=302)

    # Get todos for the active list
    todos = (
        db.query(Todo)
        .filter(Todo.list_id == list_id)
        .order_by(Todo.position)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="app.html",
        context={
            "user": user,
            "lists": lists,
            "active_list": active_list,
            "todos": todos,
        },
    )
