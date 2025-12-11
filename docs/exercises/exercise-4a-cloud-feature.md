# Exercise 4a: Cloud Feature (Parallel)

**Goal:** Use the Copilot coding agent to implement a feature via GitHub Issues

**Prerequisites:** GitHub repository with Copilot coding agent enabled

---

## The Feature

Add todo count to the browser tab title. When viewing a list, the tab should show:
- `(3) My List - Todo App` when there are 3 incomplete todos
- `My List - Todo App` when all todos are complete

---

## Why This Exercise?

The Copilot coding agent works **asynchronously** — you create an issue, assign it to Copilot, and it works in the background. This exercise demonstrates that workflow while you continue with Exercise 4b locally.

---

## Step 1: Create the GitHub Issue

Go to your repository on github.com and create a new issue.

**Your task:** Write a clear issue description that the coding agent can follow. Include:
- What the feature should do
- Where the change should be made (hint: page templates)
- Expected behavior with examples
- Any edge cases (empty list, all complete)

<details>
<summary>🤔 <i><b>Stuck?</b> Try this example issue</i></summary>

**Title:** `Add todo count to browser tab title`

**Body:**
```markdown
## Description
Update the browser tab title to show the count of incomplete todos for the current list.

## Requirements
- Format: `(N) List Name - Todo App` where N is incomplete todo count
- When all todos are complete (or list is empty): `List Name - Todo App` (no count)
- Update dynamically when todos are added/completed/deleted

## Implementation
- Update the `<title>` tag in the page template
- Use JavaScript to update the title when the todo list changes via HTMX

## Examples
- 3 incomplete todos: `(3) Shopping - Todo App`
- All complete: `Shopping - Todo App`
- Empty list: `Shopping - Todo App`
```
</details>

---

## Step 2: Assign to Copilot

1. In the issue sidebar, click **Assignees**
2. Select **Copilot** from the list
3. Copilot will start working (you'll see activity in the issue)

The coding agent typically takes 3-5 minutes to create a PR.

---

## Step 3: Continue with Exercise 4b

**Don't wait!** Proceed to [Exercise 4b](exercise-4b-local-feature.md) while the coding agent works.

You'll come back to check on this PR later.

---

## Step 4: Review the PR (Later)

When you return from Exercise 4b, check if the PR is ready.

**Review checklist:**
- [ ] PR was created by Copilot
- [ ] Title updates correctly with todo count
- [ ] Count updates when todos change (add/complete/delete)
- [ ] No count shown when list is empty or all complete

**To test locally:**
```bash
git fetch origin
git checkout <copilot-branch-name>
uv run uvicorn app.main:app --reload
```

Open the app and verify the browser tab title updates.

---

## Step 5: Provide Feedback (Optional)

If the implementation needs changes, comment on the PR mentioning `@copilot`:

```
@copilot The count isn't updating when I complete a todo.
Please make sure the title updates dynamically via HTMX events.
```

Copilot will push additional commits to address your feedback.

---

## Wrap Up

You can either:
- **Merge the PR** if the feature works correctly
- **Close the PR** if you want to skip this feature
- **Leave it open** for later review

This exercise demonstrates how the coding agent can work on features in parallel with your local development.

---

## Completion Checklist

- [ ] Issue created with clear requirements
- [ ] Copilot assigned to the issue
- [ ] PR was created by Copilot
- [ ] (Optional) Reviewed and tested the implementation
- [ ] (Optional) Used @copilot to request changes

---

## Key Takeaways

| Concept | Remember |
|---------|----------|
| Async workflow | Coding agent works in background |
| Clear issues | Better descriptions = better results |
| Parallel work | Start cloud task, continue locally |
| @copilot iteration | Comment on PR to request changes |

---

## Resources

- [About Copilot Coding Agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- [Assigning Issues to Copilot](https://docs.github.com/en/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks)
- [Reviewing Copilot PRs](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/review-copilot-prs)
