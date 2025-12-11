# Exercise 2: Bug Hunt - Solutions

This directory contains the fixed versions of files for Exercise 2.

## Bug Fixes Summary

### Bug 1: Missing Default Priority
**File:** `todos.py` - `create_todo()` function (~line 115)

**Problem:** Quick-add todos don't have a default priority set.

**Fix:** Add `priority="low"` when creating the Todo object:
```python
todo = Todo(
    list_id=list_id,
    title=title.strip(),
    position=new_pos,
    priority="low",  # Added this line
)
```

---

### Bug 2: Due Dates Not Saving
**File:** `todos.py` - `update_todo()` function (~line 226)

**Problem:** HTML date inputs send dates in `"2024-01-15"` format, but the code expected `"2024-01-15T00:00"`.

**Fix:** Change the date format string:
```python
# Before (buggy):
todo.due_date = datetime.strptime(due_date, "%Y-%m-%dT%H:%M")

# After (fixed):
todo.due_date = datetime.strptime(due_date, "%Y-%m-%d")
```

---

### Bug 3: Sidebar Count Not Updating
**File:** `todos.py` - `delete_todo()` function (~line 286)

**Problem:** The delete endpoint just returns `Response(status_code=200)` without sending an OOB update for the sidebar count.

**Fix:** Return an HTML template with OOB swap, similar to `toggle_todo`:
```python
# Before (buggy):
db.delete(todo)
db.commit()
return Response(status_code=200)

# After (fixed):
list_id = todo.list_id
db.delete(todo)
db.commit()

count = _get_list_todo_count(db, list_id)
return templates.TemplateResponse(
    request=request,
    name="partials/todo_deleted_oob.html",
    context={"list_id": list_id, "count": count},
)
```

---

### Bug 4: Overdue Styling Wrong
**File:** `utils.py` - `is_overdue()` and `is_due_today()` functions

**Problem:** Comparing full `datetime` objects (with time component) instead of just dates. A todo due "today" stored as `2024-12-08 00:00:00` compared to `datetime.now()` = `2024-12-08 14:30:00` shows as overdue because `00:00:00 < 14:30:00`. Similarly, `is_due_today` uses `==` on full datetimes, which almost never matches.

**Fix:** Compare only the date parts:
```python
# Before (buggy):
now = datetime.now()
return todo.due_date < now  # Compares including time!

# After (fixed):
today = date.today()
due = todo.due_date.date() if isinstance(todo.due_date, datetime) else todo.due_date
return due < today  # Compares dates only
```

---

## How to Use These Solutions

If you get stuck during Exercise 2, you can reference these files:

```bash
# View the solution for a specific bug
cat docs/solutions/todos.py | grep -A5 "FIX:"
cat docs/solutions/utils.py | grep -A5 "FIX:"

# Or compare with your current file
diff todo-app/src/app/routes/todos.py docs/solutions/todos.py
diff todo-app/src/app/utils.py docs/solutions/utils.py
```

To apply all fixes at once (not recommended - try to fix them yourself first!):
```bash
cp docs/solutions/todos.py todo-app/src/app/routes/todos.py
cp docs/solutions/utils.py todo-app/src/app/utils.py
```

---

## Verification

After fixing all bugs, run the tests to verify:
```bash
cd todo-app
uv run pytest tests/ -v
```

All tests should pass.
