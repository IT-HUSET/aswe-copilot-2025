# Exercise 3: Tool Building

**Goal:** Build tools that extend Copilot's capabilities

**Prerequisites:** Exercise 1 completed

### API Key Setup
Create a `.env` file in the project root (copy from `.env.example`) and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```
Get a key at: https://platform.openai.com/api-keys or use an existing one provided to you.

---

## The Mindset

Agentic developers build tools that AI can use. In this exercise you'll:
1. Create a CLI for AI image generation
2. Have Copilot use the CLI to add features to the app
3. Create a custom Copilot slash command for code review

The key insight: **Copilot can run your tools and use your custom commands.** Build good interfaces and Copilot becomes more capable.

---

## Part A: Build the CLI

### Prompt Copilot

**Recommended: Python** — simplest setup, best SDK support, matches the todo-app stack.

> ```md
> #file:docs/exercises/gen-image-cli-prompt-openai.md
>
> Use Python and Astral uv (make the script standalone and runnable with uv run). 
> Create the CLI in gen-image/.
> Include --help, input validation, and clear error messages.
> ```

<details>
<summary>Want to use a different language?</summary>

The dev container also supports:

- Java
- Node.js
- Deno

Replace "Python" in the prompt with your preferred language.

_Note:_ You can add more languages by modifying the dev container (see `.devcontainer/devcontainer.json`).
</details>

### Expected CLI Interface

```
gen-image --prompt "A cute robot" [options]

Options:
  --prompt        Image description (required)
  --aspect-ratio  square (1024x1024, default), portrait (1024x1792), landscape (1792x1024)
  --quality       standard (default), hd
  --output        Output file path (default: output.png)
  --help          Show usage
```

### Verify It Works

> ```md
> Test the gen-image CLI by generating a simple test image.
> Use --help first to confirm the interface, then generate an image.
> ```

Watch Copilot run the CLI itself.

<details>
<summary>If it doesn't work...</summary>

Common issues and how to fix them:

| Problem | Solution |
|---------|----------|
| `OPENAI_API_KEY not found` | Check `.env` file exists in project root with valid key |
| `ModuleNotFoundError` | Ask Copilot to install dependencies: "Install the required packages for gen-image" |
| Permission denied | Make script executable: `chmod +x gen-image/gen-image.py` |
| API error / rate limit | Wait a moment and retry, or check API key validity |

**General fix:** Paste the error message to Copilot and ask it to fix the issue.
</details>

---

## Part B: Create a Custom Code Review Agent & Command

Copilot supports **custom agents** (reusable AI personas with specific instructions) and **slash commands** (quick ways to invoke them). You'll create both:
- A `code-reviewer` agent with detailed review instructions
- A `/review-code` command that invokes the agent

### Step 1: Create the Agent

Agents are stored in `.github/agents/` and define the AI's behavior and instructions.

**How to create:**

*Option 1: Using VS Code UI*
1. Open Copilot Chat, click the **agent dropdown** (where it says `@workspace` or similar)
2. Select **Configure Custom Agents** → **Create new custom agent**
3. Select **Workspace**, name it `code-reviewer`

*Option 2: Using Command Palette*
1. `Cmd+Shift+P` / `Ctrl+Shift+P` → **"Chat: New Custom Agent"**
2. Select **Workspace**, name it `code-reviewer`

*Option 3: Create manually*
1. Create folder `.github/agents/` if it doesn't exist
2. Create file `.github/agents/code-reviewer.agent.md`

**Your task:** Define an agent that:
- Acts as a senior engineer providing constructive feedback
- Reviews security, performance, code quality, architecture, and testing
- Outputs findings in categories: Critical, Suggestions, Good Practices
- Includes line references and code examples

<details>
<summary>Stuck? Agent file structure</summary>

**Frontmatter:**
```yaml
---
name: code-reviewer
description: 'Senior engineer that performs comprehensive code reviews'
---
```

**Body content should cover:**
1. Role definition: "You are a senior engineer providing constructive, actionable feedback..."
2. Review areas:
   - Security (validation, authentication, injection vulnerabilities)
   - Performance (algorithm complexity, memory usage)
   - Code quality (readability, naming, duplication)
   - Architecture (patterns, separation of concerns)
   - Testing (coverage, edge cases)
3. Output format with visual indicators (🔴 Critical, 🟡 Suggestions, ✅ Good Practices)
4. Each finding should include: file:line reference, explanation, code example, rationale

**Reference:** 
- [VS Code Custom Agents Documentation](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [GitHub Copilot Code Review sample](https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files/review-code)
</details>

### Step 2: Create the Command

Commands are stored in `.github/prompts/` and provide a quick way to invoke agents.

**How to create:**

*Option 1: Using VS Code UI*
1. Open Chat view → **gear icon** → **Prompt Files** → **New prompt file**
2. Select **Workspace**, name it `review-code`

*Option 2: Using Command Palette*
1. `Cmd+Shift+P` / `Ctrl+Shift+P` → **"Chat: New Prompt File"**
2. Select **Workspace**, name it `review-code`

*Option 3: Create manually*
1. Create file `.github/prompts/review-code.prompt.md`

**Your task:** Create a simple command that references the agent:

<details>
<summary>Stuck? Command file structure</summary>

```yaml
---
agent: 'code-reviewer'
description: 'Run a comprehensive code review'
---
```

Review the currently open file or selected code. Focus on the most important issues first.
</details>

**Reference:** [VS Code Prompt Files Documentation](https://code.visualstudio.com/docs/copilot/customization/prompt-files)

### Test Your Agent & Command

**Test the slash command** by reviewing the CLI code you created in Part A:

> ```md
> /review-code #file:gen-image/gen-image.py
> ```

Or review the entire CLI folder:

> ```md
> /review-code #folder:gen-image
> ```

**Test the agent directly:**
1. Click the **agent dropdown** in Copilot Chat (where it shows the current agent/mode)
2. Select your **code-reviewer** agent
3. Type a prompt like: `Review #folder:gen-image for code quality`

