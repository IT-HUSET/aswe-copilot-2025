# ToDo Application Project Plan - Simplified Standalone Version

## Project Overview

A modern todo application built with Python, FastAPI, HTMX, and Shoelace Web Components. Demonstrates server-side rendering with SPA-like UX.

**What Makes This Special**:
- **Shoelace Components**: Accessible, consistent baseline UI out of the box
- **Zero External Dependencies**: SQLite, no cloud services, no build tools
- **Educational Focus**: Clean architecture, clear patterns, easy to understand
- **Instant Setup**: `uv run uvicorn` and you're live

## MVP Scope & Philosophy

**This is an MVP/Lab project** - educational clarity first. We prioritize:
- **Simple over complex**: Clear patterns over extensive features
- **Working over perfect**: Functional examples over edge case handling
- **Teachable over scalable**: Code easy to understand and modify
- **Zero setup friction**: No config, just run it

**UI/UX Baseline** (Shoelace defaults):
- Responsive layout (mobile, tablet, desktop)
- Dark mode via Shoelace theming
- Accessibility via Shoelace components (WCAG 2.1)

**MVP Feature Set**:
- Mock authentication (login, register, logout) - **no real security**
- Multiple todo lists per user
- Todo items with: title, notes, completion status, due dates, priority levels
- Basic search (text match on titles)
- List reordering via drag-drop (SortableJS) with visual drag handles

**Explicitly OUT of MVP Scope**:
- Tags/categories (can be added as workshop exercise)
- Advanced filtering/sorting
- Statistics dashboard
- Password reset/change (no real auth system)
- Email verification
- Rate limiting
- Extensive monitoring/observability
- CI/CD pipeline
- Database migrations (create tables on first run)

**What Makes This "Simple"**:
- ❌ No Supabase or any external service
- ❌ No PostgreSQL server or cloud database
- ❌ No real authentication (plain text passwords, mock sessions)
- ❌ No JWT tokens or password hashing
- ❌ No RLS policies or security concerns
- ✅ SQLite database (built into Python, single file)
- ✅ Data persists across restarts
- ✅ Can run immediately with `uv run uvicorn`
- ✅ Perfect for learning and workshops

## Technology Stack

### Core Technologies
- **Backend**: FastAPI 0.115+ - Modern async web framework, auto-generated API docs
- **Frontend**: HTMX 2.0+ - Server-side rendering with SPA-like UX, no build step
- **Templates**: Jinja2 - Python templating for HTML generation
- **UI Components**: Shoelace 2.20+ - Beautiful Web Components library (Material/iOS design)
- **Drag-Drop**: SortableJS 1.15+ - Drag-and-drop list reordering (CDN)
- **Database**: SQLite - Zero-config, single file, built into Python
- **ORM**: SQLAlchemy 2.0+ - Modern Python ORM with relationship management
- **Auth**: Mock sessions (UUID + cookies) - Educational only
- **Package Manager**: uv 0.5+ - 10-100x faster than pip
- **Python**: 3.13 recommended (3.12 and 3.11 also supported)
- **Browser Support**: Modern browsers only (Chrome, Firefox, Safari, Edge - last 2 versions)

### Dependencies

**Core** (`fastapi>=0.115.0`):
- `uvicorn[standard]>=0.32.0` - ASGI server with auto-reload
- `jinja2>=3.1.0` - Template engine
- `sqlalchemy>=2.0.0` - ORM for SQLite operations
- `python-multipart>=0.0.9` - Form data parsing

**Dev** (`pytest>=8.0.0`):
- `httpx>=0.27.0` - Async test client

**Total: 5 core + 2 dev dependencies** (vs 15+ in production stacks)

## Critical Technical Constraints

⚠️ **These constraints are non-negotiable for a working implementation.**

### 1. HTMX + Shoelace Form Components

**Critical**: HTMX does **not** automatically serialize Shoelace form components due to Shadow DOM encapsulation. You must use one of these approaches:

**Option A - HTMX Shoelace Extension (Recommended)**:
```html
<head>
  <script src="https://unpkg.com/htmx-ext-shoelace@2.0.0/shoelace.js"></script>
</head>
<form hx-ext="shoelace" hx-post="/api/todos">
  <sl-input name="title" required></sl-input>
  <sl-button type="submit">Add</sl-button>
</form>
```

