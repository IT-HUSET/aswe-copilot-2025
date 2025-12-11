# Todo App - Technical Requirements (Python/FastAPI Stack)

Technical decisions for the Python/FastAPI implementation. See `functional-requirements.md` for what the app does.

## Stack Decisions
- **Language**: Python 3.11+ with uv for package management
- **Framework**: FastAPI with Jinja2 templates (HTML files, not inline)
- **Database**: SQLite with SQLAlchemy ORM (zero external dependencies)
- **Auth**: Mock sessions (in-memory dict + cookies) - intentionally simple, not production-ready
- **Frontend**: HTMX for interactivity, Shoelace web components (CDN)
- **Drag-drop**: SortableJS (CDN)

## Constraints
- No Docker, no build tools, no Node/npm
- No external services (no cloud DB, no auth providers)
- Web standards only (HTML, CSS, JS)
- Must run with single command: `uv run uvicorn src.app.main:app --reload`
- Basic tests that don't require external connections

## Key Technical Considerations
- Make sure redirections are handled correctly with HTMX
- Make use of appropriate features in HTMX to handle partial updates and "OOB" swaps
- Ensure that different UI/frontend libraries (HTMX, Shoelace, SortableJS) work well together and don't conflict

## Browser Support
Modern browsers only (Chrome, Firefox, Safari, Edge - last 2 versions)
