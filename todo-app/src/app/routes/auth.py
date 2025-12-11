"""Authentication routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr, ValidationError
from sqlalchemy.orm import Session

from app.core.deps import (
    clear_session_cookie,
    create_session,
    delete_session,
    get_optional_user_id,
    is_htmx_request,
    set_session_cookie,
)
from app.database import User, get_db

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="src/app/templates")


def is_safe_redirect(url: str) -> bool:
    """Validate redirect URL to prevent open redirect attacks."""
    if not url:
        return False
    # Must start with / and not contain // (which could be //evil.com)
    return url.startswith("/") and not url.startswith("//") and "://" not in url


@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    next: Annotated[str, Form()] = "/app",
    db: Session = Depends(get_db),
):
    """Handle login form submission."""
    # Validate email format
    try:
        EmailStr._validate(email)
    except Exception:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Invalid email format"},
        )

    # Find user
    user = db.query(User).filter(User.email == email).first()
    if not user or user.password != password:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Invalid email or password"},
        )

    # Create session
    session_id = create_session(user.id)
    response = Response(status_code=200)
    set_session_cookie(response, session_id)
    # Validate redirect URL to prevent open redirect attacks
    redirect_url = next if is_safe_redirect(next) else "/app"
    response.headers["HX-Redirect"] = redirect_url
    return response


@router.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    confirm_password: Annotated[str, Form()],
    db: Session = Depends(get_db),
):
    """Handle registration form submission."""
    # Validate email format
    try:
        EmailStr._validate(email)
    except Exception:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Invalid email format"},
        )

    # Validate password length
    if len(password) < 6:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Password must be at least 6 characters"},
        )

    # Check passwords match
    if password != confirm_password:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Passwords do not match"},
        )

    # Check if user exists
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={"error": "Email already registered"},
        )

    # Create user
    user = User(email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Auto-login after registration
    session_id = create_session(user.id)
    response = Response(status_code=200)
    set_session_cookie(response, session_id)
    response.headers["HX-Redirect"] = "/app"
    return response


@router.post("/logout")
async def logout(
    request: Request,
    session_id: Annotated[str | None, Depends(get_optional_user_id)] = None,
):
    """Handle logout."""
    # Get session_id from cookie directly for deletion
    cookie_session_id = request.cookies.get("session_id")
    if cookie_session_id:
        delete_session(cookie_session_id)

    response = Response(status_code=200)
    clear_session_cookie(response)
    response.headers["HX-Redirect"] = "/login"
    return response