**Option B - Manual Serialization** (if extension unavailable):
```javascript
document.body.addEventListener('htmx:configRequest', (evt) => {
  const form = evt.detail.elt.closest('form');
  if (form) {
    form.querySelectorAll('sl-input, sl-select, sl-checkbox, sl-textarea').forEach(el => {
      if (el.name) evt.detail.parameters[el.name] = el.value;
    });
  }
});
```

**Key requirements**:
- ✅ All form elements must have a `name` attribute
- ✅ Use `hx-ext="shoelace"` on forms or parent containers
- ✅ Test form submission early in development

### 2. Global 401 Exception Handler (Required)

**Problem**: Default `HTTPException(401)` returns raw JSON `{"detail": "Not authenticated"}` for browser requests, and HTMX requests don't redirect gracefully.

**Solution**: Implement a **global exception handler** in `main.py`:
```python
from fastapi import Request
from fastapi.responses import RedirectResponse, Response

@app.exception_handler(HTTPException)
async def auth_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        login_url = f"/login?next={request.url.path}"
        # HTMX request: return 200 with HX-Redirect header
        if request.headers.get("HX-Request"):
            response = Response(status_code=200)
            response.headers["HX-Redirect"] = login_url
            return response
        # Browser request: standard redirect
        return RedirectResponse(url=login_url, status_code=302)
    raise exc
```

### 3. Web Component Hydration Safety

**Problem**: Shoelace components load asynchronously. Calling methods on them before they're defined causes `alert.toast is not a function` errors.

**When this matters**: Only when **dynamically creating** Shoelace components via JavaScript. Components in static HTML (loaded via CDN in `<head>`) are typically ready before your scripts run.

**Solution for dynamic components**:
```javascript
// For dynamically created components, wait for definition
customElements.whenDefined('sl-alert').then(() => {
    document.querySelector('sl-alert').toast();
});
```

**Safe pattern**: Components in templates loaded at page load don't typically need this guard.

### 4. OOB Updates Strategy

**Approach**: Use simple OOB swaps for sidebar count badges from the start. This keeps UI in sync without complex state management.

**Pattern**:
```html
<!-- Primary response (main content) -->
<div id="todos-list">...</div>
<!-- OOB: Update sidebar count badge -->
<span id="list-{id}-count" hx-swap-oob="true">5</span>
```

**When to use OOB**:
- Todo add/delete → update list count badge
- Todo completion toggle → update list count badge
- List delete → remove from sidebar

**Keep it simple**: Only update count badges via OOB. Don't try to sync complex state across multiple components.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (Client)                         │
│  ┌────────────────┐  ┌────────────────────────────────────┐ │
│  │ HTMX 2.0       │  │ Shoelace 2.20 + Native HTML        │ │
│  │ - hx-get/post  │  │ - Buttons, Dialogs, Alerts         │ │
│  │ - hx-swap      │  │ - Spinners, Icons, Badges          │ │
│  │ - hx-target    │  │ - Native <input> for forms (!)     │ │
│  └────────────────┘  └────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP/HTTPS (HTMX requests)
                             ↓
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Application (Python)                   │
│                                                             │
│  Routes (routes/)              Templates (templates/)       │
│  ├─ auth.py                    ├─ base.html                 │
│  ├─ pages.py                   ├─ login.html                │
│  ├─ todo_lists.py              ├─ app.html                  │
│  └─ todos.py                   └─ partials/                 │
│      ↓ validate (Pydantic)         ├─ todo_list_item.html  │
│      ↓ authenticate                ├─ todo_item.html        │
│      ↓ call ORM directly           └─ error.html            │
│                                                             │
│  SQLAlchemy ORM (database.py)                              │
│  ├─ User (email, password)                                  │
│  ├─ TodoList (name, color, position)                        │
│  └─ Todo (title, note, due_date, priority)                  │
│      ↓ relationships, CASCADE deletes                       │
└──────────────────────────┬──────────────────────────────────┘
                           │ SQLAlchemy queries
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              SQLite Database (todo.db)                      │
│  Tables: users, todo_lists, todos                           │
│  - Foreign keys with CASCADE delete                         │
│  - Indexes on email                                         │
│  - NullPool (no connection pooling)                         │
└─────────────────────────────────────────────────────────────┘

