# Exercise 7: Alternative Stack Implementation (Optional)

**Goal:** Apply your AI-assisted development skills to recreate the todo app in a different tech stack

**Prerequisites:** Completed Exercises 1-6, familiarity with another tech stack

---

## Overview

This is a freestyle exercise where you build the same todo app using a completely different technology stack of your choice. You'll start from a fresh repository and apply everything you've learned.

This exercise tests your ability to:
- Guide AI agents through unfamiliar territory
- Apply spec-driven development to greenfield projects
- Make and document architectural decisions
- Translate requirements across tech stacks

---

## Part A: Create Your Repository

### Step 1: Create from GitHub Template

1. Go to [github.com/IT-HUSET/aswe-2025-template](https://github.com/IT-HUSET/aswe-2025-template)
2. Click **"Use this template"** → **"Create a new repository"**
3. Name it for instance `todo-app-{stack}` (e.g., `todo-app-node`, `todo-app-go`)
4. Set visibility (public or private)
5. Click **"Create repository"**

### Step 2: Clone and Open in VS Code

**Option A: From VS Code**
1. Open Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`)
2. Type **"Git: Clone"** and select it
3. Enter your new repository URL
4. Choose a location and open in new window

**Option B: From Terminal**
```bash
git clone https://github.com/YOUR_USERNAME/todo-app-{stack}.git
code todo-app-{stack}
```

---

## Available Resources

### Requirements Documentation

The template includes requirements in `docs/todo-app-requirements/`:

| File | Purpose |
|------|---------|
| `functional-requirements.md` | **Your spec** — what the app must do (stack-agnostic) |
| `technical-requirements-python.md` | Reference: how Python stack made decisions |
| `implementation-spec-python.md` | Reference: detailed implementation plan |

**Rule:** Don't modify `functional-requirements.md`. Your app should satisfy the same requirements.

### Stack Suggestions

Choose based on your background or learning goals:

| Stack | Good For |
|-------|----------|
| **Node.js/Express** | JavaScript developers, familiar ecosystem |
| **Deno/Fresh** | Modern JS, built-in TypeScript, edge-ready |
| **Go/Templ** | Performance, simplicity, single binary |
| **Rust/Axum** | Systems programmers, type safety |
| **Java/Spring Boot** | Enterprise developers, mature tooling |
| **C#/.NET** | Microsoft ecosystem, Blazor option |
| **Ruby/Rails** | Rapid prototyping, convention over configuration |
| **PHP/Laravel** | Web fundamentals, huge ecosystem |

---

## Part B: Setup & Planning

### Create Your Technical Requirements

Create `docs/todo-app-requirements/technical-requirements-{stack}.md`:

> ```md
> Based on functional-requirements.md, create a technical requirements document
> for implementing this todo app in [your chosen stack].
>
> Include decisions for:
> - Language version and package manager
> - Web framework
> - Template engine (or SPA approach)
> - Database and ORM/query approach
> - Session/auth handling
> - Frontend interactivity (HTMX, or alternative)
> - UI components (Shoelace, or alternative)
> - Any constraints or trade-offs
> ```

### Initialize Your Project

Use AI to scaffold the project in the `src/` directory:

> ```md
> Initialize a new [framework] project in src/ with:
> - [Package manager] for dependencies
> - Basic project structure
> - Development server configuration
> - Update .gitignore for this stack
> ```

---

## Part C: Spec-Driven Approach

Apply the workflow from Exercise 5 to your new stack.

### Create Constitution

> ```md
> /speckit.constitution Create principles for this todo app implementation:
> - Use idiomatic [language] patterns
> - Follow [framework] conventions
> - All features need appropriate tests
> - Match the functional requirements exactly
> - Keep the implementation simple (educational purpose)
> ```

### Generate Implementation Plan

> ```md
> /speckit.specify Implement a todo app based on:
> - Functional requirements in docs/todo-app-requirements/functional-requirements.md
> - Technical choices in docs/todo-app-requirements/technical-requirements-{stack}.md
>
> This is a complete app implementation, not a single feature.
> ```

### Clarify Technical Decisions

> ```md
> /speckit.clarify
> ```

Answer questions about:
- Database choice (SQLite? PostgreSQL? In-memory?)
- Session storage approach
- Frontend interactivity method
- Component library preferences

### Generate Plan and Tasks

> ```md
> /speckit.plan
> ```

> ```md
> /speckit.tasks
> ```

---

## Part D: Iterative Implementation

### Build Core Foundation First

Start with the basics in this order:
1. Database models and migrations
2. Basic routes and templates
3. Authentication (login/logout)
4. Static assets and layout

### Implement Features Incrementally

Work through features one at a time:

> ```md
> /speckit.implement Start with task 1: [task description]
> ```

After each feature:
- Test manually in browser
- Run any automated tests
- Commit your progress

### Handle Differences from Python Version

Some things will work differently:

| Aspect | Considerations |
|--------|----------------|
| **Templates** | Jinja2 syntax vs your engine |
| **HTMX** | Works with any backend, but integration patterns vary |
| **Shoelace** | CDN works anywhere, or choose native components |
| **Sessions** | Each framework handles differently |
| **ORM** | Query patterns and migrations vary |

When stuck:

> ```md
> In [framework], how do I achieve the equivalent of [Python pattern]?
> The Python version does [description]. What's the idiomatic approach here?
> ```

---

## Part E: Validation

### Functional Checklist

Verify against `functional-requirements.md`:

- [ ] User can register with email/password
- [ ] User can login with demo credentials
- [ ] User can create/edit/delete lists
- [ ] User can create/edit/delete todos
- [ ] User can mark todos complete/incomplete
- [ ] User can drag-drop to reorder lists and todos
- [ ] User can search todos in current list
- [ ] User can toggle dark mode
- [ ] Data persists across browser sessions
- [ ] Data persists across server restarts
- [ ] Visual states work (priority colors, overdue indicators)

### Compare Implementations

> ```md
> Compare my [stack] implementation against the Python version.
> What features might be missing or behaving differently?
> Reference docs/todo-app-requirements/functional-requirements.md
> ```

---

## Part F: Document Your Decisions

### Create Implementation Notes

Add notes to your technical requirements file:

> ```md
> Add a "Implementation Notes" section documenting:
> - Challenges encountered and how solved
> - Deviations from Python approach and why
> - Stack-specific optimizations or patterns used
> - Lessons learned
> ```

### Create a README

> ```md
> Create a README.md for this implementation:
> - How to run the app
> - How to run tests
> - Key differences from the Python version
> - Any prerequisites or setup steps
> ```

---

## Part G: Commit & Share

### Commit Your Work

> ```md
> Commit all changes with a descriptive message about the [stack] implementation.
> ```

### Create Pull Request

> ```md
> Create a pull request titled "Add [stack] todo app implementation"
> with a description comparing this implementation to the Python version.
> ```

---

## Stretch Goals

If you finish early, try these challenges:

### Add the AI Feature

Port the AI suggestion feature from Exercise 6:

> ```md
> Add the AI suggestions feature to my [stack] implementation:
> - "Suggest Priority" button in edit dialog
> - "Expand Description" button in edit dialog
> - Use [appropriate HTTP client] for OpenAI API
> - Mock fallback when API key not set
> ```

### Add Quick Notes

Port the Quick Notes feature from Exercise 5:

> ```md
> Add the Quick Notes feature to my [stack] implementation:
> - Multiple timestamped notes per todo
> - Pinned notes appear first
> - Note count badge on todo items
> ```

### Performance Comparison

> ```md
> Help me benchmark this [stack] implementation against the Python version:
> - Page load times
> - API response times
> - Memory usage
> - Lines of code comparison
> ```

---

## Completion Checklist

- [ ] Created technical requirements for your stack
- [ ] Initialized project with appropriate tooling
- [ ] Used spec-driven workflow (constitution, spec, plan, tasks)
- [ ] Implemented all core features from functional requirements
- [ ] All acceptance criteria pass
- [ ] Added tests appropriate for your stack
- [ ] Documented implementation decisions
- [ ] Created README with setup instructions
- [ ] Committed and created pull request

---

## Key Takeaways

| Concept | Remember |
|---------|----------|
| Requirements are portable | Same spec, different implementation |
| AI adapts to context | Give it your stack's conventions |
| Patterns translate | MVC, REST, templates work everywhere |
| Document decisions | Future you will thank present you |
| Spec-driven scales | Works for features AND full apps |

---

## Tips for Success

1. **Start simple** — Get "Hello World" running before adding complexity
2. **Reference the Python version** — Use it as a working example, not a copy target
3. **Ask for idioms** — "What's the [stack] way to do X?"
4. **Commit often** — Small commits make it easy to backtrack
5. **Test in browser** — Don't trust AI blindly, verify manually
6. **Document as you go** — Notes while fresh are better than memory later

---

## Resources

- [HTMX Documentation](https://htmx.org/docs/) — Works with any backend
- [Shoelace Components](https://shoelace.style/) — Framework-agnostic web components
- [SortableJS](https://sortablejs.github.io/Sortable/) — Drag-drop library
- Your framework's official documentation
