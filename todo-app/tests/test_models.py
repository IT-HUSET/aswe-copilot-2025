"""Tests for Pydantic models."""

from datetime import date

import pytest
from pydantic import ValidationError

from app.models.auth import LoginRequest, RegisterRequest
from app.models.todo import TodoCreate, TodoUpdate
from app.models.todo_list import TodoListCreate, TodoListUpdate


class TestAuthModels:
    """Tests for authentication models."""

    def test_login_request_valid(self):
        """Test valid login request."""
        data = LoginRequest(email="test@example.com", password="password123")
        assert data.email == "test@example.com"
        assert data.password == "password123"

    def test_login_request_invalid_email(self):
        """Test login with invalid email."""
        with pytest.raises(ValidationError):
            LoginRequest(email="notanemail", password="password123")

    def test_register_request_valid(self):
        """Test valid registration request."""
        data = RegisterRequest(
            email="test@example.com",
            password="password123",
            confirm_password="password123",
        )
        assert data.email == "test@example.com"
        assert data.password == "password123"

    def test_register_request_password_mismatch(self):
        """Test registration with mismatched passwords."""
        with pytest.raises(ValidationError) as exc_info:
            RegisterRequest(
                email="test@example.com",
                password="password123",
                confirm_password="different123",
            )
        assert "Passwords do not match" in str(exc_info.value)

    def test_register_request_short_password(self):
        """Test registration with short password."""
        with pytest.raises(ValidationError):
            RegisterRequest(
                email="test@example.com",
                password="short",
                confirm_password="short",
            )


class TestTodoListModels:
    """Tests for todo list models."""

    def test_todo_list_create_valid(self):
        """Test valid todo list creation."""
        data = TodoListCreate(name="My List", description="A list")
        assert data.name == "My List"
        assert data.description == "A list"
        assert data.color == "#3b82f6"

    def test_todo_list_create_custom_color(self):
        """Test todo list with custom color."""
        data = TodoListCreate(name="My List", color="#ff0000")
        assert data.color == "#ff0000"

    def test_todo_list_create_invalid_color(self):
        """Test todo list with invalid color."""
        with pytest.raises(ValidationError):
            TodoListCreate(name="My List", color="red")

    def test_todo_list_create_empty_name(self):
        """Test todo list with empty name."""
        with pytest.raises(ValidationError):
            TodoListCreate(name="   ")

    def test_todo_list_create_long_name(self):
        """Test todo list with name exceeding max length."""
        with pytest.raises(ValidationError):
            TodoListCreate(name="a" * 101)

    def test_todo_list_update_partial(self):
        """Test partial update of todo list."""
        data = TodoListUpdate(name="Updated Name")
        assert data.name == "Updated Name"
        assert data.description is None
        assert data.color is None


class TestTodoModels:
    """Tests for todo models."""

    def test_todo_create_valid(self):
        """Test valid todo creation."""
        data = TodoCreate(title="My Todo")
        assert data.title == "My Todo"
        assert data.priority == "low"

    def test_todo_create_with_all_fields(self):
        """Test todo creation with all fields."""
        data = TodoCreate(
            title="My Todo",
            note="A note",
            due_date=date(2025, 12, 31),
            priority="high",
        )
        assert data.title == "My Todo"
        assert data.note == "A note"
        assert data.due_date == date(2025, 12, 31)
        assert data.priority == "high"

    def test_todo_create_due_date_from_string(self):
        """Test todo with due date from string."""
        data = TodoCreate(title="My Todo", due_date="2025-12-31")
        assert data.due_date == date(2025, 12, 31)

    def test_todo_create_empty_title(self):
        """Test todo with empty title."""
        with pytest.raises(ValidationError):
            TodoCreate(title="   ")

    def test_todo_create_long_title(self):
        """Test todo with title exceeding max length."""
        with pytest.raises(ValidationError):
            TodoCreate(title="a" * 201)

    def test_todo_create_invalid_priority(self):
        """Test todo with invalid priority."""
        with pytest.raises(ValidationError):
            TodoCreate(title="My Todo", priority="urgent")

    def test_todo_update_partial(self):
        """Test partial update of todo."""
        data = TodoUpdate(title="Updated Title")
        assert data.title == "Updated Title"
        assert data.note is None
        assert data.is_completed is None

    def test_todo_update_clear_due_date(self):
        """Test clearing due date via empty string."""
        data = TodoUpdate(due_date="")
        assert data.due_date is None