Session Management: In-memory dict {session_id: {"user_id", "expires"}}
Static Assets: styles.css (tokens + layout), app.js (HTMX handlers, SortableJS init)
CDN Assets: Shoelace, HTMX, SortableJS
```

### Authentication & Session Management (Mock)

**Session Strategy** (intentionally simple):
- Random UUID session IDs (no JWT, no password hashing)
- Plain text passwords in database
- Session cookie: `httponly=True`, `max_age=3600`
- **In-memory session storage**: `sessions = {session_id: {"user_id": str, "expires": datetime}}`
- Sessions lost on server restart (acceptable for educational use)

**Auth Flow**:
1. `/` → check cookie → redirect to `/login` if invalid
2. Login → verify email/password (plain text) → create session → set cookie → redirect `/app`
3. `/app` → if user has lists → auto-redirect to first list; else show empty state
4. Logout → delete session from memory → clear cookie → redirect `/login`

**Protected Routes**: Use `get_current_user_id` dependency (checks session dict, returns user_id or 401)

**Unauthenticated Access Handling**:
- Store intended destination: `/login?next=/app/lists/5`
- After successful login → redirect to `next` param (default: `/app`)
- For HTMX requests: return 401 + `HX-Redirect: /login?next=...` header
- Login page: friendly message "Please log in to continue"

⚠️ **INSECURE BY DESIGN** - Educational only, never production!

### Design System (Standalone)

Clean, minimalistic, productivity-focused design. **Philosophy**: Clarity over cleverness. Function over form (but with good form).

#### Color Palette
```css
:root {
  /* Primary - Blue for focus and productivity */
  --color-primary: #3b82f6;        /* Main actions, links, active states */
  --color-primary-dark: #2563eb;   /* Hover states */
  --color-primary-pale: #dbeafe;   /* Subtle backgrounds, active list item */

  /* Neutrals - Professional gray scale */
  --color-white: #ffffff;
  --color-gray-50: #f8fafc;        /* Page background, subtle hover */
  --color-gray-100: #f1f5f9;       /* Card backgrounds (dark mode) */
  --color-gray-200: #e2e8f0;       /* Borders */
  --color-gray-300: #cbd5e1;       /* Dividers, disabled borders */
  --color-gray-500: #64748b;       /* Secondary text, placeholders */
  --color-gray-700: #334155;       /* Body text */
  --color-gray-900: #0f172a;       /* Headings */

  /* Semantic - Purposeful, minimal use */
  --color-success: #10b981;        /* Completion indicators */
  --color-warning: #f59e0b;        /* Due today, medium priority */
  --color-error: #ef4444;          /* Overdue, high priority, delete */
  --color-low: #65a30d;            /* Low priority (olive/lime green) */
}
```

**Dark Mode**:
- **Default**: Follows system preference (`prefers-color-scheme: dark`)
- **Toggle**: In header, next to logout button
- **Persistence**: Stores preference in `localStorage` (key: `theme`)
- **Implementation**: Add/remove `.sl-theme-dark` class on `<html>` element
- Background: `#121212` (not pure black)
- Inverted gray scale, slightly lighter accents for contrast
- Maintains WCAG AA contrast (4.5:1 minimum)

#### Typography
- **Font**: `Inter, system-ui, -apple-system, sans-serif` (fallback to system fonts)
- **Base size**: 16px (1rem)
- **Scale**: 12px (meta), 14px (labels), 16px (body), 18px (subheadings), 20px (list names), 24px (page titles)
- **Weights**: 400 (body), 500 (emphasis), 600 (headings)
- **Line height**: 1.5 for body text (optimized for list scanning)

#### Spacing & Layout
- **Base grid**: 8px unit
- **Common values**: 4px, 8px, 12px, 16px, 24px, 32px, 48px
- **Component padding**: 16-24px
- **Gap between list items**: 12px
- **Sidebar width**: 280px
- **Container max-width**: 1024px

#### Borders & Radius
- **Border width**: 1px (standard), 4px (priority/alert indicators)
- **Border radius**: 4px (inputs), 8px (cards, buttons), 12px (large cards), 16px (modals), full (badges)

