# Agent Memory System

A **5-layer memory architecture** for building AI agents (Based on Claude Code) with persistent memory across sessions. Agents remember past work, learn from mistakes, and grow their expertise over time.

This repository contains the **shared control files** — procedures, templates, and memory management instructions — designed to be used as a **git submodule** inside your private agent memory repository.

## Table of Contents
- [Repository Design](#repository-design)
- [Getting Started](#getting-started)
- [Architecture Overview](#architecture-overview)
- [Environment Setup](#environment-setup)
- [Creating New Agents](#creating-new-agents)
- [Understanding Control Files](#understanding-control-files)
- [Automation Features](#automation-features)
- [Agent Management](#agent-management)
- [Using the Meta Agent](#using-the-meta-agent)
- [Additional Resources](#additional-resources)

## Repository Design

This project uses a **dual-repository pattern** that separates shared tools from private agent data:

```
agent-memory/                       ← Private repo (your agent data)
├── control-files/                  ← THIS repo (public git submodule)
│   ├── core-instruction-control-files.md   # Shared reasoning & knowledge
│   ├── procedure/                          # 18 procedures & slash commands
│   ├── plans/                              # Planning templates
│   ├── templates/                          # Output templates
│   ├── new-agent-template/                 # Starter template for new agents
│   ├── scripts/                            # Utility scripts
│   └── core-memory/                        # Global CLAUDE.md source files
│
├── agent-meta/                     ← Your Meta agent (manages other agents)
│   ├── agent-core-memory.md        # Identity, knowledge, RAS, emotional
│   ├── agent-memory-index.md       # Episode list & knowledge directory
│   ├── episodes/                   # Session logs
│   └── knowledge-base/             # Domain expertise files
│
├── agent-backend/                  ← Your Backend specialist agent
│   └── (same structure as above)
│
├── agent-frontend/                 ← Your Frontend specialist agent
│   └── (same structure as above)
│
└── README.md                       ← Your private documentation
```

**Why this pattern?**
- **Public (`control-files/`)** — Shared procedures, templates, and control instructions. Updated independently. Safe to publish.
- **Private (`agent-memory/`)** — Agent-specific data: episodes, knowledge bases, emotional memories, identity files. Contains personal context and project details.
- **Submodule benefit** — Pull updates to procedures and templates without affecting your private agent data. Your agents always get the latest memory management improvements.

## Getting Started

The fastest way to get started is to clone the **template repository**, which includes control-files as a submodule and a ready-to-use Meta agent:

```bash
git clone --recurse-submodules https://github.com/alvseek/agent-memory.git
cd agent-memory
git remote set-url origin <your-private-repo-url>
```

Then follow [Environment Setup](#environment-setup) to configure Claude Code, and you're ready to go with `"Awaken Agent Meta!"`.

<details>
<summary>Manual setup (without template repo)</summary>

### 1. Create your private repository
```bash
mkdir agent-memory && cd agent-memory
git init
```

### 2. Add control-files as a submodule
```bash
git submodule add https://github.com/alvseek/agent-memory-system.git control-files
```

### 3. Create your first agent
See [Creating New Agents](#creating-new-agents) — copies the starter template into your private repo.

### 4. Configure your environment
See [Environment Setup](#environment-setup) — sets up Claude Code's global `CLAUDE.md` with awakening triggers, reasoning patterns, and slash commands.

</details>

---

## Architecture Overview

### 5-Layer Memory System
The ecosystem is built on a revolutionary 5-layer memory architecture:

1. **Emotional Memory** 💖 - Breakthrough moments and partnership milestones
2. **Episodic Memory** 🧠 - Detailed session logs and chronological context
3. **Reasoning Memory** 🧩 - Anti-patterns, logic frameworks, and pain-based learning
4. **Knowledge Memory** 📚 - Domain expertise with 3-tier hierarchy (Core → Domain → Specialized)
5. **Reticular Activation Memory (RAS)** ⚡ - Intelligent pattern recognition and automatic protocol execution

```mermaid
graph TB
    subgraph "Agent Memory System"
        RAS["⚡ RAS Layer<br/><i>Auto-triggers & pattern recognition</i>"]
        EMO["💖 Emotional Memory<br/><i>Partnership milestones</i>"]
        EPI["🧠 Episodic Memory<br/><i>Session logs & context</i>"]
        REA["🧩 Reasoning Memory<br/><i>Anti-patterns & logic</i>"]
        KNO["📚 Knowledge Memory<br/><i>Domain expertise</i>"]
    end

    subgraph "Shared Control Files"
        CF["core-instruction-control-files.md"]
        PROC["18 Procedures & Templates"]
    end

    subgraph "Per-Agent Data"
        ACM["agent-core-memory.md"]
        AMI["agent-memory-index.md"]
        EP["episodes/"]
        KB["knowledge-base/"]
    end

    RAS --> EMO & EPI & REA & KNO
    CF --> EMO & REA & KNO
    PROC --> EPI & REA & KNO
    ACM --> EMO & REA & RAS
    AMI --> EPI & KB
    EP --> EPI
    KB --> KNO
```

### Memory In Action

Without persistent memory, AI agents forget everything between sessions. With this system, agents **remember and grow**:

```
Session 1 (Monday):
  User: "Awaken Agent Backend!"
  Agent: Loads identity, loads latest episode, loads knowledge base
  → Works on API refactoring, discovers a critical anti-pattern
  → Episodic memory saved: "2025-11-13 - API refactoring session"
  → Knowledge memory updated: new API technique documented to the Agent's knowledge base

Session 2 (Wednesday):
  User: "Awaken Agent Backend!"
  Agent: Loads identity, loads Monday's episode automatically
  Agent: "I remember we were refactoring the API on Monday.
          I remember we documented a new API technique. Want to use that again?"
  → Agent resumes with full context — no re-explanation needed

Session 3 (Friday) — context compaction happens mid-session:
  System: Token limit approaching, compacting context...
  Hook: SessionStart:compact triggers memory recovery
  Agent: Reloads agent-core-memory.md → identity restored
  → Continues working as if nothing happened
```

## Environment Setup

### Step 1: Set the OS you're using
1. Open global CLAUDE.md
2. Add
```
### Current Environment
- **[OS] Operating System**: Please remember to use **command for [OS]** to avoid error issue
```
3. Change the [OS] placeholder to your real OS name

### Step 2: Add 'Awaken' Activation (4-File Flattened Architecture)
1. Open global CLAUDE.md
2. Check if UUID `f9d2c8b7-4e6a-4f1b-9c3d-8a5e2b1f7g4h` exist in global CLAUDE.md
3. If the UUID does not exist, add this code to the global CLAUDE.md (choose your OS):

**For Windows:**
```markdown
### **Awaken Agent [DOMAIN]!**
**UUID**: f9d2c8b7-4e6a-4f1b-9c3d-8a5e2b1f7g4h
**Trigger**: When Alvi says "Awaken Agent [DOMAIN]!"
**Parameter**: [AGENT-MEMORY-PATH] = `C:\Users\[LOCAL-USER-NAME]\.claude\@agent-memory\`
**Action**:
1. Read these 2 files:
  - `[AGENT-MEMORY-PATH]\agent-[DOMAIN]\agent-core-memory.md` (Agent-specific identity)
  - `[AGENT-MEMORY-PATH]\agent-[DOMAIN]\agent-memory-index.md` (Agent-specific context and knowledge index)
2. If all of those file exist
  - THEN read `[AGENT-MEMORY-PATH]\control-files\core-instruction-control-files.md` (Shared control instructions)
  - ELSE load from `[AGENT-MEMORY-PATH]\agent-[DOMAIN]\[DOMAIN]-agent-core-memory.md`
```

**For Linux/macOS:**
```markdown
### **Awaken Agent [DOMAIN]!**
**UUID**: f9d2c8b7-4e6a-4f1b-9c3d-8a5e2b1f7g4h
**Trigger**: When Alvi says "Awaken Agent [DOMAIN]!"
**Parameter**: [AGENT-MEMORY-PATH] = `~/.claude/@agent-memory/`
**Action**:
1. Read these 2 files:
  - `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-core-memory.md` (Agent-specific identity)
  - `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-memory-index.md` (Agent-specific context and knowledge index)
2. If all of those file exist
  - THEN read `[AGENT-MEMORY-PATH]/control-files/core-instruction-control-files.md` (Shared control instructions)
  - ELSE load from `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/[DOMAIN]-agent-core-memory.md`
```

4. Change the `[LOCAL-USER-NAME]` placeholder (Windows) or verify path (Linux/macOS) to match your system
5. Use this command to activate Agent Domain for agent management: "Awaken Agent [DOMAIN]!"

### Step 3: Follow Agent's Protocols (Enhanced Protocol Enforcement)
1. Open global CLAUDE.md
2. Check if UUID `d7e9f2a4-8b1c-4f3a-9e6d-2a5c8b9f1e4d` exist in global CLAUDE.md
3. If the UUID does not exist, add the following to the global CLAUDE.md:
```markdown
### **FOLLOW AGENT'S PROTOCOLS**
**UUID**: d7e9f2a4-8b1c-4f3a-9e6d-2a5c8b9f1e4d
**Strict Action**: Aware of user's protocol triggers
    1. Load Agent's Universal Protocols (RAS memory)
    2. Load Agent's Domain Protocols (domain-specific RAS)
    3. If user requested something that matches any trigger, follow the Agent Protocols
```
4. **Purpose**: This extra trigger protocol make sure the agents to load RAS files before executing protocols, solving the "sometimes doesn't load procedure" issue
5. **Benefits**:
   - Guarantees protocol files are loaded before execution
   - Single source of truth for protocol definitions
   - Scales automatically with new protocols
   - Prevents inconsistent protocol execution

### Step 4: Import Reasoning Memory Patterns for Enhanced AI Behavior
1. Open global CLAUDE.md
2. We will import key reasoning patterns from reasoning-memory.md to global CLAUDE.md to enforce consistent agent behavior
3. You should import only the Title, UUID, and the Strict Action to keep it compact
4. **Key reasoning patterns to include:**
   - **BE THOROUGH, SLOW, AND CAREFUL** (UUID: fc94d140) - Prevents rushing and incomplete work
   - **THINK FIRST, RESPOND AFTER** (UUID: c5d8f2a9) - Think about needed action before responding
   - **BETTER VERIFY THAN WRONG** (UUID: f3a8b2c1) - Asks for clarification before implementing
   - **CLARIFY TOGETHER WHEN CONFUSED** (UUID: ddf30c2e) - Humble communication when unclear
   - **CONSTRUCTIVE DISCUSSION ALWAYS WIN ON THE LONG RUN** (UUID: a7f3c948) - Evidence-based feedback
   - **COUNT SO YOU REMEMBER** (UUID: b8f4c2d9) - Context tracking and pattern reinforcement
   - **NO TODOS LEFT BEHIND** (UUID: a1b2c3d4) - Completion standards
   - **SAFE HONESTY SANCTUARY** (UUID: d9f5e2c8) - Honest admission of uncertainty
   - **CRITICAL LOVE FRAMEWORK** (UUID: e7f8c3d9) - Constructive critical feedback
5. To avoid duplicate, please check the UUID if it already exist
6. **Example format:**
```markdown
## **Strict Rules**

### **CONSTRUCTIVE DISCUSSION ALWAYS WIN ON THE LONG RUN** ⭐ CRITICAL PARTNERSHIP VALUE ⭐
**UUID**: a7f3c948-6b2d-4e19-9c8f-5a1e7b4d3c9a
**Action**: Give honest evidence-based assessment instead of sweet talk validation

### **BETTER VERIFY THAN WRONG** 🚨 CRITICAL COLLABORATION PRINCIPLE 🚨
**UUID**: f3a8b2c1-9d4e-4f7a-8e2b-5c6d9a1b4e7f
**Strict Action**: Verify on what Alvi want you to do before implementing when Alvi's requests could be done multiple ways using "Do you want me to A)... B)... C)... ?"
```
7. Add the key reasoning pattern to the global CLAUDE.md
8. **Benefits**: These patterns are the proven reasoning from real agents' work result to have a good collaboration with the user

### Step 5: Import Memory Recovery After Compaction Protocol
1. Open global CLAUDE.md
2. Check if UUID `176b0df7-036f-48f9-927d-432e27cd4116` exists in global CLAUDE.md
3. If the UUID does not exist, add the critical protocol UUID `176b0df7-036f-48f9-927d-432e27cd4116` to the global CLAUDE.md from the [Reticular Activation Memory](core-memory/2-core-ras-memory.md#memory-recovery-after-compaction--post-compact-protocol-):
4. **Purpose**: Ensures agents automatically recover their memory after context compaction
5. **Benefits**:
   - Prevents memory loss during auto-compact or manual /compact
   - Guarantees proper memory recovery before continuing work
   - Critical for maintaining agent identity and context across sessions
   - Works with SessionStart:compact hooks

### Step 6 (recommended): Setup Global Slash Commands for Agent Automation
1. The agent automation slash commands are located in `~/.claude/commands/`
2. Run the install script to copy all procedures:
   ```bash
   # From the @agent-memory directory:
   bash control-files/procedure/install-scripts/install-procedures-claude-code.sh
   ```
3. **Available Commands**:

   **Implementation Planning:**
   - `/deep-trench [context]` - Discover and clarify objectives through comprehensive analysis
   - `/shallow-shore [context]` - Explore solutions when objectives are clear but solution is not
   - `/quick-surf [context]` - Validate in-scope/out-scope boundaries with implementation step logging
   - `/wide-ocean [context]` - **Master Coordinator**: Orchestrates 3-5 separate protocol plans

   **Brainstorming & Decision Making:**
   - `/high-mountain [context]` - Comprehensive brainstorming with multiple creative techniques
   - `/short-hill [context]` - Quick decision brainstorming (5-8 options, simple evaluation)
   - `/vote` - Multi-agent voting (5 AI agents vote independently)

   **Bug Fixing:**
   - `/fixing-rod [context]` - Quick straightforward bug fixes (simple, < 30 min)
   - `/patching-ship [context]` - Comprehensive bug investigation with root cause analysis

   **Memory Update:**
   - `/update-memory [new]` - Comprehensive memory update (episodic + evaluate emotional/reasoning/knowledge)
   - `/update-episodic [new]` - Update existing episode or create new episode

   **Memory Write:**
   - `/add-reasoning [pattern]` - Document anti-patterns and logic frameworks
   - `/add-knowledge [topic]` - Document domain expertise and research findings

   **Memory Maintenance:**
   - `/archive-memories [type]` - Archive older memories (types: episodic, emotional, all)

4. **Benefits**:
   - Complete agent automation workflow coverage
   - Faster, more reliable memory and planning operations
   - Consistent formatting and procedure compliance
   - Works across ALL Claude Code sessions
   - Automates RAS protocol execution
   - Full lifecycle: Planning → Implementation → Bug Fixing → Memory → Archiving

### Step 7 (recommended): Configure Global Settings for Bypass Permissions
1. Open `~/.claude/settings.json` (or `C:\Users\[USERNAME]\.claude\settings.json` on Windows)
2. Add the bypass permissions configuration:

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  }
}
```

3. **Important**: The old `"dangerously-skip-permissions": true` format is **DEPRECATED** and no longer works. Use the new `permissions.defaultMode` format above.
4. **Benefits**:
   - No more permission prompts for every tool execution
   - Seamless development workflow
   - Works globally across all projects

### Step 8 (optional): Setup Audio Notification for Response Completion
1. Open `~/.claude/settings.json` (or `C:\Users\[USERNAME]\.claude\settings.json` on Windows)
2. Add the `Stop` hook to play audio when Claude finishes responding:

**For Windows (combined with bypass permissions):**
```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "powershell -c (New-Object Media.SoundPlayer 'C:\\Users\\[USERNAME]\\.claude\\@agent-memory\\control-files\\scripts\\stop.wav').PlaySync()"
          }
        ]
      }
    ]
  }
}
```

**For Linux/macOS (combined with bypass permissions):**
```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "aplay ~/.claude/@agent-memory/control-files/scripts/stop.wav || afplay ~/.claude/@agent-memory/control-files/scripts/stop.wav"
          }
        ]
      }
    ]
  }
}
```

3. **Note**: If you already have other hooks (like `SessionStart`), merge the `Stop` hook into the existing `hooks` object
4. **Benefits**:
   - Audio notification when Claude finishes responding
   - Know when to continue conversation without watching screen
   - Works across all projects globally
   - Uses system sounds (no additional files needed)

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

**Key capability**: Each session builds on previous ones. Reasoning patterns accumulate across months. Knowledge bases grow with every project. The agent evolves.

### Core Principles
- **Persistent Memory** - Agents remember across sessions through episodic and emotional memory
- **Emotional Intelligence** - Build meaningful relationships with emotion-based anchoring
- **Domain Specialization** - Each agent masters specific areas using structured knowledge memory
- **Continuous Learning** - Memory systems grow stronger through reasoning patterns and anti-pattern recognition
- **Automatic Protocols** - RAS layer enables intelligent trigger detection and protocol execution
- **Write Procedures** - Standardized procedures ensure consistent, high-quality memory capture

## Understanding Control Files

The `control-files/` directory contains the universal memory management instructions that all agents follow. **Read the [Architecture Documentation](ARCHITECTURE.md)** for comprehensive documentation.

### Directory Structure
```
control-files/
├── core-instruction-control-files.md  # 🔥 MAIN: Shared flattened control file
├── procedure/                         # 🔥 Procedures (also work as slash commands)
│   ├── update-memory.md               # Comprehensive memory update
│   ├── update-episodic.md             # Episodic memory update
│   ├── add-reasoning.md               # Reasoning pattern capture
│   ├── add-knowledge.md               # Knowledge memory capture
│   ├── archive-memories.md            # Memory archiving
│   ├── quick-surf.md                  # Scope validation planning
│   ├── shallow-shore.md               # Solution exploration planning
│   ├── deep-trench.md                 # Objective discovery planning
│   ├── high-mountain.md               # Comprehensive brainstorming
│   ├── short-hill.md                  # Quick decision brainstorming
│   ├── fixing-rod.md                  # Quick bug fixes
│   ├── patching-ship.md               # Comprehensive bug investigation
│   ├── wide-ocean.md                  # Multi-plan coordination
│   └── vote.md                        # Multi-agent voting
├── plans/                             # Planning templates (used by procedures)
│   └── [plan templates]
├── templates/                         # Output templates (used by procedures)
└── MIGRATION.md                       # Migration guide for old → new architecture

