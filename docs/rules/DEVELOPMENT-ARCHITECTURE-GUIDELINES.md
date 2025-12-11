# Development and Architecture Guidelines (Simplified)

## Core Philosophy

- **Keep It Simple (KISS/YAGNI)**: Prefer straightforward solutions over speculative complexity. Simple code is easier to understand, maintain, and debug.
- **Single Responsibility**: Each module/class/function should have one well-defined purpose.
- **Loose Coupling, High Cohesion**: Components should be independent but internally focused.
- **DRY**: Avoid duplication, but don't abstract prematurely.
- **No Broken Windows**: Fix small problems before they spread.

## Architectural Principles

- **Use Existing Patterns**: Check for established solutions before inventing new ones.
- **Evaluate Trade-offs**: Weigh pros/cons for important decisions (DB choice, service boundaries, etc.).
- **Right-sized Modules**: Not too coarse (monolith), not too fine (fragmentation).
- **Clean Interfaces**: Modules communicate through well-defined APIs only.

### CUPID Properties

- **Composable**: Clear contracts, minimal coupling
- **Unix Philosophy**: Do one thing well
- **Predictable**: Consistent behavior, clear failure modes
- **Idiomatic**: Follow familiar patterns and conventions
- **Domain-Aligned**: Structure reflects business concepts

## Coding Standards

- Write clean, readable code with descriptive names
- Keep functions/classes short and focused
- Follow **SOLID** principles
- Document "why," not obvious "what"
- Log significant operations and errors
- Check for existing functionality before writing new code
- Use latest stable versions of frameworks/libraries

## Workflow

- Work in small, incremental steps
- Validate understanding before implementing
- Write tests for critical functionality
- Keep documentation (README, setup) updated but concise

## Dependencies

- Add only when necessary; check alternatives first
- Use latest stable versions
- Prefer lightweight, well-established libraries
- Audit regularly for vulnerabilities

## Common Pitfalls

- **NEVER** create duplicate files (file_v2.xyz, file_new.xyz)
- **NEVER** add dependencies without checking alternatives
- **NEVER** modify core frameworks without explicit instruction
- **NEVER** use `git rebase --skip` (causes data loss)

## Reality Check

Before implementing, ask:
1. What is the core user need?
2. What's the minimal solution?
3. Am I over-engineering?