#### Shadows
- **Cards**: `0 1px 3px rgba(0,0,0,0.1)` (default), `0 4px 6px rgba(0,0,0,0.1)` (hover)
- **Modals**: `0 20px 25px rgba(0,0,0,0.1)`
- **Focus ring**: `0 0 0 3px rgba(59,130,246,0.5)` - WCAG 2.4.7 compliant

#### Transitions
- **Fast**: 100ms (checkbox toggle)
- **Standard**: 150ms (buttons, hover)
- **Slow**: 200ms (modals)
- **Easing**: ease-out
- **Reduced motion**: Respects `prefers-reduced-motion`

#### Accessibility (WCAG 2.1 AA)
- **Touch targets**: 44x44px minimum
- **Focus indicators**: 3px solid blue ring, visible on all backgrounds
- **Color contrast**: 4.5:1 text, 3:1 UI elements
- **Never**: Remove focus outlines, use color alone for status

### UI Components (Shoelace)

**Shoelace Components** (all work with HTMX in Shoelace 2.20+):
- `<sl-button>` - Primary, secondary, danger variants
- `<sl-input>` - Text inputs with prefix/suffix icon slots
- `<sl-textarea>` - Multi-line text
- `<sl-select>` + `<sl-option>` - Dropdowns
- `<sl-checkbox>` - Checkboxes (e.g., todo completion)
- `<sl-color-picker>` - Color selection
- `<sl-dialog>` - Modal dialogs for forms and confirmations
- `<sl-alert>` - Success, error, warning notifications
- `<sl-spinner>` - Loading indicators
- `<sl-icon>` - Icons from Shoelace icon library
- `<sl-badge>` - Counts, priority indicators
- `<sl-card>` - Content containers
- `<sl-divider>` - Visual separators

**Key requirement**: All form elements must have a `name` attribute for HTMX serialization.

**Shoelace Shadow DOM Notes**:
- Use `::part()` selectors to style internal elements (e.g., `sl-input::part(prefix)`)
- Store data in `data-*` attributes on parent elements for event delegation
- Use `customElements.whenDefined()` before calling methods on **dynamically created** components
- Inline `onclick` handlers on Shoelace buttons work normally
- For icon buttons (`<sl-icon-button>`), use `onclick` with `event.stopPropagation()` to prevent event bubbling

### Visual Specifications

| Element | Style |
|---------|-------|
| **Priority High** | Red badge (`danger`) + 4px red left border |
| **Priority Medium** | Amber badge (`warning`) + 4px amber left border |
| **Priority Low** | Green badge (`success`) + 4px olive/lime left border (`--color-low`) |
| **Active list item** | Blue-100 background (`#dbeafe`) + blue text + 3px left border |
| **Overdue todo** | 4px red left border + red due date text |
| **Due today** | Amber due date text |
| **Completed todo** | 60% opacity, strikethrough title |

**Input Field Icons**: Use Shoelace's `slot="prefix"` with `<sl-icon>`. Icons: `envelope` (email), `lock` (password), `search`, `plus-circle` (quick-add). Style with `sl-input::part(prefix) { padding-left: 12px; }`.

**Hover Behaviors**:
- List items: show edit/delete buttons, hide count badge (hidden by default)
- Todo items: show edit/delete buttons and drag handle on hover
- Drag handles: hidden by default (`opacity: 0`), show on hover (`opacity: 0.5`), grabbing cursor on drag

### Drag-Drop Implementation (SortableJS)

**Handle classes and CSS**:
```css
/* List drag handle */
.drag-handle {
    cursor: grab;
    opacity: 0;
    transition: opacity 0.15s;
}
.list-item:hover .drag-handle { opacity: 0.5; }
.drag-handle:active { cursor: grabbing; opacity: 1; }

/* Todo drag handle (same pattern) */
.todo-drag-handle { /* same styles */ }
.todo-item:hover .todo-drag-handle { opacity: 0.5; }
```