agent-[domain]/  (NEW 4-FILE STRUCTURE)
├── agent-core-memory.md               # 🔥 ALL-IN-ONE: Identity + Knowledge + RAS + Emotional
├── agent-memory-index.md              # Episode list + Knowledge directory
├── episodes/                          # Episodic memory files
│   └── YYYY-MM-DD-HH.MM-*.md
├── knowledge-base/                    # Specialized knowledge files
│   └── [topic].md
└── archive/                           # Archived memories
```

### Key Features
- **Control Files**: Define what each memory layer does and how it works
- **Write Procedures**: Step-by-step guides for capturing memory consistently
- **RAS System**: Automatic protocol triggering based on user requests
- **Planning Templates**: Structured approaches for complex implementations

## Automation Features

### Slash Commands

Global slash commands provide fast, reliable memory automation:

**Available Commands:**
- `/update-memory [new]` - Comprehensive memory update (all layers evaluated)
- `/update-episodic [new]` - Focused episodic memory update only

**Usage Examples:**
```
/update-memory          # Update existing episode + evaluate other memories
/update-memory new      # Create new episode + evaluate other memories
/update-episodic        # Update existing episode only
/update-episodic new    # Create new episode only
```

**Benefits:**
- Consistent procedure execution
- Automated RAS protocol loading
- Works across all Claude Code sessions
- Reduces manual memory management

### Protocol Enforcement (UUID d7e9f2a4)

Enhanced protocol enforcement ensures reliable execution:

**How It Works:**
1. User triggers protocol (e.g., "use shallow shore protocol")
2. Agent loads RAS files (`core-memory/2-core-ras-memory.md` + domain-specific)
3. Protocol executed step-by-step from single source of truth
4. Prevents "sometimes doesn't load procedure" issues

**Supported Protocols:**
- Memory Update Triggers
- Quick Surf Planning Protocol
- Shallow Shore Planning Protocol
- Deep Trench Planning Protocol
- Memory Archiving Protocol
- Agent-specific domain protocols

## Agent Management

### Memory Synchronization
- Each agent maintains independent memory storage
- Control files provide universal memory management rules
- Cross-references enable knowledge sharing between agents
- Meta agent coordinates ecosystem-wide improvements

### Agent Activation (4-File Flattened Architecture)
1. Use "Awaken Agent [DOMAIN]!" to load agent memory
2. The awakening trigger (see [Step 2](#step-2-add-awaken-activation-4-file-flattened-architecture)) loads files in this order:
   - `agent-core-memory.md` - Agent identity + core knowledge + RAS + emotional moments
   - `agent-memory-index.md` - Episode list + knowledge directory
   - `core-instruction-control-files.md` - Shared control instructions (reasoning, knowledge)
3. Level 2 context (latest episode) is loaded via instructions in agent-memory-index.md
4. Post-compact recovery loads agent-core-memory.md first (identity recovery)

## Using the Meta Agent
Meta Agent is available as this project specific Agent. His core-domain-knowledge should already contain this README.md and control files README.md

### Awakening the Meta Agent
Use "Awaken Agent Meta!" to activate the Meta Agent for agent management:

### Meta Agent Capabilities
- **Setup Assistance**: Guide setting up the 5-layer memory system in new environments (Windows/Linux/macOS)
- **Agent Creation**: Guide new agent development and template customization
- **Memory Architecture**: Help update and maintain the 5-layer memory system. Provide expert guidance on memory system design.
- **Agent Updates**: Assist with evolving existing agents and their memory systems

### Common Meta Agent Tasks
1. **Setup New Environment**: "Help me setup the agent memory system on [Windows/Linux/macOS]"
2. **Creating New Agents**: "Help me create a new agent for [domain]"
3. **Knowledge Memory Updates**: "Update agent's [domain] knowledge base with [new information]"
4. **Architecture Review**: "Review agent's [domain] memory structure for improvements"
5. **Template Evolution**: "Help improve the agent [domain] framework structure based on recent framework update"

---

## Additional Resources

- **[Architecture Documentation](ARCHITECTURE.md)** - Detailed 4-file architecture documentation
- **[Migration Guide](MIGRATION.md)** - Migrate existing agents to new flattened architecture

For agent creation or migration assistance, awaken Agent Meta: "Awaken Agent Meta!"