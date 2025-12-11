"""Tests for todo list routes."""

import pytest

from app.database import Todo, TodoList


class TestTodoLists:
    """Tests for todo list CRUD operations."""

    def test_create_list(self, authenticated_client, test_user, db_session):
        """Test creating a new todo list."""
        response = authenticated_client.post(
            "/api/lists",
            data={
                "name": "New List",
                "description": "A new list",
                "color": "#ff0000",
            },
        )
        assert response.status_code == 200
        assert "HX-Redirect" in response.headers

        # Verify in database
        created = db_session.query(TodoList).filter(TodoList.name == "New List").first()
        assert created is not None
        assert created.description == "A new list"
        assert created.color == "#ff0000"
        assert created.user_id == test_user.id

    def test_create_list_empty_name(self, authenticated_client):
        """Test creating list with empty name fails."""
        response = authenticated_client.post(
            "/api/lists",
            data={
                "name": "   ",
            },
        )
        assert response.status_code == 200
        assert b"required" in response.content

    def test_get_list(self, authenticated_client, test_list):
        """Test getting a specific list."""
        response = authenticated_client.get(f"/api/lists/{test_list.id}")
        assert response.status_code == 200
        assert test_list.name.encode() in response.content

    def test_get_list_not_found(self, authenticated_client):
        """Test getting a non-existent list."""
        response = authenticated_client.get("/api/lists/nonexistent-id")
        assert response.status_code == 404

    def test_update_list(self, authenticated_client, test_list, db_session):
        """Test updating a list."""
        response = authenticated_client.put(
            f"/api/lists/{test_list.id}",
            data={
                "name": "Updated Name",
                "description": "Updated description",
                "color": "#00ff00",
            },
        )
        assert response.status_code == 200

        # Verify in database
        db_session.refresh(test_list)
        assert test_list.name == "Updated Name"
        assert test_list.description == "Updated description"
        assert test_list.color == "#00ff00"

    def test_delete_list(self, authenticated_client, test_list, db_session):
        """Test deleting a list."""
        list_id = test_list.id
        response = authenticated_client.delete(f"/api/lists/{list_id}")
        assert response.status_code == 200
        assert "HX-Redirect" in response.headers

        # Verify deleted
        deleted = db_session.query(TodoList).filter(TodoList.id == list_id).first()
        assert deleted is None

    def test_delete_list_cascades_todos(self, authenticated_client, test_list, db_session):
        """Test that deleting a list also deletes its todos."""
        # Create some todos in the list
        for i in range(3):
            todo = Todo(
                list_id=test_list.id,
                title=f"Todo {i}",
                position=i,
            )
            db_session.add(todo)
        db_session.commit()

        # Verify todos exist
        todo_count = db_session.query(Todo).filter(Todo.list_id == test_list.id).count()
        assert todo_count == 3

        # Delete the list
        list_id = test_list.id
        response = authenticated_client.delete(f"/api/lists/{list_id}")
        assert response.status_code == 200

        # Verify todos are deleted (CASCADE)
        remaining = db_session.query(Todo).filter(Todo.list_id == list_id).count()
        assert remaining == 0

    def test_reorder_lists(self, authenticated_client, test_user, db_session):
        """Test reordering lists via drag-and-drop."""
        # Create three lists
        list1 = TodoList(user_id=test_user.id, name="List 1", position=0)
        list2 = TodoList(user_id=test_user.id, name="List 2", position=1)
        list3 = TodoList(user_id=test_user.id, name="List 3", position=2)
        db_session.add_all([list1, list2, list3])
        db_session.commit()

        # Reorder: List 3, List 1, List 2
        response = authenticated_client.post(
            "/api/lists/reorder",
            data={"list_id": [str(list3.id), str(list1.id), str(list2.id)]},
        )
        assert response.status_code == 200

        # Verify new positions
        db_session.refresh(list1)
        db_session.refresh(list2)
        db_session.refresh(list3)
        assert list3.position == 0
        assert list1.position == 1
        assert list2.position == 2