**JavaScript initialization** (app.js):
```javascript
function initSortable(containerId, handleClass, onEndCallback) {
    const el = document.getElementById(containerId);
    if (el && typeof Sortable !== 'undefined') {
        new Sortable(el, { animation: 150, handle: handleClass, ghostClass: 'sortable-ghost', onEnd: onEndCallback });
    }
}

// Re-initialize after HTMX swaps
document.body.addEventListener('htmx:afterSwap', (evt) => {
    if (evt.detail.target.id === 'sidebar-lists') initSortable('sidebar-lists', '.drag-handle', () => htmx.trigger(el, 'end'));
    if (evt.detail.target.id === 'todos-list') initSortable('todos-list', '.todo-drag-handle', (e) =>
        htmx.ajax('POST', `/api/todos/${e.item.dataset.todoId}/reorder`, { values: { position: e.newIndex }, swap: 'none' }));
});
```

**Backend reorder**: Shift positions of affected items between old and new position, then set item to new position. Standard array reorder algorithm.

**Empty States**:
- Large icon (120px), gray-400 color
- Title + single sentence message
- One primary CTA button

### Request Flow

1. **HTMX Pattern**: User action → `hx-get/post/delete` → server returns HTML partial → HTMX swaps into DOM
2. **Data Flow**: Route → authenticate → validate (Pydantic) → query ORM → render template → return HTML

## Domain Model

### SQLAlchemy Database Models

**database.py** (pseudo code):
```python
from sqlalchemy import create_engine, NullPool
DATABASE_URL = "sqlite:///./todo.db"
engine = create_engine(DATABASE_URL,
                       connect_args={"check_same_thread": False},
                       poolclass=NullPool)  # Avoid file-locking issues

class User(Base):
    id, email (unique, indexed), password (plain text), created_at
    relationship: todo_lists (CASCADE delete)

class TodoList(Base):
    id, user_id (FK→users), name(100), description, color(7), position, timestamps
    relationships: user, todos (CASCADE delete)

class Todo(Base):
    id, list_id (FK→todo_lists), title(200), note, is_completed, completed_at,
    due_date, priority (low/medium/high), position, timestamps
    relationship: todo_list

def init_db(): Base.metadata.create_all()
def get_db(): yield SessionLocal() (with cleanup)
```

**Features**: CASCADE deletes, email index, UUID PKs, auto timestamps

### Pydantic Models

**Request/Response validation**:
```python
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)  # Min 6 chars
    confirm_password: str

class TodoListCreate(BaseModel):
    name: str = Field(max_length=100)
    description: Optional[str]
    color: str = Field(default="#3b82f6", pattern="^#[0-9a-fA-F]{6}$")  # Hex validation

class TodoCreate(BaseModel):
    title: str = Field(max_length=200)
    note: Optional[str] = Field(default=None, max_length=2000)  # Reasonable limit
    due_date: Optional[date] = None
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")

class TodoUpdate(BaseModel):
    # All Optional: title, note, is_completed, due_date, priority, position
```

**Key Validations**: EmailStr, max lengths, password min 6 chars, hex colors, priority enum

## Project Structure

```
todo-lab-python/
├── pyproject.toml, README.md, PROJECT_PLAN_SIMPLE.md
├── todo.db (created on first run)
└── src/app/
    ├── main.py, config.py, database.py, utils.py
    ├── core/deps.py (auth, db dependencies)
    ├── models/ (Pydantic: auth.py, todo_list.py, todo.py)
    ├── routes/ (auth.py, pages.py, todo_lists.py, todos.py)
    ├── templates/ (base.html, login.html, register.html, app.html, 404.html, partials/*)
    └── static/ (css/styles.css, js/app.js)
tests/ (conftest.py, test_*.py, test_integration.py)
```

**Key Simplifications**: No services/ layer (routes call ORM directly), no .env required, single database file

## Template & Code Conventions

**Template Variable Naming** (consistent across all templates):
- `list` - TodoList object in partials (when iterating)
- `active_list` - Currently selected TodoList in main app view
- `lists` - List of TodoList objects
- `todo` - Todo object
- `todos` - List of Todo objects
- `user` - Current user object
- `error` - Error message string

**Template Fallback Pattern** (for partials used in multiple contexts):
```jinja2
{% set current_list = list if list is defined else active_list %}
```
Use when a partial may receive either `list` (from loop) or `active_list` (from page context).

