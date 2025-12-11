"""Integration tests for full user journeys."""

import pytest

from app.database import Todo, TodoList, User


class TestUserJourneys:
    """Full user journey integration tests."""

    def test_register_create_list_add_todo_logout_login_verify(self, client, db_session):
        """Test complete user journey: register -> add list -> add todo -> logout -> login -> verify."""
        # Register
        response = client.post(
            "/auth/register",
            data={
                "email": "journey@example.com",
                "password": "journey123",
                "confirm_password": "journey123",
            },
        )
        assert response.status_code == 200
        assert "session_id" in client.cookies

        # Create list
        response = client.post(
            "/api/lists",
            data={
                "name": "Journey List",
                "description": "Test journey",
                "color": "#10b981",
            },
        )
        assert response.status_code == 200

        # Get the created list
        created_list = db_session.query(TodoList).filter(TodoList.name == "Journey List").first()
        assert created_list is not None

        # Add todo
        response = client.post(
            "/api/todos",
            data={
                "list_id": created_list.id,
                "title": "Journey Todo",
            },
        )
        assert response.status_code == 200

        # Logout
        response = client.post("/auth/logout")
        assert response.status_code == 200

        # Login again
        response = client.post(
            "/auth/login",
            data={
                "email": "journey@example.com",
                "password": "journey123",
            },
        )
        assert response.status_code == 200

        # Verify data persisted
        response = client.get(f"/api/lists/{created_list.id}")
        assert response.status_code == 200
        assert b"Journey List" in response.content
        assert b"Journey Todo" in response.content

    def test_delete_list_cascades_to_todos(self, authenticated_client, test_user, db_session):
        """Test that deleting a list also deletes all its todos."""
        # Create list with multiple todos
        todo_list = TodoList(
            user_id=test_user.id,
            name="Cascade Test List",
            position=0,
        )
        db_session.add(todo_list)
        db_session.commit()

        # Add todos
        for i in range(5):
            todo = Todo(
                list_id=todo_list.id,
                title=f"Cascade Todo {i}",
                position=i,
            )
            db_session.add(todo)
        db_session.commit()

        # Verify todos exist
        todo_count = db_session.query(Todo).filter(Todo.list_id == todo_list.id).count()
        assert todo_count == 5

        # Delete list
        list_id = todo_list.id
        response = authenticated_client.delete(f"/api/lists/{list_id}")
        assert response.status_code == 200

        # Verify list deleted
        deleted_list = db_session.query(TodoList).filter(TodoList.id == list_id).first()
        assert deleted_list is None

        # Verify all todos deleted (CASCADE)
        remaining_todos = db_session.query(Todo).filter(Todo.list_id == list_id).count()
        assert remaining_todos == 0

    def test_delete_user_cascades_to_lists_and_todos(self, db_session):
        """Test that deleting a user cascades to all their lists and todos."""
        # Create user
        user = User(email="cascade@example.com", password="cascade123")
        db_session.add(user)
        db_session.commit()

        # Create lists with todos
        for i in range(2):
            todo_list = TodoList(
                user_id=user.id,
                name=f"User List {i}",
                position=i,
            )
            db_session.add(todo_list)
            db_session.commit()

            for j in range(3):
                todo = Todo(
                    list_id=todo_list.id,
                    title=f"User Todo {i}-{j}",
                    position=j,
                )
                db_session.add(todo)
        db_session.commit()

        # Verify data exists
        list_count = db_session.query(TodoList).filter(TodoList.user_id == user.id).count()
        assert list_count == 2

        # Delete user
        user_id = user.id
        db_session.delete(user)
        db_session.commit()

        # Verify all data deleted
        remaining_lists = db_session.query(TodoList).filter(TodoList.user_id == user_id).count()
        assert remaining_lists == 0

    def test_protected_route_redirect_with_next(self, client, test_user, db_session):
        """Test that protected routes redirect to login with next parameter."""
        # Create a list for the user
        todo_list = TodoList(
            user_id=test_user.id,
            name="Protected List",
            position=0,
        )
        db_session.add(todo_list)
        db_session.commit()

        # Try to access without authentication
        response = client.get(f"/app/lists/{todo_list.id}", follow_redirects=False)
        assert response.status_code == 302
        assert f"/login?next=/app/lists/{todo_list.id}" in response.headers["location"]

    def test_todo_completion_updates_count(self, authenticated_client, test_list, db_session):
        """Test that completing a todo updates the list count via OOB swap."""
        # Create todo
        todo = Todo(
            list_id=test_list.id,
            title="Count Test Todo",
            position=0,
        )
        db_session.add(todo)
        db_session.commit()

        # Toggle completion
        response = authenticated_client.patch(f"/api/todos/{todo.id}/toggle")
        assert response.status_code == 200

        # Response should include OOB swap for count
        assert b"hx-swap-oob" in response.content

    def test_todo_search_filters_correctly(self, authenticated_client, test_list, db_session):
        """Test that search filters todos correctly."""
        # Create todos with different titles
        todos_data = [
            "Buy groceries",
            "Buy new laptop",
            "Call mom",
            "Send email to boss",
            "Buy birthday gift",
        ]
        for i, title in enumerate(todos_data):
            todo = Todo(list_id=test_list.id, title=title, position=i)
            db_session.add(todo)
        db_session.commit()

        # Search for "buy"
        response = authenticated_client.get(
            f"/api/todos/search?list_id={test_list.id}&q=buy"
        )
        assert response.status_code == 200

        # Should find 3 todos with "buy" in title
        content = response.content.decode()
        assert "Buy groceries" in content
        assert "Buy new laptop" in content
        assert "Buy birthday gift" in content
        assert "Call mom" not in content
        assert "Send email" not in content