The `#file:` and `#folder:` syntax tells Copilot exactly what to review. You can also use `#selection` for currently selected code.

<details>
<summary>If the command or agent doesn't appear...</summary>

**For agents:**
- Ensure file is in `.github/agents/`
- File must end in `.agent.md`
- Check `name` field in frontmatter

**For commands:**
- Ensure file is in `.github/prompts/`
- File must end in `.prompt.md`
- Check `agent` field matches the agent name exactly

**General:**
- Reload VS Code window (Cmd/Ctrl+Shift+P → "Reload Window")
</details>

---

## Part C: Add Logo to Login Page

Now have Copilot use the CLI tool to add a feature.

> ```md
> Use the gen-image CLI to generate a logo for the todo app:
> - Prompt: "Minimal todo list app logo, checkmark icon, modern flat design, blue and white"
> - Square aspect ratio
> - Save to todo-app/src/app/static/images/logo.png
>
> Then add the logo to the login page, centered above the form, max width 120px.
> ```

**Watch Copilot:**
1. Run your CLI with the right arguments
2. Edit the login template
3. Add CSS for the logo

### Test

Visit the login page — logo should appear.

---

## Part D: Generate Welcome Banner (Optional)

Add a welcome image to the main app.

> ```md
> Use the gen-image CLI to create a welcome banner:
> - Prompt: "Productivity illustration, person completing tasks, minimal style, soft colors"
> - Landscape aspect ratio
> - Save to todo-app/src/app/static/images/welcome-banner.png
>
> Add it to the empty state when a list has no todos.
> Show it centered with "No todos yet!" text below.
> ```

---

## Completion Checklist

- [ ] CLI works with `--help`
- [ ] `code-reviewer` agent available in agent dropdown
- [ ] `/review-code` command invokes the agent
- [ ] Copilot successfully runs the CLI
- [ ] Logo appears on login page
- [ ] (Optional) Welcome banner appears on empty todo lists

---

## Key Takeaways

| Concept | Remember |
|---------|----------|
| Tools for AI | Build CLIs that Copilot can use |
| Good interfaces | Clear args, validation, help text |
| Composability | Small tools combine into features |
| Let AI drive | Prompt Copilot to use your tools |
| Custom agents | `.github/agents/*.agent.md` — reusable AI personas |
| Custom commands | `.github/prompts/*.prompt.md` — invoke agents with `/command` |

---

## Stretch Challenges

| Challenge | Prompt |
|-----------|--------|
| List backgrounds | "Generate unique background for each todo list using gen-image" |
| Avatar generator | "Use gen-image to create user avatars based on username" |
| Todo icons | "Generate small icons for high-priority todos" |

---

## API Reference

**Model:** `dall-e-3`

**Parameters:**
- `prompt` — text description
- `size` — 1024x1024 (square), 1024x1792 (portrait), 1792x1024 (landscape)
- `quality` — standard, hd

**Docs:** [OpenAI Image Generation](https://platform.openai.com/docs/guides/image-generation)

---

## Resources

- [OpenAI API Docs](https://platform.openai.com/docs)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [OpenAI Node SDK](https://github.com/openai/openai-node)
- [VS Code Custom Agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [VS Code Prompt Files](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
- [GitHub Custom Agents Configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [GitHub Customization Library](https://docs.github.com/en/copilot/tutorials/customization-library)
