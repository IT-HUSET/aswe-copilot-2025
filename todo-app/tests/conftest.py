"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh in-memory database for each test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with overridden database dependency."""
    from app.core.deps import sessions

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # Clear sessions before each test
    sessions.clear()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    sessions.clear()


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    from app.database import User

    user = User(
        email="test@example.com",
        password="testpass123",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def authenticated_client(client, test_user):
    """Create an authenticated test client."""
    from app.core.deps import create_session

    session_id = create_session(test_user.id)
    client.cookies.set("session_id", session_id)
    return client


@pytest.fixture
def test_list(db_session, test_user):
    """Create a test todo list."""
    from app.database import TodoList

    todo_list = TodoList(
        user_id=test_user.id,
        name="Test List",
        description="A test list",
        color="#3b82f6",
        position=0,
    )
    db_session.add(todo_list)
    db_session.commit()
    db_session.refresh(todo_list)
    return todo_list


@pytest.fixture
def test_todo(db_session, test_list):
    """Create a test todo item."""
    from app.database import Todo

    todo = Todo(
        list_id=test_list.id,
        title="Test Todo",
        note="A test note",
        priority="medium",
        position=0,
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo
