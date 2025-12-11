# Exercise 1: Copilot Fundamentals

**Goal:** Master Copilot Agent Mode basics while exploring the codebase

## Useful Documentation Links
- [Copilot Cheat Sheet](https://docs.github.com/en/copilot/reference/cheat-sheet)
- [Copilot - Get Started with Chat](https://docs.github.com/en/copilot/how-tos/chat-with-copilot/get-started-with-chat)
- [Copilot - Chat in IDE](https://docs.github.com/en/copilot/how-tos/chat-with-copilot/chat-in-ide)
- [VS Code - Copilot Chat](https://code.visualstudio.com/docs/copilot/chat/copilot-chat)

---

## Part A: Interface Orientation

### Open Copilot Chat

| Platform | Shortcut |
|----------|----------|
| Windows/Linux | `Ctrl+Alt+I` |
| macOS | `Cmd+Option+I` |

### Know the Modes

| Mode | Purpose | Use When |
|------|---------|----------|
| **Ask** | Q&A, explanations | Learning, understanding code |
| **Edit** | Targeted file changes | Small, specific edits |
| **Agent** | Autonomous multi-file work | Features, refactoring, complex tasks |
| **Plan** (preview) | Create and refine implementation plans | Planning complex work |

**Try it:** Switch between modes using the dropdown. Notice how the UI changes.

**Initial Mode:** Select **Ask** mode to start.

### Select Your Model

Click the model picker. Recommended: **Claude Sonnet 4.5**.

---

## Part B: Chat Participants & Variables

### Chat Participants (`@`) - _[read more here](https://docs.github.com/en/copilot/reference/cheat-sheet?tool=vscode#chat-participants)_

Type `@` in the chat to invoke specialized experts:

| Participant | Purpose | Example |
|-------------|---------|---------|
| `@workspace` | Search entire codebase for context | `@workspace How does auth work?` |
| `@terminal` | Context about terminal/shell | `@terminal Why did this command fail?` |
| `@vscode` | VS Code commands and features | `@vscode How do I change theme?` |
| `@github` | GitHub skills (search, PRs, issues) | `@github Search for HTMX examples` |

**Try it:**

> ```md
> @workspace What is the tech stack of this app?
> ```

### Chat Variables (`#`) - _[read more here](https://docs.github.com/en/copilot/reference/cheat-sheet?tool=vscode#chat-variables)_

Reference specific context with `#`:

| Variable | Purpose | Example |
|----------|---------|---------|
| `#file` | Include specific file | `#file:src/app/main.py Explain this` |
| `#selection` | Currently selected code | `#selection What does this do?` |
| `#codebase` | Full codebase context | `#codebase Find auth patterns` |

**Try it:**

> ```md
> #file:todo-app/src/app/routes/todos.py Explain the create_todo function
> ```

### Slash Commands (`/`) - _[read more here](https://docs.github.com/en/copilot/reference/cheat-sheet?tool=vscode#slash-commands-1)_

Quick actions without typing full prompts:

| Command | Purpose |
|---------|---------|
| `/explain` | Explain selected code |
| `/fix` | Propose fix for problems |
| `/tests` | Generate unit tests |
| `/doc` | Add documentation |
| `/new` | Create new project |
| `/clear` | Clear chat history |

**Try it:** Select some code (_for instance `todo-app/src/app/main.py`_), then type `/explain`

_What option does Copilot give you?_

---

## Part C: Explore the Codebase

### Ask About Architecture

> ```md
> @workspace What is the tech stack and architecture of this app?
> ```

Expected answer: FastAPI, SQLAlchemy, HTMX, Shoelace, Jinja2 templates.

### Ask About Features

> ```md
> @workspace How does authentication work in this app?
> ```

> ```md
> @workspace How are todos stored and retrieved?
> ```

### Combine Participants and Variables

> ```md
> @workspace #file:todo-app/src/app/database.py What relationships exist between models?
> ```

---

## Part D: Custom Instructions

Custom instructions tell Copilot how to behave in your project.
(Read more _**[here](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot)**_)

### Generate default Repository Instructions Using Copilot
The quickest way to get started is to have Copilot generate a base set of instructions for you. Simply press the button/link "**Generate Agent Instructions**" in the chat UI (see bewlow).

<img src="../../assets/copilot-chat.jpg" height="300"/><br/>

### Update instructions with mode specific rules

This project already has some sample coding guidelines and rules documented. Make Copilot add suitable references to the in the custom instructions file.

**Reference files under `docs/rules/`:**
- [CRITICAL-RULES-AND-GUARDRAILS.md](../rules/CRITICAL-RULES-AND-GUARDRAILS.md)
- [DEVELOPMENT-ARCHITECTURE-GUIDELINES.md](../rules/DEVELOPMENT-ARCHITECTURE-GUIDELINES.md)
- [UX-UI-GUIDELINES.md](../rules/UX-UI-GUIDELINES.md)
- [WEB-DEV-GUIDELINES.md](../rules/WEB-DEV-GUIDELINES.md)
- [PYTHON-DEVELOPMENT-GUIDELINES.md](../rules/PYTHON-DEVELOPMENT-GUIDELINES.md)

**Task:** Ask Copilot to generate custom instructions based on these existing rules:

> ```md
> Update the custom instructions (file:#.github/copilot-instructions.md) file with links to vital guidelines and rules 
> documents under the #file:docs/rules/ folder. Only link and reference the files, do NOT duplicate content.
> Keep the instructions concise and actionable.
> ```


### Review Generated Instructions

**Review:** Ensure the generated instructions:
- Reflect the actual tech stack (FastAPI, SQLAlchemy, HTMX, Shoelace)
- Include key rules from the guidelines (using primarily links to files, not duplicating content)
- Are appropriate for Copilot (not too long, actionable)
- Do **NOT** contain links to documents that shoundn't be _**eagerly**_ referenced and loaded (e.g., "CRITICAL-RULES-AND-GUARDRAILS.md" should be referenced, but not "PERSONAL-NOTE.md")


### Verify Instructions Apply

After creating the file, type this in a new chat window/conversation:

> ```md
> What coding guidelines should you follow?
> ```

Copilot should reference your custom instructions.

You can verify that the correct instructions, guidelines and rules file are being applied by checking the message at the top of the chat window: <br>
<img src="../../assets/referenced-docs.jpg" height="140"/><br/>



### Path-Specific Instructions (_**Optional**_)

Create `.github/instructions/tests.instructions.md`:

```markdown
---
applyTo: "tests/**/*.py"
---

When writing tests:
- Use pytest fixtures
- One assertion per test when possible
- Use descriptive test names: test_<function>_<scenario>_<expected>
```

---

## Part E: First Agent Task

Switch to **Agent** mode using the dropdown.

### Task 1: Add a Health Check Endpoint

**Goal:** Add a `GET /health` endpoint that returns `{"status": "ok", "timestamp": "<current ISO time>"}`

**Your task:** Craft a prompt that tells Copilot what you need. Consider:
- What information does Copilot need?
- Should you reference any existing files for context?

<br/>
<details>
<summary>🤔 <i><b>Stuck?</b> Try this approach</i></summary>

Describe the requirement clearly. Copilot will analyze the codebase and find the right location.
</details>

**Review:** Before accepting, check that:
- The endpoint follows existing patterns in the codebase
- The code makes sense to you

**Verify:** 
- _Ask Copilot_ to **run the todo app for you**
- Test manually with `curl http://localhost:8000/health`

### Task 2: Try Checkpoints

Checkpoints are automatic snapshots during Agent Mode. They let you restore to any previous state.

**Enable:** Settings → `chat.checkpoints.enabled` (usually on by default)

**Your task:**
1. Add another endpoint (your choice — maybe `/echo` or `/version`)
2. After it works, find the checkpoint for your health check request
3. Click **Restore Checkpoint** — watch the new endpoint disappear
4. Click **Redo** to bring it back

**Tip:** Enable `chat.checkpoints.showFileChanges` to see which files each request modified.

> **Note:** Checkpoints are session snapshots. Use Git for permanent version control.

---

## Part F: GitHub Copilot CLI (Optional)

[GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli) is an agentic AI assistant that runs directly in your terminal. It can read files, modify code, and execute commands—all through natural language.

### Installation

Requires Node.js 22+.

```bash
# Installation, if running locally (already installed in dev container)
npm install -g @github/copilot
```

### Basic Usage

```bash
# Start an interactive session
copilot

# One-off prompt
copilot -p "What does this project do?"
```

### Useful Slash Commands

| Command | Purpose |
|---------|---------|
| `/login` | Authenticate to GitHub |
| `/model` | Choose AI model (Claude Sonnet 4, GPT-5, etc.) |
| `/usage` | View token usage stats |
| `?` | Show help |

### Reference Files with `@`

```
Explain @src/app/main.py
Fix the bug in @src/app/routes/todos.py
```

### Try It

Navigate to this project folder and start Copilot CLI:

```bash
copilot
```

Then try this prompt: 
> ```md
> What is the tech stack of this project?
> ```

---

## Completion Checklist

- [ ] Can switch between Ask/Edit/Agent modes
- [ ] Understand chat participants (`@workspace`, `@terminal`, `@github`)
- [ ] Explored GitHub Copilot CLI (`copilot` command)
- [ ] Can use variables (`#file:`, `#selection`)
- [ ] Know slash commands (`/explain`, `/fix`, `/tests`)
- [ ] Created custom instructions file
- [ ] Completed health check endpoint
- [ ] Understand checkpoints (restore and redo)

---

## Key Takeaways

| Concept | Remember |
|---------|----------|
| `@workspace` | Searches entire codebase |
| `@terminal` | Terminal context |
| `@github` | GitHub operations (issues, PRs) |
| Copilot CLI | Agentic AI in your terminal (`copilot`) |
| `#file:path` | Reference specific file |
| `/explain` | Quick explanation |
| Custom instructions | `.github/copilot-instructions.md` |
| Agent Mode | Autonomous multi-file work |
| Checkpoints | Restore workspace to previous state |

---

## Quick Reference

```
# Chat participants
@workspace How does X work?
@terminal Why did this fail?
@github Search for examples

# Variables
#file:path/to/file.py Explain this
#selection What does this do?

# Slash commands
/explain  /fix  /tests  /doc  /new  /clear

# Custom instructions
.github/copilot-instructions.md          # Repository-wide
.github/instructions/NAME.instructions.md # Path-specific
```

---

## Resources

- [Copilot Cheat Sheet](https://docs.github.com/en/copilot/reference/cheat-sheet)
- [Asking Questions in Your IDE](https://docs.github.com/en/copilot/using-github-copilot/asking-github-copilot-questions-in-your-ide)
- [Chat Checkpoints](https://code.visualstudio.com/docs/copilot/chat/chat-checkpoints)
- [Custom Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot)
- [Customization Library](https://docs.github.com/copilot/tutorials/customization-library)
- [Copilot Chat Cookbook](https://docs.github.com/en/copilot/tutorials/copilot-chat-cookbook)
