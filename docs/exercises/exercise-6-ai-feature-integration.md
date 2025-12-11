# Exercise 6: AI Feature Integration

**Goal:** Use Spec Kit to design and implement an AI-powered feature locally

**Prerequisites:** Exercise 5 completed (Spec Kit initialized, constitution created), OPENAI_API_KEY configured (see README)

---

## The Feature

Add two AI buttons to the edit dialog:
1. **Suggest Priority** — AI recommends low/medium/high
2. **Expand Description** — AI generates helpful subtasks

This exercise builds on the Spec Kit foundation from Exercise 5. You'll use the spec-driven workflow to define the feature, then implement it locally with Agent Mode.

---

## Part A: Spec-Driven Design

Since you already have Spec Kit initialized and a constitution from Exercise 5, skip straight to specification.

### Write Specification

> ```md
> /speckit.specify Add AI Suggestions feature:
> - Two AI-powered buttons in the edit todo dialog
> - "Suggest Priority" button next to priority dropdown
>   - Calls OpenAI API to analyze todo title and notes
>   - Returns recommended priority: low, medium, or high
> - "Expand Description" button next to notes textarea
>   - Uses AI to generate helpful subtasks/details
>   - Appends expanded content to notes field
> - Backend service with OpenAI integration (httpx)
> - Mock fallback when OPENAI_API_KEY not set
> - Proper error handling and loading states
> ```

### Clarify Requirements

> ```md
> /speckit.clarify
> ```

Answer the AI's questions:
- API timeout? → 10 seconds
- Rate limiting? → No, simple implementation
- Cache responses? → No

### Generate Plan

> ```md
> /speckit.plan Use these technical choices:
> - Service module: src/app/services/ai_assistant.py
> - Routes: src/app/routes/ai_suggestions.py
> - Use httpx for async HTTP calls
> - Mock functions return deterministic test data
> - Frontend uses fetch() with loading states
> - Use sl-icon name="lightbulb" for AI buttons
> ```

**Review:** `specs/002-ai-suggestions/plan.md`

### Generate Tasks

> ```md
> /speckit.tasks
> ```

**Review:** `specs/002-ai-suggestions/tasks.md`

---

## Part B: Implement with Spec Kit

### Let Spec Kit Drive Implementation

> ```md
> /speckit.implement
> ```

Watch as the AI executes tasks from your spec:
1. Creates the service module with OpenAI integration
2. Adds mock fallback functions
3. Creates API endpoints
4. Registers the router
5. Adds UI buttons to the template
6. Implements loading states and error handling

### If Something Fails

> ```md
> The [component] failed with: [error]
> Please fix and continue with the remaining tasks.
> ```

---

## Part C: Test the Implementation

### Start the Dev Server

```bash
uv run uvicorn app.main:app --reload
```

### Test with Mock (No API Key)

1. Ensure `OPENAI_API_KEY` is not set
2. Edit a todo
3. Click "Suggest Priority" — should return mock value
4. Click "Expand with AI" — should return mock subtasks
5. Verify loading states appear during requests

### Test with Real API

1. Set `OPENAI_API_KEY` in your `.env` file
2. Restart the dev server
3. Edit a todo with a descriptive title
4. Click "Suggest Priority" — should return AI-suggested priority
5. Click "Expand with AI" — should return AI-generated content

### Test Error Handling

> ```md
> Temporarily break the AI endpoint (e.g., invalid API key) and verify
> the UI shows appropriate error messages instead of crashing.
> ```

### Run Tests

```bash
uv run pytest tests/ -v -k ai
```

---

## Part D: Review, Commit & Create Pull Request

### Review the Generated Code

Check that the implementation follows your spec:
- [ ] Service module in `src/app/services/ai_assistant.py`
- [ ] Routes in `src/app/routes/ai_suggestions.py`
- [ ] Router registered in `main.py`
- [ ] UI buttons in template
- [ ] Loading states work
- [ ] Error handling works
- [ ] Mock fallback works without API key

### Make Adjustments

If anything doesn't match your expectations:

> ```md
> The [component] doesn't match the spec. It should [expected behavior]
> but instead [actual behavior]. Please fix.
> ```

### Commit, Push & Create PR

> ```md
> Create a new branch called feature/ai-suggestions, commit all changes
> with message "Add AI suggestion feature for todos", push to origin,
> and create a pull request with a description based on the spec.
> ```

<details>
<summary>Stuck? Try this approach</summary>

> ```md
> 1. Create branch feature/ai-suggestions
> 2. Commit all changes with message "Add AI suggestion feature for todos"
> 3. Push branch to origin
> 4. Create PR titled "Add AI suggestion buttons to edit dialog"
>    with description summarizing the two AI features
> ```
</details>

---

## Completion Checklist

- [ ] Created spec using existing Spec Kit constitution
- [ ] Generated plan and tasks for AI feature
- [ ] Implemented feature with `/speckit.implement`
- [ ] Mock fallback works without API key
- [ ] Real API integration works with API key
- [ ] Loading states display correctly
- [ ] Error handling shows user-friendly messages
- [ ] Tests pass
- [ ] Changes committed and pushed
- [ ] Pull request created

---

## Key Takeaways

| Concept | Remember |
|---------|----------|
| Spec continuity | Reuse constitution across features |
| Spec-driven implementation | `/speckit.implement` executes your tasks |
| Mock-first development | Test without external dependencies |
| Graceful degradation | App works with or without API key |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Mock not triggering | Check OPENAI_API_KEY is unset |
| API timeout | Increase timeout in service module |
| 401 from OpenAI | Verify API key is valid |
| UI not updating | Check fetch response handling |

---

## Resources

- [GitHub Spec Kit](https://github.com/github/spec-kit)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [httpx Documentation](https://www.python-httpx.org/)
