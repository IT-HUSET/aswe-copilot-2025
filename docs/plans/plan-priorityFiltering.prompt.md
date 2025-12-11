# Plan: Add Priority Filtering to Todo List

Add interactive priority filter buttons (All, High, Medium, Low) that work alongside existing search functionality using HTMX and Shoelace components.

**Note**: This feature extends beyond the MVP scope defined in `docs/todo-app-requirements/functional-requirements.md` (which lists advanced filtering as out-of-scope). This is an educational workshop extension to demonstrate HTMX state management patterns.

## Steps

1. **Update search endpoint in `todo-app/src/app/routes/todos.py`**
   - Add `priority: str = "all"` query parameter to `search_todos` function
   - Apply SQLAlchemy filter when `priority != "all"`: `query = query.filter(Todo.priority == priority)`
   - Include priority in template context: `context={"todos": todos, "list": list_obj, "search_query": q, "priority_filter": priority}`
   - Validate priority value is in `["all", "low", "medium", "high"]`, default to "all" if invalid

2. **Update search bar in `todo-app/src/app/templates/partials/todo_list_content.html`**
   - Add `id="search-input"` to the existing `sl-input` for search to enable HTMX targeting
   - Keep existing `name="q"` attribute for form serialization

3. **Add filter button group to `todo-app/src/app/templates/partials/todo_list_content.html`**
   - Insert `<div class="priority-filters">` with `<sl-button-group label="Filter by priority">` between search bar and quick-add form
   - Create four buttons (All/High/Medium/Low) with:
     - `hx-get="/api/todos/search"`
     - `hx-target="#todos-list"`
     - `hx-vals='js:{"list_id": "{{ current_list.id }}", "q": document.querySelector("#search-input").value || "", "priority": "<value>"}'` (dynamically captures search input)
     - `variant="{{ 'primary' if priority_filter == '<value>' else 'default' }}"` for active state
     - `label="Filter by <priority> priority"` for accessibility
   - **Priority filter resets to "all" when switching lists** (simplest, most predictable UX)

4. **Style filter controls in `todo-app/src/app/static/css/styles.css`**
   - Add `.priority-filters` class with `margin-bottom: 16px;` for spacing between search and filters
   - Ensure consistent spacing with existing `.search-bar` pattern

5. **Write tests in `todo-app/tests/test_todos.py`**
   - Test filtering by each priority level individually (high/medium/low)
   - Test "all" returns all todos regardless of priority
   - Test combination of priority filter + text search (both filters applied)
   - Test priority filter with empty list returns empty result
   - Test priority filter preserves todo ordering by position
   - Test invalid priority value defaults to "all"
   - Test that creating a todo while filter is active shows the new todo if it matches the filter

## Implementation Notes

### HTMX + Shoelace Integration
- Using `hx-vals='js:...'` to dynamically capture search input value because Shoelace components use Shadow DOM
- Alternative approach: wrap buttons in form with hidden inputs, but `js:` expression is cleaner for this use case
- The `id="search-input"` on search bar enables reliable DOM querying

### UX Decision: Filter State on List Switch
- **Chosen approach**: Priority filter resets to "all" when switching lists
- **Rationale**: Simpler mental model, predictable behavior, avoids per-list state management
- **Alternative considered**: Store filter per list in session (rejected: adds complexity for minimal benefit in educational context)

## Future Enhancements (Out of Scope)

1. **Visual icons for priority buttons** - Could add Bootstrap Icons (`exclamation-triangle` for High, `dash-circle` for Medium, `circle` for Low) and/or color indicators matching todo item priority badges (red/amber/green)

2. **URL parameters and bookmarking** - Add `hx-push-url="true"` to make filtered views bookmarkable. Would require:
   - Reading priority from URL query params on initial page load
   - Updating list selection to preserve priority in URL
   - More complex but enables shareable filtered views

3. **Combined filter controls** - If adding more filters (completed/active, due date), consider consolidating into a unified filter bar component
