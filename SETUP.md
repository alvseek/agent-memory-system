# Setup Guide

Step-by-step guide for configuring agent-memory with Claude Code or Codex and creating new agents. For a quick start, see the [Quick Start](https://github.com/alvseek/agent-memory/blob/master/QUICKSTART.md) in the agent-memory repository.

## Table of Contents
- [Environment Setup](#environment-setup)
- [Claude Code Setup](#claude-code-setup)
- [Codex Setup](#codex-setup)
- [Read Tool Token Limit](#read-tool-token-limit)
- [Manual Setup](#manual-setup)
- [Creating New Agents](#creating-new-agents)

## Environment Setup

Run the relevant setup script from the `@agent-memory` directory.

## Claude Code Setup

```bash
bash control-files/setup-scripts/setup-claude-code.sh
```

The Claude Code setup script runs 4 steps interactively:

| Step | What it configures | Target |
|------|-------------------|--------|
| 0 | **User identity & OS** - name, philosophy, agent vision, operating system | `core-memory/` source files |
| 1 | **Global CLAUDE.md** - compiles RAS triggers, reasoning patterns, and user profile | `~/.claude/CLAUDE.md` |
| 2 | **Slash commands** - installs all procedures as global commands | `~/.claude/commands/` |
| 3 | **Settings** - hooks (audio notification, memory refresh after compaction) + bypass permissions + disable attribution + Read tool 64K limit | `~/.claude/settings.json` + `~/.claude.json` |

Steps that are already configured are automatically skipped. Re-running the script is safe - it updates what changed and leaves the rest intact.

## Codex Setup

```bash
bash control-files/setup-scripts/setup-codex.sh
```

The Codex setup script runs 3 steps interactively:

| Step | What it configures | Target |
|------|-------------------|--------|
| 0 | **User identity & OS** - name, philosophy, agent vision, operating system | `core-memory/` source files |
| 1 | **Global AGENTS.md** - compiles RAS triggers, reasoning patterns, and user profile for Codex | `~/.codex/AGENTS.md` |
| 2 | **Codex skills** - converts all procedures into reusable Codex user skills | `~/.agents/skills/` |

In Codex, `AGENTS.md` is the global instruction layer, and skills are the closest equivalent to Claude slash commands for reusable workflows.

## Claude Code Setup Details

For a detailed breakdown of the file structure, compilation system, and memory architecture, see the [Architecture Documentation](ARCHITECTURE.md).

**Step 0** prompts for your name, philosophy, and vision, then selects the correct OS configuration.

**Step 1** compiles the `core-memory/` source files (user profile, environment, RAS triggers, reasoning patterns) into a single `CLAUDE.md` and writes it to `~/.claude/CLAUDE.md`. This is where the Awaken trigger, post-compact recovery, and reasoning patterns live.

**Step 2** copies all procedures from `procedures/` to `~/.claude/commands/`, enabling slash commands like `/high-wizard`, `/update-episodic`, `/wrap-up`, etc. Uses a manifest to clean up stale commands from previous installations. See [Architecture Documentation](ARCHITECTURE.md#common-slash-commands) for the full command list.

**Step 3** merges hooks and permissions into `~/.claude/settings.json` without overwriting existing settings:
- **Stop hook** - plays `stop.wav` when Claude finishes responding
- **SessionStart:compact hook** - triggers memory refresh after context compaction
- **Bypass permissions** - prompts whether to skip permission prompts for tool executions (recommended)
- **Disable attribution** - removes the `Co-Authored-By: Claude` trailer from commits and PRs
- **Read tool 64K limit** - increases `tengu_amber_wren.maxTokens` from 10K to 64K in `~/.claude.json` (requires restart)

## Codex Setup Details

**Step 0** uses the same user configuration flow as Claude Code so the compiled memory reflects your identity, philosophy, and operating system.

**Step 1** compiles the `core-memory/` source files into a single global Codex instruction file and writes it to `~/.codex/AGENTS.md`.

**Step 2** converts each procedure in `control-files/procedures/` and `control-files/procedures/memory/` into a Codex user skill under `~/.agents/skills/`. Each installed skill wraps the original procedure markdown in a Codex-native `SKILL.md` so it can be invoked explicitly or discovered implicitly by Codex.

Codex setup intentionally does not include a settings or hooks step here. Codex hooks are currently experimental, and on Windows they are not a stable equivalent to the Claude Code settings flow.

## Read Tool Token Limit

Claude Code's Read tool has a default token limit controlled by a Statsig feature flag (`tengu_amber_wren`), which may be as low as 10K tokens. This causes large memory files (like `agent-core-memory.md` or `agent-memory-index.md`) to fail loading during awakening.

**To increase the limit to 64K tokens**, edit `~/.claude.json` and find the `tengu_amber_wren` entry inside the `statsigValues` object:

```json
"tengu_amber_wren": {
  "targetedRangeNudge": true,
  "maxTokens": 10000
}
```

Change `maxTokens` to `64000`:

```json
"tengu_amber_wren": {
  "targetedRangeNudge": true,
  "maxTokens": 64000
}
```

> **Note**: `~/.claude.json` is Claude Code's internal config (not `settings.json`). This change survives sessions but may be reset by Claude Code updates - re-check after updating CLI versions.

Restart Claude Code for the change to take effect.

## Manual Setup

If you prefer to configure manually instead of using the script, edit these files directly:

- **User identity**: `control-files/core-memory/0-core-user-profile.md` - replace placeholder values
- **OS selection**: `control-files/core-memory/1-core-environment-memory.md` - uncomment your OS section
- **Compile CLAUDE.md**: `bash control-files/core-memory/compile-scripts/compile-write-to-claude.sh`
- **Slash commands**: `bash control-files/procedures/setup-scripts/setup-all-claude-code.sh`
- **Settings**: `bash control-files/scripts/setup-scripts/setup-settings-claude-code.sh`
- **Compile Codex AGENTS.md**: `bash control-files/core-memory/compile-scripts/compile-write-to-codex.sh`
- **Codex skills**: `bash control-files/procedures/setup-scripts/setup-all-codex.sh`

For detailed architecture information, see the [Architecture Documentation](ARCHITECTURE.md).

## Creating New Agents

### Step 1: Copy the Template
1. Copy the entire `new-agent-template/` folder and subfolder:
   `cp -r control-files/new-agent-template agent-[DOMAIN]`
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
# Core Instruction - [DOMAIN] Agent -> # Core Instruction - Frontend Agent
**Name**: Agent [DOMAIN] -> **Name**: Agent Frontend
**Role**: [DOMAIN] Agent -> **Role**: Frontend Agent
**Main Purpose**: [Description] -> **Main Purpose**: [Domain specific purpose]
**UUID**: [GENERATE-NEW-UUID] -> **UUID**: [Your new UUID]
```
