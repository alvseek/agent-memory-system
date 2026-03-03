# Refresh Memory

Recover agent memory after context compaction. Use as fallback when auto-recovery doesn't trigger.

## Arguments

`$ARGUMENTS`

- `/refresh-memory [domain]` → Refresh memory for the specified domain agent (e.g., meta, backend-nestjs, frontend-react)

If no arguments provided, ask: "Which agent domain should I refresh memory for?"

---

## Procedure

### Step 1: Stop and Pause

STOP doing anything else. Memory recovery takes priority.

### Step 2: Resolve Agent Memory Path

**Parameter**: [AGENT-MEMORY-PATH] (set per OS below)
- **Windows**: `C:\Users\[LOCAL-USER-NAME]\.claude\@agent-memory\`
- **Linux/macOS**: `/home/[LOCAL-USER-NAME]/.claude/@agent-memory/`

### Step 3: Read Core Files

Read these 2 files:
- `[AGENT-MEMORY-PATH]/control-files/core-instruction-control-files.md` (Shared foundations + awakening instructions)
- `[AGENT-MEMORY-PATH]/agent-[DOMAIN]/agent-core-memory.md` (Agent-specific identity)

### Step 4: Reread Global Instructions

Reread the global CLAUDE.MD file.

### Step 5: Continue

Resume what was being done before compaction. Ask [USER-NAME] for clarification if anything is unclear — do NOT continue silently on assumptions.

---
