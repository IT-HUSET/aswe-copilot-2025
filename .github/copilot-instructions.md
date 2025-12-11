# Copilot Instructions for Agentic Software Engineering Workshop

## Project Context

Educational workshop codebase with a **FastAPI + HTMX + Shoelace todo app** (`todo-app/`) and supporting docs/exercises. Intentionally simplified for learning — NOT production-ready (plain text passwords, in-memory sessions).

## Architecture Overview

### Todo App Stack (`todo-app/`)
- **Backend:** FastAPI (Python 3.11+) with SQLAlchemy ORM + SQLite
- **Frontend:** HTMX 2.x for dynamic interactions, Shoelace web components for UI, vanilla JS for theme/sorting
- **Templates:** Jinja2 with template globals for utility functions (`is_overdue`, `format_date`, etc.)
- **Data flow:** HTMX sends POST/PUT/DELETE → FastAPI routes → SQLAlchemy → SQLite → Jinja2 partials → HTMX swaps DOM

### Directory Structure
```
todo-app/src/app/
├── main.py           # FastAPI app, lifespan, demo seed data
├── database.py       # SQLAlchemy models (User, TodoList, Todo)
├── utils.py          # Template utility functions
├── core/deps.py      # Auth dependencies (session-based)
├── models/           # Pydantic request/response models
├── routes/           # API routers (auth, pages, todo_lists, todos)
├── templates/        # Jinja2 (base.html, app.html, partials/)
└── static/           # CSS + JS (theme toggle, Sortable.js integration)
```

## Critical Patterns

### HTMX Interaction Pattern
- Routes return **HTML fragments** (partials), not JSON
- Use `hx-post`, `hx-get`, `hx-swap`, `hx-target` for dynamic updates
- Example: Creating a todo returns `partials/todo_item_with_oob.html` with out-of-band swaps (`hx-swap-oob`) to update sidebar counts
- Error handling: Return `partials/error.html` with appropriate status codes
- Unauthorized (401): Return `HX-Redirect` header for HTMX requests, else `RedirectResponse`

### Database Access
- **In-memory SQLite** for tests: `sqlite:///:memory:` with `StaticPool` (see `tests/conftest.py`)
- **File-based SQLite** for dev: `todo.db` in project root
- All timestamps use `datetime.now(timezone.utc)` (see `database.py:utc_now()`)
- Models use UUID strings for IDs: `generate_uuid()` helper
- CASCADE deletes: User → TodoLists → Todos

### Authentication (Simplified)
- Plain text passwords (`User.password`) — **educational only**
- In-memory session dict (`app/core/deps.py:sessions`)
- Sessions lost on server restart (acceptable for workshop)
- Protected routes use `Depends(get_current_user_id)`
- Verify list/todo ownership: `_verify_list_access()` pattern in routes

### Template Globals
Register utility functions in router files (e.g., `todos.py`):
```python
templates.env.globals["is_overdue"] = is_overdue
templates.env.globals["format_date"] = format_date
```

## Development Workflow

### Commands (run from `todo-app/`)
```bash
# Quick start (syncs deps + starts server)
./run.sh

# Manual workflow
uv sync                              # Install/sync dependencies
uv run uvicorn app.main:app --reload # Start server (localhost:8000)
uv run pytest tests/ -v              # Run tests
```

### Testing Patterns
- Fixtures: `client`, `authenticated_client`, `test_user`, `test_list`, `test_todo` (see `conftest.py`)
- Override `get_db` dependency for in-memory test DB
- Clear session dict before each test
- Use `TestClient` from `fastapi.testclient`

### Python Conventions
- **Package manager:** `uv` (NOT pip/poetry) — 10-100x faster
- **src layout:** `src/app/` (not flat structure)
- **Dependencies:** Use `uv add <package>` to modify `pyproject.toml`
- **Dev deps:** Included in main `dependencies` for workshop simplicity (normally use `[project.optional-dependencies]`)
- **Type hints:** Python 3.11+ syntax (`str | None`, not `Optional[str]`)
- **Imports:** Absolute from `app.*`, never relative

