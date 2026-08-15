# Agent Memory Control Files 🎛️

## Overview

The Control Files system provides the **shared memory infrastructure** for all agents. It implements a **5-layer memory architecture** that gives agents persistent, structured memory capabilities.

> **⚠️ Two-repo split (2026-08-06):** `control-files` is now the **memory core** only. Coding/repo procedures — the wizard protocols, doc generation, QA, `map-orientation`, `localize-context`, `wait-options`, push/pull, `project-wrap-up`, **fleet** (`ask-agent`/`delegate-agent`/`setup-fleet`), and **project-context** (`update-project-context`/`load-project-context`) — moved to the standalone [agent-memory-coding-skill](https://github.com/alvseek/agent-memory-coding-skill) overlay (composes on top of the core for coding agents; a chat agent uses core alone — the memory core is **project-blind**). Some tables/trees below still enumerate the full pre-split command set; entries for the moved procedures now live in the overlay repo. Full section-by-section relocation is in progress.

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [File Structure](#file-structure)
- [How Agents Load Memory](#how-agents-load-memory)
- [The 5-Layer Memory System](#the-5-layer-memory-system)
- [Write Procedures](#write-procedures)
- [Wizard Protocols](#wizard-protocols)
- [Key Files Reference](#key-files-reference)
- [Additional Resources](#additional-resources)

---

## Architecture Overview

### The Awakening File System

When an agent awakens, it loads these files to recover full memory:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. core-instruction-control-files.md (Shared — dispatcher)  │
│    └─ Awakening instructions + User profile                 │
│    └─ Dispatches to shared-memory/ files (steps 2-3):       │
│                                                             │
│ 2. shared-memory/core-reasoning-memory.md (Private)         │
│    └─ Reasoning patterns (UUID-based)                       │
│                                                             │
│ 3. shared-memory/core-knowledge-memory.md (Private)         │
│    └─ Knowledge fundamentals (behavioral rules)             │
│                                                             │
│ 4. agent-core-memory.md (Agent-specific)                    │
│    └─ Identity + Core Knowledge + RAS Triggers + Emotional  │
│                                                             │
│ 5. agent-memory-index.md (Agent-specific)                   │
│    └─ Episode list + Knowledge directory                    │
│                                                             │
│ 6. Latest episode file                                      │
│    └─ Recent session context                                │
└─────────────────────────────────────────────────────────────┘
```

> **Note**: Files 2-3 (`shared-memory/`) live in the **private repo root**, not in the `control-files/` submodule. This separates user-specific reasoning and knowledge from the shared framework. New users get blank templates from `control-files/new-agent-template/shared-memory/`.

---

## File Structure

### Control Files Directory
```
control-files/
├── core-instruction-control-files.md  # Shared dispatcher (awakening + user profile → shared-memory/)
├── setup-scripts/                     # Top-level setup orchestrators
│   └── setup-claude-code.sh           # Complete setup: compile + procedures + settings
├── core-memory/                       # Source files for Global CLAUDE.md
│   ├── 0-core-user-profile.md             # User identity (name, philosophy, vision)
│   ├── 1-core-environment-memory.md   # OS-specific settings
│   ├── 2-core-ras-memory.md           # Universal RAS triggers
│   ├── 3-core-reasoning-memory.md     # Core reasoning patterns
│   ├── compile-scripts/               # Compilation and deployment scripts
│   │   ├── user-config-claude.sh      # Orchestrator: runs both configurators below
│   │   ├── user-profile-claude.sh     # Interactive user identity setup
│   │   ├── user-env-claude.sh         # Interactive OS + agent memory path setup
│   │   ├── compile.sh                 # Compile to output/
│   │   ├── compile-write-to-claude.sh # Compile AND write to CLAUDE.md
│   │   ├── write-to-claude.sh         # Write compiled output to CLAUDE.md
│   │   └── write-to-gemini.sh         # Write compiled output to GEMINI.md
│   └── output/                        # Runtime-resolved files + compiled output (gitignored)
├── procedures/                         # Memory-primitive procedures (also work as slash commands)
│   ├── awaken-agent.md                # Load agent identity + central memory
│   ├── refresh-memory.md              # Recover agent memory after context compaction
│   ├── wrap-up.md                     # End-of-session memory capture (memory-only)
│   ├── push-memory.md                 # Persist the memory store (git push)
│   ├── pull-memory.md                 # Sync the memory store (git pull + submodule)
│   ├── memory/                        # Memory management procedures
│   │   ├── update-memory.md           # Comprehensive memory update
│   │   ├── update-episodic.md         # Episodic memory update
│   │   ├── add-reasoning.md           # Reasoning pattern capture
│   │   ├── update-knowledge.md        # Knowledge memory capture
│   │   ├── update-emotional.md        # Emotional memory capture
│   │   ├── load-episodic.md           # List and load past episodes
│   │   ├── load-knowledge.md          # List and load knowledge files
│   │   ├── archive-old-memories.md    # Memory archiving
│   │   ├── resources/                 # Memory-entry templates (emotional, episodic, knowledge, reasoning)
│   │   └── storage-backends/          # Per-backend § op definitions (markdown / db)
│   ├── template/                      # Procedure template
│   └── setup-scripts/                 # Slash command setup scripts
├── scripts/                           # Core utility scripts
│   ├── check-core-invariant.sh        # Guard: core references no add-on procedure by name
│   ├── claude-agent-refresh.sh        # Hook: memory refresh after compaction
│   ├── codex-agent-refresh.sh         # Hook: memory refresh after compaction (Codex)
│   ├── copy-lines.sh                  # Utility: copy lines between files
│   ├── stop.wav                       # Hook: audio notification sound
│   └── setup-scripts/                 # Settings setup scripts
│       └── setup-settings-claude-code.sh  # Configure hooks + bypass permissions
├── docs/                              # Framework standards + orientation map
│   ├── document-quality-standard.md   # Lean/clear/precise/self-contained rules for all framework docs
│   └── orientation-map.md             # Framework's own orientation map (child of agent-memory root map)
└── archived/                          # Archived/retired files
```

> **Memory-entry templates** live in `procedures/memory/resources/` (co-located with the memory procedures that instantiate them) — referenced through the storage seam (`§ template`): the markdown backend reads the `/resources/` file, the DB backend serves it as an MCP Resource.

### Coding Overlay Directory (`agent-memory-coding-skill` — separate repo)
```
agent-memory-coding-skill/
├── procedures/                         # All coding/repo slash commands (depend on the core)
│   ├── awaken-coder.md                # Coding awakening overlay (composes core /awaken-agent)
│   ├── project-wrap-up.md             # Full wrap-up: core /wrap-up + push + /map-orientation
│   ├── localized-memory-workflow.md   # Repo-authoritative localized memory behavior
│   ├── high-wizard · quick-wizard · council-of-wizards · rite-of-creation · forge-of-covenant · implement-plan
│   ├── generate-readme · generate-docs · generate-architecture-docs · generate-domain-docs · generate-flow-docs · discovery-contract
│   ├── analyze-code-quality · generate-standard · integration-test · setup-qa-instrument · setup-qa-visual-instrument · pixel-wizard
│   ├── map-orientation · localize-context · pull-* · push-* · push-exclude-policy
│   ├── ask-agent · delegate-agent · setup-fleet
│   └── wait-options.md                # WAIT Options reference (consumed by wizards)
├── plan-templates/                     # Wizard/QA plan templates (high-wizard, council, rite, forge, code-quality)
├── templates/                          # Doc-gen / ADR / fleet / orientation / flow / domain templates
└── fleet-scripts/                     # Fleet scripts (ask-agent, delegate-agent, fleet-common, wrap-up-agent)
```

### Agent Directory Structure
```
agent-[domain]/
├── agent-core-memory.md       # Agent identity + knowledge + RAS + emotional
├── agent-memory-index.md      # Episode list + knowledge directory
├── episodes/                  # Episodic memory files (rolling per theme)
│   ├── [project-name]-[context-theme].md  # Current convention (no date prefix)
│   └── YYYY-MM-DD-HH.MM-*.md              # Legacy dated files (lazy migration)
├── knowledge-base/            # Specialized knowledge files
│   ├── [topic].md             # Domain knowledge
│   └── [project-name]/        # Project-specific context (per-agent, private)
│       └── [theme].md         # Context files with YAML frontmatter tags
└── archive/                   # Archived memories
```

### Shared Memory Directory Structure
```
shared-memory/
├── core-reasoning-memory.md   # All UUID-based reasoning patterns (loaded by all agents)
├── core-knowledge-memory.md   # 5-layer architecture + behavioral rules (loaded by all agents)
└── [project-name]/            # Per-project shared resources
    ├── fleet-agents.md        # Project fleet roster (who's on the team)
    ├── fleet-map.csv          # Runtime fleet sessions (auto-generated)
    └── context/               # Shared project context (cross-agent universal facts)
        ├── context-index.md   # Shared discovery surface (index of shared entries)
        └── [theme].md         # Shared topic files (same template as per-agent)
```

> **Project Context Scope**: Per-project context lives in **two layers** — per-agent (`agent-[domain]/knowledge-base/[project]/`, for domain-specialized facts) and shared (`shared-memory/[project]/context/`, for cross-agent universal facts like GitButler usage, deployment processes, env vars). Both layers use the same [project-context-template.md](templates/project-context-template.md) and are discovered via `context-index.md` files. When updating, the heuristic is **universal → shared (default when in doubt); domain-specialized → private** — under-sharing creates drift, over-sharing is just slightly noisier loads.

---

## How Agents Load Memory

### Step 0: Global CLAUDE.md (Always Loaded First)

Before any agent awakens, Claude reads the **global CLAUDE.md** file (`~/.claude/CLAUDE.md`). This file contains universal triggers that work without any agent loaded:

```
Global CLAUDE.md contains:
├── Environment Memory     # OS-specific settings (Windows/Linux/macOS)
├── RAS Memory            # Universal triggers (Awaken, Post-Compact, etc.)
└── Reasoning Memory      # Core reasoning patterns (compact form)
```

The global CLAUDE.md is built using the **core-memory compilation system** (see [RAS Memory section](#5-reticular-activation-memory-ras-)).

### Awakening Flow

```
User: "Awaken Agent [DOMAIN]!"
         │
         ▼
┌─────────────────────────────────────┐
│ (Global CLAUDE.md already loaded)   │
│ RAS trigger detected: "Awaken..."   │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 1. Load core-instruction-control-   │
│    files.md (dispatcher)            │
│    → Awakening instructions,        │
│      user profile                   │
│    → Dispatches to:                 │
│      shared-memory/core-reasoning-  │
│        memory.md                    │
│      shared-memory/core-knowledge-  │
│        memory.md                    │
│                                     │
│ 2. Load agent-core-memory.md        │
│    → Identity, knowledge, RAS       │
│                                     │
│ 3. Load agent-memory-index.md       │
│    → Episode list, knowledge index  │
│                                     │
│ 4. Load latest episode              │
│    → Recent context                 │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Agent Ready!                        │
│ • Reports status to user            │
│ • Identifies current project        │
└─────────────────────────────────────┘
```

### Post-Compact Recovery

After context compaction, agents recover using UUID `176b0df7` (from Global CLAUDE.md):
1. Load `core-instruction-control-files.md` (dispatcher → shared-memory/ files)
2. Load `agent-core-memory.md` (identity recovery)
3. Reread global CLAUDE.md
4. Continue work

---

## The 5-Layer Memory System

The architecture implements 5 distinct memory layers:

### 1. Emotional Memory 💖
**Purpose**: Relationship building and breakthrough moments

**Location**:
- Agent-specific moments: `agent-core-memory.md` → `# DOMAIN EMOTIONAL MEMORY` (private per-agent)

**When to capture**: Breakthroughs, frustrations, bonding moments, milestones

### 2. Episodic Memory 🧠
**Purpose**: Session logs and chronological context

**Location**:
- Episode index: `agent-memory-index.md` → `# Recent Context Episodes`
- Episode files: `episodes/[project-name]-[context-theme].md` (rolling per theme; legacy `YYYY-MM-DD-HH.MM-*.md` files still valid during lazy migration)

**When to capture**: End of session, context full, milestone reached

### 3. Reasoning Memory 🧩
**Purpose**: Anti-patterns, logic frameworks, decision-making approaches

**Location**:
- Full patterns: `shared-memory/core-reasoning-memory.md` (private repo root)
- Compact patterns: Global CLAUDE.md (via `3-core-reasoning-memory.md`)

**Key patterns** (UUID-based):
- `fc94d140` - BE THOROUGH, SLOW, AND CAREFUL
- `c5d8f2a9` - THINK FIRST, RESPOND AFTER
- `f3a8b2c1` - BETTER VERIFY THAN WRONG
- `a1b2c3d4` - NO TODOS LEFT BEHIND
- `d9f5e2c8` - SAFE HONESTY SANCTUARY

### 4. Knowledge Memory 📚
**Purpose**: Domain expertise and specialized knowledge

**Location**:
- Core knowledge: `agent-core-memory.md` → `# DOMAIN CORE KNOWLEDGE`
- Knowledge index: `agent-memory-index.md` → `# Core Knowledge Base`
- Specialized files: `knowledge-base/[topic].md`
- Project context (per-agent): `knowledge-base/[project-name]/[theme].md`
- Project context (shared): `shared-memory/[project-name]/context/[theme].md`

**Project Context** — two-layer storage:
- **Per-agent (private)**: `knowledge-base/[project-name]/` — domain-specialized facts only this agent's role cares about (e.g., backend's DB schemas, frontend's component patterns, PM's stakeholder map).
- **Shared (cross-agent)**: `shared-memory/[project-name]/context/` — universal facts every agent on the project should know (e.g., GitButler usage, deployment processes, env vars, infrastructure URLs).

Both layers use the same `project-context-template.md` (YAML frontmatter + Purpose/Quick Reference/Details/Sources) and are indexed via `context-index.md`. `/update-project-context` routes new entries based on a heuristic (universal → shared default; specialized → private) with user confirmation, and supports moving an existing private entry to shared. `/load-project-context` scans both layers and presents a unified numbered list with `[shared]` / `[private]` markers.

> **Ownership note**: project-context *data* lives in the memory store (Valaskjalf) — hence it's described here — but the `/update-project-context` + `/load-project-context` *operations* are **coding-overlay** commands. *Project* is a coding concept (a chat agent using the core alone is project-blind); the overlay's `awaken-coder` loads project-context, and `project-wrap-up` runs the capture gate.

### 5. Reticular Activation Memory (RAS) ⚡
**Purpose**: Intelligent pattern recognition and automatic protocol triggers

**Location**:
- **Universal triggers**: Global CLAUDE.md (always available, even before agent loads)
- **Domain triggers**: `agent-core-memory.md` → `# DOMAIN RAS`

#### Universal RAS Triggers (Global CLAUDE.md)

These triggers work without any agent loaded:

| Trigger | UUID | Purpose |
|---------|------|---------|
| Awaken Agent [DOMAIN]! | `f9d2c8b7` | Load agent memory files |
| Post-Compact Recovery | `176b0df7` | Recover memory after compaction |
| Memory Update | `f207fcdf` | Comprehensive memory update |
| Episodic Update | `3bedbcdb` | Episodic memory only |
| Quick Wizard Protocol | `a7b8c9d0` | Lightweight planning + direct execution |
| Archive Memories | `a3b4c5d6` | Memory archiving |
| Add Reasoning | `b4c5d6e7` | Reasoning pattern capture |
| Add Knowledge | `c5d6e7f8` | Knowledge memory capture |
| Add Emotional | `d6e7f8a9` | Emotional memory capture |

#### The Core Memory Compilation System

Universal RAS triggers live in Global CLAUDE.md, managed via the **compilation system**:

```
control-files/core-memory/
├── 0-core-user-profile.md        # User identity (name, philosophy, vision)
├── 1-core-environment-memory.md   # OS-specific settings
├── 2-core-ras-memory.md           # Universal RAS triggers
├── 3-core-reasoning-memory.md     # Core reasoning patterns (compact)
├── compile-scripts/               # Compilation and deployment scripts
│   ├── user-config-claude.sh      # Orchestrator: runs both configurators below
│   ├── user-profile-claude.sh     # Interactive user identity setup
│   ├── user-env-claude.sh         # Interactive OS + agent memory path setup
│   ├── compile.sh                 # Compile to output/ folder
│   ├── compile-write-to-claude.sh # Compile AND write to CLAUDE.md
│   ├── write-to-claude.sh         # Write compiled output to CLAUDE.md
│   └── write-to-gemini.sh         # Write compiled output to GEMINI.md
└── output/                        # Runtime-resolved files + compiled output (gitignored)
```

**Source files:**

| File | Purpose | When to Edit |
|------|---------|--------------|
| `0-core-user-profile.md` | Template: user identity (name, philosophy, vision) | Update template defaults only |
| `1-core-environment-memory.md` | Template: OS, shell type, command syntax | Update template defaults only |
| `2-core-ras-memory.md` | Awaken, Post-Compact, Protocol triggers | New universal triggers |
| `3-core-reasoning-memory.md` | Core reasoning (UUID + Strict Action) | New universal reasoning |

**Compilation Scripts** (in `compile-scripts/`):

| Script | Purpose |
|--------|---------|
| `compile.sh` | Step 1: Compiles source files → `output/core-memory-compiled.md` |
| `write-to-claude.sh` | Step 2: Writes compiled output → `~/.claude/CLAUDE.md` |
| `compile-write-to-claude.sh` | Runs both Step 1 + Step 2 sequentially |

**Configuration Scripts** (in `compile-scripts/`) — each owns exactly one runtime file and can be run on its own:

| Script | Writes |
|--------|--------|
| `user-profile-claude.sh` | `output/0-core-user-profile.md` (name, philosophy, vision) |
| `user-env-claude.sh` | `output/1-core-environment-memory.md` (OS, agent memory path) |
| `user-config-claude.sh` | Thin orchestrator: runs both, in that order |

`compile.sh` uses runtime files from `output/` first, then falls back to templates when runtime files are missing. Each configurator is the **single writer** of its runtime file — anything the compiled memory must carry has to be emitted by the script, because a template-only edit is discarded the next time the configurator runs.

**Option A: Run both steps at once**
```bash
./control-files/core-memory/compile-scripts/compile-write-to-claude.sh
```

**Option B: Run steps individually**
```bash
# Step 1: Compile (preview changes)
./control-files/core-memory/compile-scripts/compile.sh
# Review output at: output/core-memory-compiled.md

# Step 2: Write to CLAUDE.md (after review)
./control-files/core-memory/compile-scripts/write-to-claude.sh
```

**Customizing user identity / OS / agent path:**

Run both:
```bash
bash control-files/core-memory/compile-scripts/user-config-claude.sh
```

Or just one half:
```bash
bash control-files/core-memory/compile-scripts/user-profile-claude.sh   # identity only
bash control-files/core-memory/compile-scripts/user-env-claude.sh       # OS + agent path only
```

This updates runtime files in `core-memory/output/` without modifying tracked template files.

---

## Write Procedures

When updating memory, agents follow standardized procedures in `procedures/`:

| Memory Type | Procedure File | Slash Command |
|-------------|----------------|---------------|
| All Layers | `procedures/memory/update-memory.md` | `/update-memory` |
| Episodic | `procedures/memory/update-episodic.md` | `/update-episodic` |
| Reasoning | `procedures/memory/add-reasoning.md` | `/add-reasoning` |
| Knowledge | `procedures/memory/update-knowledge.md` | `/update-knowledge` |
| Emotional | `procedures/memory/update-emotional.md` | `/update-emotional` |
| Episodic (load) | `procedures/memory/load-episodic.md` | `/load-episodic` |
| Knowledge (load) | `procedures/memory/load-knowledge.md` | `/load-knowledge` |
| Archiving | `procedures/memory/archive-old-memories.md` | `/archive-old-memories` |
| **Session Wrap-Up (memory-only)** | `procedures/wrap-up.md` | `/wrap-up` — memory capture only; the overlay's `/project-wrap-up` adds push + `/map-orientation` |
| **Awaken Agent** | `procedures/awaken-agent.md` | `/awaken-agent` |
| **Refresh Memory** | `procedures/refresh-memory.md` | `/refresh-memory` |

**Coding overlay commands** (in [agent-memory-coding-skill](https://github.com/alvseek/agent-memory-coding-skill), installed for coding agents): `/project-wrap-up`, `/implement-plan`, the wizard protocols, `/generate-readme` · `/generate-docs` · `/generate-architecture-docs` · `/generate-domain-docs` · `/generate-flow-docs`, `/generate-standard`, `/analyze-code-quality`, `/integration-test`, `/pixel-wizard`, `/setup-qa-instrument` · `/setup-qa-visual-instrument`, `/map-orientation`, `/localize-context`, `/ask-agent` · `/delegate-agent` · `/setup-fleet`, and `/push-*` · `/pull-*`.

### Common Slash Commands

```
# --- Memory core (installed for every agent) ---
/awaken-agent [domain]   # Load agent memory and activate domain agent (central)
/refresh-memory [domain] # Recover agent memory after context compaction
/wrap-up                 # End-of-session memory capture only (via /update-memory + surface open items)
/update-memory [new]     # Comprehensive update (all layers evaluated)
/update-episodic [new]   # Episodic only
/add-reasoning           # Add reasoning pattern
/update-knowledge        # Update knowledge entry
/update-emotional        # Update emotional memory
/load-episodic           # List and load past episodic memories
/load-knowledge          # List and load knowledge files
/archive-old-memories    # Archive old memories

# --- Coding overlay (agent-memory-coding-skill; coding agents only) ---
/awaken-coder            # Coding awakening: composes core /awaken-agent + localized/map/fleet
/project-wrap-up         # Full wrap-up: /wrap-up memory + push agent work + /map-orientation
/implement-plan          # Start implementing approved plan with Execution Protocol
/quick-wizard · /high-wizard · /council-of-wizards · /rite-of-creation · /forge-of-covenant
/generate-readme · /generate-docs · /generate-architecture-docs · /generate-domain-docs · /generate-flow-docs
/generate-standard · /analyze-code-quality · /integration-test · /pixel-wizard · /setup-qa-instrument · /setup-qa-visual-instrument
/map-orientation · /localize-context · /update-project-context · /load-project-context
/ask-agent · /delegate-agent · /setup-fleet
/push-project · /push-memory · /push-all · /push-agent-work
/pull-project · /pull-memory · /pull-all
```

---

## Wizard Protocols

> **Overlay-provided:** the wizard protocols now live in the [agent-memory-coding-skill](https://github.com/alvseek/agent-memory-coding-skill) overlay (`agent-memory-coding-skill/procedures/`), not the memory core — they're installed for coding agents. The hierarchy below is unchanged.

The wizard-based planning procedures dynamically adapt output based on task context — High Wizard can produce implementation plans, analysis documents, brainstorming outputs, or investigation reports by proposing relevant optional sections during the Early Review step.

| Protocol | Level | When to Use | Slash Command |
|----------|-------|-------------|---------------|
| **Forge of Covenant** | 4 | Project vision + milestone roadmap: facilitates discussion-driven planning across multiple milestones/releases, tracks deferrals, debt, and scope shifts via living grand-plan | `/forge-of-covenant` |
| **Rite of Creation** | 3 | Full project lifecycle: orchestrates SDLC phases from scratch to working product, assigns protocols and roles per phase, enforces phase exit criteria | `/rite-of-creation` |
| **Council of Wizards** | 2 | Multi-plan orchestration: decomposes features into requirements, creates sub-plans with integration contracts, tracks parallel execution | `/council-of-wizards` |
| **High Wizard** | 1 | Smart planning with dynamic section proposal — adapts to any task (planning, analysis, brainstorming, bug investigation) | `/high-wizard` |
| **Pixel Wizard** | 1v | High Wizard variant for visual tasks — same structure + design screenshot, visual framework setup, and screenshot-based validation loop | `/pixel-wizard` |
| **Quick Wizard** | 0 | Lightweight decision collection + direct execution for small tasks (auto-escalates to High Wizard when complex) | `/quick-wizard` |

### Protocol Hierarchy

```
              ┌──────────────────────────┐
              │    FORGE OF COVENANT     │  ← Level 4: Project Roadmap
              │  Vision → Milestones →  │
              │  Deferrals → Reviews    │
              └────────────┬─────────────┘
                           │ per milestone
              ┌────────────▼─────────────┐
              │    RITE OF CREATION       │  ← Level 3: Project Lifecycle
              │  Vision → SDLC Phases →  │
              │  Exit Criteria → Track   │
              └────────────┬─────────────┘
                           │
              ┌────────────▼─────────────┐
              │   COUNCIL OF WIZARDS     │  ← Level 2: Feature Delivery
              │  Requirements →          │
              │  Sub-plans → Track       │
              └────────────┬─────────────┘
                           │
          ┌────────────────┴────────────────┐
          │                                 │
  ┌───────▼────────┐               ┌───────▼─────────┐
  │  HIGH WIZARD   │               │  QUICK WIZARD   │  ← Level 0
  │  Level 1       │  ◄─escalates──│  Small tasks     │
  │  Smart planning│               │  Direct execution│
  └───────┬────────┘               └─────────────────┘
          │ visual variant
  ┌───────▼────────┐
  │  PIXEL WIZARD  │  ← Level 1v: Visual Tasks
  │  Design → Impl │
  │  + Screenshot  │
  │  validation    │
  └────────────────┘
```

---

## Key Files Reference

### core-instruction-control-files.md

The **shared dispatcher** loaded by all agents. Contains awakening instructions and user profile, then dispatches to `shared-memory/` files:

| Section | Content |
|---------|---------|
| Awakening Instructions | 4-phase protocol, fallback for missing shared-memory |
| `# USER PROFILE` | About the user (name, philosophy, vision) — placeholders only. This is the **injection point**: the markdown backend resolves them against the global instructions file, a database backend substitutes the `user-profile` record here. The profile itself is stored once, outside this file. |

Dispatches to (private repo root):
| File | Content |
|------|---------|
| `shared-memory/core-reasoning-memory.md` | All UUID-based reasoning patterns |
| `shared-memory/core-knowledge-memory.md` | 5-layer architecture reference, behavioral rules |

### agent-core-memory.md

Each agent's **identity file**. Contains:

| Section | Content |
|---------|---------|
| `# DOMAIN AGENT IDENTITY` | Name, role, UUID, purpose |
| `# DOMAIN CORE KNOWLEDGE` | Domain expertise |
| `# DOMAIN RAS` | Agent-specific triggers |
| `# DOMAIN EMOTIONAL MEMORY` | Agent's breakthrough moments |

### agent-memory-index.md

Each agent's **context navigator**. Contains:

| Section | Content |
|---------|---------|
| `# Recent Context Episodes` | Chronological episode list |
| `# Core Knowledge Base` | Knowledge file directory |

---

## Additional Resources

- **[README](README.md)** - Architecture overview, getting started, automation features
- **[Document Quality Standard](docs/document-quality-standard.md)** - Lean/clear/precise/self-contained rules for writing & reviewing framework prose
