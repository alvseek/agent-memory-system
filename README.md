# Agent Memory System — Memory Core

The **memory core** of the [Agent Memory](https://github.com/alvseek/agent-memory) architecture — the domain-agnostic memory primitives (awaken, memory read/write, session wrap-up) plus the templates and compilation tooling that every agent needs. Designed to be used as a **git submodule** inside your private agent-memory repository.

Coding- and repo-oriented procedures (wizards, doc generation, QA, localization, push/pull) live in the **separate** [agent-memory-coding-skill](https://github.com/alvseek/agent-memory-coding-skill) overlay — an independent repo that composes on top of this core for coding agents. A plain chat agent uses this core alone.

---

## Table of Contents

- [What Is This?](#what-is-this)
- [Two-Repo Architecture](#two-repo-architecture)
- [How Do I Set It Up?](#how-do-i-set-it-up)
- [How Do I Use It?](#how-do-i-use-it)
- [How Does It Work Inside?](#how-does-it-work-inside)
- [What Decisions Were Made?](#what-decisions-were-made)

---

## What Is This?

This submodule provides the **memory-primitive** infrastructure for the [5-layer agent memory system](https://github.com/alvseek/agent-memory): procedures that teach agents how to manage their own memory (episodic, knowledge, reasoning, emotional, project-context), awaken from central memory, recover after compaction, and wrap up a session. It knows nothing about repos, git, wizards, or fleet — those are the overlay's job.

### Architecture

```
control-files/
├── core-instruction-control-files.md  # Shared reasoning & knowledge (loaded by all agents)
├── procedures/                         # Memory-primitive procedures (also work as slash commands)
│   ├── awaken-agent.md                # Load agent identity + central memory
│   ├── refresh-memory.md              # Post-compaction recovery
│   ├── wrap-up.md                     # End-of-session memory capture (memory-only)
│   ├── push-memory.md                 # Persist the memory store (git push)
│   ├── pull-memory.md                 # Sync the memory store (git pull + submodule)
│   ├── memory/                        # Memory management (10 procedures) + resources/ (entry templates) + storage-backends/
│   └── setup-scripts/                 # 2-repo-aware setup orchestrators (core / core+skill)
├── new-agent-template/                 # Starter template for new agents
├── core-memory/                        # Source files for Global CLAUDE.md compilation
├── docs/                               # Framework standards + orientation map
└── scripts/                            # Core scripts (copy-lines, invariant guard, refresh)
```

For the complete file tree and agent directory structure, see [ARCHITECTURE.md](ARCHITECTURE.md).

### Tech Stack

- **Scripts**: Bash (cross-platform via Git Bash on Windows)
- **Content**: Markdown with YAML frontmatter (for knowledge base tagging)
- **Integration**: Claude Code slash commands and hooks

---

## Two-Repo Architecture

The framework is split into two independent, standalone repos with a strict **one-way dependency**:

| Repo | Role | Contents |
|------|------|----------|
| **control-files** (this repo) | Memory core | Awaken, memory read/write, session wrap-up, memory templates, compilation. Standalone; MCP-wrappable later. |
| **[agent-memory-coding-skill](https://github.com/alvseek/agent-memory-coding-skill)** | Coding overlay | Wizards, doc-gen, QA, fleet, `map-orientation`, `localize-context`, `wait-options`, push/pull, `project-wrap-up`, `awaken-coder`. |

- **The overlay depends on the core; the core never references the overlay by name** — enforced by [`scripts/check-core-invariant.sh`](scripts/check-core-invariant.sh).
- **Composition is agent-side, additive — not override.** The overlay's `awaken-coder` simply orchestrates *"run the core `/awaken-agent`, then localized-home + orientation map + fleet."*
- **Each repo installs itself.** A **chat agent** runs this core's installer only; a **coding agent** also runs the overlay's own installer (the overlay ships its own `setup-scripts/`). The two installers use **separate manifests**, so they coexist in the same commands dir and clean up independently.

---

## How Do I Set It Up?

### As Part of Agent Memory

If you cloned the [agent-memory](https://github.com/alvseek/agent-memory) template, the setup script handles everything:

```bash
# Memory core — every agent (chat or coding):
bash control-files/procedures/setup-scripts/setup-all-claude-code.sh

# Coding agents ALSO run the overlay's own installer (separate repo):
bash /path/to/agent-memory-coding-skill/setup-scripts/setup-all-claude-code.sh
```

Each repo installs itself — a coding agent runs both installers (they use separate manifests and coexist). For detailed setup options and manual alternatives, see the [Setup Guide](SETUP.md).

### Updating the Submodule

Pull the latest control-files updates:

```bash
cd control-files && git pull origin main && cd ..
git add control-files && git commit -m "chore: bump control-files submodule"
```

Or use the built-in command: `/pull-memory` (provided by the coding overlay).

---

## How Do I Use It?

The core installs as slash commands to `~/.claude/commands/`. These are the **memory primitives**:

### Memory Procedures

| Command | Purpose |
|---------|---------|
| `/update-memory` | Comprehensive update (all layers evaluated) |
| `/update-episodic` | Session log only |
| `/add-reasoning` | Reasoning pattern capture |
| `/update-knowledge` | Knowledge entry capture |
| `/update-emotional` | Emotional memory capture |
| `/load-episodic` | Browse and load past episodic memories |
| `/load-knowledge` | Browse and load knowledge base files |
| `/archive-old-memories` | Archive old memories with evaluation |

### Core Operational Commands

| Command | Purpose |
|---------|---------|
| `/awaken-agent [domain]` | Load agent memory and activate (central) |
| `/refresh-memory [domain]` | Recover memory after context compaction |
| `/wrap-up` | End-of-session **memory capture only** (via `/update-memory` + surface open items) |

> **Coding agents**: the overlay adds `/project-wrap-up` (composes `/wrap-up`, then push + `/map-orientation`), the wizard protocols (`/quick-wizard` → `/forge-of-covenant`), `/implement-plan`, doc generation (`/generate-readme`, `/generate-docs`, …), QA (`/analyze-code-quality`, `/integration-test`, …), fleet (`/ask-agent`, `/delegate-agent`, `/setup-fleet`), `/map-orientation`, `/localize-context`, and push/pull. See the [overlay repo](https://github.com/alvseek/agent-memory-coding-skill).

### Compilation

Compile core-memory source files into the global CLAUDE.md:

```bash
# Full compile + write
bash core-memory/compile-scripts/compile-write-to-claude.sh

# Step by step (preview first)
bash core-memory/compile-scripts/compile.sh          # Compile to output/
bash core-memory/compile-scripts/write-to-claude.sh  # Write to ~/.claude/CLAUDE.md
```

---

## How Does It Work Inside?

### Core Instruction File

`core-instruction-control-files.md` is the shared control file loaded by every agent at awakening. It contains:

| Section | Content |
|---------|---------|
| Awakening Instructions | Central awakening protocol (Phase 1 identity + Phase 2 central context) |
| User Profile | User identity (name, philosophy, vision) |
| Reasoning Memory | UUID-based reasoning patterns with emotional anchoring |
| Knowledge Memory | 5-layer architecture reference, behavioral rules |

### Core Memory Compilation

The Global CLAUDE.md (always loaded before any agent awakens) is built from modular source files:

```
core-memory/
├── 0-core-user-profile.md        → User identity
├── 1-core-environment-memory.md  → OS-specific settings
├── 2-core-ras-memory.md          → Universal RAS triggers (Awaken, Post-Compact, etc.)
├── 3-core-reasoning-memory.md    → Core reasoning patterns (compact form)
└── compile-scripts/              → Build tooling
```

The compilation system concatenates source files, strips HTML comments, and writes the result to `~/.claude/CLAUDE.md`.

### Procedure Structure

Every procedure follows a consistent format and doubles as a slash command:

1. **Arguments** — What the command accepts (e.g., `[domain]`, `[context]`)
2. **Procedure** — Step-by-step instructions for the agent to follow
3. **Templates** — Output format templates (where applicable)

Procedures are installed as slash commands to `~/.claude/commands/` by the setup script.

For the complete loading flow, memory layer details, and the coding overlay, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## What Decisions Were Made?

### Memory Core / Coding Overlay Split

**Context**: A foreign consuming agent (coding *or* chat-based) should be able to load memory with no coding-specific procedures baked into the output.
**Decision**: Slim `control-files` to memory primitives; extract all coding/repo procedures into the standalone [agent-memory-coding-skill](https://github.com/alvseek/agent-memory-coding-skill) overlay. One-way dependency (overlay → core), machine-checked by an invariant guard.
**Trade-off**: Two repos + cross-repo links to maintain, but the core is genuinely standalone and MCP-wrappable, and chat agents get a leak-free memory experience.

### Procedures as Slash Commands

**Context**: Memory update procedures needed to be easily executable during sessions without remembering file paths.
**Decision**: Every procedure file doubles as a slash command — same file, installed to `~/.claude/commands/`.
**Trade-off**: Procedure files must follow Claude Code's command format, but eliminates duplication between docs and automation.

### Core Memory Compilation

**Context**: Global CLAUDE.md needs to combine user identity, RAS triggers, and reasoning patterns from separate source files for maintainability.
**Decision**: Modular source files (`0-*.md`, `1-*.md`, etc.) + bash compilation scripts that concatenate and deploy.
**Trade-off**: Extra build step after editing source files, but enables per-section editing, multi-target output (Claude, Gemini), and clean separation of concerns.

---

## Additional Resources

- **[ARCHITECTURE.md](ARCHITECTURE.md)** — File structure, loading flow, 5-layer memory details, coding overlay
- **[SETUP.md](SETUP.md)** — Environment configuration and creating new agents
- **[MCP.md](MCP.md)** — Connect agents to databases, APIs, and tools via MCP
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — How to contribute to the shared framework
- **[docs/document-quality-standard.md](docs/document-quality-standard.md)** — Lean/clear/precise/self-contained rules for writing & reviewing framework prose
