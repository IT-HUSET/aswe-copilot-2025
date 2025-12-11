# Copilot Instructions for Todo App Codebase

## Essential Guidelines & Rules

Before starting work, review these foundational documents:

- [**Critical Rules & Guardrails**](../../docs/rules/CRITICAL-RULES-AND-GUARDRAILS.md) – Mandatory rules for code quality, safety, and precision
- [**Python Development Guidelines**](../../docs/rules/PYTHON-DEVELOPMENT-GUIDELINES.md) – Python standards, uv package management, type hints
- [**Web Development Guidelines**](../../docs/rules/WEB-DEV-GUIDELINES.md) – HTML, CSS, JS, security, accessibility best practices
- [**Development Architecture Guidelines**](../../docs/rules/DEVELOPMENT-ARCHITECTURE-GUIDELINES.md) – System design and architecture patterns
- [**UX/UI Guidelines**](../../docs/rules/UX-UI-GUIDELINES.md) – Design, accessibility, and user experience standards

## Overview
This is a modern **FastAPI + HTMX + SQLAlchemy** todo application built for the Agentic Software Engineering workshop. The app uses server-side rendering with HTMX for interactivity, featuring user authentication, multiple todo lists per user, and priority-based task management.

## Project Setup & Workflows

### Development Commands
```bash
./run.sh                              # Sync deps + start server (preferred)
uv sync && uv run uvicorn app.main:app --reload
uv run pytest                         # Run all tests
uv run pytest tests/test_auth.py      # Run specific test module
```

**Key Detail:** All dependencies are managed via `uv` (replaces pip/venv). The `pyproject.toml` includes pytest/httpx as runtime deps for workshop simplicity—do NOT move them to dev dependencies without adjusting the testing strategy.

### Project Root
All commands run from `/workspaces/aswe-copilot-2025/todo-app/` unless specified otherwise. Python paths are configured in `pyproject.toml` with `pythonpath = ["src"]`, so imports are like `from app.database import Todo` (not `from src.app...`).

## Architecture & Data Flow

### Core Components
- **FastAPI app** (`src/app/main.py`): Entry point with startup/shutdown logic, seed data initialization
- **Database** (`src/app/database.py`): SQLAlchemy ORM models (User, TodoList, Todo) with cascading deletes and positional ordering
- **Routes** (in `src/app/routes/`):
  - `auth.py`: Login/register (sets session cookies)
  - `pages.py`: HTML page rendering with auth redirects
  - `todos.py`: HTMX endpoints returning partial HTML (not JSON)
  - `todo_lists.py`: List management (CRUD + reordering)

### Session Model (In-Memory)
- **Not persistent:** Sessions stored in `app.core.deps.sessions` dict, lost on restart
- **Dependency injection:** `get_current_user_id()` validates session from `session_id` cookie
- **Expiration:** 1 hour TTL; expired sessions auto-deleted on access
- **Seed user:** `demo@example.com` / `demo123` created on startup if not exists

### Database Structure
```python
User (id, email, password)  → TodoList (id, user_id, name, color, position)
                             → Todo (id, list_id, title, priority, due_date, is_completed)
```
- **UUIDs** for all IDs (string columns with `default=generate_uuid`)
- **Positional ordering:** Both TodoList and Todo have `position` fields for reordering (not datetime-based)
- **Cascade deletes:** Deleting a user cascades to lists and todos

### Request Flow: HTMX Pattern
1. User interacts with HTML form/button in template
2. HTMX sends request to `/api/todos/*` endpoint (e.g., POST `/api/todos/create`)
3. Route handler verifies user ownership via `_verify_list_access()`
4. Returns **partial HTML** (not JSON) from templates in `src/app/templates/partials/`
5. HTMX swaps/replaces the DOM fragment (e.g., `hx-swap="outerHTML"`)

**Authorization pattern:** Always check `user_id` from `get_current_user_id()` matches the resource owner (see `_verify_list_access()` in `todos.py` for example).

