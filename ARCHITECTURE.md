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
│ 1. agent-core-memory.md (Agent-specific)                    │
│    └─ Identity + Core Knowledge + RAS Triggers + Emotional  │
│                                                             │
│ 2. agent-memory-index.md (Agent-specific)                   │
│    └─ Episode list + Knowledge directory                    │
│                                                             │
│ 3. core-instruction-control-files.md (Shared)               │
│    └─ About the user + Reasoning patterns + Knowledge basics │
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
├── core-memory/                       # Source files for Global CLAUDE.md
│   ├── 1-core-environment-memory.md   # OS-specific settings
│   ├── 2-core-ras-memory.md           # Universal RAS triggers
│   ├── 3-core-reasoning-memory.md     # Core reasoning patterns
│   ├── compile.sh                     # Compile to compiled/
│   └── compile-write-to-claude.sh     # Compile AND write to CLAUDE.md
├── procedure/                         # 🔥 Procedures (also work as slash commands)
│   ├── high-wizard.md                 # Smart planning with dynamic section proposal
│   ├── quick-wizard.md                # Lightweight decision collection + direct execution
│   ├── wide-ocean.md                  # Multi-plan coordination
│   ├── memory/                        # Memory management procedures
│   │   ├── update-memory.md           # Comprehensive memory update
│   │   ├── update-episodic.md         # Episodic memory update
│   │   ├── add-reasoning.md           # Reasoning pattern capture
│   │   ├── add-knowledge.md           # Knowledge memory capture
│   │   ├── add-emotional.md           # Emotional memory capture
│   │   └── archive-memories.md        # Memory archiving
│   ├── template/                      # Procedure template
│   └── install-scripts/               # Slash command installers
├── plans/                             # Planning templates (used by procedures)
│   └── [templates: *-template.md]
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
│   └── [topic].md
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
│ 1. Load agent-core-memory.md        │
│    → Identity, knowledge, RAS       │
│                                     │
│ 2. Load agent-memory-index.md       │
│    → Episode list, knowledge index  │
│                                     │
│ 3. Load core-instruction-control-   │
│    files.md (shared)                │
│    → Reasoning patterns, basics     │
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
1. Load `agent-core-memory.md` (identity recovery)
2. Load `core-instruction-control-files.md` (reasoning patterns)
3. Reread global CLAUDE.md
4. Continue work

---

## The 5-Layer Memory System

The architecture implements 5 distinct memory layers:

### 1. Emotional Memory 💖
**Purpose**: Relationship building and breakthrough moments

**Location**:
- Agent-specific moments: `agent-core-memory.md` → `# DOMAIN EMOTIONAL MEMORY`
- About the user: `core-instruction-control-files.md` → `# EMOTIONAL MEMORY`

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
| Wide Ocean Protocol | `b4f7a2e9` | Master coordinator for 3-5 sub-plans |
| Deep Trench Protocol | `e2709f48` | Comprehensive planning |
| Shallow Shore Protocol | `27602fae` | Quick planning |
| Quick Surf Protocol | `6e1343e7` | Scope validation |
| Vote Protocol | `a8c3f5e2` | Multi-agent voting |

#### The Core Memory Compilation System

Universal RAS triggers live in Global CLAUDE.md, managed via the **compilation system**:

```
control-files/core-memory/
├── 1-core-environment-memory.md   # OS-specific settings
├── 2-core-ras-memory.md           # Universal RAS triggers
├── 3-core-reasoning-memory.md     # Core reasoning patterns (compact)
├── compile.sh                     # Compile to compiled/ folder
└── compile-write-to-claude.sh     # Compile AND write to CLAUDE.md
```

**Source files:**

| File | Purpose | When to Edit |
|------|---------|--------------|
| `1-core-environment-memory.md` | OS, shell type, command syntax | Different OS or shell |
| `2-core-ras-memory.md` | Awaken, Post-Compact, Protocol triggers | New universal triggers |
| `3-core-reasoning-memory.md` | Core reasoning (UUID + Strict Action) | New universal reasoning |

**Compilation Scripts:**

| Script | Purpose |
|--------|---------|
| `compile.sh` | Step 1: Compiles source files → `compiled/core-memory-compiled.md` |
| `compiled/write-to-claude.sh` | Step 2: Writes compiled output → `~/.claude/CLAUDE.md` |
| `compile-write-to-claude.sh` | Runs both Step 1 + Step 2 sequentially |

**Option A: Run both steps at once**
```bash
./control-files/core-memory/compile-write-to-claude.sh
```

**Option B: Run steps individually**
```bash
# Step 1: Compile (preview changes)
./control-files/core-memory/compile.sh
# Review output at: compiled/core-memory-compiled.md

# Step 2: Write to CLAUDE.md (after review)
./control-files/core-memory/compiled/write-to-claude.sh
```

**Customizing for different OS:**

Edit `1-core-environment-memory.md` - it contains pre-built sections for Windows, Linux, and macOS. Simply:
1. Comment out the current OS section
2. Uncomment the section for your OS
3. Run the compilation scripts

---

## Write Procedures

When updating memory, agents follow standardized procedures in `procedure/`:

| Memory Type | Procedure File | Slash Command |
|-------------|----------------|---------------|
| All Layers | `procedure/memory/update-memory.md` | `/update-memory` |
| Episodic | `procedure/memory/update-episodic.md` | `/update-episodic` |
| Reasoning | `procedure/memory/add-reasoning.md` | `/add-reasoning` |
| Knowledge | `procedure/memory/add-knowledge.md` | `/add-knowledge` |
| Emotional | `procedure/memory/add-emotional.md` | `/add-emotional` |
| Archiving | `procedure/memory/archive-memories.md` | `/archive-memories` |

### Common Slash Commands

```
/update-memory [new]     # Comprehensive update (all layers evaluated)
/update-episodic [new]   # Episodic only
/add-reasoning           # Add reasoning pattern
/add-knowledge           # Add knowledge entry
/archive-memories        # Archive old memories
```

---

## Wizard Protocols

The `procedure/` directory contains wizard-based planning procedures. High Wizard dynamically adapts its output based on task context — it can produce implementation plans, analysis documents, brainstorming outputs, or investigation reports by proposing relevant optional sections during the Early Review step.

| Protocol | When to Use | Slash Command |
|----------|-------------|---------------|
| **High Wizard** | Smart planning with dynamic section proposal — adapts to any task (planning, analysis, brainstorming, bug investigation) | `/high-wizard` |
| **Quick Wizard** | Lightweight decision collection + direct execution for small tasks (auto-escalates to High Wizard when complex) | `/quick-wizard` |
| **Wide Ocean** | Master coordinator for features requiring 3-5 separate sub-plans | `/wide-ocean` |

### Protocol Hierarchy

```
                    ┌─────────────────────┐
                    │     WIDE OCEAN      │  ← Master Coordinator
                    │  Coordinates 3-5    │
                    │    sub-plans        │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
      ┌───────▼───────┐                ┌────────▼────────┐
      │  HIGH WIZARD  │                │  QUICK WIZARD   │
      │ Smart planning │                │ Small tasks     │
      │ with dynamic   │  ◄─escalates── │ Direct execution│
      │ section proposal│                └─────────────────┘
      └────────────────┘
```

---

## Key Files Reference

### core-instruction-control-files.md

The **shared control file** loaded by all agents. Contains:

| Section | Content |
|---------|---------|
| `# EMOTIONAL MEMORY` | About the user (philosophy, vision) |
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
