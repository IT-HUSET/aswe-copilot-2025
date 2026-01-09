![Let's build agentically!](assets/lets-build-agentically.jpg?raw=true)


# Agentic Software Engineering with Copilot Workshop 2025


<br/>


## Prerequisites

- **GitHub account** and **GitHub Copilot** subscription
- For local development:
    - **VS Code** with GitHub Copilot extension
    - **Docker Desktop** or equivalent, for local Dev Container support
- Alternative: Use **GitHub Codespaces**

<br/>

## Getting Started / Preparations

Follow the steps below to prepare your development environment for the exercises. Note that you have two options for launching the development environment: either **locally using Dev Containers and VS Code**, or using **GitHub Codespaces**.

- _Benefit of local development with **Dev Container**_: Works offline (and not dependent on network conditions), more control over environment
- _Benefit of **GitHub Codespaces**_: No local setup required (and quicker setup), works on any machine

<br/>

### **Step 1.** Fork the Repository
To be able to push your own changes, you need to fork this repository to your own personal GitHub account. <br/>
_**See also:**_ [Keeping your fork in sync](#keeping-your-fork-in-sync), in case the original repository is updated later.
<br/><br/>


Step 1: Click the "Fork" button at the top-right of this page<br/>
<img src="assets/fork.png" height="30"/>

Step 2: Select your _**PERSONAL**_ GitHub account as the _**owner**_ of the fork<br/>
<img src="assets/fork-step2.jpg" height="300"/><br/>
_**NOTE**: Do NOT fork to an organization account, as this may cause issues with GitHub Copilot and GitHub Codespaces access._

<br/>

### **Step 2 - (OPTION 1)** - Launch the dev environment in local **Dev Container**
Launch the development environment in a _Dev Container_ locally using _Docker Desktop_ (or similar) and _VS Code_.

#### **2.1. Configure VS Code**
<img src="https://code.visualstudio.com/assets/docs/copilot/setup/setup-copilot-sign-in.png" width="300" alt="GitHub Copilot sign in">

##### **2.1.1. Install VS Code**
Ensure you have the latest version of [VS Code](https://code.visualstudio.com/download) installed.

##### **2.1.2. Login to GitHub and Set Up Copilot**
Ensure that you are logged in to your GitHub account in VS Code.
    - Read more: [Sign in to GitHub in VS Code](https://code.visualstudio.com/docs/editor/github#_sign-in-to-github)
    - And even more: [Set up Copilot in VS Code](https://code.visualstudio.com/docs/copilot/setup#_set-up-copilot-in-vs-code)

##### **2.1.3. Install Extensions**
- Ensure that the [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) is installed and enabled in VS Code.
- Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) in VS Code.


#### **2.2. Clone Project in VS Code**
- Open VS Code
- Open Command Palette (`Cmd+Shift+P` or `Ctrl+Shift+P`)
- Type "Git: Clone" and select it<br/>
    <img src="assets/vscode-clone.png" height="300"/><br/>


#### **2.3. Open Project in Dev Container**
Launch the development environment in a Dev Container locally using Docker Desktop (or similar) and VS Code.

##### **2.3.1. Ensure Docker is Running**
Make sure Docker Desktop (or your preferred Docker environment) is installed and running on your machine.

##### **2.3.2. Open Project in Dev Container**
- When prompted by VS Code, click "Reopen in Container"<br/>
    <img src="assets/reopen-in-container.jpg" height="150"/><br/>
- If not prompted, open the Command Palette (`Cmd+Shift+P` or `Ctrl+Shift+P`), type "Dev Containers: Reopen in Container", and select it.<br/>
- Let VS Code build and start the Dev Container. _This may take several minutes on first run._


<br/>

### **Step 2 - (OPTION 2)** - Launch the dev environment in **GitHub Codespaces**
- Click "Code" and then "Create codespace on main" in the GitHub UI<br/>
    <img src="assets/code.png" height="30"/><br/>
    <img src="assets/codespacer.png" height="30"/>
    <br/>
- Let GitHub set up the Codespace. _This may take several minutes on first run._

<br/>

### **Step 3.** Verify Setup
Wait for the development environment to load completely. You should see the project files in the VS Code Explorer panel, and you should see the banner below indicating that the Dev Container has been setup successfully. 

<img src="assets/dev-container-done.png" height="150"/><br/>

Alternatively (usually when running in a codespace), you may also just see an empty terminal prompt: 

<img src="assets/dev-container-done-terminal.jpg" height="70"/><br/>

To verify that everything is working correctly, use the terminal (open a new one if necessary) to run the following command to check the copilot CLI version: 

```bash
copilot --version
```

You should then see output similar to this: 

<img src="assets/dev-container-verify.jpg" height="77"/><br/>


<br/>

---

<br/>



## Overview of Exercises

| Exercise | Focus |
|----------|-------|
| [1. Copilot Fundamentals](docs/exercises/exercise-1-copilot-fundamentals.md) | Modes, commands, custom instructions, codebase exploration |
| [2. Bug Hunt](docs/exercises/exercise-2-bug-hunt.md) | Fix 4 planted bugs with Agent Mode |
| [3. Tool Building](docs/exercises/exercise-3-tool-building.md) | Build CLI tool, setup custom agent & command for review |
| [4a. Cloud Feature](docs/exercises/exercise-4a-cloud-feature.md) | Copilot coding agent via GitHub Issues |
| [4b. Local Feature](docs/exercises/exercise-4b-local-feature.md) | Plan → Implement → Verify workflow |
| [5. Spec-Driven Development](docs/exercises/exercise-5-spec-driven-development.md) | GitHub Spec Kit workflow |
| [6. AI Feature Integration](docs/exercises/exercise-6-ai-feature-integration.md) | Spec Kit + OpenAI integration |
| [7. Alternative Stack](docs/exercises/exercise-7-alternative-stack.md) | Rebuild todo app in different stack (optional) |


### Todo App Commands Reference

<img src="assets/todo-app.jpg" height="600"/><br/>

The simple Todo App used in the exercises is located in the `todo-app/` folder. You can use the commands below to run and test the app. 
The app runs at http://localhost:8000 by default.

```bash
cd todo-app

## Install dependencies
uv sync

# Start app
uv run uvicorn app.main:app --reload

# Start app on custom port
uv run uvicorn app.main:app --reload --port 3000

# Run tests
uv run pytest tests/ -v
```


## Useful Links

### GitHub Copilot
https://docs.github.com/en/copilot/how-tos/configure-personal-settings/configure-in-ide

- [GitHub Copilot in VS Code cheat sheet](https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features)
- [GitHub Copilot Chat Cookbook](https://docs.github.com/copilot/tutorials/copilot-chat-cookbook)

#### Specific topics
- [Custom Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot)
- [Chat Checkpoints](https://code.visualstudio.com/docs/copilot/chat/chat-checkpoints)
- [GitHub Custom Agents Configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Copilot Chat Cookbook](https://docs.github.com/en/copilot/tutorials/copilot-chat-cookbook)
- [About Copilot Coding Agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)

#### Customizing Copilot
- [GitHub Customization Library](https://docs.github.com/en/copilot/tutorials/customization-library)
- [Awesome Copilot](https://github.com/github/awesome-copilot)


### Prompt/Context Engineering Guides
- [GitHub Copilot Prompt Engineering Guide](https://docs.github.com/en/copilot/concepts/prompting/prompt-engineering)
- [Claude - Best Practices for Prompt Engineering](https://www.claude.com/blog/best-practices-for-prompt-engineering)
- [Anthropic - Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [GPT-5 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide)


### Dev Containers
- [Dev Containers](https://containers.dev)
- [Dev Containers Features](https://containers.dev/features)
- [VS Code - Developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers)
- [JetBrains - Connect to Dev Container](https://www.jetbrains.com/help/idea/connect-to-devcontainer.html)


### Useful Tools
- [GitHub Spec Kit](https://github.com/github/spec-kit)
- [Gitingest](https://gitingest.com/)
- [The /llms.txt file](https://llmstxt.org)


### Useful MCP servers
- [Fetch - Downloading web content as markdown](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch)
- [Context 7 - Documentation lookup](https://github.com/upstash/context7)
- [Ref.tools - Documentation lookup](https://ref.tools/)
- [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Sequential Thinking](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking)


### Interesting Readings / Viewing
- [Simon Willison - The Lethal Trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
- [YouTube - The Message Every Engineer Needs to Hear](https://www.youtube.com/watch?v=XKCBcScElBg)
- More comping soon...


---

## Keeping Your Fork in Sync

If the original repository is updated after you fork, you can pull in those changes.

**Option 1: Via GitHub UI** (easiest)<br/>
On your fork's GitHub page, click **"Sync fork"** if your branch is behind:<br/>
<img src="assets/sync-fork.jpg" height="140"/><br/>
_(Then select "Update branch" if prompted.)_

**Option 2: Via command line**
```bash
# Check if upstream remote exists
git remote -v
```

If `upstream` is not listed, add it:
```bash
git remote add upstream https://github.com/computation-ninja/aswe-copilot-2025.git
```

Then fetch and merge:
```bash
git fetch upstream
git checkout main
git merge upstream/main

# Optional: push to your fork's remote
git push origin main
```
