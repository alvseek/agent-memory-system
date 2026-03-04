# Setup Guide

Step-by-step guide for configuring Claude Code's global settings and creating new agents. For a quick start, see the [Quick Start](https://github.com/alvseek/agent-memory/blob/master/QUICKSTART.md) in the agent-memory repository.

## Table of Contents
- [Environment Setup](#environment-setup)
- [What the Script Does](#what-the-script-does)
- [Manual Setup](#manual-setup)
- [Creating New Agents](#creating-new-agents)

## Environment Setup

Run the setup script from the `@agent-memory` directory:
```bash
bash control-files/setup-scripts/setup-claude-code.sh
```

The script runs 4 steps interactively:

| Step | What it configures | Target |
|------|-------------------|--------|
| 0 | **User identity & OS** — name, philosophy, agent vision, operating system | `core-memory/` source files |
| 1 | **Global CLAUDE.md** — compiles RAS triggers, reasoning patterns, and user profile | `~/.claude/CLAUDE.md` |
| 2 | **Slash commands** — installs all procedures as global commands | `~/.claude/commands/` |
| 3 | **Settings** — hooks (audio notification, memory refresh after compaction) + bypass permissions | `~/.claude/settings.json` |

Steps that are already configured are automatically skipped. Re-running the script is safe — it updates what changed and leaves the rest intact.

## What the Script Does

For a detailed breakdown of the file structure, compilation system, and memory architecture, see the [Architecture Documentation](ARCHITECTURE.md).

**Step 0** prompts for your name, philosophy, and vision, then selects the correct OS configuration. Skipped if already configured.

**Step 1** compiles the `core-memory/` source files (user profile, environment, RAS triggers, reasoning patterns) into a single `CLAUDE.md` and writes it to `~/.claude/CLAUDE.md`. This is where the Awaken trigger, post-compact recovery, and reasoning patterns live.

**Step 2** copies all procedures from `procedures/` to `~/.claude/commands/`, enabling slash commands like `/high-wizard`, `/update-episodic`, `/wrap-up`, etc. Uses a manifest to clean up stale commands from previous installations. See [Architecture Documentation](ARCHITECTURE.md#common-slash-commands) for the full command list.

**Step 3** merges hooks and permissions into `~/.claude/settings.json` without overwriting existing settings:
- **Stop hook** — plays `stop.wav` when Claude finishes responding
- **SessionStart:compact hook** — triggers memory refresh after context compaction
- **Bypass permissions** — prompts whether to skip permission prompts for tool executions (recommended)

## Manual Setup

If you prefer to configure manually instead of using the script, edit these files directly:

- **User identity**: `control-files/core-memory/0-core-user-profile.md` — replace placeholder values
- **OS selection**: `control-files/core-memory/1-core-environment-memory.md` — uncomment your OS section
- **Compile CLAUDE.md**: `bash control-files/core-memory/compile-scripts/compile-write-to-claude.sh`
- **Slash commands**: `bash control-files/procedures/setup-scripts/setup-all-claude-code.sh`
- **Settings**: `bash control-files/scripts/setup-scripts/setup-settings-claude-code.sh`

For detailed architecture information, see the [Architecture Documentation](ARCHITECTURE.md).

## Creating New Agents

### Step 1: Copy the Template
1. Copy the entire `new-agent-template/` folder and subfolder:
   - **Windows**: `powershell -c "Copy-Item control-files/new-agent-template -Destination agent-[DOMAIN] -Recurse -Force"`
   - **Linux/macOS**: `cp -r control-files/new-agent-template agent-[DOMAIN]`
2. Replace `[DOMAIN]` with your specific domain (e.g., `frontend`, `backend`, `qa`)
3. Navigate into your new agent folder

### Step 2: Replace Domain Placeholders
Replace all instances of `[DOMAIN]` with your specific domain:
- `agent-core-memory.md` - Main flattened agent file (identity + knowledge + RAS + emotional)
- `agent-memory-index.md` - Episode list and knowledge directory
- Inside all the copied `.md` files, replace `[DOMAIN]` with your domain name

### Step 3: Update Agent Identity
- Update agent identity, role, and purpose in `agent-core-memory.md`
- Generate a new UUID for the agent

**Key Placeholders to Replace in `agent-core-memory.md`:**
```markdown
# Core Instruction - [DOMAIN] Agent → # Core Instruction - Frontend Agent
**Name**: Agent [DOMAIN] → **Name**: Agent Frontend
**Role**: [DOMAIN] Agent → **Role**: Frontend Agent
**Main Purpose**: [Description] → **Main Purpose**: [Domain specific purpose]
**UUID**: [GENERATE-NEW-UUID] → **UUID**: [Your new UUID]
```
