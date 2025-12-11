"""Authentication and dependency injection."""

from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from uuid import uuid4

from fastapi import Cookie, HTTPException, Request, Response

# In-memory session storage - sessions lost on restart
sessions: dict[str, dict] = {}


def create_session(user_id: str) -> str:
    """Create a new session for a user."""
    session_id = str(uuid4())
    sessions[session_id] = {
        "user_id": user_id,
        "expires": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return session_id


def delete_session(session_id: str) -> None:
    """Delete a session."""
    if session_id in sessions:
        del sessions[session_id]


def get_session(session_id: Optional[str]) -> Optional[dict]:
    """Get session data if valid."""
    if not session_id or session_id not in sessions:
        return None
    session = sessions[session_id]
    if session["expires"] < datetime.now(timezone.utc):
        del sessions[session_id]
        return None
    return session


async def get_current_user_id(
    session_id: Annotated[Optional[str], Cookie()] = None
) -> str:
    """Dependency to get the current user ID from session."""
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return session["user_id"]


async def get_optional_user_id(
    session_id: Annotated[Optional[str], Cookie()] = None
) -> Optional[str]:
    """Dependency to optionally get the current user ID."""
    session = get_session(session_id)
    return session["user_id"] if session else None


def set_session_cookie(response: Response, session_id: str) -> None:
    """Set the session cookie on a response."""
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=3600,
        samesite="lax",
    )


def clear_session_cookie(response: Response) -> None:
    """Clear the session cookie."""
    response.delete_cookie(key="session_id")


def is_htmx_request(request: Request) -> bool:
    """Check if the request is from HTMX."""
    return request.headers.get("HX-Request") == "true"
