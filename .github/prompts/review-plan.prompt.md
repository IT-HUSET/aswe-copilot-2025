---
description: 'Review plans, specs, PRDs, or requirements for completeness, clarity, and technical accuracy'
agent: 'agent'
tools: 
  ['context7/*', 'fetch/*', 'edit', 'search', 'usages', 'changes', 'fetch']
---

# Review Spec / Plan / Requirements

Review the following specification, plan, PRD, or requirement document for completeness, clarity, and technical accuracy.

**Document to review:** ${input:specPath:Path to spec file or describe focus areas}

## Principles
- **Read-only** - Don't modify specs during review
- **Be critical** - Challenge assumptions, find edge cases, identify ambiguities

## Review Checklist

### Completeness
- Functional: Features, workflows, use cases, success/error states
- Non-functional: Performance, security, accessibility, compatibility
- Technical: Data models, APIs, integrations, error handling
- Edge cases: Validation, timeouts, retries, boundary conditions
- Testing: Acceptance criteria, test scenarios
- Operations: Deployment, monitoring, rollback

### Clarity
- No vague terms ("fast", "user-friendly") or undefined terms
- Developers can implement without guessing
- No TBD/TODO items or missing referenced docs
- Consistent naming and examples

### Technical Accuracy
- Current library/framework versions, no deprecated APIs
- Follows security (OWASP) and accessibility (WCAG) standards
- Technically feasible with realistic performance expectations

### Scope
- In-scope items necessary; out-of-scope explicitly stated
- No scope creep or "nice-to-haves" as requirements

### Stakeholders & Success
- All stakeholder needs addressed
- Success criteria specific, measurable, testable
- User journeys and error states defined

## Output

Generate a concise markdown report:

```markdown
# Spec Review: [Name] - [Date]

## Summary
- Overall: Ready / Minor Updates / Significant Rework / Not Ready
- Key findings (3-5 bullets)

## Issues by Priority
### Critical (block implementation)
### High (should fix)
### Medium (fix during)
### Low (nice-to-have)

## Readiness
- Can implementation start? What must be fixed first?
```

After the report, offer to update the spec or proceed to implementation.
