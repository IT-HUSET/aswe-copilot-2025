# Changelog

## Unreleased (2025-12-11)

- Fix: Ensure new todos receive a default priority of "low" when created.
  - Set database column default in `src/app/database.py`.
  - Explicitly set `priority="low"` in the quick-add handler at `src/app/routes/todos.py`.
- Fix: Accept both `YYYY-MM-DD` and `YYYY-MM-DDTHH:MM` formats when updating a todo's due date (`src/app/routes/todos.py`).
- Tests: Full test suite passing locally: `58 passed`.

No breaking changes.