## Essential Guidelines

Before making changes, review these project-specific rules (in priority order):

1. **[Critical Rules & Guardrails](../docs/rules/CRITICAL-RULES-AND-GUARDRAILS.md)** - Non-negotiable principles: be concise, surgical changes, fix forward, no destructive commands
2. **[Development & Architecture Guidelines](../docs/rules/DEVELOPMENT-ARCHITECTURE-GUIDELINES.md)** - KISS/YAGNI, SOLID, CUPID properties, dependency management
3. **[Python Development Guidelines](../docs/rules/PYTHON-DEVELOPMENT-GUIDELINES.md)** - `uv` package manager, src layout, ruff/mypy, type hints, testing with pytest
4. **[Web Development Guidelines](../docs/rules/WEB-DEV-GUIDELINES.md)** - Semantic HTML, CSS/JS best practices, performance, security, accessibility
5. **[UX/UI Guidelines](../docs/rules/UX-UI-GUIDELINES.md)** - Design patterns, component usage, accessibility standards

**Key takeaways:**
- Be concise, make surgical changes, clean up obsolete code
- Never reformat entire project or use destructive commands (`rm -rf`, `git rebase --skip`)
- Never create duplicate files (`file_v2.py`) or add dependencies without evaluating alternatives
- Use `uv` (not pip), Python 3.11+ type hints, src layout, absolute imports
- For UI: validate visually, follow WCAG accessibility, use semantic HTML

## UI/Frontend Details

### Shoelace Components
- Use `<sl-button>`, `<sl-input>`, `<sl-dialog>`, `<sl-icon>`, etc.
- Theme toggle: `.sl-theme-light` / `.sl-theme-dark` classes on `<body>`
- Icons: `<sl-icon name="..."></sl-icon>` (Bootstrap Icons)

### JavaScript Specifics
- **Theme:** Persists in `localStorage`, initialized on DOMContentLoaded
- **Drag-drop:** SortableJS for list/todo reordering, triggers HTMX `end` event
- **HTMX events:** Listen to `htmx:afterRequest` for post-action cleanup (e.g., close dialogs)

### Styling
- Custom CSS in `static/css/styles.css`
- Priority indicators: Red (high), amber (medium), green (low) via left borders + badges
- Overdue todos: Red border + red date text
- Dark mode: Shoelace variables + custom overrides

## Functional Boundaries

### In Scope
- User auth (mock sessions)
- Multiple todo lists per user
- Todos with title, notes, due dates, priority
- Search by title (live, debounced)
- List/todo reordering (up/down buttons or drag-drop)
- Dark mode toggle
- Responsive design

### Explicitly Out of Scope
- Real auth (password hashing, OAuth, JWT)
- Tags/labels, advanced filtering, sorting options
- Email verification, password reset
- Rate limiting, multi-user collaboration
- Offline support, file attachments, recurring todos

## Key References

- **Requirements:** `docs/todo-app-requirements/functional-requirements.md` - Feature scope, domain model, visual states
- **Architecture:** `docs/misc/ADR/ADR-001-tech-stack-selection.md` - Tech stack rationale, tradeoffs
- **Demo data:** `todo-app/src/app/main.py:seed_demo_data()` - Example user/lists/todos structure

## Common Pitfalls

1. **HTMX responses:** Return HTML, not JSON (FastAPI defaults to JSON)
2. **Template globals:** Must register functions per router, not just in `main.py`
3. **List ownership:** Always verify `user_id` matches before querying TodoList/Todo
4. **Out-of-band swaps:** Use `hx-swap-oob` to update multiple DOM elements (e.g., sidebar counts)
5. **Test DB isolation:** Use `StaticPool` + `:memory:` for tests to avoid file locking
6. **Datetime handling:** Always use `timezone.utc`, never naive datetimes