**Shared Utilities** (`src/app/utils.py`):
```python
def is_overdue(todo: Todo) -> bool:
    """True if due_date < today AND not completed"""

def is_due_today(todo: Todo) -> bool:
    """True if due_date == today"""
```
Always pass these helpers to todo templates - never duplicate logic in routes.

**HTMX OOB Swaps**: Use `hx-swap-oob="true"` to update sidebar count badges when todos change. See "Critical Technical Constraints" section 4 for pattern.

## Non-Functional Requirements

**HTTP Headers** (all dynamic responses):
```python
response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
response.headers["Pragma"] = "no-cache"
```

**UI Synchronization**:
- Sidebar todo counts update immediately on add/remove (HTMX OOB)
- No page refresh required to see count changes
- All related UI components stay in sync

**Data Persistence Acceptance Criteria**:
- [ ] User adds todo, logs out, logs back in → todo visible
- [ ] Verify with fresh browser/incognito window
- [ ] Data survives server restart (SQLite file)

**Session Expiry**: See "Unauthenticated Access Handling" in Architecture section. Key: never show raw 401 - always redirect with `next` param.

## Features & Requirements

### Phase 1: Authentication & Basic Structure

#### 1.1 Authentication System (Mock)
- [ ] Login/register pages with forms
- [ ] Session cookie management (UUID in-memory)
- [ ] Protected routes (auth dependency)
- [ ] Error handling for auth failures

**Acceptance Criteria**:
- Validates email format, password min 6 chars, passwords match
- Success: create session in memory, set cookie, redirect /app (or `?next=` destination)
- Failure: show error in form
- Logout: delete from sessions dict, clear cookie, redirect /login
- Protected routes redirect to `/login?next={current_path}` if unauthenticated
- Login page shows context message when `next` param present

**Implementation**: In-memory dict `sessions = {uuid: {"user_id": str, "expires": datetime}}`, plain text password check

#### 1.2 Base UI Layout

**Base Template** (templates/base.html):
- [ ] Shoelace 2.20+ CDN imports (CSS + Web Components)
- [ ] Dark mode toggle (Shoelace theme switcher)
- [ ] Responsive layout (mobile-first, 320px+)
- [ ] Warning banner (educational project notice)

**Layout Components**:
- [ ] Header: logo, user email, logout button
- [ ] Sidebar: list of todo lists with counts, add button
- [ ] Main: todo display area with `<sl-spinner>` loading states
- [ ] Empty states with helpful CTAs

### Phase 2: Todo Lists Management

#### 2.1 Todo List CRUD
- [ ] View all todo lists (sidebar)
- [ ] Create new todo list
- [ ] Edit todo list (name, description, color)
- [ ] Delete todo list (with confirmation)
- [ ] Reorder todo lists (drag-drop with SortableJS, handles hidden until hover)
- [ ] Select active list (highlight in sidebar)
- [ ] Display todo count per list

**Acceptance Criteria**:
- Create with name (required), description, color (default blue)
- Click list → load todos in main area
- Delete with confirmation (CASCADE to todos via FK)
- Drag handles: hidden by default (opacity: 0), visible on hover (opacity: 0.5)

**Implementation**: Routes call ORM directly (no service layer), SortableJS for drag-drop, position recalculated on drop, CASCADE deletes via FK


#### 2.2 List UI Components

**List Item** (partials/todo_list_item.html):
- [ ] `<sl-card>` with color indicator, name, todo count badge
- [ ] Edit/delete/reorder action buttons
- [ ] Active state highlighting

**Forms**:
- [ ] Add/Edit: `<sl-dialog>` with name input, description, color picker
- [ ] Delete: confirmation dialog with warning

**Empty State**: Icon + message + CTA button

### Phase 3: Todo Items Management

#### 3.1 Todo CRUD
- [ ] View todos in selected list
- [ ] Create new todo with title
- [ ] Edit todo (modal form)
- [ ] Delete todo (with confirmation)
- [ ] Mark todo as complete/incomplete (checkbox)
- [ ] Reorder todos within list (drag-drop with SortableJS)
- [ ] Add notes to todo (expandable section)
- [ ] Set due date (date picker)
- [ ] Set priority level (dropdown: low/medium/high)

