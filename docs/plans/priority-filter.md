# Priority Filter Implementation Plan

## Overview
Add priority filtering to the todo app using HTMX + Shoelace button groups. Users can filter todos by priority (all/high/medium/low) within the currently selected list. Filter state persists across interactions and combines with existing search functionality.

## Research Summary

### HTMX Filtering Patterns
- Use `hx-get` on interactive elements (buttons, inputs) to trigger filtered queries
- Multiple parameters via `hx-vals` attribute (JSON format)
- Combine filters by including all params in single request
- Debounce inputs with `delay:` modifier on `hx-trigger`
- Target specific DOM elements for partial updates (`hx-target`, `hx-swap`)
- Example pattern: `hx-get="/api/todos/search" hx-vals='{"priority": "high", "list_id": "123"}' hx-target="#todos-list"`

### Shoelace Button Groups
- Component: `<sl-button-group>` wraps multiple `<sl-button>` elements
- Visual grouping with seamless borders between buttons
- Supports all button variants (primary, neutral, success, warning, danger)
- Supports size variants (small, medium, large)
- Active state: use `variant="primary"` for selected, `variant="neutral"` for unselected
- JavaScript required to toggle active state on click

## Implementation Plan

### 1. Backend Changes

#### File: `todo-app/src/app/routes/todos.py`

**Modify `search_todos()` endpoint** (lines 42-70):
- Add optional `priority` query parameter (default: `None` for "all")
- Validate priority value (must be `None`, `"high"`, `"medium"`, `"low"`)
- Update query filter to include priority if specified
- Pass `priority_filter` to template context

```python
@router.get("/search", response_class=HTMLResponse)
async def search_todos(
    request: Request,
    user_id: Annotated[str, Depends(get_current_user_id)],
    list_id: str,
    q: str = "",
    priority: str | None = None,  # NEW PARAMETER
    db: Session = Depends(get_db),
):
    """Search todos by title and optionally filter by priority in a specific list."""
    # ... existing list verification code ...
    
    query = db.query(Todo).filter(Todo.list_id == list_id)

    # Title search (existing)
    if q.strip():
        query = query.filter(Todo.title.ilike(f"%{q.strip()}%"))
    
    # Priority filter (NEW)
    if priority and priority in ("high", "medium", "low"):
        query = query.filter(Todo.priority == priority)

    todos = query.order_by(Todo.position).all()

    return templates.TemplateResponse(
        request=request,
        name="partials/todos_list.html",
        context={
            "todos": todos, 
            "list": list_obj, 
            "search_query": q,
            "priority_filter": priority if priority else "all"  # NEW CONTEXT - handle None
        },
    )
```

**No new routes required** - extend existing `/api/todos/search` endpoint.

### 2. Frontend Template Changes

#### File: `todo-app/src/app/templates/partials/todo_list_content.html`

**Add priority filter UI** after search bar (after line 43, before quick-add form):

```html
<!-- Search -->
<div class="search-bar">
    <sl-input
        placeholder="Search todos..."
        clearable
        hx-get="/api/todos/search"
        hx-trigger="keyup changed delay:300ms, search"
        hx-target="#todos-list"
        hx-swap="innerHTML"
        hx-vals='js:{list_id: "{{ current_list.id }}", priority: getActivePriority()}'
        name="q"
        id="search-input">
        <sl-icon slot="prefix" name="search"></sl-icon>
    </sl-input>
</div>

<!-- Priority Filter (NEW SECTION) -->
<div class="priority-filter" id="priority-filter">
    <sl-button-group label="Filter by priority">
        <sl-button 
            size="small" 
            variant="primary" 
            data-priority="all"
            onclick="filterByPriority('all', '{{ current_list.id }}')">
            All
        </sl-button>
        <sl-button 
            size="small" 
            variant="neutral" 
            data-priority="high"
            onclick="filterByPriority('high', '{{ current_list.id }}')">
            <sl-icon name="exclamation-circle"></sl-icon>
            High
        </sl-button>
        <sl-button 
            size="small" 
            variant="neutral" 
            data-priority="medium"
            onclick="filterByPriority('medium', '{{ current_list.id }}')">
            <sl-icon name="dash-circle"></sl-icon>
            Medium
        </sl-button>
        <sl-button 
            size="small" 
            variant="neutral" 
            data-priority="low"
            onclick="filterByPriority('low', '{{ current_list.id }}')">
            <sl-icon name="circle"></sl-icon>
            Low
        </sl-button>
    </sl-button-group>
</div>

<!-- Quick add todo -->
<!-- ... existing quick-add form ... -->
```

