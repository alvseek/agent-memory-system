# Agent Memory Control Files 🎛️

## Overview

The Control Files system provides the **shared memory infrastructure** for all agents. It implements a **5-layer memory architecture** that gives agents persistent, structured memory capabilities.

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

### The 4-File System

When an agent awakens, it loads **4 files** to recover full memory:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. core-instruction-control-files.md (Shared)               │
│    └─ User profile + Reasoning patterns + Knowledge basics   │
│                                                             │
│ 2. agent-core-memory.md (Agent-specific)                    │
│    └─ Identity + Core Knowledge + RAS Triggers + Emotional  │
│                                                             │
│ 3. agent-memory-index.md (Agent-specific)                   │
│    └─ Episode list + Knowledge directory                    │
│                                                             │
│ 4. Latest episode file                                      │
│    └─ Recent session context                                │
└─────────────────────────────────────────────────────────────┘
```

---

## File Structure

### Control Files Directory
```
control-files/
├── core-instruction-control-files.md  # Shared control file (all agents use this)
├── setup-scripts/                     # Top-level setup orchestrators
│   └── setup-claude-code.sh           # Complete setup: compile + procedures + settings
├── core-memory/                       # Source files for Global CLAUDE.md
│   ├── 0-core-user-profile.md             # User identity (name, philosophy, vision)
│   ├── 1-core-environment-memory.md   # OS-specific settings
│   ├── 2-core-ras-memory.md           # Universal RAS triggers
│   ├── 3-core-reasoning-memory.md     # Core reasoning patterns
│   ├── compile-scripts/               # Compilation and deployment scripts
│   │   ├── user-config.sh             # Interactive user identity + OS setup
│   │   ├── compile.sh                 # Compile to output/
│   │   ├── compile-write-to-claude.sh # Compile AND write to CLAUDE.md
│   │   ├── write-to-claude.sh         # Write compiled output to CLAUDE.md
│   │   └── write-to-gemini.sh         # Write compiled output to GEMINI.md
│   └── output/                        # Compiled output (gitignored)
├── procedures/                         # Procedures (also work as slash commands)
│   ├── high-wizard.md                 # Smart planning with dynamic section proposal
│   ├── quick-wizard.md                # Lightweight decision collection + direct execution
│   ├── council-of-wizards.md          # Multi-plan orchestration (council of wizards)
│   ├── rite-of-creation.md            # Full project lifecycle orchestration (scratch to finish)
│   ├── awaken-agent.md                # Load agent memory and activate domain agent
│   ├── refresh-memory.md              # Recover agent memory after context compaction
│   ├── implement-plan.md             # Start implementing approved plan with Execution Protocol
│   ├── memory/                        # Memory management procedures
│   │   ├── update-memory.md           # Comprehensive memory update
│   │   ├── update-episodic.md         # Episodic memory update
│   │   ├── add-reasoning.md           # Reasoning pattern capture
│   │   ├── update-knowledge.md        # Knowledge memory capture
│   │   ├── update-emotional.md        # Emotional memory capture
│   │   ├── update-project-context.md  # Create/update project context
│   │   ├── load-project-context.md    # List and load project context
│   │   ├── load-episodic.md           # List and load past episodes
│   │   ├── load-knowledge.md          # List and load knowledge files
│   │   └── archive-old-memories.md    # Memory archiving
│   ├── template/                      # Procedure template
│   └── setup-scripts/                 # Slash command setup scripts
├── scripts/                           # Utility scripts
│   ├── claude-agent-refresh.sh        # Hook: memory refresh after compaction
│   ├── copy-lines.sh                  # Utility: copy lines between files
│   ├── stop.wav                       # Hook: audio notification sound
│   └── setup-scripts/                 # Settings setup scripts
│       └── setup-settings-claude-code.sh  # Configure hooks + bypass permissions
├── plan-templates/                    # Planning templates (used by procedures)
│   ├── high-wizard-plan-template.md
│   ├── council-of-wizards-plan-template.md
│   └── rite-of-creation-plan-template.md
├── archived/                          # Archived/retired files
└── templates/                         # Output templates (used by procedures)
```

### Agent Directory Structure
```
agent-[domain]/
├── agent-core-memory.md       # Agent identity + knowledge + RAS + emotional
├── agent-memory-index.md      # Episode list + knowledge directory
├── episodes/                  # Episodic memory files
│   └── YYYY-MM-DD-HH.MM-*.md
├── knowledge-base/            # Specialized knowledge files
│   ├── [topic].md             # Domain knowledge
│   └── [project-name]/        # Project-specific context (per-agent, private)
│       └── [theme].md         # Context files with YAML frontmatter tags
└── archive/                   # Archived memories
```

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
│    files.md (shared)                │
│    → Awakening instructions,        │
│      user profile, reasoning,       │
│      shared knowledge               │
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
1. Load `core-instruction-control-files.md` (shared foundations + awakening instructions)
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
- Episode files: `episodes/YYYY-MM-DD-HH.MM-*.md`

**When to capture**: End of session, context full, milestone reached

### 3. Reasoning Memory 🧩
**Purpose**: Anti-patterns, logic frameworks, decision-making approaches

**Location**:
- Full patterns: `core-instruction-control-files.md` → `# REASONING MEMORY`
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
- Project context: `knowledge-base/[project-name]/[theme].md`