**Acceptance Criteria**:
- Quick-add with title only
- Checkbox toggles completion + completed_at timestamp
- Overdue = due_date < today AND not completed (server-side)
- Edit validates title required, max 200 chars
- Delete with confirmation

**Implementation**: Overdue calculated in route, position auto-managed, completion toggle updates timestamp

#### 3.2 Todo UI Components

**Todo Item** (partials/todo_item.html):
- [ ] Checkbox for completion (strikethrough when done)
- [ ] Title, priority badge, due date display
- [ ] Edit/delete/reorder action buttons
- [ ] Visual indicators: overdue (red), due today (blue), priority colors

**Forms**:
- [ ] Quick add: input + button, Enter submits
- [ ] Edit dialog: title, notes, due date, priority, completion toggle

**Empty State**: Icon + message

### Phase 4: Search (MVP Minimal)

#### 4.1 Basic Search
- [ ] Search todos by title text match (case-insensitive)
- [ ] Search input with HTMX live search (300ms debounce)
- [ ] Clear search button
- [ ] Show "X results" or "No results" message

**Acceptance Criteria**:
- Filter current list only
- Partial text match on title (case-insensitive)
- Empty search shows all

**Implementation**: `Todo.title.ilike(f"%{query}%")` with HTMX debounce 300ms

### Phase 5: Polish & Testing

#### 5.1 UX Polish

**Core**:
- [ ] Loading spinners during HTMX requests
- [ ] Error/success alerts (`<sl-alert>`)
- [ ] Form validation feedback
- [ ] Responsive breakpoints (mobile/tablet/desktop)

**Optional Enhancements**:
- [ ] Keyboard shortcuts (Ctrl+N, Esc, Enter)
- [ ] ARIA labels, screen reader support

#### 5.2 Testing
- [ ] Pydantic model validation tests
- [ ] Route tests with in-memory SQLite
- [ ] Auth flow tests
- [ ] CASCADE delete verification

#### 5.3 Integration Tests (Full User Journeys)
- [ ] Register → add list → add todo → logout → login → verify data persists
- [ ] Add todo with due date → verify overdue display next day
- [ ] Delete list → verify CASCADE deletes all todos
- [ ] Multiple browser tabs → verify UI sync (OOB swaps)
- [ ] Fresh incognito window test for data persistence
- [ ] Access `/app/lists/5` when logged out → redirect to login with `next` → login → lands on `/app/lists/5`

## Implementation Strategy

### Development Phases

#### Phase 1: Foundation & Auth
- Setup: uv, dependencies, FastAPI structure
- Database: SQLAlchemy models (User, TodoList, Todo) with NullPool
- Auth: In-memory sessions, login/register routes
- Templates: Base layout, login page, Shoelace imports
- Seed demo data on startup

**Deliverable**: Register, login, logout working

#### Phase 2: Lists
- TodoList CRUD routes (call ORM directly)
- App layout (header, sidebar, main)
- List display, create/edit/delete, reordering

**Deliverable**: Manage multiple todo lists

#### Phase 3: Todos
- Todo CRUD routes (call ORM directly)
- Display templates, quick-add, edit form
- Completion toggle, delete, reordering

**Deliverable**: Manage todos with all MVP features

#### Phase 4: Polish
- Search (title match, HTMX debounce)
- Loading indicators, error messages
- Visual indicators (overdue, priorities)
- Basic tests
- README

**Deliverable**: Functional MVP, tested, documented

### Technical Implementation Details

#### HTMX Patterns

```html
<!-- CRUD operations -->
<form hx-post="/api/lists" hx-target="#container" hx-swap="afterbegin">
<button hx-delete="/api/lists/{id}" hx-confirm="Delete?" hx-target="closest .item">
<input hx-patch="/api/todos/{id}/toggle" hx-target="closest .todo-item">

<!-- Live search -->
<input hx-get="/api/search" hx-trigger="keyup changed delay:300ms" hx-target="#results">
```

**Key Patterns**: `hx-post/get/patch/delete`, `hx-target` (swap destination), `hx-swap` (strategy), `hx-confirm`, `hx-trigger` (debounce)

#### Database & Seed Data

