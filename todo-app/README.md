# Todo App

Modern todo application built with Python, FastAPI, HTMX, and Shoelace Web Components.

## Quick Start

```bash
# User run.sh to sync dependencies and start the server
./run.sh

# Alternatively, manual sync and run:

## Install dependencies
uv sync
## Run the server
uv run uvicorn app.main:app --reload
```

Access at http://localhost:8000

**Demo credentials:** `demo@example.com` / `demo123`

## Features

- User authentication (mock sessions)
- Multiple todo lists per user
- Todo items with title, notes, due dates, and priority levels
- Search todos by title
- Simple list/todo reordering (up/down buttons)
- Dark mode support
- Responsive design

## Tech Stack

- **Backend:** FastAPI
- **Frontend:** HTMX + Shoelace Web Components
- **Database:** SQLite with SQLAlchemy ORM
- **Templates:** Jinja2

## Development

```bash
# Run tests
uv run pytest

# Run with auto-reload
uv run uvicorn app.main:app --reload
```

## Project Structure

```
src/app/
├── main.py           # FastAPI app entry point
├── database.py       # SQLAlchemy models and database setup
├── utils.py          # Shared utility functions
├── core/deps.py      # Authentication dependencies
├── models/           # Pydantic validation models
├── routes/           # API routes
├── templates/        # Jinja2 templates
└── static/           # CSS and JavaScript
```

## Educational Notice

This is an educational project with intentionally simplified authentication (plain text passwords, in-memory sessions). **Not for production use.**
