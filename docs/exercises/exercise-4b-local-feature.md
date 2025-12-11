# Exercise 4b: Local Feature (Plan → Implement → Verify)

**Goal:** Build a feature locally using Plan → Implement → Verify workflow

**Prerequisites:** Exercise 3 completed, Exercise 4a started (running in parallel), todo-app running

---

## The Feature

Add filter buttons (All, Low, Medium, High) above the todo list that filter displayed todos by priority.

---

## The Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   PLAN      │ ──> │  IMPLEMENT  │ ──> │   VERIFY    │
│             │     │             │     │             │
│ Research    │     │ New chat    │     │ Tests       │
│ Design      │     │ Follow plan │     │ Visual      │
│ Review plan │     │             │     │ Code review │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## Phase 1: Plan

### Step 1: Enter Plan Mode

Switch Copilot to **Plan Mode** (if available) or use Agent Mode with planning focus.

### Step 2: Research & Design

**Your task:** Create a prompt that instructs Copilot to:
1. Analyze the existing codebase to understand current patterns
2. Research HTMX filtering patterns
3. Research Shoelace button group components
4. Design a plan for implementing priority filtering
5. Save the plan to `docs/plans/priority-filter.md`

The plan should include:
- Files to modify/create
- Backend changes (API endpoint modifications)
- Frontend changes (HTML, CSS, JavaScript)
- How HTMX will handle the filter requests
- Research should be done via web searches and Context7 MCP

<details>
<summary>Stuck? Try this approach</summary>

> ```md
> I want to add priority filtering to the todo list. Before implementing:
>
> 1. Analyze @workspace to understand:
>    - How the current todo search works
>    - What HTMX patterns are used
>    - How Shoelace components are styled
>
> 2. Research using web searches and Context7 MCP:
>    - HTMX filtering patterns and best practices
>    - Shoelace button groups for filter UI
>
> 3. Create a detailed implementation plan covering:
>    - Backend: API changes to filter by priority
>    - Frontend: Filter button UI with HTMX
>    - Styling: Active state for selected filter
>    - Testing: What tests to add
>
> Save the plan to docs/plans/priority-filter.md
> Do NOT implement yet - just create the plan.
> ```
</details>

### Step 3: Review the Plan

Use the `/review-plan` command (or ask Copilot directly) to review the generated plan.

> ```md
> Review #file:docs/plans/priority-filter.md for:
> - Completeness (are all aspects covered?)
> - Consistency with existing codebase patterns
> - Potential issues or missing edge cases
> - Suggest improvements if needed
> ```

### Step 4: Refine the Plan

Based on the review feedback, update the plan. Ask Copilot to make specific adjustments:

> ```md
> Update the plan in #file:docs/plans/priority-filter.md to address:
> [list the feedback items to address]
> ```

**Checkpoint:** You should have a reviewed and refined plan in `docs/plans/priority-filter.md` before proceeding.

---

## Phase 2: Implement

### Step 1: Start Fresh & Create Feature Branch

**Important:** Start a new Copilot Chat conversation. This ensures clean context focused on implementation.

**Your task:** Instruct Copilot to create a feature branch for your work.

<details>
<summary>Stuck? Try this approach</summary>

> ```md
> Create a new git branch called feature/priority-filter and switch to it.
> ```
</details>

### Step 2: Implement from Plan

**Your task:** Create a prompt that instructs Copilot to implement the feature following your plan.

Reference the plan file and instruct Copilot to:
- Follow the plan step by step
- Implement backend changes first, then frontend
- Follow existing code patterns in the codebase

<details>
<summary>Stuck? Try this approach</summary>

> ```md
> Implement the priority filtering feature following the plan in
> #file:docs/plans/priority-filter.md
>
> Work through the plan systematically:
> 1. Backend changes first
> 2. Then frontend/template changes
> 3. Then styling
>
> Follow existing patterns in @workspace for code style and conventions.
> ```
</details>

### Step 3: Manual Testing

Test the feature manually:

```bash
# Ensure server is running
cd todo-app
uv run uvicorn app.main:app --reload
```

1. Open http://localhost:8000
2. Create todos with different priorities
3. Click each filter button
4. Verify correct todos are shown

---

## Phase 3: Verify

### Step 1: Add Tests

**Your task:** Instruct Copilot to add tests for the new filtering functionality.

Tests should cover:
- Filter by each priority level (low, medium, high)
- "All" filter shows all todos
- Filter combined with search query
- Edge cases (empty results, no todos)

<details>
<summary>Stuck? Try this approach</summary>