**Update quick-add form** `hx-on::after-request` to reset filter (line ~49):

```html
<form class="quick-add-form"
      hx-post="/api/todos"
      hx-target="#todos-list"
      hx-swap="beforeend"
      hx-on::after-request="if(event.detail.successful) { this.reset(); resetPriorityFilter('{{ current_list.id }}'); }">
```

#### File: `todo-app/src/app/templates/partials/todos_list.html`

**Update empty state message** to reflect active filters:

```html
{% if todos %}
{% for todo in todos %}
{% include "partials/todo_item.html" %}
{% endfor %}
{% else %}
<div class="empty-todos">
    <sl-icon name="inbox" class="empty-icon"></sl-icon>
    {% set active_filter = priority_filter|default("all") %}
    {% set query = search_query|default("") %}
    {% if query and active_filter != 'all' %}
    <p>No todos match "{{ query }}" with {{ active_filter }} priority</p>
    {% elif query %}
    <p>No todos match "{{ query }}"</p>
    {% elif active_filter != 'all' %}
    <p>No {{ active_filter }} priority todos</p>
    {% else %}
    <p>No todos yet. Add your first task above!</p>
    {% endif %}
</div>
{% endif %}
```

### 3. JavaScript Changes

#### File: `todo-app/src/app/static/js/app.js`

**Add priority filter functions** (after theme toggle, before Sortable init):

```javascript
// Priority filter functions
function getActivePriority() {
    const activeBtn = document.querySelector('#priority-filter sl-button[variant="primary"]');
    const priority = activeBtn ? activeBtn.dataset.priority : 'all';
    return priority === 'all' ? '' : priority;
}

function filterByPriority(priority, listId) {
    // Update button states (active = primary, inactive = neutral)
    const buttons = document.querySelectorAll('#priority-filter sl-button');
    buttons.forEach(btn => {
        if (btn.dataset.priority === priority) {
            btn.setAttribute('variant', 'primary');
        } else {
            btn.setAttribute('variant', 'neutral');
        }
    });

    // Get current search query
    const searchInput = document.getElementById('search-input');
    const searchQuery = searchInput ? searchInput.value : '';

    // Trigger HTMX request with priority filter
    const priorityParam = priority === 'all' ? '' : priority;
    htmx.ajax('GET', '/api/todos/search', {
        target: '#todos-list',
        swap: 'innerHTML',
        values: {
            list_id: listId,
            q: searchQuery,
            priority: priorityParam
        }
    });
}

function resetPriorityFilter(listId) {
    // Reset to "all" after adding new todo
    filterByPriority('all', listId);
}
```

**Handle search input clear event** (in DOMContentLoaded):

```javascript
document.addEventListener('DOMContentLoaded', () => {
    // ... existing theme init code ...
    initSortable();
    
    // Handle search clear button
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('sl-clear', () => {
            const listId = document.querySelector('[data-list-id]')?.dataset.listId;
            if (listId) {
                const activeBtn = document.querySelector('#priority-filter sl-button[variant="primary"]');
                const activePriority = activeBtn?.dataset.priority || 'all';
                
                htmx.ajax('GET', '/api/todos/search', {
                    target: '#todos-list',
                    swap: 'innerHTML',
                    values: { 
                        list_id: listId, 
                        q: '', 
                        priority: activePriority === 'all' ? '' : activePriority 
                    }
                });
            }
        });
    }
});
```

