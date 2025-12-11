# Copilot Instructions

## Project Overview
Educational workshop on agentic software engineering. Main artifact: `todo-app/` (FastAPI + HTMX + Shoelace). Project structure includes exercises (`docs/exercises/`), requirements specs (`docs/todo-app-requirements/`), and development guidelines (`docs/rules/`).

## Essential Reading

**Read these files BEFORE making changes:**
- `docs/rules/CRITICAL-RULES-AND-GUARDRAILS.md` - Non-negotiable rules, forbidden commands, core philosophy
- `docs/rules/PYTHON-DEVELOPMENT-GUIDELINES.md` - Modern Python with `uv`, ruff, project structure
- `docs/rules/DEVELOPMENT-ARCHITECTURE-GUIDELINES.md` - KISS/YAGNI, SOLID, CUPID principles
- `docs/rules/UX-UI-GUIDELINES.md` - Visual hierarchy, accessibility, touch targets
- `docs/rules/WEB-DEV-GUIDELINES.md` - HTML/CSS/JS best practices, security, performance
- `docs/misc/AGENTIC-CODING-TIPS.md` - Workflow optimization, priming, validation loops

## Architecture & Tech Stack

### Todo App Stack (Python-based)
- **Backend:** FastAPI with uvicorn
- **Frontend:** HTMX (server-driven) + Shoelace Web Components
- **Database:** SQLite + SQLAlchemy ORM
- **Templates:** Jinja2
- **Package Manager:** `uv` (replaces pip/venv/poetry)

### Key Patterns
- **Server-rendered UI:** HTMX swaps HTML fragments, no React/Vue
- **OOB Swaps:** Multiple UI updates in single response via `hx-swap-oob`
  - Example: Updating todo item + sidebar counter simultaneously (see `templates/partials/todo_item_with_oob.html`)
- **Authentication:** In-memory sessions (educational only, NOT production-safe)
  - Sessions in `app/core/deps.py`, plain-text passwords
- **UUIDs:** All primary keys use UUID strings via `generate_uuid()`
- **UTC everywhere:** `utc_now()` for all timestamps

## Critical Development Commands

```bash
# Todo app workflow (from /workspaces/aswe-copilot-2025/todo-app/)
./run.sh                              # Syncs deps + starts server (http://localhost:8000)
uv sync                               # Install/update dependencies
uv run uvicorn app.main:app --reload  # Manual server start
uv run pytest tests/ -v               # Run all tests

# Dependencies
uv add <package>                      # Add runtime dependency
uv add --dev <package>                # Add dev dependency
```

**Demo credentials:** `demo@example.com` / `demo123`

## Project Conventions

### Database Models (`app/database.py`)
- Use `declarative_base()`, cascade deletes configured on relationships
- Index pattern: `Index("ix_table_columns", "col1", "col2")`
- Example: `User` → `TodoList` → `Todo` (cascading deletes)

### Routing Pattern (`app/routes/*.py`)
- Each router has its own `Jinja2Templates` instance
- Register utility functions in template globals:
  ```python
  templates.env.globals["is_overdue"] = is_overdue
  ```
- API routes return HTML partials for HTMX swapping

### Testing Setup (`tests/conftest.py`)
- In-memory SQLite per test (`StaticPool`)
- Override `get_db` dependency + clear sessions in `client` fixture
- Pattern: Fixture creates user/lists/todos, tests modify and verify

### File Organization
- Models in `app/models/*.py` (Pydantic validation schemas)
- SQLAlchemy in `app/database.py` (DB models)
- Dependencies in `app/core/deps.py` (auth, session management)
- Utilities in `app/utils.py` (date formatting, validation helpers)

## Key Files & Locations

- **App entry:** `todo-app/src/app/main.py` (FastAPI app + demo data seeding)
- **Auth logic:** `todo-app/src/app/core/deps.py` (session management)
- **HTMX patterns:** `todo-app/src/app/templates/partials/` (reusable fragments)
- **Requirements:** `docs/todo-app-requirements/functional-requirements.md` (stack-agnostic spec)
- **Implementation spec:** `docs/todo-app-requirements/implementation-spec-python.md` (detailed reference)

## Common Workflows

### Adding a Feature
1. Check `docs/todo-app-requirements/functional-requirements.md` for alignment
2. Write tests first (`tests/test_*.py`)
3. Implement route handler (`app/routes/`)
4. Create/update templates (`app/templates/`)
5. Run `uv run pytest tests/ -v` to verify

### Debugging HTMX
- Browser DevTools → Network tab for HTMX requests
- Check response HTML structure (should be valid partial)
- Verify `hx-target`, `hx-swap` attributes in templates

### Database Changes
- Modify `app/database.py` models
- Delete `todo.db` to recreate (no migrations in this educational app)
- Restart server to trigger `init_db()` + demo data seeding

## Critical Commands & Conventions

See `docs/rules/PYTHON-DEVELOPMENT-GUIDELINES.md` for:
- Using `uv` for package management (never `pip`)
- Running commands with `uv run` (auto-syncs environment)
- Code formatting with `ruff format .` (not Black)
- Linting with `ruff check . --fix`

See `docs/rules/CRITICAL-RULES-AND-GUARDRAILS.md` for:
- Forbidden commands (never use)
- Small & precise changes philosophy
- Clean-up requirements
- Visual validation requirements
