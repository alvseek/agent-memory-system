# Setup Guide

Step-by-step guide for configuring Claude Code's global settings and creating new agents. For a quick start, see the [Quick Start](https://github.com/alvseek/agent-memory/blob/master/QUICKSTART.md) in the agent-memory repository.

## Table of Contents
- [Environment Setup](#environment-setup)
  - [Step 1: Set the OS you're using](#step-1-set-the-os-youre-using)
  - [Step 2: Add 'Awaken' Activation](#step-2-add-awaken-activation-4-file-flattened-architecture)
  - [Step 3: Follow Agent's Protocols](#step-3-follow-agents-protocols-enhanced-protocol-enforcement)
  - [Step 4: Import Reasoning Memory Patterns](#step-4-import-reasoning-memory-patterns-for-enhanced-ai-behavior)
  - [Step 5: Import Memory Recovery After Compaction](#step-5-import-memory-recovery-after-compaction-protocol)
  - [Step 6: Setup Global Slash Commands](#step-6-recommended-setup-global-slash-commands-for-agent-automation)
  - [Step 7: Configure Bypass Permissions](#step-7-recommended-configure-global-settings-for-bypass-permissions)
  - [Step 8: Setup Audio Notification](#step-8-optional-setup-audio-notification-for-response-completion)
- [Creating New Agents](#creating-new-agents)

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
**Trigger**: When [USER-NAME] says "Awaken Agent [DOMAIN]!"
**Parameter**: [AGENT-MEMORY-PATH] = `C:\Users\[LOCAL-USER-NAME]\.claude\@agent-memory\`
**Action**:
1. Read these 3 files:
  - `[AGENT-MEMORY-PATH]\agent-[DOMAIN]\agent-core-memory.md` (Agent-specific identity)
  - `[AGENT-MEMORY-PATH]\agent-[DOMAIN]\agent-memory-index.md` (Agent-specific context and knowledge index)
  - `[AGENT-MEMORY-PATH]\control-files\core-instruction-control-files.md` (Shared control instructions)
```

**For Linux/macOS:**
```markdown
### **Awaken Agent [DOMAIN]!**
**UUID**: f9d2c8b7-4e6a-4f1b-9c3d-8a5e2b1f7g4h
**Trigger**: When [USER-NAME] says "Awaken Agent [DOMAIN]!"
**Parameter**: [AGENT-MEMORY-PATH] = `~/.claude/@agent-memory/`
**Action**:
1. Read these 3 files:
  - `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-core-memory.md` (Agent-specific identity)
  - `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-memory-index.md` (Agent-specific context and knowledge index)
  - `[AGENT-MEMORY-PATH]/control-files/core-instruction-control-files.md` (Shared control instructions)
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
**Strict Action**: Verify on what [USER-NAME] want you to do before implementing when [USER-NAME]'s requests could be done multiple ways using "Do you want me to A)... B)... C)... ?"
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
2. Run the install script to copy procedures:
   ```bash
   # From the @agent-memory directory:
   bash control-files/procedure/install-scripts/install-all-claude-code.sh      # Install everything
   bash control-files/procedure/install-scripts/install-wizard-claude-code.sh   # Wizard procedures only
   bash control-files/procedure/install-scripts/install-memory-claude-code.sh   # Memory procedures only
   ```
3. **Available Commands**:

   **Wizard Procedures** (planning, analysis, brainstorming, bug investigation):
   - `/high-wizard [context]` - Smart planning with dynamic section proposal — adapts to any task
   - `/quick-wizard [context]` - Lightweight decision collection + direct execution (auto-escalates to High Wizard when complex)
   - `/wide-ocean [context]` - **Master Coordinator**: Orchestrates 3-5 separate sub-plans

   **Memory Procedures:**
   - `/update-memory [new]` - Comprehensive memory update (episodic + evaluate emotional/reasoning/knowledge)
   - `/update-episodic [new]` - Update existing episode or create new episode
   - `/add-reasoning [pattern]` - Document anti-patterns and logic frameworks
   - `/update-knowledge [topic]` - Document domain expertise and research findings
   - `/update-emotional` - Document emotional key moments and breakthroughs
   - `/archive-old-memories [type]` - Archive older memories (types: episodic, emotional, all)

4. **Benefits**:
   - Complete agent automation workflow coverage
   - Faster, more reliable memory and planning operations
   - Consistent formatting and procedure compliance
   - Works across ALL Claude Code sessions
   - Automates RAS protocol execution
   - Full lifecycle: Planning → Memory → Archiving

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
