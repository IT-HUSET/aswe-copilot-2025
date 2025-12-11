"""Shared utility functions for templates and routes."""

from datetime import date, datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.database import Todo


def is_overdue(todo: "Todo") -> bool:
    """Return True if due_date < today AND not completed."""
    if todo.is_completed or not todo.due_date:
        return False
    today = date.today()
    # FIX: Convert datetime to date for proper comparison
    due = todo.due_date.date() if isinstance(todo.due_date, datetime) else todo.due_date
    return due < today


def is_due_today(todo: "Todo") -> bool:
    """Return True if due_date == today."""
    if not todo.due_date:
        return False
    today = date.today()
    # FIX: Convert datetime to date for proper comparison
    due = todo.due_date.date() if isinstance(todo.due_date, datetime) else todo.due_date
    return due == today


def format_date(dt: datetime | date | None) -> str:
    """Format a date for display."""
    if dt is None:
        return ""
    if isinstance(dt, datetime):
        dt = dt.date()
    return dt.strftime("%b %d, %Y")


def format_date_input(dt: datetime | date | None) -> str:
    """Format a date for HTML date input (YYYY-MM-DD)."""
    if dt is None:
        return ""
    if isinstance(dt, datetime):
        dt = dt.date()
    return dt.strftime("%Y-%m-%d")
