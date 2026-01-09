"""FastAPI Todo Application - Main Entry Point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError

from app.database import SessionLocal, Todo, TodoList, User, init_db
from app.routes import api, auth, pages, todo_lists, todos
from app.utils import format_date, format_date_input, is_due_today, is_overdue

templates = Jinja2Templates(directory="src/app/templates")


def seed_demo_data():
    """Seed demo user and data if not exists."""
    db = SessionLocal()
    try:
        # Check if demo user exists
        demo_user = db.query(User).filter(User.email == "demo@example.com").first()
        if demo_user:
            return

        # Create demo user
        demo_user = User(
            email="demo@example.com",
            password="demo123",
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)

        # Create sample todo list
        work_list = TodoList(
            user_id=demo_user.id,
            name="Work Tasks",
            description="Important work items",
            color="#3b82f6",
            position=0,
        )
        db.add(work_list)
        db.commit()
        db.refresh(work_list)

        # Create sample todos
        sample_todos = [
            Todo(
                list_id=work_list.id,
                title="Review project plan",
                note="Check the new requirements document",
                priority="high",
                position=0,
            ),
            Todo(
                list_id=work_list.id,
                title="Update documentation",
                priority="medium",
                position=1,
            ),
            Todo(
                list_id=work_list.id,
                title="Send weekly report",
                priority="low",
                position=2,
            ),
        ]
        for todo in sample_todos:
            db.add(todo)
        db.commit()

        # Create personal list
        personal_list = TodoList(
            user_id=demo_user.id,
            name="Personal",
            description="Personal tasks and reminders",
            color="#10b981",
            position=1,
        )
        db.add(personal_list)
        db.commit()
        db.refresh(personal_list)

        personal_todos = [
            Todo(
                list_id=personal_list.id,
                title="Buy groceries",
                priority="medium",
                position=0,
            ),
            Todo(
                list_id=personal_list.id,
                title="Call mom",
                priority="high",
                position=1,
            ),
        ]
        for todo in personal_todos:
            db.add(todo)
        db.commit()

    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    init_db()
    seed_demo_data()
    yield
    # Shutdown (no cleanup needed)


app = FastAPI(
    title="Todo App",
    description="Modern todo application with FastAPI, HTMX, and Shoelace",
    version="0.1.0",
    lifespan=lifespan,
)

# Mount static files
app.mount("/static", StaticFiles(directory="src/app/static"), name="static")

# Include routers
app.include_router(api.router)
app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(todo_lists.router)
app.include_router(todos.router)


@app.exception_handler(SQLAlchemyError)
async def db_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors."""
    return templates.TemplateResponse(
        request=request,
        name="partials/error.html",
        context={"error": "Database error occurred"},
        status_code=500,
    )


@app.exception_handler(401)
async def unauthorized_handler(request: Request, exc):
    """Handle unauthorized access."""
    from fastapi.responses import RedirectResponse, Response

    # Only use next= for page routes (not API endpoints, which use POST/PUT/DELETE)
    next_url = request.url.path
    if next_url.startswith("/api/"):
        next_url = "/app"

    if request.headers.get("HX-Request") == "true":
        response = Response(status_code=401)
        response.headers["HX-Redirect"] = f"/login?next={next_url}"
        return response

    return RedirectResponse(url=f"/login?next={next_url}", status_code=302)
