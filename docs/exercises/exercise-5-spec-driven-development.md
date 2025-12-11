# Exercise 5: Spec-Driven Development

**Goal:** Use [GitHub Spec Kit](https://github.com/github/spec-kit) to build a feature from specification

**Prerequisites:** Exercise 4b completed, familiarity with Agent Mode

---

## What is Spec Kit?

Spec Kit transforms "vibe coding" into structured AI development:
- **Constitution** → Project principles and constraints
- **Specification** → What to build (requirements)
- **Plan** → How to build it (technical design)
- **Tasks** → Step-by-step implementation
- **Implement** → AI executes the tasks

### Why Spec-Driven?

In previous exercises, you used prompts like "add priority filtering." But complex features benefit from structured specs that:
- Document requirements before coding
- Generate consistent implementation plans
- Make it easy to change requirements and regenerate code

### How It Works

Spec Kit installs **slash commands** in Copilot Chat. After setup, type `/` in Copilot Chat to see commands like `/speckit.specify`, `/speckit.plan`, etc. These commands guide you through the spec-driven workflow.

---

## Setup

### Install Spec Kit

```bash
# Already aliased in devcontainer
specify version

# Or install manually (if running locally)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

### Initialize in Project

```bash
specify init . --ai copilot --force
```

This creates:
```
.github/prompts/     # Copilot prompt files
.specify/            # Spec Kit config and templates
```

---

## Part A: Create Constitution

The constitution defines project rules that apply to ALL features.

> ```md
> /speckit.constitution Create principles for this todo app:
> - Use existing FastAPI patterns and type hints
> - All new features need pytest tests
> - Use Shoelace components and HTMX patterns
> - Validate all user input server-side
> - Keep functions small and focused
> ```

**Review:** Check `.specify/memory/constitution.md`

---

## Part B: Write Specification

### The Feature: Quick Notes

Add timestamped notes to todos — users can add multiple notes per todo.

> ```md
> /speckit.specify Add a Quick Notes feature:
> - Users can add multiple notes to any todo
> - Each note has: content, timestamp, optional "pinned" status
> - Notes appear in collapsible section below todo
> - Pinned notes appear first
> - Todo item shows note count badge
> - Notes are editable and deletable
> ```

### Clarify Requirements

> ```md
> /speckit.clarify
> ```

Answer the AI's questions:
- Max note length? → 500 characters
- Markdown support? → No, plain text
- Max notes per todo? → 50

**Review:** Check `specs/001-quick-notes/spec.md`

---

## Part C: Generate Plan

> ```md
> /speckit.plan Use these technical choices:
> - Add Note model with ForeignKey to Todo
> - Create notes.py routes following existing patterns
> - Use HTMX hx-swap="outerHTML" for inline editing
> - Use sl-details for collapsible section
> - Use sl-badge for count display
> - Cascade delete notes when todo deleted
> ```

**Review generated files:**
- `specs/001-quick-notes/plan.md` — Technical design
- `specs/001-quick-notes/data-model.md` — Database schema

### Validate Plan

> ```md
> /speckit.analyze
> ```

Fix any inconsistencies before proceeding.

---

## Part D: Generate Tasks

> ```md
> /speckit.tasks
> ```

**Review:** `specs/001-quick-notes/tasks.md`

Tasks are ordered by dependency. Tasks marked `[P]` can run in parallel.

Example task list:
1. Create Note model in database.py
2. Create notes routes in routes/notes.py
3. Register router in main.py
4. Create note partials templates
5. Add notes section to todo_item.html
6. Add tests for notes CRUD
7. Add tests for cascade delete

---

## Part E: Implement

> ```md
> /speckit.implement
> ```

**Watch the AI:**
1. Execute tasks in order
2. Create files following patterns
3. Run commands if needed
4. Report progress

### If Something Fails

> ```md
> The Note model creation failed with: [error]
> Please fix and continue.
> ```

### Test the Implementation

```bash
uv run uvicorn app.main:app --reload
```

Try the feature:
1. Create a todo
2. Add a note to it
3. Pin the note
4. Add more notes
5. Delete a note

```bash
uv run pytest tests/ -v -k note
```

---

## Part F: Commit, Push & Create Pull Request

### Commit Changes

> ```md
> Commit all changes with a descriptive message about the Quick Notes feature.
> ```

### Push and Create PR

> ```md
> Push the current branch to origin and create a pull request with:
> - Title: "Add Quick Notes feature to todos"
> - Description summarizing what was implemented
> ```

<details>
<summary>Stuck? Try this approach</summary>

> ```md
> Create a new branch called feature/quick-notes, commit all changes,
> push to origin, and create a pull request titled "Add Quick Notes feature"
> with a description of the feature based on the spec.
> ```
</details>

---

## Completion Checklist

- [ ] Initialized Spec Kit in project
- [ ] Created constitution with project principles
- [ ] Wrote feature specification
- [ ] Generated technical plan
- [ ] Generated task breakdown
- [ ] Implemented feature with `/speckit.implement`
- [ ] Feature works (notes can be added/edited/deleted)
- [ ] Tests pass
- [ ] Changes committed and pushed
- [ ] Pull request created

---

## Key Takeaways

| Concept | Remember |
|---------|----------|
| Constitution first | Establish rules before features |
| Specs are executable | They directly generate code |
| Clarify early | Use `/speckit.clarify` to surface assumptions |
| Validate often | Use `/speckit.analyze` to check consistency |
| Iterate freely | Easy to change specs and regenerate |

---

## Spec Kit Commands

| Command | Purpose |
|---------|---------|
| `/speckit.constitution` | Define project principles |
| `/speckit.specify` | Write feature requirements |
| `/speckit.clarify` | AI asks clarifying questions |
| `/speckit.plan` | Generate technical design |
| `/speckit.tasks` | Break plan into tasks |
| `/speckit.analyze` | Check consistency |
| `/speckit.implement` | Execute tasks |
| `/speckit.checklist` | Generate quality checklists |

---

## Resources

- [GitHub Spec Kit](https://github.com/github/spec-kit)
- [Spec-Driven Development Blog](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
