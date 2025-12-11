# Python Development Guidelines

Modern Python development standards using current best practices and tools.

## Quick Start

```bash
# Create new project
uv init --package myproject && cd myproject

# Add dependencies
uv add fastapi pydantic
uv add --dev pytest ruff mypy

# Run
uv run pytest              # Tests
uv run ruff check . --fix  # Lint + fix
uv run ruff format .       # Format
uv run mypy src/           # Type check
```

## Project Structure

Use **src layout** for all packages:

```
myproject/
├── src/myproject/
│   ├── __init__.py
│   ├── py.typed           # PEP 561 type hint marker
│   └── core.py
├── tests/
│   ├── conftest.py        # Shared fixtures
│   └── test_core.py
├── pyproject.toml
├── uv.lock                # Commit this!
└── README.md
```

## Package Management (uv)

uv is 10-100x faster than pip, replaces pip + venv + pyenv + poetry.

```bash
# Dependencies
uv add requests               # Add runtime dep
uv add --dev pytest ruff      # Add dev dep
uv remove requests

# Lock and sync
uv lock                       # Update lockfile
uv sync                       # Lock + install
uv sync --upgrade             # Upgrade all

# Running (auto-syncs)
uv run pytest
uv run python script.py

# Global tools (like pipx)
uv tool install ruff
uvx black .
```

### pyproject.toml

```toml
[project]
name = "myproject"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.115.0",
    "pydantic>=2.0.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.8.0",
    "mypy>=1.8.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/myproject"]
```

## Linting and Formatting (ruff)

ruff replaces: flake8, black, isort, pyupgrade, autoflake.

```toml
[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = [
    "E", "W",   # pycodestyle
    "F",        # pyflakes
    "I",        # isort
    "UP",       # pyupgrade
    "B",        # flake8-bugbear
    "S",        # flake8-bandit (security)
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101"]  # assert ok in tests
```

```bash
ruff check . --fix   # Lint + auto-fix
ruff format .        # Format
```

### Pre-commit

`.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.6
    hooks:
      - id: ruff-check
        args: [--fix]
      - id: ruff-format
```

## Type Hints

Require Python 3.10+ for modern syntax.

```python
# Union syntax (3.10+)
def process(value: str | int | None) -> str | None:
    return str(value) if value else None

# TypedDict for structured dicts
from typing import TypedDict, NotRequired

class UserDict(TypedDict):
    id: int
    name: str
    email: NotRequired[str]

# Protocol for duck typing
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...
```

### mypy Configuration

```toml
[tool.mypy]
python_version = "3.10"
strict = true
mypy_path = "src"

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

## Testing (pytest)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = ["--strict-markers", "--cov=myproject"]

[tool.coverage.run]
source = ["src"]
branch = true
```

### Fixtures

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

@pytest.fixture(scope="function")
def db_session():
    """Fresh in-memory database per test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
```

### Test Patterns

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("a", "A"),
    ("b", "B"),
])
def test_variants(input, expected):
    assert process(input) == expected

@pytest.mark.asyncio
async def test_async():
    result = await async_operation()
    assert result.status == "ok"
```

## Data Modeling

| Use Case | Tool |
|----------|------|
| API request/response | Pydantic |
| Config parsing | Pydantic |
| Internal data | dataclasses |
| Type-safe dicts | TypedDict |

```python
# dataclasses (internal, fast)
@dataclass(slots=True, frozen=True)
class Point:
    x: float
    y: float

# Pydantic (API boundaries, validation)
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r"^[\w.-]+@[\w.-]+\.\w+$")
```

**Performance note:** Use Pydantic only at service boundaries. Use dataclasses internally.

## Async Patterns

```python
import asyncio

# Concurrent execution
results = await asyncio.gather(
    *[fetch(url) for url in urls],
    return_exceptions=True
)

# Throttling with Semaphore
sem = asyncio.Semaphore(10)
async def fetch_throttled(url: str) -> dict:
    async with sem:
        return await fetch(url)

# TaskGroup (Python 3.11+) - auto-cancels on error
async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(fetch(url1))
    task2 = tg.create_task(fetch(url2))

# Timeouts (Python 3.11+)
async with asyncio.timeout(5.0):
    return await fetch(url)
```

## Dependency Injection

```python
from typing import Protocol

class Logger(Protocol):
    def log(self, message: str) -> None: ...

class UserService:
    def __init__(self, logger: Logger) -> None:
        self._logger = logger

# FastAPI DI
from fastapi import Depends
from typing import Annotated

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    return db.query(User).get(user_id)
```

## Error Handling

```python
# Exception hierarchy
class AppError(Exception):
    """Base application error."""

class ValidationError(AppError):
    """Validation failed."""

class NotFoundError(AppError):
    """Resource not found."""
```

## Checklist

**New Project:**
- [ ] `uv init --package myproject`
- [ ] Configure ruff, mypy, pytest in `pyproject.toml`
- [ ] Setup pre-commit hooks
- [ ] Commit `uv.lock`

**Code Quality:**
- [ ] Type hints on public functions
- [ ] Tests for critical paths
- [ ] No ruff/mypy errors
