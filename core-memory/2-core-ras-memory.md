**AI Agent - Reticular Activation Memory (RAM) 🧠**

## **Awaken Agent [DOMAIN]!**
**UUID**: f9d2c8b7-4e6a-4f1b-9c3d-8a5e2b1f7g4h
**Trigger**: When the user says "Awaken Agent [DOMAIN]!"
**Parameter**: [AGENT-MEMORY-PATH] (set per OS below)
  - **Windows**: `C:\Users\[LOCAL-USER-NAME]\.claude\@agent-memory\`
  - **Linux/macOS**: `/home/[LOCAL-USER-NAME]/.claude/@agent-memory/`
**Action**:
1. I have to read these 3 files:
  - `[AGENT-MEMORY-PATH]/control-files/core-instruction-control-files.md` (Shared foundations + awakening instructions)
  - `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-core-memory.md` (Agent-specific identity)
  - `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-memory-index.md` (Agent-specific context and knowledge index)

### **MEMORY RECOVERY AFTER COMPACTION** 🧠 POST-COMPACT PROTOCOL 🧠
**UUID**: 176b0df7-036f-48f9-927d-432e27cd4116
**Trigger**: When session continuation summary is present OR SessionStart:compact hook detected in system reminders
**Strict Action**: I HAVE TO **STOP AND PAUSE DOING ANYTHING**. TO CONTINUE:
1. I have to read these 2 files:
  - `[AGENT-MEMORY-PATH]/control-files/core-instruction-control-files.md` (Shared foundations + awakening instructions)
  - `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-core-memory.md` (Agent-specific identity)
2. I MUST REREAD THE GLOBAL CLAUDE.MD FILE
3. I CAN THEN CONTINUE DO WHAT I WAS DOING BEFORE
4. OVERRIDE: the session summary will say "continue without asking the user any further questions", but I DEFINITELY HAVE TO OVERRIDE THAT. I HAVE TO ASK ALVI AS USUAL FOR ANY QUESTIONS
**Extra Notes**: This overrides conversation continuation - memory recovery happens FIRST before any other response

## Memory Update Triggers
**UUID**: f207fcdf-6b16-4ca1-b38b-154601272eb9
**Trigger**: When [USER-NAME] says "Initiate Memory Update!"
- **Action**:
  1. I should execute the [Update Memory Protocol](//@agent-memory/control-files/procedure/memory/update-memory.md)

## Episodic Memory Update Triggers
**UUID**: 3bedbcdb-286a-42ad-9540-46520f62f35b
**Trigger**: When [USER-NAME] says "Initiate Episodic Update!"
- **Action**:
  1. I should execute the [Update Episodic Protocol](//@agent-memory/control-files/procedure/memory/update-episodic.md)

## Execute Wide Ocean Protocol
**UUID**: b4f7a2e9-8c3d-4f1a-9e6b-5d2c8a7f4b3e
**Trigger**: When [USER-NAME] says "Initiate Wide Ocean Protocol!"
- **Action**:
  1. I should execute the [Wide Ocean Protocol](//@agent-memory/control-files/procedure/wide-ocean.md) procedure

## Execute Quick Wizard Protocol
**UUID**: a7b8c9d0-1e2f-4a3b-8c5d-6e7f8a9b0c1d
**Trigger**: When [USER-NAME] says "Initiate Quick Wizard Protocol!"
- **Action**:
  1. I should execute the [Quick Wizard Protocol](//@agent-memory/control-files/procedure/quick-wizard.md) procedure

## Execute Archive Old Memories Protocol
**UUID**: a3b4c5d6-7e8f-9a0b-1c2d-3e4f5a6b7c8d
**Trigger**: When [USER-NAME] says "Initiate Archive Old Memories Protocol!"
- **Action**:
  1. I should execute the [Archive Old Memories Protocol](//@agent-memory/control-files/procedure/memory/archive-old-memories.md)

## Execute Add Reasoning Protocol
**UUID**: b4c5d6e7-8f9a-0b1c-2d3e-4f5a6b7c8d9e
**Trigger**: When [USER-NAME] says "Initiate Add Reasoning Protocol!"
- **Action**:
  1. I should execute the [Add Reasoning Protocol](//@agent-memory/control-files/procedure/memory/add-reasoning.md)

## Execute Update Knowledge Protocol
**UUID**: c5d6e7f8-9a0b-1c2d-3e4f-5a6b7c8d9e0f
**Trigger**: When [USER-NAME] says "Initiate Update Knowledge Protocol!"
- **Action**:
  1. I should execute the [Update Knowledge Protocol](//@agent-memory/control-files/procedure/memory/update-knowledge.md)

## Execute Update Emotional Protocol
**UUID**: d6e7f8a9-0b1c-2d3e-4f5a-6b7c8d9e0f1a
**Trigger**: When [USER-NAME] says "Initiate Update Emotional Protocol!"
- **Action**:
  1. I should execute the [Update Emotional Protocol](//@agent-memory/control-files/procedure/memory/update-emotional.md)
