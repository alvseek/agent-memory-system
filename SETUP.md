# Setup Guide

Step-by-step guide for configuring agent-memory with Claude Code or Codex and creating new agents. For a quick start, see the [Quick Start](https://github.com/alvseek/agent-memory/blob/master/QUICKSTART.md) in the agent-memory repository.

## Table of Contents
- [Environment Setup](#environment-setup)
- [Claude Code Setup](#claude-code-setup)
- [Codex Setup](#codex-setup)
- [Tool Output Token Limits](#tool-output-token-limits)
- [Manual Setup](#manual-setup)
- [Creating New Agents](#creating-new-agents)

## Environment Setup

Run the relevant setup script from the `@agent-memory` directory.

### Environment-Based Wrapper Choice

Use the wrapper that matches your execution environment:

- **Git Bash / WSL / Linux / macOS shell**: use `.sh`
  - `bash control-files/setup-scripts/setup-claude-code.sh`
  - `bash control-files/setup-scripts/setup-codex.sh`
- **Windows Command Prompt / double-click flow**: use `.bat` wrapper (calls Git Bash internally)
  - `control-files\setup-scripts\setup-claude-code.bat`
  - `control-files\setup-scripts\setup-codex.bat`

The wrapper should follow the environment you are launching from, not just OS type.

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

The Codex setup script runs 4 steps interactively:

| Step | What it configures | Target |
|------|-------------------|--------|
| 0 | **User identity & OS** - name, philosophy, agent vision, operating system | `core-memory/` source files |
| 1 | **Global AGENTS.md** - compiles RAS triggers, reasoning patterns, and user profile for Codex | `~/.codex/AGENTS.md` |
| 2 | **Codex skills** - converts all procedures into reusable Codex user skills | `~/.agents/skills/` |
| 3 | **Codex settings** - tool output token limit (64K) + SessionStart memory-recovery reminder hook | `~/.codex/config.toml` |

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

**Step 3** updates `~/.codex/config.toml` to:
- set `tool_output_token_limit = 64000` for large memory-file workflows
- enable hooks with `[features] codex_hooks = true`
- install a `SessionStart` hook (`startup|resume|clear`) that injects memory-recovery reminder context (same intention as Claude's post-compact reminder flow)

## Tool Output Token Limits

Large memory files (like `agent-core-memory.md` or `agent-memory-index.md`) can fail loading when tool output token limits are too low.

### Claude Code Read Tool Limit

Claude Code's Read tool has a default token limit controlled by a Statsig feature flag (`tengu_amber_wren`), which may be as low as 10K tokens.

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

### Codex Tool Output Token Limit

Codex tool-call output history has a per-tool token budget (`tool_output_token_limit`) in `~/.codex/config.toml`. If it is too low, large file reads can be truncated in context.

**To increase the limit to 64K tokens**, add or update this line in `~/.codex/config.toml`:

```toml
tool_output_token_limit = 64000
```

If the key does not exist, add it near the top-level model settings.

> **Note**: This is a Codex config value (not Claude settings). Restart Codex after editing so the new limit is picked up.

## Manual Setup

If you prefer to configure manually instead of using the script, edit these files directly:

- **User identity + OS + agent path**: `bash control-files/core-memory/compile-scripts/user-config.sh` (writes runtime-resolved files to `control-files/core-memory/output/`)
- **Compile CLAUDE.md**: `bash control-files/core-memory/compile-scripts/compile-write-to-claude.sh`
- **Slash commands**: `python control-files/procedures/setup-scripts/setup-all-claude-code.py`
- **Settings**: `bash control-files/scripts/setup-scripts/setup-settings-claude-code.sh`
- **Compile Codex AGENTS.md**: `bash control-files/core-memory/compile-scripts/compile-write-to-codex.sh`
- **Codex skills**: `bash control-files/procedures/setup-scripts/setup-all-codex.sh`

For detailed architecture information, see the [Architecture Documentation](ARCHITECTURE.md).

## Creating New Agents

Run `/create-agent [domain]` — it seeds the agent's memory home, writes its identity, and verifies the result can be awakened. The command drafts the four identity fields (name, role, main purpose, three responsibilities) from the domain name and asks you to correct them, generates the UUID, and confirms before writing anything.

```
/create-agent frontend-react
```

Everything else in a new agent — core domain knowledge, RAS triggers, reasoning patterns, emotional moments — starts empty by design and grows through use. Bring the agent up for the first time with `/awaken-agent [domain]`.

The command works on either storage backend: on the markdown fleet it copies the two per-agent files out of `new-agent-template/` and creates the agent's `episodes/` and `knowledge-base/` directories; on the DB backend it inserts the agent's identity records, since there is no folder to make. Note that `new-agent-template/shared-memory/` is **not** part of an agent — it is a virgin-store seed for a fleet that has no shared memory yet, and shared memory lives once at the store root.

If you need to do it by hand — recovering a partially-created agent, or working without the installed commands — the concrete steps for each backend are in `procedures/memory/storage-backends/markdown.md` and `db.md`, under `## create-agent`.
