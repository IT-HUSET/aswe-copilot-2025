# Todo App - Functional Requirements

## Purpose
Educational lab project for AI coding agent workshops. Must be simple to understand, run, and port to other languages/frameworks.

## Domain Model

### Entities
- **User**: id, email (unique), password, created_at
- **TodoList**: id, user_id (FK), name, description, color (hex), position, timestamps
- **Todo**: id, list_id (FK), title, note, is_completed, completed_at, due_date, priority (low/medium/high), position, timestamps

### Relationships
- User → many TodoLists (CASCADE delete)
- TodoList → many Todos (CASCADE delete)

## Features

### Authentication (Mock/Simple)
- Login page with email/password
- Registration page with email/password/confirm
- Logout functionality
- Session-based auth (cookie)
- Protected routes redirect to login with return URL
- Demo credentials seeded: `demo@example.com` / `demo123`

**Note**: This is intentionally NOT production-ready auth. Plain text passwords, in-memory sessions acceptable.

### Todo Lists
- View all lists in sidebar
- Create list (name required, description optional, color picker)
- Edit list (name, description, color)
- Delete list with confirmation (cascades to todos)
- Reorder lists via drag-drop
- Display incomplete todo count per list
- Auto-select first list after login
- Visual: color indicator bar for each list

### Todo Items
- View todos in selected list
- Quick-add: single input field for title, Enter to submit
- Full edit: dialog with title, notes, due date, priority
- Delete with confirmation
- Toggle completion (checkbox)
- Reorder via drag-drop within list
- Fields:
  - Title (required, max 200 chars)
  - Notes (optional, multi-line)
  - Due date (optional, date picker)
  - Priority: low, medium, high (default: medium)
  - Completed flag + completion timestamp

### Search
- Search input above todo list
- Filter current list by title (case-insensitive partial match)
- Live search as user types (debounced)
- Clear search to show all

### Visual States

| State | Indicator |
|-------|-----------|
| Priority high | Red badge + red left border |
| Priority medium | Amber/yellow badge + amber left border |
| Priority low | Green badge + green left border |
| Overdue (past due + not completed) | Red left border + red date text |
| Due today | Amber date text |
| Completed | Reduced opacity + strikethrough title |
| Active list (selected) | Highlighted background + accent border |

### UI/UX Behaviors
- Responsive: sidebar collapses on mobile
- Dark mode toggle (persists in localStorage)
- Hover states: show edit/delete buttons, show drag handles
- Drag handles hidden by default, visible on hover
- Loading indicators during async operations
- Empty states with helpful message + CTA button
- Confirmation dialogs for destructive actions
- Toast notifications for errors

### Data Persistence
- Data persists across browser sessions
- Data persists across server restarts (file-based DB)
- Sessions may be lost on restart (acceptable for educational use)

## Out of Scope
- Real authentication (password hashing, OAuth, JWT)
- Tags/categories/labels
- Advanced filtering (by date, priority, completion)
- Sorting options
- Statistics/dashboard
- Email verification
- Password reset
- Rate limiting
- Multi-user collaboration
- Mobile native app
- Offline support
- File attachments
- Recurring todos
- Subtasks

## Acceptance Criteria
- [ ] Register new user → lands on app with empty state
- [ ] Login with demo credentials → sees seeded data
- [ ] Create list → appears in sidebar with count 0
- [ ] Add todo → appears in list, sidebar count increments
- [ ] Complete todo → visual change, count decrements
- [ ] Delete todo → removed from list, count decrements
- [ ] Delete list → list and all todos removed
- [ ] Drag-drop list → new order persists after refresh
- [ ] Drag-drop todo → new order persists after refresh
- [ ] Set due date in past → shows overdue indicator
- [ ] Dark mode toggle → theme changes and persists
- [ ] Search → filters todos, clear restores all
- [ ] Logout → returns to login, session cleared
- [ ] Access protected page when logged out → redirects to login → after login returns to original page
