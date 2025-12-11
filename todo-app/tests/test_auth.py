"""Tests for authentication routes."""

import pytest

from app.core.deps import sessions


class TestAuth:
    """Tests for authentication flows."""

    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post(
            "/auth/register",
            data={
                "email": "new@example.com",
                "password": "password123",
                "confirm_password": "password123",
            },
        )
        assert response.status_code == 200
        assert "HX-Redirect" in response.headers

    def test_register_duplicate_email(self, client, test_user):
        """Test registration with existing email."""
        response = client.post(
            "/auth/register",
            data={
                "email": test_user.email,
                "password": "password123",
                "confirm_password": "password123",
            },
        )
        assert response.status_code == 200
        assert b"already registered" in response.content

    def test_register_password_mismatch(self, client):
        """Test registration with mismatched passwords."""
        response = client.post(
            "/auth/register",
            data={
                "email": "new@example.com",
                "password": "password123",
                "confirm_password": "different123",
            },
        )
        assert response.status_code == 200
        assert b"do not match" in response.content

    def test_register_short_password(self, client):
        """Test registration with short password."""
        response = client.post(
            "/auth/register",
            data={
                "email": "new@example.com",
                "password": "short",
                "confirm_password": "short",
            },
        )
        assert response.status_code == 200
        assert b"at least 6" in response.content

    def test_login_success(self, client, test_user):
        """Test successful login."""
        response = client.post(
            "/auth/login",
            data={
                "email": test_user.email,
                "password": "testpass123",
            },
        )
        assert response.status_code == 200
        assert "HX-Redirect" in response.headers
        assert "session_id" in response.cookies

    def test_login_invalid_password(self, client, test_user):
        """Test login with wrong password."""
        response = client.post(
            "/auth/login",
            data={
                "email": test_user.email,
                "password": "wrongpassword",
            },
        )
        assert response.status_code == 200
        assert b"Invalid" in response.content

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user."""
        response = client.post(
            "/auth/login",
            data={
                "email": "noone@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 200
        assert b"Invalid" in response.content

    def test_login_with_next_redirect(self, client, test_user):
        """Test login redirects to next parameter."""
        response = client.post(
            "/auth/login",
            data={
                "email": test_user.email,
                "password": "testpass123",
                "next": "/app/lists/test",
            },
        )
        assert response.status_code == 200
        assert response.headers.get("HX-Redirect") == "/app/lists/test"

    def test_login_blocks_open_redirect(self, client, test_user):
        """Test login blocks open redirect attempts."""
        # Test external URL
        response = client.post(
            "/auth/login",
            data={
                "email": test_user.email,
                "password": "testpass123",
                "next": "https://evil.com",
            },
        )
        assert response.status_code == 200
        assert response.headers.get("HX-Redirect") == "/app"

        # Test protocol-relative URL
        response = client.post(
            "/auth/login",
            data={
                "email": test_user.email,
                "password": "testpass123",
                "next": "//evil.com",
            },
        )
        assert response.status_code == 200
        assert response.headers.get("HX-Redirect") == "/app"

    def test_logout(self, authenticated_client):
        """Test logout clears session."""
        response = authenticated_client.post("/auth/logout")
        assert response.status_code == 200
        assert response.headers.get("HX-Redirect") == "/login"


class TestProtectedRoutes:
    """Tests for protected route access."""

    def test_app_requires_auth(self, client):
        """Test /app redirects to login when not authenticated."""
        response = client.get("/app", follow_redirects=False)
        assert response.status_code == 302
        assert "/login" in response.headers["location"]

    def test_app_accessible_when_authenticated(self, authenticated_client):
        """Test /app is accessible when authenticated."""
        response = authenticated_client.get("/app")
        assert response.status_code == 200

    def test_api_requires_auth(self, client):
        """Test API routes redirect to login when not authenticated."""
        # The app redirects unauthenticated requests to login page
        # For browser requests, this provides a better UX than 401
        response = client.get("/api/lists", follow_redirects=False)
        assert response.status_code == 302
        assert "/login" in response.headers["location"]