**database.py**:
```python
from sqlalchemy import create_engine, NullPool
engine = create_engine("sqlite:///./todo.db",
                       connect_args={"check_same_thread": False},
                       poolclass=NullPool)
def init_db(): Base.metadata.create_all()
def get_db(): yield SessionLocal() (cleanup on exit)
```

**Startup seed** (main.py) - uses `lifespan` context manager (not deprecated `@app.on_event`):
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()  # Create tables
    seed_demo_data()  # demo@example.com / demo123 + sample list + todos
    yield
    # Shutdown (cleanup if needed)

app = FastAPI(lifespan=lifespan)
```

#### Authentication & Route Examples

**In-memory sessions** (core/deps.py):
```python
from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import Cookie, HTTPException

sessions = {}  # {session_id: {"user_id": str, "expires": datetime}}

def create_session(user_id: str) -> str:
    session_id = str(uuid4())
    sessions[session_id] = {"user_id": user_id, "expires": datetime.now(timezone.utc) + timedelta(hours=1)}
    return session_id

async def get_current_user_id(
    session_id: Annotated[str | None, Cookie()] = None
) -> str:
    if not session_id or session_id not in sessions:
        raise HTTPException(401, "Not authenticated")
    session = sessions[session_id]
    if session["expires"] < datetime.now(timezone.utc):
        del sessions[session_id]
        raise HTTPException(401, "Session expired")
    return session["user_id"]
```

**Auth routes** (routes/auth.py):
```python
@router.post("/login")
async def login(email: str = Form(), password: str = Form(), db = Depends(get_db)):
    user = db.query(User).filter_by(email=email).first()
    if not user or user.password != password:  # Plain text!
        return error_partial("Invalid credentials")

    session_id = create_session(user.id)
    response = Response()
    response.set_cookie("session_id", session_id, httponly=True, max_age=3600)
    response.headers["HX-Redirect"] = "/app"
    return response

# Similar for register (check duplicates, create user, auto-login)
# Logout: delete from sessions dict, clear cookie
```

**Route example** (routes/todo_lists.py - NO service layer):
```python
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

# Type aliases for cleaner signatures
CurrentUser = Annotated[str, Depends(get_current_user_id)]
DbSession = Annotated[Session, Depends(get_db)]

@router.post("/api/lists")
async def create_list(data: TodoListCreate, user_id: CurrentUser, db: DbSession):
    # Calculate position
    max_pos = db.query(func.max(TodoList.position)).filter_by(user_id=user_id).scalar()

    # Create directly
    new_list = TodoList(user_id=user_id, name=data.name, position=(max_pos or -1) + 1, ...)
    db.add(new_list)
    db.commit()

    return templates.TemplateResponse("partials/todo_list_item.html", {"list": new_list})
```

#### Error Handling

See "Critical Technical Constraints" section for 401 handler pattern.

**Additional handlers** (main.py):
- `SQLAlchemyError` → render `partials/error.html` with "Database error", status 500
- `404` → HTMX requests get `partials/error.html`, browser requests get `404.html`

**Client-side** (app.js): Listen for `htmx:responseError`, show `<sl-alert>` toast (use `customElements.whenDefined` first).

**Validation**: Pydantic auto-validates; FastAPI returns 422 for invalid data.


## Testing Strategy

**Test categories**:
- **Pydantic validation**: Test model constraints (max lengths, patterns, required fields)
- **Route tests**: Use in-memory SQLite (`sqlite:///:memory:`) fixture, test CRUD operations
- **Auth flow**: Verify register sets cookie, login succeeds with correct credentials, protected routes return 401
- **CASCADE delete**: Create list with todos, delete list, verify todos deleted

**Fixture pattern**: Create in-memory DB, create tables, yield session, drop tables after test.

## Development Setup

**Initial setup**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh  # Install uv
uv init
uv add fastapi uvicorn[standard] jinja2 python-multipart sqlalchemy
uv add --dev pytest httpx
uv run uvicorn app.main:app --reload
```

Access `http://localhost:8000`, login with `demo@example.com` / `demo123`

**Workflow**:
- Run server: `uv run uvicorn app.main:app --reload`
- Run tests: `uv run pytest`
- View DB: `sqlite3 todo.db` or DB Browser for SQLite
- Reset DB: `rm todo.db` (recreated on restart)

---
