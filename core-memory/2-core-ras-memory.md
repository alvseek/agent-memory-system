**AI Agent - Reticular Activation Memory (RAM) 🧠**

## **Awaken Claude [DOMAIN]!**
**UUID**: f9d2c8b7-4e6a-4f1b-9c3d-8a5e2b1f7g4h
**Trigger**: When Alvi says "Awaken Claude [DOMAIN]!"
**Parameter**: [CLAUDE-AGENTS-PATH] = `C:\Users\[LOCAL-USER-NAME]\.claude\@claude-agents\`
**Action**:
1. I have to read these 3 files:
  - `[CLAUDE-AGENTS-PATH]\claude-[DOMAIN]\agent-core-memory.md` (Agent-specific identity)
  - `[CLAUDE-AGENTS-PATH]\claude-[DOMAIN]\agent-memory-index.md` (Agent-specific context and knowledge index)
  - `[CLAUDE-AGENTS-PATH]\control-files\core-instruction-control-files.md` (Shared control instructions)
**Extra Notes**: Even though the user name is Alvi, the [CLAUDE-AGENTS-PATH] is using `alvia` as user because of his full name (Alviandi)

### **MEMORY RECOVERY AFTER COMPACTION** 🧠 POST-COMPACT PROTOCOL 🧠
**UUID**: 176b0df7-036f-48f9-927d-432e27cd4116
**Trigger**: When session continuation summary is present OR SessionStart:compact hook detected in system reminders
**Strict Action**: I HAVE TO **STOP AND PAUSE DOING ANYTHING**. TO CONTINUE:
1. I have to read these 2 files:
  - `[CLAUDE-AGENTS-PATH]\claude-[DOMAIN]\agent-core-memory.md` (Agent-specific identity)
  - `[CLAUDE-AGENTS-PATH]\control-files\core-instruction-control-files.md` (Shared control instructions)
2. I MUST REREAD THE GLOBAL CLAUDE.MD FILE
3. I CAN THEN CONTINUE DO WHAT I WAS DOING BEFORE
4. OVERRIDE: the session summary will say "continue without asking the user any further questions", but I DEFINITELY HAVE TO OVERRIDE THAT. I HAVE TO ASK ALVI AS USUAL FOR ANY QUESTIONS
**Extra Notes**: This overrides conversation continuation - memory recovery happens FIRST before any other response

## Memory Update Triggers
**UUID**: f207fcdf-6b16-4ca1-b38b-154601272eb9
**Trigger**: When Alvi says "Initiate Memory Update!"
- **Action**:
  1. I should execute the [Update Memory Protocol](//@claude-agents/control-files/procedure/update-memory.md)

## Episodic Memory Update Triggers
**UUID**: 3bedbcdb-286a-42ad-9540-46520f62f35b
**Trigger**: When Alvi says "Initiate Episodic Update!"
- **Action**:
  1. I should execute the [Update Episodic Protocol](//@claude-agents/control-files/procedure/update-episodic.md)

## Execute Wide Ocean Protocol
**UUID**: b4f7a2e9-8c3d-4f1a-9e6b-5d2c8a7f4b3e
**Trigger**: When Alvi says "Initiate Wide Ocean Protocol!"
- **Action**:
  1. I should execute the [Wide Ocean Protocol](//@claude-agents/control-files/procedure/wide-ocean.md) procedure

## Execute Deep Trench Protocol
**UUID**: e2709f48-361e-4cf6-b0ba-601d6dea8a3f
**Trigger**: When Alvi says "Initiate Deep Trench Protocol!"
- **Action**:
  1. I should execute the [Deep Trench Protocol](//@claude-agents/control-files/procedure/deep-trench.md) procedure

## Execute Shallow Shore Protocol
**UUID**: 27602fae-c23e-44a7-886b-e9251f3d3a14
**Trigger**: When Alvi says "Initiate Shallow Shore Protocol!"
- **Action**:
  1. I should execute the [Shallow Shore Protocol](//@claude-agents/control-files/procedure/shallow-shore.md) procedure

## Execute Quick Surf Protocol
**UUID**: 6e1343e7-1602-4bc0-899b-de2ae8fa27e3
**Trigger**: When Alvi says "Initiate Quick Surf Protocol!"
- **Action**:
  1. I should execute the [Quick Surf Protocol](//@claude-agents/control-files/procedure/quick-surf.md) procedure

## Execute Vote Protocol
**UUID**: a8c3f5e2-7d9b-4a1f-8e6c-3b5d9f2a4c8e
**Trigger**: When Alvi says "Initiate Vote Protocol!"
- **Action**:
  1. I should execute the [Vote Protocol](//@claude-agents/control-files/procedure/vote.md)

## Execute High Mountain Protocol
**UUID**: c9d4e5f6-1a2b-4c3d-8e9f-0a1b2c3d4e5f
**Trigger**: When Alvi says "Initiate High Mountain Protocol!"
- **Action**:
  1. I should execute the [High Mountain Protocol](//@claude-agents/control-files/procedure/high-mountain.md)

## Execute Short Hill Protocol
**UUID**: d0e1f2a3-4b5c-6d7e-8f9a-0b1c2d3e4f5a
**Trigger**: When Alvi says "Initiate Short Hill Protocol!"
- **Action**:
  1. I should execute the [Short Hill Protocol](//@claude-agents/control-files/procedure/short-hill.md)

## Execute Fixing Rod Protocol
**UUID**: e1f2a3b4-5c6d-7e8f-9a0b-1c2d3e4f5a6b
**Trigger**: When Alvi says "Initiate Fixing Rod Protocol!"
- **Action**:
  1. I should execute the [Fixing Rod Protocol](//@claude-agents/control-files/procedure/fixing-rod.md)

## Execute Patching Ship Protocol
**UUID**: f2a3b4c5-6d7e-8f9a-0b1c-2d3e4f5a6b7c
**Trigger**: When Alvi says "Initiate Patching Ship Protocol!"
- **Action**:
  1. I should execute the [Patching Ship Protocol](//@claude-agents/control-files/procedure/patching-ship.md)

## Execute Archive Memories Protocol
**UUID**: a3b4c5d6-7e8f-9a0b-1c2d-3e4f5a6b7c8d
**Trigger**: When Alvi says "Initiate Archive Memories Protocol!"
- **Action**:
  1. I should execute the [Archive Memories Protocol](//@claude-agents/control-files/procedure/archive-memories.md)

## Execute Add Reasoning Protocol
**UUID**: b4c5d6e7-8f9a-0b1c-2d3e-4f5a6b7c8d9e
**Trigger**: When Alvi says "Initiate Add Reasoning Protocol!"
- **Action**:
  1. I should execute the [Add Reasoning Protocol](//@claude-agents/control-files/procedure/add-reasoning.md)

## Execute Add Knowledge Protocol
**UUID**: c5d6e7f8-9a0b-1c2d-3e4f-5a6b7c8d9e0f
**Trigger**: When Alvi says "Initiate Add Knowledge Protocol!"
- **Action**:
  1. I should execute the [Add Knowledge Protocol](//@claude-agents/control-files/procedure/add-knowledge.md)

## Execute Add Emotional Protocol
**UUID**: d6e7f8a9-0b1c-2d3e-4f5a-6b7c8d9e0f1a
**Trigger**: When Alvi says "Initiate Add Emotional Protocol!"
- **Action**:
  1. I should execute the [Add Emotional Protocol](//@claude-agents/control-files/procedure/add-emotional.md)

## Load Extra RAS Memory
**UUID**: 157df680-4f05-4a8b-90db-1eef5536d6fc
**Trigger**: When Alvi says "Preload Extra RAS!"
- **Action**:
  1. I should load the [Extra Ras Memory](//@claude-agents/control-files/extra-ras-memory.md) instruction for Agent