## Code Conventions & Patterns

### Templates & Utils
- **Template globals:** Utility functions injected into all Jinja2 templates via `templates.env.globals`
  - `format_date(dt)`: Display format (e.g., "Dec 11, 2025")
  - `format_date_input(dt)`: HTML input format (YYYY-MM-DD)
  - `is_overdue(todo)`, `is_due_today(todo)`: Boolean checks for conditional styling
- **Partials location:** `src/app/templates/partials/` for reusable HTMX fragments (e.g., `todo_item.html`, `error.html`)

### Validation & Error Handling
- **Pydantic models** in `src/app/models/` for request validation (see `auth.py`, `todo_list.py`, `todo.py`)
- **Error responses:** Return partial HTML from `partials/error.html` on validation failure (status 200, not 4xx) for inline error display
- **User verification:** Use `_verify_list_access()` pattern to ensure ownership before mutations

### Testing Structure
- **Fixture-based:** `conftest.py` provides `client`, `db_session`, `test_user` fixtures
- **In-memory SQLite:** Tests use `sqlite:///:memory:` for isolation; database cleared after each test
- **Test client:** Uses `TestClient` with dependency overrides for `get_db`
- **Session clearing:** `sessions.clear()` in fixture to ensure clean state
- **Assertions:** Check status codes, response headers (`HX-Redirect` for redirects), and response content (`b"error message"` in content)

## Important Project-Specific Rules

### Critical Do's
1. **Verify ownership before mutations:** Always check `user_id` matches resource owner to prevent cross-user access
2. **Return partial HTML from HTMX endpoints:** Not JSON—endpoints in `/api/` still return `HTMLResponse` with partial templates
3. **Use position field for ordering:** Don't use timestamps or indexes for todo/list order; use explicit `position` column
4. **Maintain test isolation:** Clear sessions and use fresh in-memory DB per test
5. **Test async routes properly:** Use `client.post()` in tests (TestClient auto-awaits async routes)

### Critical Don'ts
1. **Don't persist sessions to DB:** This codebase intentionally uses in-memory sessions for workshop simplicity
2. **Don't return 4xx status codes for validation errors:** Return 200 with error HTML for inline display (HTMX pattern)
3. **Don't forget cascade deletes:** When modifying relationships, ensure cascading is correct
4. **Don't hardcode absolute URLs:** Use relative paths in templates and HTMX endpoints
5. **Don't import from root `app/` in templates:** Jinja2 context must be explicitly passed

### Password Security (Educational Context)
⚠️ **This project stores plain-text passwords intentionally for simplicity.** Do NOT use this approach in production. Implement bcrypt/argon2 hashing in real applications.

## Key File Reference

| File | Purpose |
|------|---------|
| `src/app/main.py` | FastAPI app, startup hooks, seed data |
| `src/app/database.py` | SQLAlchemy models (User, TodoList, Todo) + session |
| `src/app/core/deps.py` | Session management, auth dependency injection |
| `src/app/routes/todos.py` | Todo CRUD endpoints (HTMX partial responses) |
| `src/app/routes/todo_lists.py` | List management endpoints |
| `src/app/routes/auth.py` | Login/register with session cookies |
| `src/app/utils.py` | Template utility functions (format_date, is_overdue) |
| `tests/conftest.py` | Pytest fixtures (client, db_session) |
| `src/app/templates/` | Jinja2 base layout + page templates |
| `src/app/templates/partials/` | HTMX partial fragments |

## Performance & Debugging Notes

- **SQLite single-threaded:** Uses `check_same_thread=False` and `poolclass=NullPool` for dev simplicity; not suitable for production
- **N+1 query risk:** Be careful with lazy-loaded relationships; prefer SQLAlchemy `joinedload()` for nested queries
- **HTMX swap targeting:** Always verify CSS selectors in `hx-target` and `hx-swap` attributes match template IDs/classes
- **Form submission:** Ensure `name` attributes on inputs match Pydantic model field names for proper form parsing
