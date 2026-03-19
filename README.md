# Agent Memory System

The shared control files for the [Agent Memory](https://github.com/alvseek/agent-memory) architecture — procedures, templates, and memory management instructions designed to be used as a **git submodule** inside your private agent-memory repository.

---

## Table of Contents

- [What Is This?](#what-is-this)
- [How Do I Set It Up?](#how-do-i-set-it-up)
- [How Do I Use It?](#how-do-i-use-it)
- [How Does It Work Inside?](#how-does-it-work-inside)
- [What Decisions Were Made?](#what-decisions-were-made)

---

## What Is This?

This submodule provides the shared infrastructure for the [5-layer agent memory system](https://github.com/alvseek/agent-memory): procedures that teach agents how to manage their own memory, planning protocols for structured work, templates for consistent output, and scripts for setup automation.

### Architecture

```
control-files/
├── core-instruction-control-files.md  # Shared reasoning & knowledge (loaded by all agents)
├── procedures/                         # 28 procedures (also work as slash commands)
│   ├── high-wizard.md                 # Smart planning
│   ├── quick-wizard.md                # Lightweight decisions
│   ├── council-of-wizards.md          # Multi-plan orchestration
│   ├── rite-of-creation.md            # Full project lifecycle
│   ├── forge-of-covenant.md           # Project vision + milestone roadmap
│   ├── awaken-agent.md                # Load agent memory
│   ├── refresh-memory.md              # Post-compaction recovery
│   ├── implement-plan.md              # Execute approved plans
│   ├── wrap-up.md                     # End-of-session save + push
│   └── memory/                        # Memory management (10 procedures)
├── plan-templates/                     # Planning templates (used by wizard protocols)
├── templates/                          # Output templates (readme, etc.)
├── new-agent-template/                 # Starter template for new agents
├── core-memory/                        # Source files for Global CLAUDE.md compilation
├── scripts/                            # Utility scripts (hooks, copy-lines)
└── setup-scripts/                      # Top-level setup orchestrators
```

For the complete file tree and agent directory structure, see [ARCHITECTURE.md](ARCHITECTURE.md).

### Tech Stack

- **Scripts**: Bash (cross-platform via Git Bash on Windows)
- **Content**: Markdown with YAML frontmatter (for knowledge base tagging)
- **Integration**: Claude Code slash commands and hooks

---

## How Do I Set It Up?

### As Part of Agent Memory

If you cloned the [agent-memory](https://github.com/alvseek/agent-memory) template, the setup script handles everything:

```bash
bash control-files/setup-scripts/setup-claude-code.sh
```

This runs 4 steps: user config → compile CLAUDE.md → install slash commands → configure settings.

For detailed setup options and manual alternatives, see the [Setup Guide](SETUP.md).

### Updating the Submodule

Pull the latest control-files updates:

```bash
cd control-files && git pull origin master && cd ..
git add control-files && git commit -m "chore: bump control-files submodule"
```

Or use the built-in command: `/pull-memory`

---

## How Do I Use It?

### Wizard Protocols

Planning protocols for structured work, from quick decisions to full project lifecycles:

| Protocol | Level | When to Use | Command |
|----------|-------|-------------|---------|
| **Quick Wizard** | 0 | Small tasks, lightweight decisions | `/quick-wizard` |
| **High Wizard** | 1 | Smart planning, adapts to any task | `/high-wizard` |
| **Council of Wizards** | 2 | Multi-plan orchestration | `/council-of-wizards` |
| **Rite of Creation** | 3 | Full project lifecycle | `/rite-of-creation` |
| **Forge of Covenant** | 4 | Project vision + milestone roadmap | `/forge-of-covenant` |

Quick Wizard auto-escalates to High Wizard when the task is too complex. Higher-level protocols delegate individual plans to High Wizard or Quick Wizard for execution.

### Memory Procedures

| Command | Purpose |
|---------|---------|
| `/update-memory` | Comprehensive update (all layers evaluated) |
| `/update-episodic` | Session log only |
| `/add-reasoning` | Reasoning pattern capture |
| `/update-knowledge` | Knowledge entry capture |
| `/update-emotional` | Emotional memory capture |
| `/update-project-context` | Create/update project-specific context |
| `/load-project-context` | Browse and load project context files |
| `/load-episodic` | Browse and load past episodic memories |
| `/load-knowledge` | Browse and load knowledge base files |
| `/archive-old-memories` | Archive old memories with evaluation |

### Operational Commands

| Command | Purpose |
|---------|---------|
| `/awaken-agent [domain]` | Load agent memory and activate |
| `/refresh-memory [domain]` | Recover memory after context compaction |
| `/implement-plan` | Start implementing an approved plan |
| `/wrap-up` | End-of-session: save episodic + auto-detect project context + push all |
| `/push-project` | Commit and push current project |
| `/push-memory` | Commit and push agent memory |
| `/push-all` | Push both project + agent memory |
| `/pull-project` | Pull latest for current project |
| `/pull-memory` | Pull agent memory + update submodule |
| `/pull-all` | Pull both project + agent memory |

### Generation & Quality Commands

| Command | Purpose |
|---------|---------|
| `/generate-readme [path]` | Generate 7Q README from codebase investigation |
| `/generate-standard [path]` | Generate project `quality-standard.md` from codebase conventions |
| `/analyze-code-quality [scope]` | Standalone code quality analysis (8 dimensions + project standard) |

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
| Awakening Instructions | 4-phase protocol for agent startup |
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

For the complete loading flow, memory layer details, and wizard protocol hierarchy, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## What Decisions Were Made?

### Procedures as Slash Commands

**Context**: Memory update procedures needed to be easily executable during sessions without remembering file paths.
**Decision**: Every procedure file doubles as a slash command — same file, installed to `~/.claude/commands/`.
**Trade-off**: Procedure files must follow Claude Code's command format, but eliminates duplication between docs and automation.

### Core Memory Compilation

**Context**: Global CLAUDE.md needs to combine user identity, RAS triggers, and reasoning patterns from separate source files for maintainability.
**Decision**: Modular source files (`0-*.md`, `1-*.md`, etc.) + bash compilation scripts that concatenate and deploy.
**Trade-off**: Extra build step after editing source files, but enables per-section editing, multi-target output (Claude, Gemini), and clean separation of concerns.

### Wizard Protocol Hierarchy

**Context**: Different tasks need different levels of planning rigor — from quick fixes to full project lifecycles.
**Decision**: 4-level wizard hierarchy (Quick → High → Council → Rite) with automatic escalation from lower to higher levels.
**Trade-off**: More procedures to maintain, but each level is focused and appropriately scoped. Quick Wizard handles 80% of tasks; higher levels exist for when they're genuinely needed.

---

## Additional Resources

- **[ARCHITECTURE.md](ARCHITECTURE.md)** — File structure, loading flow, 5-layer memory details, wizard protocol hierarchy
- **[SETUP.md](SETUP.md)** — Environment configuration and creating new agents
- **[MCP.md](MCP.md)** — Connect agents to databases, APIs, and tools via MCP
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — How to contribute to the shared framework
