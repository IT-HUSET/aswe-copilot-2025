"""SQLite database configuration and models."""

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.pool import NullPool

DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=NullPool,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def generate_uuid() -> str:
    return str(uuid4())


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)  # Plain text - educational only!
    created_at = Column(DateTime, default=utc_now)

    todo_lists = relationship(
        "TodoList", back_populates="user", cascade="all, delete-orphan"
    )


class TodoList(Base):
    __tablename__ = "todo_lists"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String(7), default="#3b82f6")  # Hex color
    position = Column(Integer, default=0)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="todo_lists")
    todos = relationship("Todo", back_populates="todo_list", cascade="all, delete-orphan")

    __table_args__ = (Index("ix_todo_lists_user_position", "user_id", "position"),)


class Todo(Base):
    __tablename__ = "todos"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    list_id = Column(String(36), ForeignKey("todo_lists.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    note = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority = Column(String(10), default="low")  # low, medium, high
    position = Column(Integer, default=0)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    todo_list = relationship("TodoList", back_populates="todos")

    __table_args__ = (Index("ix_todos_list_position", "list_id", "position"),)


def init_db() -> None:
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
