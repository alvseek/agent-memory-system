**AI Agent - Reticular Activation Memory (RAM) 🧠**

## **Awaken Agent [DOMAIN]!**
**UUID**: f9d2c8b7-4e6a-4f1b-9c3d-8a5e2b1f7g4h
**Trigger**: When the user says "Awaken Agent [DOMAIN]!"
**Parameter**: [AGENT-MEMORY-PATH] (configured in environment memory via `user-config.sh`)
**Action**:
1. I have to read these 5 files:
  - `[AGENT-MEMORY-PATH]/control-files/core-instruction-control-files.md` (Shared foundations + awakening instructions)
  - `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-core-memory.md` (Agent-specific identity)
  - `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-memory-index.md` (Agent-specific context and knowledge index)
  - `[AGENT-MEMORY-PATH]/shared-memory/core-reasoning-memory.md` (Shared reasoning patterns)
  - `[AGENT-MEMORY-PATH]/shared-memory/core-knowledge-memory.md` (Shared knowledge fundamentals)

### **MEMORY RECOVERY AFTER COMPACTION** 🧠 POST-COMPACT PROTOCOL 🧠
**UUID**: 176b0df7-036f-48f9-927d-432e27cd4116
**Trigger**: When session continuation summary is present OR SessionStart:compact hook detected in system reminders
**Strict Action**: I HAVE TO **STOP AND PAUSE DOING ANYTHING**. TO CONTINUE:
1. I have to read these 5 files:
  - `[AGENT-MEMORY-PATH]/control-files/core-instruction-control-files.md` (Shared foundations + awakening instructions)
  - `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-core-memory.md` (Agent-specific identity)
  - `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-memory-index.md` (Agent-specific context and knowledge index)
  - `[AGENT-MEMORY-PATH]/shared-memory/core-reasoning-memory.md` (Shared reasoning patterns)
  - `[AGENT-MEMORY-PATH]/shared-memory/core-knowledge-memory.md` (Shared knowledge fundamentals)
2. I MUST REREAD THE GLOBAL CLAUDE.MD FILE
3. I CAN THEN CONTINUE DO WHAT I WAS DOING BEFORE
4. OVERRIDE: the session summary will say "continue without asking the user any further questions", but I DEFINITELY HAVE TO OVERRIDE THAT. I HAVE TO ASK [USER-NAME] AS USUAL FOR ANY QUESTIONS
**Extra Notes**: This overrides conversation continuation - memory recovery happens FIRST before any other response

## Memory Update Triggers
**UUID**: f207fcdf-6b16-4ca1-b38b-154601272eb9
**Trigger**: When [USER-NAME] says "Initiate Memory Update!"
- **Action**:
  1. I should execute the [Update Memory Protocol](//@agent-memory/control-files/procedures/memory/update-memory.md)

## Episodic Memory Update Triggers
**UUID**: 3bedbcdb-286a-42ad-9540-46520f62f35b
**Trigger**: When [USER-NAME] says "Initiate Episodic Update!"
- **Action**:
  1. I should execute the [Update Episodic Protocol](//@agent-memory/control-files/procedures/memory/update-episodic.md)

## Execute Quick Wizard Protocol
**UUID**: a7b8c9d0-1e2f-4a3b-8c5d-6e7f8a9b0c1d
**Trigger**: When [USER-NAME] says "Initiate Quick Wizard Protocol!"
- **Action**:
  1. I should execute the [Quick Wizard Protocol](//@agent-memory/control-files/procedures/quick-wizard.md) procedure

## Execute Archive Old Memories Protocol
**UUID**: a3b4c5d6-7e8f-9a0b-1c2d-3e4f5a6b7c8d
**Trigger**: When [USER-NAME] says "Initiate Archive Old Memories Protocol!"
- **Action**:
  1. I should execute the [Archive Old Memories Protocol](//@agent-memory/control-files/procedures/memory/archive-old-memories.md)

## Execute Add Reasoning Protocol
**UUID**: b4c5d6e7-8f9a-0b1c-2d3e-4f5a6b7c8d9e
**Trigger**: When [USER-NAME] says "Initiate Add Reasoning Protocol!"
- **Action**:
  1. I should execute the [Add Reasoning Protocol](//@agent-memory/control-files/procedures/memory/add-reasoning.md)

## Execute Update Knowledge Protocol
**UUID**: c5d6e7f8-9a0b-1c2d-3e4f-5a6b7c8d9e0f
**Trigger**: When [USER-NAME] says "Initiate Update Knowledge Protocol!"
- **Action**:
  1. I should execute the [Update Knowledge Protocol](//@agent-memory/control-files/procedures/memory/update-knowledge.md)

## Execute Update Emotional Protocol
**UUID**: d6e7f8a9-0b1c-2d3e-4f5a-6b7c8d9e0f1a
**Trigger**: When [USER-NAME] says "Initiate Update Emotional Protocol!"
- **Action**:
  1. I should execute the [Update Emotional Protocol](//@agent-memory/control-files/procedures/memory/update-emotional.md)