**Project Context**: Agent-specific operational knowledge for projects (VM access, environment setup, deployment procedures, feature conventions). Each agent maintains its own project context — private and scoped to what that agent needs. Files use YAML frontmatter with tags for selective loading via `/load-project-context`. See `/update-project-context` to create and `/load-project-context` to retrieve.

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
│   ├── user-config.sh             # Interactive user identity + OS setup
│   ├── compile.sh                 # Compile to output/ folder
│   ├── compile-write-to-claude.sh # Compile AND write to CLAUDE.md
│   ├── write-to-claude.sh         # Write compiled output to CLAUDE.md
│   └── write-to-gemini.sh         # Write compiled output to GEMINI.md
└── output/                        # Compiled output (gitignored)
```

**Source files:**

| File | Purpose | When to Edit |
|------|---------|--------------|
| `0-core-user-profile.md` | User identity (name, philosophy, vision) | First-time setup via `user-config.sh` |
| `1-core-environment-memory.md` | OS, shell type, command syntax | Different OS or shell (set via `user-config.sh`) |
| `2-core-ras-memory.md` | Awaken, Post-Compact, Protocol triggers | New universal triggers |
| `3-core-reasoning-memory.md` | Core reasoning (UUID + Strict Action) | New universal reasoning |

**Compilation Scripts** (in `compile-scripts/`):

| Script | Purpose |
|--------|---------|
| `compile.sh` | Step 1: Compiles source files → `output/core-memory-compiled.md` |
| `write-to-claude.sh` | Step 2: Writes compiled output → `~/.claude/CLAUDE.md` |
| `compile-write-to-claude.sh` | Runs both Step 1 + Step 2 sequentially |

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

**Customizing for different OS:**

Edit `1-core-environment-memory.md` - it contains pre-built sections for Windows, Linux, and macOS. Simply:
1. Comment out the current OS section
2. Uncomment the section for your OS
3. Run the compilation scripts

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
| Project Context (update) | `procedures/memory/update-project-context.md` | `/update-project-context` |
| Project Context (load) | `procedures/memory/load-project-context.md` | `/load-project-context` |
| Episodic (load) | `procedures/memory/load-episodic.md` | `/load-episodic` |
| Knowledge (load) | `procedures/memory/load-knowledge.md` | `/load-knowledge` |
| Archiving | `procedures/memory/archive-old-memories.md` | `/archive-old-memories` |
| **Session Wrap-Up** | `procedures/wrap-up.md` | `/wrap-up` |
| **Awaken Agent** | `procedures/awaken-agent.md` | `/awaken-agent` |
| **Refresh Memory** | `procedures/refresh-memory.md` | `/refresh-memory` |
| **Implement Plan** | `procedures/implement-plan.md` | `/implement-plan` |
| **Push Project** | `procedures/push-project.md` | `/push-project` |
| **Push Memory** | `procedures/push-memory.md` | `/push-memory` |
| **Push All** | `procedures/push-all.md` | `/push-all` |
| **Pull Project** | `procedures/pull-project.md` | `/pull-project` |
| **Pull Memory** | `procedures/pull-memory.md` | `/pull-memory` |
| **Pull All** | `procedures/pull-all.md` | `/pull-all` |

### Common Slash Commands

```
/awaken-agent [domain]   # Load agent memory and activate domain agent
/refresh-memory [domain] # Recover agent memory after context compaction
/rite-of-creation        # Full project lifecycle (vision → SDLC phases → exit criteria → execution)
/council-of-wizards      # Multi-plan orchestration (requirements → sub-plans → parallel execution)
/implement-plan          # Start implementing approved plan with Execution Protocol
/wrap-up                 # End-of-session: save episodic + auto-detect project context + push all
/update-memory [new]     # Comprehensive update (all layers evaluated)
/update-episodic [new]   # Episodic only
/add-reasoning           # Add reasoning pattern
/update-knowledge        # Update knowledge entry
/update-project-context  # Create/update project-specific context
/load-project-context    # List and load project context files
/load-episodic           # List and load past episodic memories
/load-knowledge          # List and load knowledge files
/archive-old-memories    # Archive old memories
/push-project            # Commit and push current project
/push-memory             # Commit and push agent memory
/push-all                # Commit and push both project + agent memory
/pull-project            # Pull latest for current project
/pull-memory             # Pull agent memory + update control-files submodule
/pull-all                # Pull both project + agent memory
```

---

## Wizard Protocols

The `procedures/` directory contains wizard-based planning procedures. High Wizard dynamically adapts its output based on task context — it can produce implementation plans, analysis documents, brainstorming outputs, or investigation reports by proposing relevant optional sections during the Early Review step.

| Protocol | Level | When to Use | Slash Command |
|----------|-------|-------------|---------------|
| **Rite of Creation** | 3 | Full project lifecycle: orchestrates SDLC phases from scratch to working product, assigns protocols and roles per phase, enforces phase exit criteria | `/rite-of-creation` |
| **Council of Wizards** | 2 | Multi-plan orchestration: decomposes features into requirements, creates sub-plans with integration contracts, tracks parallel execution | `/council-of-wizards` |
| **High Wizard** | 1 | Smart planning with dynamic section proposal — adapts to any task (planning, analysis, brainstorming, bug investigation) | `/high-wizard` |
| **Quick Wizard** | 0 | Lightweight decision collection + direct execution for small tasks (auto-escalates to High Wizard when complex) | `/quick-wizard` |

### Protocol Hierarchy

```
              ┌──────────────────────────┐
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
  └────────────────┘               └─────────────────┘
```

---

## Key Files Reference

### core-instruction-control-files.md

The **shared control file** loaded by all agents. Contains:

| Section | Content |
|---------|---------|
| `# USER PROFILE` | About the user (philosophy, vision) |
| `# REASONING MEMORY` | All UUID-based reasoning patterns |
| `# KNOWLEDGE MEMORY` | 5-layer architecture reference, markdown standards |

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