> ```md
> Add tests for the priority filtering feature in tests/test_todos.py.
>
> Test cases needed:
> - test_filter_by_priority_low
> - test_filter_by_priority_high
> - test_filter_all_shows_all_todos
> - test_filter_with_search_query
> - test_filter_empty_results
>
> Follow the existing test patterns in @workspace.
> ```
</details>

Run the tests:
```bash
uv run pytest tests/test_todos.py -k filter -v
```

### Step 2: Visual Validation

Use Chrome DevTools MCP to visually verify the feature. The MCP runs Chrome in **headless mode** — no browser window appears, but Copilot can capture screenshots.

> ```md
> Using Chrome DevTools MCP:
> 1. Navigate to http://localhost:8000 and log in
> 2. Create a todo list with todos at different priorities
> 3. Take a screenshot showing the filter buttons
> 4. Click the "High" filter and take another screenshot
> 5. Verify only high-priority todos are shown
> ```

**Manual alternative:** If the MCP isn't available, test manually in your browser.

### Step 3: Local Code Review

Use the `/review-code` command you created in Exercise 3 to review your changes before pushing.

> ```md
> /review-code #folder:todo-app/src
> ```

**After the review:**
- Read through the findings (🔴 Critical, 🟡 Suggestions, ✅ Good Practices)
- Address any **Critical** issues before proceeding
- Suggestions can be addressed now or later

<details>
<summary>If you skipped Exercise 3 Part B...</summary>

Ask Copilot directly:
> ```md
> Review the changes I made for priority filtering. Check for:
> - Security issues (input validation, injection)
> - Performance concerns
> - Code quality (naming, structure, duplication)
> - Missing error handling
> ```
</details>

### Step 4: Commit, Push & Create Pull Request

**Your task:** Instruct Copilot to commit your changes, push the branch, and create a pull request.

<details>
<summary>Stuck? Try this approach</summary>

> ```md
> Commit all changes with a descriptive message about the priority filtering feature.
> Push the feature/priority-filter branch to origin.
> Create a pull request with title "Add priority filtering to todo list"
> and a description summarizing what was implemented.
> ```
</details>

### Step 5: Iterate with @copilot (Optional)

Once your PR is open on GitHub, you can use the **Copilot coding agent** to make additional changes by mentioning `@copilot` in PR comments.

**Example comments:**
```
@copilot Please add input validation to ensure priority is one of: low, medium, high
```
```
@copilot The filter button styling doesn't match the existing design. Update it to use the same styles as the search button.
```

Copilot will push commits directly to the PR branch. You can continue iterating until you're satisfied.

> **Note:** Only users with write access to the repository can trigger the coding agent via @copilot mentions.

<details>
<summary>If @copilot doesn't respond...</summary>

- Ensure Copilot coding agent is enabled for the repository
- Check you have write access to the repository
- Verify you have a Copilot Pro, Pro+, Business, or Enterprise subscription
</details>

---

## Completion Checklist

- [ ] Plan created and saved to `docs/plans/priority-filter.md`
- [ ] Plan reviewed and refined
- [ ] Feature branch created
- [ ] Feature implemented from plan (new chat session)
- [ ] Filter buttons visible and styled
- [ ] Each filter shows correct todos
- [ ] Active button highlighted
- [ ] Works with search
- [ ] Tests added and passing
- [ ] Visual validation completed
- [ ] Local code review completed (critical issues addressed)
- [ ] Changes committed and pushed
- [ ] Pull request created
- [ ] (Optional) Used @copilot in PR for additional changes

---

## Don't Forget: Check on Exercise 4a

Before moving on, circle back to [Exercise 4a](exercise-4a-cloud-feature.md) and check if the Copilot coding agent has created a PR for the browser tab title feature.

---

## Key Takeaways

| Concept | Remember |
|---------|----------|
| Plan first | Research and design before coding |
| Save plans | `docs/plans/` for implementation specs |
| Fresh context | New chat for implementation phase |
| Review before push | Use `/review-code` locally, fix critical issues |
| Feature branches | Isolate work, enable PR collaboration |
| @copilot in PRs | Mention to request changes from coding agent |

---

## Stretch Challenges

| Challenge | Description |
|-----------|-------------|
| Count badges | Add todo count to each filter button |
| Persistence | Save active filter to localStorage |
| Keyboard shortcuts | Add 1-4 keys for filter switching |
| URL state | Reflect filter in URL query params |

---

## Resources

- [Copilot Chat Cookbook](https://docs.github.com/en/copilot/tutorials/copilot-chat-cookbook)
- [About Copilot Coding Agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- [Reviewing Copilot PRs](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/review-copilot-prs)
- [HTMX Documentation](https://htmx.org/docs/)
- [Shoelace Components](https://shoelace.style/)