**Update existing htmx:afterSwap handler** (modify existing, don't create new):

```javascript
// Re-initialize sortable after HTMX swaps
document.body.addEventListener('htmx:afterSwap', (evt) => {
    if (evt.detail.target.id === 'sidebar-lists') {
        initListSortable();
    }
    if (evt.detail.target.id === 'todos-list' || evt.detail.target.id === 'main-content') {
        initTodoSortable();
        
        // Reset priority filter to "all" when switching lists (main-content swap)
        if (evt.detail.target.id === 'main-content') {
            const priorityButtons = document.querySelectorAll('#priority-filter sl-button');
            if (priorityButtons.length > 0) {
                priorityButtons.forEach(btn => {
                    btn.setAttribute('variant', btn.dataset.priority === 'all' ? 'primary' : 'neutral');
                });
            }
        }
    }
});
```

### 4. CSS Changes

#### File: `todo-app/src/app/static/css/styles.css`

**Add priority filter styles** (after `.quick-add-form`, around line 365):

```css
/* Priority filter */
.priority-filter {
    margin: 0 0 16px 0;
}

.priority-filter sl-button-group {
    width: 100%;
    display: flex;
}

.priority-filter sl-button {
    flex: 1;
    transition: all 0.15s ease;
}

.priority-filter sl-icon {
    font-size: 14px;
    margin-right: 4px;
}

/* Ensure button group buttons are equal width */
.priority-filter sl-button::part(base) {
    justify-content: center;
}
```

### 5. Integration Points

#### Search + Filter Interaction
- Search input uses `hx-vals='js:{...}'` to dynamically include priority via `getActivePriority()` helper
- Filter buttons trigger search with current search query via `htmx.ajax()`
- Both parameters sent to same `/api/todos/search` endpoint
- Server applies both filters simultaneously

#### State Management
- Priority filter state tracked via button `variant` attribute (primary = active, neutral = inactive)
- Helper function `getActivePriority()` reads active button state
- Filter resets to "all" when:
  - Switching to different list (via `htmx:afterSwap` on `#main-content`)
  - Adding new todo (via `resetPriorityFilter()`)
- Search clear button (`sl-clear` event) maintains active priority filter

#### Visual Consistency
- Filter buttons use Shoelace components (matches existing UI)
- Icons: `exclamation-circle` (high), `dash-circle` (medium), `circle` (low)
- Colors: high=danger, medium=warning, low=success (via badge variants already in use)
- Size: `small` to match search input proportion

### 6. Testing Checklist

**Manual Testing:**
- [ ] Filter by high → only high priority todos shown
- [ ] Filter by medium → only medium priority todos shown
- [ ] Filter by low → only low priority todos shown
- [ ] Filter by all → all todos shown
- [ ] Active button has primary variant (blue)
- [ ] Search + filter combination works correctly
- [ ] Search clear (X button) maintains active filter
- [ ] Empty state messages reflect active filters
- [ ] Adding new todo resets filter to "all"
- [ ] Switching lists resets filter to "all"
- [ ] Filter state updates without page reload (HTMX)
- [ ] Button group renders correctly in light/dark mode
- [ ] Mobile responsive (button group wraps or shrinks appropriately)
- [ ] Keyboard navigation through filter buttons works

**Edge Cases:**
- [ ] List with no todos of selected priority shows helpful empty state
- [ ] Filter works on list with 1 todo
- [ ] Filter works on list with 100+ todos
- [ ] Search query + priority filter both empty shows all
- [ ] Search query clears but filter remains active
- [ ] Toggling todo completion while filter is active (todo remains visible)
- [ ] Editing todo priority while filter is active (todo remains visible until re-filter)

### 7. Files Summary

| File | Action | Changes |
|------|--------|---------|
| `routes/todos.py` | Modify | Add `priority` param to `search_todos()`, update query logic, add to context with None handling |
| `templates/partials/todo_list_content.html` | Modify | Add priority filter UI (button group), update search `hx-vals` with dynamic priority, update quick-add event |
| `templates/partials/todos_list.html` | Modify | Update empty state messages for filter combinations, add template defaults |
| `static/js/app.js` | Modify | Add `getActivePriority()`, `filterByPriority()`, `resetPriorityFilter()`, handle `sl-clear` event, update existing `htmx:afterSwap` handler |
| `static/css/styles.css` | Modify | Add `.priority-filter` styles |

**No new files created.**

## Implementation Steps

1. **Backend first**: Modify `search_todos()` endpoint to accept and handle `priority` parameter (ensure None is converted to "all")
2. **Template updates**: Add filter UI to `todo_list_content.html`, update empty states with safe defaults
3. **JavaScript**: Implement filter toggle logic, state management helpers, and search clear event handler
4. **CSS**: Add styling for filter component (after `.quick-add-form` section)
5. **Manual testing**: Verify all interactions work as expected
6. **Edge case testing**: Test combinations and boundary conditions

## Known Limitations

1. **Edited todo visibility**: When a todo's priority is changed while a filter is active, the todo remains visible in the list until the user manually re-applies the filter. This is acceptable for the workshop scope and avoids complex real-time filtering logic.

2. **No URL state**: Filter state is not persisted in URL query parameters, so filtered views are not shareable via URL. This is intentional to keep the implementation simple for educational purposes.

## Alternative Approaches Considered

### Hidden Input + hx-include
- **Pros**: More declarative, less JavaScript
- **Cons**: Doesn't work with button-triggered filtering, creates unnecessary state duplication
- **Decision**: Use JavaScript-based state management via button variant attributes

### Radio Buttons Instead of Button Group
- **Pros**: Native HTML, simpler JavaScript
- **Cons**: Less visually appealing, doesn't match Shoelace design system
- **Decision**: Use button group for visual consistency

### Separate Filter Endpoint
- **Pros**: Clearer separation of concerns
- **Cons**: Duplicates logic, requires syncing search/filter state across multiple endpoints
- **Decision**: Extend existing `/search` endpoint for simplicity

### URL Query Parameters for Filter State
- **Pros**: Shareable URLs, browser back/forward support
- **Cons**: More complex state management, HTMX doesn't update URL by default
- **Decision**: Use button variant state for workshop simplicity (acceptable tradeoff)

### Persist Filter State in localStorage
- **Pros**: Filter persists across sessions
- **Cons**: More complex, may confuse users when filter is active but not visible
- **Decision**: Reset on list change for predictable UX

### Auto-refresh on Todo Edit/Toggle
- **Pros**: Edited todos immediately disappear if they no longer match filter
- **Cons**: Surprising UX, adds complexity to multiple endpoints
- **Decision**: Accept that edited todos remain visible until manual re-filter

## Open Questions
- Should filter persist when switching lists or reset to "all"? **Decision: Reset to "all"**
- Should newly added todos be immediately filtered if active filter excludes them? **Decision: Reset filter to "all" after add**
- Mobile layout: horizontal scroll or vertical stack? **Decision: Horizontal scroll (native button-group behavior)**
- Should search clear also reset priority filter? **Decision: No - maintain filter when clearing search**

## Review Notes

### Key Improvements from Initial Plan
1. **Simplified state management**: Removed hidden input approach in favor of reading button variant attributes directly
2. **Better template safety**: Added `|default()` filters to handle undefined context variables
3. **Search clear handling**: Added explicit `sl-clear` event listener to maintain filter state
4. **JavaScript patterns**: Modified existing event handlers instead of creating duplicates
5. **CSS placement**: More accurate line number guidance (after `.quick-add-form`, ~line 365)

### Acknowledged Limitations
- Edited todos remain visible until manual re-filter (acceptable for workshop scope)
- No URL state persistence (intentional simplification)
- Filter state lost on page refresh (acceptable - resets to "all")

## Success Criteria
- Users can filter todos by priority with single click
- Filter combines seamlessly with existing search
- UI clearly indicates active filter state
- No JavaScript errors in console
- Follows existing code patterns and style conventions
- All tests pass
