# Requirements Documentation

## Structure

| File | Purpose |
|------|---------|
| `functional-requirements.md` | What the app does (stack-agnostic) |
| `technical-requirements-{stack}.md` | Technology choices for a specific stack |

## Current Implementations

- `technical-requirements-python.md` - Python/FastAPI/SQLite
- `implementation-spec-python.md` - Detailed implementation spec/plan, generated from requirements (as example/reference)

## Porting to Another Stack

1. Use `functional-requirements.md` as your spec (don't modify it)
2. Create `technical-requirements-{stack}.md` with your technology choices
3. Generate a detailed implementation plan from both documents

Example files for other stacks:
- `technical-requirements-java.md`
- `technical-requirements-deno.md`
- `technical-requirements-node.md`

## Key Decisions for Each Stack

When creating a new technical requirements file, decide on:
- Language version and package manager
- Web framework and template engine
- Database and ORM/query builder
- Session/auth approach
- Frontend interactivity (HTMX or alternative)
- UI components (Shoelace or alternative)
