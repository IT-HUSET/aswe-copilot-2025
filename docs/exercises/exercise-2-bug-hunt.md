# Exercise 2: Bug Hunt

**Goal:** Fix 4 bugs using Copilot Agent Mode

**Prerequisites:** Exercise 1 completed, todo-app running

---

## Setup

```bash
cd todo-app
uv run uvicorn app.main:app --reload
```

> The app has 4 planted bugs. Your job: find and fix them with Copilot.
>
> **The challenge:** Describe the *symptom* to Copilot, not the solution. Let AI do the detective work.
>
> Solutions available in [`docs/solutions/`](../solutions/) if you get stuck.

---

## Bug 1: Missing Default Priority

**Symptom:** Quick-add todos have no priority set.

**Reproduce:**
1. Add a todo using just the title field
2. Edit it — priority is empty or wrong

**Your task:** Craft a prompt describing this bug to Copilot. Focus on the symptom, not the fix.

<br/>
<details>
<summary>🤔 <i><b>Stuck?</b> Try this prompt</i></summary>

> ```md
> @workspace Quick-add todos don't have a default priority.
> Find where todos are created and ensure they get a default priority, then implement the fix.
> ```

You may find that you need to ask Copilot again to actually implement the fix after it identifies the problem: 
> ```md
> Please implement the suggested fix.
> ```
</details>

<br/>
<details>
<summary>Hint (if Copilot can't find it)</summary>

File: `todo-app/src/app/routes/todos.py` — `create_todo` function.
Add `priority="low"` when creating the Todo object.
</details>

<br/>

**Verify:** New quick-add todos show priority "low" when edited.

---

## Bug 2: Due Dates Not Saving

**Symptom:** Setting a due date in edit dialog doesn't persist.

**Reproduce:**
1. Edit a todo and set a due date
2. Save and reopen — due date is gone

**Your task:** Describe the symptom to Copilot. What's the user experiencing?

<br/>
<details>
<summary>🤔 <i><b>Stuck?</b> Try this prompt</i></summary>

> ```md
> @workspace Due dates aren't saving when I edit todos.
> The date disappears after saving. Find and fix the issue.
> ```

Again, you may need to ask Copilot to implement the fix after it identifies the problem.
</details>

<br/>
<details>
<summary>Hint (if Copilot can't find it)</summary>

File: `todo-app/src/app/routes/todos.py` — `update_todo` function.
HTML date inputs send `"2024-01-15"` format.
Change `"%Y-%m-%dT%H:%M"` to `"%Y-%m-%d"`.
</details>

<br/>

**Verify:** Due dates persist after editing.

---

## Bug 3: Sidebar Count Not Updating

**Symptom:** Deleting a todo doesn't update the sidebar count.

**Reproduce:**
1. Create a list with 3+ todos
2. Delete one — sidebar count stays the same

**Your task:** This is an HTMX issue. How would you describe it to Copilot?

<br/>
<details>
<summary>🤔 <i><b>Stuck?</b> Try this prompt</i></summary>

> ```md
> @workspace When I delete a todo, the sidebar count doesn't update.
> The count only updates after a page refresh. Fix it.
> ```

Again, you may need to ask Copilot to implement the fix after it identifies the problem.
</details>

<br/>
<details>
<summary>Hint (if Copilot can't find it)</summary>

File: `todo-app/src/app/routes/todos.py` — `delete_todo` function.
The function just returns `Response(status_code=200)` without updating the sidebar.
Fix: Return an HTML response with an OOB swap to update the count, similar to how `toggle_todo` does it.
</details>

<br/>

**Verify:** Sidebar count updates immediately after deletion.

---

## Bug 4: Overdue Styling Wrong

**Symptom:** Overdue/due-today styling appears on wrong todos.

**Reproduce:**
1. Create todos with yesterday, today, and tomorrow due dates
2. Check styling — today's todo shows as overdue, "due today" styling never appears

**Your task:** This is a datetime comparison bug. Describe what you observe.

<details>
<summary>🤔 <i><b>Stuck?</b> Try this prompt</i></summary>

> ```md
> @workspace The overdue styling is wrong. Todos due today are showing
> as overdue, and the "due today" styling never appears. Check the date comparison logic.
> ```

Again, you may need to ask Copilot to implement the fix after it identifies the problem.
</details>

<br/>

<details>
<summary>Hint (if Copilot can't find it)</summary>

File: `todo-app/src/app/utils.py` — `is_overdue` and `is_due_today` functions.
The bug: comparing full datetime (with time) instead of just dates.
Fix: compare `.date()` parts only:
```python
today = date.today()
return todo.due_date.date() < today  # for is_overdue
return todo.due_date.date() == today  # for is_due_today
```
</details>

<br/>

**Verify:** Yesterday=red (overdue), today=orange, tomorrow=normal.

---

## Final Check

Open a new terminal and run all tests:
```bash
cd todo-app
uv run pytest tests/ -v
```

All tests _but one_ should pass, i.e. you should get a test failure like this:
```bash
tests/test_todos.py:29: AssertionError
=============== short test summary info ================
FAILED tests/test_todos.py::TestTodos::test_create_todo - AssertionError: assert None == 'low'
```

---

## Part B: Write a Test (Optional)

Now that all bugs are fixed, practice writing tests with Copilot.

### Task: Add a Test for Default Priority

**Goal:** Write a test that verifies new todos get `priority="low"` by default, and fix any existing tests that fail because of this new behavior.

**Your task:** Ask Copilot to create a new test and fix existing tests. Consider:
- Where do existing tests live? (`todo-app/tests/`)
- What pattern do existing tests follow?
- Use `/tests` slash command or describe what you need?

<br/>

<details>
<summary>🤔 <i><b>Stuck?</b> Try this prompt</i></summary>

> ```md
> @workspace Add a test that verifies new todos created without explicit priority get "low" as the default. 
> Also fix any existing tests that fail because of this new behavior.
> Follow the existing test patterns in tests/test_todos.py.
> ```
</details>

<br/>

**Verify:** Run `uv run pytest tests/test_todos.py -v` — your new test should pass.

---

## Key Takeaways

| Concept | Remember |
|---------|----------|
| Context | Use `@workspace` + describe the symptom |
| Silent failures | Watch for `except: pass` — errors vanish silently |
| Date/time bugs | Compare `.date()` not full datetime with time |
| HTMX OOB swaps | Need correct `response_class` for out-of-band updates |
| Default values | Set defaults explicitly, don't assume DB defaults apply |

---

## Resources

- [Copilot Chat Cookbook: Debugging](https://docs.github.com/en/copilot/tutorials/copilot-chat-cookbook#debugging-code)
- [Using @workspace](https://docs.github.com/en/copilot/using-github-copilot/asking-github-copilot-questions-in-your-ide)
- [/fix Slash Command](https://docs.github.com/en/copilot/reference/cheat-sheet#slash-commands)
