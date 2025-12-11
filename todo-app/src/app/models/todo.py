"""Pydantic models for todos."""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TodoCreate(BaseModel):
    title: str = Field(max_length=200)
    note: Optional[str] = None
    due_date: Optional[date] = None
    priority: str = Field(default="low", pattern=r"^(low|medium|high)$")

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("due_date", mode="before")
    @classmethod
    def parse_due_date(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            return datetime.strptime(v, "%Y-%m-%d").date()
        return v


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200)
    note: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[date] = None
    priority: Optional[str] = Field(default=None, pattern=r"^(low|medium|high)$")
    position: Optional[int] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip() if v else v

    @field_validator("due_date", mode="before")
    @classmethod
    def parse_due_date(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            return datetime.strptime(v, "%Y-%m-%d").date()
        return v
